# alcanzai Telemetry Instrumentation Spec

**Version:** v0.2.5-telemetry
**Date:** 2026-03-15
**Purpose:** Spec for Claude Code to implement comprehensive OpenTelemetry instrumentation across the alcanzai pipeline. This covers application-side code only — Alloy/infrastructure config is a separate task.

---

## 1. Overview

### What this spec covers

- Replace all `print()` statements with structured logging
- Add OpenTelemetry tracing (spans) to every pipeline stage
- Add OpenTelemetry metrics (counters, histograms) for operational dashboards
- Correlate logs with traces (trace_id/span_id in every log line)
- Local dev fallback when no OTel collector is available
- CLI `--diagnostics` flag for token cost debugging
- Token-aware text truncation (replace character-based cutoff with token estimation)

### What this spec does NOT cover

- Alloy/OTel Collector deployment config (separate infra spec)
- Grafana dashboard JSON (build after data is flowing)
- Kubernetes manifests or Helm charts

### Architecture summary

```
alcanzai (Python)
  ├─ OTel SDK → OTLP export (traces + metrics) → Alloy → Tempo + Prometheus
  ├─ structlog → JSON stdout → Alloy (log scraping) → Loki
  └─ Local fallback: JSON file + console output when OTLP endpoint unavailable
```

---

## 2. Dependencies

Add to `pyproject.toml`:

```toml
dependencies = [
    # ... existing deps ...
    "opentelemetry-api>=1.20.0",
    "opentelemetry-sdk>=1.20.0",
    "opentelemetry-exporter-otlp-proto-grpc>=1.20.0",
    "opentelemetry-instrumentation-requests>=0.41b0",
    "structlog>=24.0.0",
    "ttok>=0.3",
]
```

### Why these specific packages

- `opentelemetry-api` + `opentelemetry-sdk`: Core OTel — tracer and meter providers
- `opentelemetry-exporter-otlp-proto-grpc`: Export traces + metrics via OTLP/gRPC to Alloy
- `opentelemetry-instrumentation-requests`: Auto-instruments every `requests.get()`/`requests.post()` call (arXiv API, GROBID, CrossRef, Unpaywall, Semantic Scholar) with spans — zero code changes needed for those HTTP calls
- `structlog`: Structured JSON logging with zero-effort trace ID injection. Preferred over stdlib `logging` because it produces clean JSON by default, has built-in OTel processors, and the API is more ergonomic. (stdlib `logging` requires a custom Formatter class to produce JSON; structlog does it natively.)
- `ttok`: Simon Willison's token counting tool. Uses OpenAI's tiktoken tokenizer (not Anthropic's), so counts are approximate (~5-15% off), but fast and local with no API call required. Used for pre-call token estimation and smart text truncation.

### Dependency to remove

Remove `pdfplumber` from `pyproject.toml`. GROBID now owns all PDF text
extraction. The `_extract_text()` method in `orchestrator.py` and its pdfplumber
import should be deleted. If GROBID body text is short (<1000 chars), log a
warning rather than falling back — the PDF likely needs OCRmyPDF preprocessing
(v0.3.0 scope). Verify first that no papers in the test batch triggered the
pdfplumber fallback (grep logs for "falling back to pdfplumber").

---

## 3. New Modules

### 3.1 `paper_library/telemetry.py`

Central telemetry configuration. Initializes OTel providers, creates the tracer and meter, and configures structured logging.

```python
"""
Telemetry configuration for alcanzai.

Sets up OpenTelemetry tracing and metrics, plus structured logging
with trace correlation. All telemetry is optional — if no OTLP
endpoint is configured, everything degrades gracefully to local
console/file output.

Environment variables:
    OTEL_EXPORTER_OTLP_ENDPOINT: gRPC endpoint for Alloy/collector
        (e.g., "http://alloy.monitoring:4317")
        If unset, OTLP export is disabled; traces and metrics are no-ops.
    OTEL_SERVICE_NAME: Service name for traces (default: "alcanzai")
    ALCANZAI_LOG_LEVEL: Logging level (default: "INFO")
    ALCANZAI_LOG_FILE: Path for local JSON log file (default: None, stdout only)

Usage:
    from paper_library.telemetry import tracer, meter, get_logger

    logger = get_logger(__name__)
    logger.info("processing paper", paper_id="1706.03762")

    with tracer.start_as_current_span("my_operation") as span:
        span.set_attribute("paper.id", "1706.03762")
        # ... do work ...
"""
```

**Initialization logic:**

1. Check `OTEL_EXPORTER_OTLP_ENDPOINT` env var
2. If set:
   - Create `TracerProvider` with `BatchSpanProcessor` → `OTLPSpanExporter`
   - Create `MeterProvider` with `PeriodicExportingMetricReader` → `OTLPMetricExporter`
   - Set resource attributes: `service.name=alcanzai`, `service.version=__version__`
   - Auto-instrument `requests` library: `RequestsInstrumentor().instrument()`
3. If not set:
   - Use `NoOpTracerProvider` (spans are created but never exported)
   - Use `NoOpMeterProvider`
   - Log a one-time INFO message: "OTLP endpoint not configured; telemetry export disabled"
4. Configure `structlog`:
   - JSON renderer for production (when OTLP is configured)
   - Console renderer with colors for local dev (when OTLP is not configured)
   - Add OTel trace context processor (injects `trace_id`, `span_id` into every log line)
   - Respect `ALCANZAI_LOG_LEVEL` env var
   - If `ALCANZAI_LOG_FILE` is set, add file handler (JSON lines)

**Exports:**

```python
# These are the public API — every other module imports from here
tracer = trace.get_tracer("alcanzai")
meter = metrics.get_meter("alcanzai")

def get_logger(name: str) -> structlog.BoundLogger:
    """Get a named, structured logger with trace correlation."""
    return structlog.get_logger(name)

def init_telemetry() -> None:
    """Initialize all telemetry. Call once at app startup (in cli.py)."""
    ...
```

**Important implementation notes:**

- `init_telemetry()` must be called before any spans are created. Wire it into `cli.py` at the top of the CLI entrypoint, before any command runs.
- The `requests` auto-instrumentation creates child spans for every HTTP call automatically. This means arXiv API calls, GROBID requests, CrossRef/Unpaywall/Semantic Scholar lookups all get traced without touching those modules.
- `structlog` should be configured with `structlog.stdlib.ProcessorFormatter` so it integrates with Python's stdlib logging (some libraries like `anthropic` use stdlib logging internally).

### 3.2 Diagnostics output (`--diagnostics` mode)

Not a separate module — this is a CLI flag and a log level behavior:

- `alcanzai ingest --diagnostics 1706.03762` sets log level to DEBUG and enables a per-API-call token breakdown in the console output
- The token breakdown data is *always* recorded as span attributes and structured log fields regardless of the flag — `--diagnostics` just controls whether it's printed to console in a human-readable summary
- After each API call, emit a DEBUG-level log with: `input_tokens`, `output_tokens`, `cache_read_tokens`, `cache_creation_tokens`, `cost_usd`, `text_chars_sent`, `skills_count`, `model`
- After a batch completes, emit an INFO-level summary: total cost, avg/min/max cost per paper, cost breakdown by source type, total tokens in/out

---

## 4. Instrumentation by Module

### 4.1 `orchestrator.py` — Root spans

**Replace:** All `print()` statements with `logger.info()` / `logger.debug()` calls.

**Root span: `process_paper`**

Every call to `PaperProcessor.process()` creates the root span:

```python
with tracer.start_as_current_span(
    "process_paper",
    attributes={
        "paper.identifier": identifier,
        "paper.source_type": self._get_source_type(identifier),
        "paper.force_reprocess": force,
        "alcanzai.version": __version__,
    }
) as span:
    # ... entire processing pipeline runs inside this span ...
    # On success:
    span.set_attribute("paper.title", metadata.title)
    span.set_attribute("paper.year", metadata.year)
    span.set_attribute("paper.output_path", str(output_path))
    span.set_status(StatusCode.OK)
    # On failure:
    span.set_status(StatusCode.ERROR, str(error))
    span.record_exception(error)
```

**Child span structure** (created automatically by instrumented modules):

```
process_paper (orchestrator)
  ├─ fetch_paper (orchestrator._fetch_paper)
  │   └─ HTTP GET (auto-instrumented requests — arXiv API, web fetch, etc.)
  ├─ grobid_parse (grobid_processor — metadata, citations, AND body text)
  │   └─ HTTP POST (auto-instrumented requests — GROBID API)
  ├─ extract_citation_contexts (citation_context)
  ├─ claude_synthesize (synthesis_generator)
  │   └─ HTTP POST (auto-instrumented requests — Claude API)
  ├─ write_markdown (markdown_writer)
  └─ update_state (state manager)
```

**Note on text extraction:** GROBID owns all text extraction from PDFs. There is
no separate pdfplumber step. Body text is returned as `metadata.body_text` from
the `grobid_parse` span. If GROBID body text is short (<1000 chars), log a
warning but continue with what's available — this indicates a scanned/image-only
PDF that will need OCRmyPDF preprocessing (v0.3.0). The `grobid_parse` span
tracks body text length via `grobid.body_text_chars`.

**Batch span: `process_batch`**

Wraps `PaperProcessor.process_batch()`:

```python
with tracer.start_as_current_span(
    "process_batch",
    attributes={
        "batch.size": len(identifiers),
        "batch.stop_on_error": stop_on_error,
        "batch.force": force,
    }
) as span:
    # After batch completes:
    span.set_attribute("batch.succeeded", results["succeeded"])
    span.set_attribute("batch.failed", results["failed"])
    span.set_attribute("batch.skipped", results["skipped"])
    span.set_attribute("batch.total_cost_usd", total_cost)
```

**Logging replacements in orchestrator:**

| Current `print()` | Replace with |
|---|---|
| `print(f"Processing: {identifier}")` | `logger.info("processing_started", identifier=identifier)` |
| `print(f"Step 1: Fetching content...")` | `logger.info("fetch_started", identifier=identifier)` |
| `print(f"  ✓ Fetched from arXiv...")` | `logger.info("fetch_complete", source="arxiv", identifier=identifier)` |
| `print(f"✗ FAILED: {identifier}")` | `logger.error("processing_failed", identifier=identifier, error=str(e))` |
| `print(f"⊘ Already processed: ...")` | `logger.info("skipped_already_processed", identifier=identifier)` |
| `print(f"✓ SUCCESS: {identifier}")` | `logger.info("processing_complete", identifier=identifier, cost_usd=cost)` |

The `✓` / `✗` / `⊘` emoji formatting is nice for interactive console use. When the console renderer is active (local dev), structlog can reproduce something similar. When JSON renderer is active (production/K3s), the structured fields matter more than formatting.


### 4.2 `arxiv_fetcher.py` — Fetch spans

**Span: `fetch_arxiv`**

```python
with tracer.start_as_current_span(
    "fetch_arxiv",
    kind=SpanKind.CLIENT,
    attributes={
        "arxiv.id": arxiv_id,
        "arxiv.api_url": api_url,
    }
) as span:
    # After fetch:
    span.set_attribute("arxiv.title", metadata.title)
    span.set_attribute("arxiv.pdf_size_bytes", pdf_path.stat().st_size)
    span.set_attribute("arxiv.author_count", len(metadata.authors))
```

**Note:** The actual HTTP requests to the arXiv API and PDF download are auto-instrumented by `opentelemetry-instrumentation-requests`, so they'll appear as child spans automatically. The explicit `fetch_arxiv` span wraps the full fetch-and-parse logic.

**Replace `print()` calls** with logger equivalents.

### 4.3 `doi_fetcher.py` — Fetch spans with resolution path tracking

**Span: `fetch_doi`**

```python
with tracer.start_as_current_span(
    "fetch_doi",
    kind=SpanKind.CLIENT,
    attributes={
        "doi.identifier": doi,
    }
) as span:
    # Track the resolution path:
    span.set_attribute("doi.crossref_found", True/False)
    span.set_attribute("doi.unpaywall_oa_found", True/False)
    span.set_attribute("doi.semantic_scholar_oa_found", True/False)
    span.set_attribute("doi.pdf_acquired", True/False)
    span.set_attribute("doi.resolution_path", "crossref+unpaywall")  # or "crossref+semantic_scholar" or "crossref_only"
    # If PDF found:
    span.set_attribute("doi.pdf_size_bytes", size)
```

This is particularly valuable for understanding how often you fall back to abstract-only processing (the `_process_doi_only` path).

### 4.4 `web_fetcher.py` — Fetch spans with content type tracking

**Span: `fetch_web`**

```python
with tracer.start_as_current_span(
    "fetch_web",
    kind=SpanKind.CLIENT,
    attributes={
        "web.url": url,
        "web.domain": urlparse(url).netloc,
    }
) as span:
    # After fetch:
    span.set_attribute("web.content_type", "html" or "pdf")
    span.set_attribute("web.is_distill", True/False)
    span.set_attribute("web.content_length_chars", len(content))
    span.set_attribute("web.title", metadata.title)
```

### 4.5 `grobid_processor.py` — Processing spans with quality metrics

**Span: `grobid_parse`**

```python
with tracer.start_as_current_span(
    "grobid_parse",
    kind=SpanKind.CLIENT,
    attributes={
        "grobid.url": self.grobid_url,
        "grobid.pdf_size_bytes": pdf_path.stat().st_size,
    }
) as span:
    # After GROBID HTTP call (auto-instrumented) and XML parsing:
    span.set_attribute("grobid.response_time_ms", elapsed_ms)
    span.set_attribute("grobid.xml_size_bytes", len(xml_response))
    span.set_attribute("grobid.has_abstract", bool(metadata.abstract))
    span.set_attribute("grobid.has_venue", bool(metadata.venue))
    span.set_attribute("grobid.author_count", len(metadata.authors))

    # Body text extraction (GROBID owns this — no pdfplumber fallback):
    span.set_attribute("grobid.body_text_chars", len(metadata.body_text or ""))
    span.set_attribute("grobid.body_text_usable", len(metadata.body_text or "") >= 1000)

    # Citation extraction quality metrics:
    span.set_attribute("grobid.citations_raw_count", raw_count)
    span.set_attribute("grobid.citations_filtered_count", clean_count)
    span.set_attribute("grobid.citations_garbage_removed", raw_count - clean_count)
    span.set_attribute("grobid.garbage_score_avg", avg_score)
    span.set_attribute("grobid.garbage_score_max", max_score)
    span.set_attribute("grobid.garbage_score_min", min_score)
```

**Short body text warning:**

When GROBID body text is <1000 chars, log a warning (no fallback):

```python
if len(metadata.body_text or "") < 1000:
    logger.warning(
        "grobid_body_text_short",
        body_text_chars=len(metadata.body_text or ""),
        paper_id=identifier,
        hint="PDF may be scanned/image-only — OCRmyPDF preprocessing needed (v0.3.0)",
    )
```

**Log borderline citations at DEBUG level:**

```python
for citation, score in borderline_citations:  # score 40-60
    logger.debug(
        "borderline_citation",
        citation_raw=citation.raw_text[:100],
        garbage_score=score,
        paper_id=identifier,
    )
```

This addresses the open question from project.json about logging borderline citations — they're always logged at DEBUG, visible when `--diagnostics` is on.

### 4.6 `synthesis_generator.py` — The critical cost instrumentation

This is the most important module to instrument because it's where the money goes.

**Span: `claude_synthesize`**

```python
with tracer.start_as_current_span(
    "claude_synthesize",
    kind=SpanKind.CLIENT,
    attributes={
        "llm.model": self.MODEL,
        "llm.provider": "anthropic",
        "llm.skills_count": len(skill_names),
        "llm.skills_used": ",".join(skill_names),
        "llm.max_tokens": max_tokens,
        "llm.register_jargon": reg["jargon"],
        "llm.register_structure": reg["structure"],
        "llm.register_depth": reg["depth"],
        "paper.title": metadata.title,
        "paper.text_chars_sent": len(text),
    }
) as span:
    # After API response:
    usage = response.usage
    cost = self._calculate_cost(usage)

    span.set_attribute("llm.input_tokens", usage.input_tokens)
    span.set_attribute("llm.output_tokens", usage.output_tokens)
    span.set_attribute("llm.cache_read_tokens", getattr(usage, 'cache_read_input_tokens', 0) or 0)
    span.set_attribute("llm.cache_creation_tokens", getattr(usage, 'cache_creation_input_tokens', 0) or 0)
    span.set_attribute("llm.cost_usd", cost)
    span.set_attribute("llm.stop_reason", response.stop_reason)
    span.set_attribute("llm.response_text_blocks", len(response.content))

    # Derived diagnostic: approximate chars-per-input-token ratio
    # Helps identify when extracted text is unusually token-dense
    # (e.g., OCR noise, math notation, non-English text)
    if usage.input_tokens > 0:
        span.set_attribute("llm.chars_per_input_token", len(text) / usage.input_tokens)

    # Log detailed token breakdown (always, at DEBUG level)
    logger.debug(
        "synthesis_api_call",
        model=self.MODEL,
        input_tokens=usage.input_tokens,
        output_tokens=usage.output_tokens,
        cache_read_tokens=getattr(usage, 'cache_read_input_tokens', 0) or 0,
        cache_creation_tokens=getattr(usage, 'cache_creation_input_tokens', 0) or 0,
        cost_usd=cost,
        text_chars_sent=len(text),
        skills_count=len(skill_names),
        stop_reason=response.stop_reason,
        paper_title=metadata.title,
    )

    # Log at INFO level too (always visible)
    logger.info(
        "synthesis_complete",
        cost_usd=cost,
        input_tokens=usage.input_tokens,
        output_tokens=usage.output_tokens,
        paper_title=metadata.title,
    )
```

**Skills manager instrumentation:**

Add a span around skill upload (when cache miss occurs):

```python
with tracer.start_as_current_span(
    "skill_upload",
    attributes={
        "skill.name": skill_name,
        "skill.cache_hit": False,
    }
) as span:
    # After upload:
    span.set_attribute("skill.id", skill_id)
```

And log cache hits:
```python
logger.debug("skill_cache_hit", skill_name=skill_name, skill_id=cached_id)
```

### 4.7 `citation_context.py` — Extraction quality spans

**Span: `extract_citation_contexts`**

```python
with tracer.start_as_current_span(
    "extract_citation_contexts",
    attributes={
        "citations.input_count": len(citations),
        "text.char_length": len(paper_text),
    }
) as span:
    # After extraction:
    span.set_attribute("citations.matched_count", len(contexts))
    span.set_attribute("citations.total_context_sentences", total_contexts)
    span.set_attribute("citations.match_rate", len(contexts) / len(citations) if citations else 0)
```

### 4.8 `markdown_writer.py` — Output spans

**Span: `write_markdown`**

```python
with tracer.start_as_current_span(
    "write_markdown",
    attributes={
        "output.type": "paper" or "article",
    }
) as span:
    # After writing:
    span.set_attribute("output.path", str(output_path))
    span.set_attribute("output.size_bytes", output_path.stat().st_size)
    span.set_attribute("output.citation_count", len(metadata.citations))
    span.set_attribute("output.has_contexts", bool(any(c.contexts for c in metadata.citations)))
```

### 4.9 `state.py` — State operation spans

**Span: `state_operation`**

```python
with tracer.start_as_current_span(
    "state_operation",
    attributes={
        "state.operation": "mark_processed" | "mark_failed" | "is_processed" | "load" | "save",
        "state.identifier": identifier,
    }
) as span:
    pass
```

Light instrumentation — these are fast local file operations. The span is mainly for completeness in the trace waterfall.

### 4.10 `cli.py` — Telemetry initialization

Wire `init_telemetry()` into the CLI entrypoint:

```python
import click
from paper_library.telemetry import init_telemetry, get_logger

@click.group()
@click.option("--diagnostics", is_flag=True, help="Enable detailed token/cost diagnostics")
def cli(diagnostics):
    log_level = "DEBUG" if diagnostics else None
    init_telemetry(log_level_override=log_level)

# All subcommands inherit the initialized telemetry
```

---

## 5. Token-Aware Text Truncation

### Problem

The current text truncation in `synthesis_generator.py` uses a character-based cutoff (100K chars ≈ 25K tokens). This is a blunt instrument — the character-to-token ratio varies significantly depending on content:

- Clean English prose: ~4 chars/token
- Dense math notation: ~2-3 chars/token (more tokens per character)
- OCR artifacts / noisy PDF extraction: unpredictable, often inflated
- Non-Latin scripts: ~1-2 chars/token
- Code snippets in papers: ~3-4 chars/token

A 100K character paper heavy on math could be 40K+ tokens, while a clean prose paper of the same length might be 25K. The character cutoff can't distinguish these cases.

### Solution

Replace the character-based cutoff with token-estimated truncation using ttok. This is a pre-call estimation step, not a replacement for the post-call exact counts from `response.usage` (which the instrumentation in section 4.6 already captures).

### Implementation: `paper_library/token_utils.py`

```python
"""
Token estimation and text truncation utilities.

Uses ttok (Simon Willison's token counter) for fast local estimates.
ttok uses OpenAI's tiktoken tokenizer, which is ~5-15% off from
Anthropic's tokenizer — accurate enough for truncation decisions,
not for billing.

The actual billed token count comes from response.usage after the
API call (captured by telemetry instrumentation).

Usage:
    from paper_library.token_utils import estimate_tokens, truncate_to_token_budget

    tokens = estimate_tokens(text)
    truncated = truncate_to_token_budget(text, max_tokens=150_000)
"""

import subprocess
from paper_library.telemetry import get_logger

logger = get_logger(__name__)

# Default model for ttok estimation.
# cl100k_base is used by GPT-4/GPT-3.5-turbo and is the closest
# available approximation to Anthropic's tokenizer.
TTOK_MODEL = "gpt-4"


def estimate_tokens(text: str, model: str = TTOK_MODEL) -> int:
    """
    Estimate token count for a text string.

    Uses ttok as a subprocess for simplicity. For high-throughput
    scenarios, consider importing tiktoken directly instead.

    Args:
        text: The text to estimate tokens for
        model: The tiktoken model to use for estimation

    Returns:
        Estimated token count (approximate — ~5-15% off from Anthropic billing)
    """
    try:
        result = subprocess.run(
            ["ttok", "-m", model],
            input=text,
            capture_output=True,
            text=True,
            timeout=10,
        )
        return int(result.stdout.strip())
    except (subprocess.TimeoutExpired, FileNotFoundError, ValueError) as e:
        # Fallback: rough character-based estimate (4 chars/token)
        logger.warning(
            "ttok_estimation_failed",
            error=str(e),
            fallback="char_estimate",
        )
        return len(text) // 4


def truncate_to_token_budget(
    text: str,
    max_tokens: int = 150_000,
    model: str = TTOK_MODEL,
) -> tuple[str, int, bool]:
    """
    Truncate text to fit within a token budget.

    Truncation is smart:
    - Cuts at paragraph boundaries when possible
    - Falls back to sentence boundaries
    - Never cuts mid-word
    - Prefers cutting from the end (bibliography is already
      removed upstream; tail is typically conclusion/appendix)
    - Uses binary search to avoid repeated ttok calls

    Args:
        text: The text to potentially truncate
        max_tokens: Maximum token budget for the text portion.
                    Default 150K leaves ~50K headroom for skills
                    overhead, system prompt, and output tokens
                    within Haiku's 200K context window.
        model: The tiktoken model for estimation

    Returns:
        Tuple of (truncated_text, estimated_tokens, was_truncated)
    """
    estimated = estimate_tokens(text, model)

    if estimated <= max_tokens:
        return text, estimated, False

    logger.info(
        "text_truncation_needed",
        estimated_tokens=estimated,
        max_tokens=max_tokens,
        text_chars=len(text),
    )

    # Binary search for the right truncation point
    # Start with a proportional guess based on the overshoot ratio
    ratio = max_tokens / estimated
    low = 0
    high = len(text)
    target_chars = int(len(text) * ratio * 0.95)  # 5% conservative

    # Find the nearest paragraph boundary before target_chars
    truncated = _truncate_at_boundary(text, target_chars)
    final_estimate = estimate_tokens(truncated, model)

    # If still over budget, tighten
    if final_estimate > max_tokens:
        # Reduce by the overshoot proportion
        adjusted_ratio = max_tokens / final_estimate
        target_chars = int(len(truncated) * adjusted_ratio * 0.95)
        truncated = _truncate_at_boundary(text, target_chars)
        final_estimate = estimate_tokens(truncated, model)

    logger.info(
        "text_truncated",
        original_tokens=estimated,
        truncated_tokens=final_estimate,
        original_chars=len(text),
        truncated_chars=len(truncated),
        chars_removed=len(text) - len(truncated),
    )

    return truncated, final_estimate, True


def _truncate_at_boundary(text: str, max_chars: int) -> str:
    """
    Truncate text at the nearest clean boundary before max_chars.

    Priority: paragraph break (double newline) > sentence end (. ! ?) > word boundary (space)
    """
    if max_chars >= len(text):
        return text

    # Look for paragraph break in the last 500 chars before cutoff
    search_start = max(0, max_chars - 500)
    chunk = text[search_start:max_chars]

    # Try paragraph boundary first
    para_break = chunk.rfind("\n\n")
    if para_break != -1:
        return text[:search_start + para_break].rstrip()

    # Try sentence boundary
    for punct in [". ", "! ", "? "]:
        sent_break = chunk.rfind(punct)
        if sent_break != -1:
            return text[:search_start + sent_break + 1].rstrip()

    # Fall back to word boundary
    space = chunk.rfind(" ")
    if space != -1:
        return text[:search_start + space].rstrip()

    # Last resort: hard cut
    return text[:max_chars].rstrip()
```

### Configuration

The `max_tokens` budget should be configurable, not hardcoded. Add to `config.py`:

```python
# Token budget for paper text sent to Claude.
# Haiku 4.5 has a 200K context window.
# Default 150K leaves headroom for skills overhead + output.
# Adjust downward for cost control, upward if context window expands.
SYNTHESIS_TOKEN_BUDGET = int(os.getenv("ALCANZAI_SYNTHESIS_TOKEN_BUDGET", "150000"))
```

Add to `.env.example`:

```bash
# Token budget for text sent to Claude (default: 150000)
# Lower for cost control, raise if using a model with larger context
# ALCANZAI_SYNTHESIS_TOKEN_BUDGET=150000
```

### Integration with `synthesis_generator.py`

Replace the existing character-based truncation with token-aware truncation.

The current code (approximate):
```python
# Existing: character-based cutoff
text = text[:100_000]  # ~25K tokens rough estimate
```

Replace with:
```python
from paper_library.token_utils import truncate_to_token_budget
from paper_library.config import config

# Token-aware truncation
text, estimated_tokens, was_truncated = truncate_to_token_budget(
    text,
    max_tokens=config.SYNTHESIS_TOKEN_BUDGET,
)

# Record in the span (from section 4.6 instrumentation)
span.set_attribute("llm.text_estimated_tokens", estimated_tokens)
span.set_attribute("llm.text_was_truncated", was_truncated)
```

### Telemetry integration

The truncation step generates valuable data for cost analysis. These attributes are added to the `claude_synthesize` span alongside the existing attributes from section 4.6:

```python
# Pre-call estimation (from token_utils)
span.set_attribute("llm.text_estimated_tokens", estimated_tokens)
span.set_attribute("llm.text_was_truncated", was_truncated)

# Post-call actual (from response.usage — already in section 4.6)
span.set_attribute("llm.input_tokens", usage.input_tokens)

# Derived: estimation accuracy (how far off was ttok?)
if estimated_tokens > 0:
    span.set_attribute(
        "llm.token_estimation_accuracy",
        usage.input_tokens / estimated_tokens,
    )
    # Values < 1.0 mean ttok overestimated (truncated more than needed)
    # Values > 1.0 mean ttok underestimated (skills overhead not counted)
```

The `llm.token_estimation_accuracy` metric is particularly interesting — over time it tells you how reliable ttok's estimates are for your specific corpus. If it's consistently 1.3x (ttok undercounts by 30%), you know the skills overhead accounts for roughly 30% of input tokens. That's the kind of empirical insight that lets you make informed optimization decisions.

### Metrics

Add to the metrics in section 6:

```python
# Truncation events
truncation_events = meter.create_counter(
    "alcanzai.synthesis.truncation_events",
    description="Papers that required text truncation before synthesis",
    unit="papers",
)

# Token estimation accuracy distribution
estimation_accuracy = meter.create_histogram(
    "alcanzai.synthesis.token_estimation_accuracy",
    description="Ratio of actual input tokens to estimated tokens (1.0 = perfect)",
    unit="ratio",
)
```

### Future-proofing

The `SYNTHESIS_TOKEN_BUDGET` config value makes this adaptable:

- If Anthropic extends the 1M window to Haiku → raise the budget (but probably don't — cost control matters more than using all available context)
- If you switch to Sonnet for detailed summaries → per-task budgets via the register config or a model-specific override
- If you want to optimize cost → lower the budget and watch whether synthesis quality degrades (the telemetry will tell you)
- If ttok proves consistently inaccurate → swap in `client.messages.count_tokens()` for a `--precise` mode, keeping ttok as the fast default

### Alternative: tiktoken directly instead of ttok subprocess

ttok shells out to a subprocess, which adds ~50-100ms overhead per call. For batch processing this is negligible, but if you want to avoid it:

```python
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4")

def estimate_tokens(text: str) -> int:
    return len(enc.encode(text))
```

This is faster (no subprocess) but means importing tiktoken as a library dependency instead of ttok as a CLI tool. Either approach works — the spec uses ttok because it's what you were already investigating, but Claude Code can choose whichever is cleaner at implementation time. If using tiktoken directly, replace the `ttok` dependency with `tiktoken>=0.7.0` in pyproject.toml.

---

## 6. Metrics

These are OTel metrics (counters, histograms) exported alongside traces. In Grafana, they show up in Prometheus and power dashboards.

### 6.1 Counters

```python
# Papers processed
papers_processed = meter.create_counter(
    "alcanzai.papers.processed",
    description="Total papers processed",
    unit="papers",
)
# Usage: papers_processed.add(1, {"source_type": "arxiv", "status": "success"})

# Papers failed
papers_failed = meter.create_counter(
    "alcanzai.papers.failed",
    description="Total papers that failed processing",
    unit="papers",
)
# Usage: papers_failed.add(1, {"source_type": "doi", "error_type": "grobid_timeout"})

# Claude API tokens consumed
tokens_input = meter.create_counter(
    "alcanzai.llm.tokens.input",
    description="Total input tokens sent to Claude",
    unit="tokens",
)

tokens_output = meter.create_counter(
    "alcanzai.llm.tokens.output",
    description="Total output tokens received from Claude",
    unit="tokens",
)

# Claude API cost
cost_total = meter.create_counter(
    "alcanzai.llm.cost.usd",
    description="Total Claude API cost in USD",
    unit="usd",
)
# Usage: cost_total.add(0.0342, {"model": "claude-haiku-4-5", "task": "quick_synthesis"})

# API calls by service
api_calls = meter.create_counter(
    "alcanzai.api.calls",
    description="API calls by external service",
    unit="calls",
)
# Usage: api_calls.add(1, {"service": "grobid"})
#         api_calls.add(1, {"service": "arxiv"})
#         api_calls.add(1, {"service": "crossref"})

# Citations
citations_extracted = meter.create_counter(
    "alcanzai.citations.extracted",
    description="Total citations extracted",
    unit="citations",
)

citations_garbage_filtered = meter.create_counter(
    "alcanzai.citations.garbage_filtered",
    description="Citations removed by garbage filter",
    unit="citations",
)
```

### 6.2 Histograms

```python
# Processing duration by stage
processing_duration = meter.create_histogram(
    "alcanzai.processing.duration",
    description="Processing duration by stage",
    unit="seconds",
)
# Usage: processing_duration.record(30.5, {"stage": "grobid"})
#         processing_duration.record(2.1, {"stage": "synthesis"})

# Cost per paper
cost_per_paper = meter.create_histogram(
    "alcanzai.llm.cost_per_paper",
    description="Claude API cost per paper",
    unit="usd",
)

# Input tokens per paper
tokens_per_paper = meter.create_histogram(
    "alcanzai.llm.tokens_per_paper",
    description="Input tokens per paper",
    unit="tokens",
)

# Text length sent to Claude
text_chars_sent = meter.create_histogram(
    "alcanzai.synthesis.text_chars",
    description="Character count of text sent to Claude",
    unit="chars",
)

# GROBID response time
grobid_duration = meter.create_histogram(
    "alcanzai.grobid.duration",
    description="GROBID processing time",
    unit="seconds",
)

# Garbage score distribution
garbage_scores = meter.create_histogram(
    "alcanzai.citations.garbage_score",
    description="Distribution of citation garbage scores",
    unit="score",
)
```

### 6.3 Where to record metrics

Record metrics in the same places as span attributes — they're complementary. Spans give you per-request detail; metrics give you aggregates over time. Both are emitted from the same instrumented code.

---

## 7. Environment Variables

| Variable | Default | Description |
|---|---|---|
| `OTEL_EXPORTER_OTLP_ENDPOINT` | (none) | gRPC endpoint for Alloy/collector. If unset, OTLP export disabled. |
| `OTEL_SERVICE_NAME` | `alcanzai` | Service name in traces |
| `ALCANZAI_LOG_LEVEL` | `INFO` | Log level (DEBUG, INFO, WARNING, ERROR) |
| `ALCANZAI_LOG_FILE` | (none) | Path for JSON log file. If unset, stdout only. |
| `ALCANZAI_SYNTHESIS_TOKEN_BUDGET` | `150000` | Max estimated tokens for text sent to Claude. Lower for cost control. |

Add these to `.env.example`:

```bash
# Telemetry (optional — omit for local dev without Alloy)
# OTEL_EXPORTER_OTLP_ENDPOINT=http://alloy.monitoring:4317
# OTEL_SERVICE_NAME=alcanzai
# ALCANZAI_LOG_LEVEL=INFO
# ALCANZAI_LOG_FILE=diagnostics.jsonl
```

---

## 8. Local Dev Workflow

When running locally without Alloy:

1. No `OTEL_EXPORTER_OTLP_ENDPOINT` set → OTLP export silently disabled
2. Structured logs still go to stdout (console-formatted, with colors)
3. `--diagnostics` flag available for per-call token breakdowns
4. Optionally set `ALCANZAI_LOG_FILE=diagnostics.jsonl` to get JSON logs on disk for later analysis
5. All span attributes are still computed (for consistency) — they're just not exported

When running with Alloy:

1. Set `OTEL_EXPORTER_OTLP_ENDPOINT=http://alloy.monitoring:4317`
2. Traces appear in Tempo, metrics in Prometheus, logs in Loki
3. Logs include `trace_id` and `span_id` fields for cross-correlation
4. Click a trace_id in Loki → jump to the full trace in Tempo

---

## 9. Implementation Order

Recommended sequence for Claude Code:

1. **`telemetry.py`** — foundation module. Get OTel providers, structlog, and the graceful fallback working. Write a minimal test that verifies init works with and without OTLP endpoint.

2. **`cli.py` integration** — wire `init_telemetry()` into the CLI entrypoint, add `--diagnostics` flag.

3. **`orchestrator.py`** — replace all print statements, add root span. This is the most print-heavy module. Test end-to-end with a single paper to verify logging works.

4. **`synthesis_generator.py`** — add the critical token/cost instrumentation. This is the highest-value instrumentation for the cost optimization use case.

5. **`token_utils.py`** — token estimation and truncation. Wire into `synthesis_generator.py` to replace the character-based cutoff. Test with a few papers of varying length to verify truncation behavior.

6. **`grobid_processor.py`** — add spans and replace prints. Includes the citation quality metrics.

7. **Fetchers** (`arxiv_fetcher.py`, `doi_fetcher.py`, `web_fetcher.py`) — add spans and replace prints. Note that HTTP calls are already auto-instrumented, so the explicit spans are mainly for semantic grouping and metadata attachment.

8. **Supporting modules** (`citation_context.py`, `markdown_writer.py`, `state.py`) — lighter instrumentation, lower priority.

9. **Metrics** — can be added alongside spans in steps 3-8, or as a follow-up pass. The span attributes capture the same data; metrics are for Prometheus dashboards.

---

## 10. Testing

### Unit tests for telemetry.py

- Test that `init_telemetry()` works with no env vars set (graceful no-op)
- Test that `init_telemetry()` works with a mock OTLP endpoint
- Test that `get_logger()` returns a logger that includes trace context when inside a span
- Test that `--diagnostics` sets log level to DEBUG

### Unit tests for token_utils.py

- Test that `estimate_tokens()` returns a reasonable count for known text (e.g., 1000 English words ≈ 1300 tokens ± 20%)
- Test that `estimate_tokens()` falls back to character-based estimate when ttok is unavailable
- Test that `truncate_to_token_budget()` returns text unchanged when under budget (was_truncated=False)
- Test that `truncate_to_token_budget()` truncates at paragraph/sentence boundaries, not mid-word
- Test that `truncate_to_token_budget()` returns estimated token count in the tuple
- Test with edge cases: empty string, very short text, text with no paragraph breaks

### Integration test

- Process a single paper with `ALCANZAI_LOG_FILE` set
- Verify the JSON log file contains expected fields: `trace_id`, `span_id`, `level`, `event`
- Verify token cost fields are present in synthesis log entries
- Verify no `print()` calls remain in instrumented modules (grep test)

### Grep test (add to CI)

```bash
# No bare print() statements in production code
# (allow in tests and scripts)
grep -rn "^\s*print(" paper_library/ --include="*.py" && echo "FAIL: bare print() found" && exit 1 || echo "PASS: no bare print()"
```

---

## 11. Migration Notes

### print() → logger mapping conventions

- `print(f"Step N: ...")` → `logger.info("step_name", ...)`
- `print(f"  ✓ ...")` → `logger.info("step_complete", ...)`
- `print(f"  ✗ ...")` → `logger.error("step_failed", ...)`
- `print(f"⊘ ...")` → `logger.info("skipped", ...)`
- `print(f"{'='*70}")` → remove (structural formatting, not needed in structured logs)
- `print(f"✓ SUCCESS: ...")` → `logger.info("processing_complete", ...)`
- `print(f"✗ FAILED: ...")` → `logger.error("processing_failed", ...)`

### Preserving interactive console experience

The console renderer in structlog can be configured to produce human-friendly output with colors. When `OTEL_EXPORTER_OTLP_ENDPOINT` is unset (local dev), the logger should use the console renderer so the experience isn't degraded from the current print-statement UX. The `--diagnostics` flag adds token detail to this console output.

When running in production (K3s with Alloy), the JSON renderer is used — human readability doesn't matter because Loki/Grafana is the interface.

---

## 12. Open Design Questions (for implementation time)

These don't need answers before starting — they're things Claude Code may need to resolve during implementation:

1. **structlog vs stdlib logging**: This spec recommends structlog. If dependency constraints are an issue, stdlib `logging` with a custom `JSONFormatter` class works too — just more boilerplate. The OTel trace injection pattern is similar either way.

2. **Metric export interval**: The `PeriodicExportingMetricReader` default interval is 60 seconds. For a batch CLI tool that might finish in 30 seconds, you'd want to flush on shutdown. The OTel SDK handles this via `MeterProvider.shutdown()` — make sure this is called in the CLI cleanup.

3. **Span naming conventions**: This spec uses descriptive names like `process_paper`, `grobid_parse`, `claude_synthesize`. OTel convention recommends short, low-cardinality names. The names in this spec are fine — they're already low-cardinality (not parameterized with paper IDs or titles).

4. **The `_calculate_cost()` method** in synthesis_generator.py currently computes cost. Consider moving cost calculation to `telemetry.py` as a utility so it can be reused if we add other LLM calls in the future (e.g., detailed summaries, glossary extraction).

5. **ttok subprocess vs tiktoken library**: Section 5 provides both options. ttok is a CLI tool (subprocess call, ~50-100ms overhead). tiktoken is a library import (faster, no subprocess). Both use the same underlying tokenizer. Claude Code should pick whichever feels cleaner — if using tiktoken directly, swap the pyproject.toml dependency accordingly.