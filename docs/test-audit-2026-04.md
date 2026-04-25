# Test Audit — 2026-04-22

**Auditor:** Claude (Opus 4.7), autonomous session  
**Corpus:** `tests/` directory at commit `93ccde2` on branch `claude`  
**Baseline:** 157 passed, 26 deselected (integration), 1 warning — `pytest -m "not integration"`  
**Purpose:** Categorize every test for a future exomonad session to delegate fix work to Gemini. Findings-only; no code changes.

---

## Verdict Legend

| Verdict | Meaning |
|---|---|
| **keep** | Well-formed; tests meaningful behavior with reasonable assertions |
| **improve** | Tests the right thing but has specific weaknesses (weak assertion, fragile fixture, redundant scope, etc.) |
| **rewrite** | Doesn't test what it claims to; structure needs redesign |
| **delete** | Redundant, broken, obsoleted by other tests, or pure scaffolding |

For downstream work, each improve/rewrite/delete finding includes:
- **Why**: specific diagnosis
- **Suggested fix**: concrete prescription (what a better version looks like)
- **Priority**: H / M / L (for ordering fix PRs)

---

## Methodology

1. Read every file in `tests/` and `tests/legacy/`
2. For each test function, determine:
   - What behavior is being tested?
   - Are the assertions actually sensitive to that behavior? (Would the test fail if the SUT regressed?)
   - Are fixtures appropriate / over-mocked / brittle?
   - Is there redundant coverage elsewhere?
3. Categorize + record rationale
4. Surface cross-cutting patterns separately

---

## Executive Summary

**Corpus:** 11 active test files + 4 legacy files, ~170 tests (157 unit + 26 integration; 1 misclassified). Baseline `pytest -m "not integration"`: 157 passed, 1 warning.

**Overall health:** Better than I expected on first read. The largest test files (`test_doi_fetcher.py`, `test_web_fetcher.py`, `test_citation_context.py`) are genuinely well-crafted — good section structure, realistic fixtures, mocking discipline, edge-case awareness. These three files account for ~65% of the corpus and are largely **keep**.

**The rot is concentrated.** The following files have serious quality issues that dominate the fix queue:

| File | Tests | Main problem | Priority |
|---|---|---|---|
| `tests/test_pipeline.py` | 1 | Silent API cost leak — integration test runs on every `pytest` invocation with no assertion | **H** |
| `tests/test_telemetry.py` | 4 | All tautologies or non-assertions; blocks issue #3 (local trace validation) | **H** |
| `tests/test_synthesis_generator.py` | 3 | Zero unit tests; no verification of the Claude API request shape | **H** |
| `tests/legacy/*.py` | ~10 | Pre-pytest manual scripts, superseded, still taking up space | **M** |

**Approximate verdict breakdown** (numbers are loose; individual counts are in each file's section):

| Verdict | Active tests | Legacy tests |
|---|---|---|
| **keep** | ~140 | 0 |
| **improve** | ~22 | 0 |
| **rewrite** | ~7 | 0 |
| **delete** | 0 | ~10 |
| **add (new)** | ~35–45 | — |

**Top structural observations** (expanded below):
1. **No tests for `models.py`** — Pydantic validation is tested transitively only
2. **No tests for `state.py` / `StateManager`** — deduplication logic relies on transitive orchestrator-path testing
3. **Mock-helper duplication** across `test_doi_fetcher.py` and `test_web_fetcher.py`
4. **Weak assertions are a pattern** — several tests use "should not raise" / existence checks / broad ranges where structural verification is achievable

**Good news:** nothing in the audit suggests the test suite is silently hiding a live bug in the shipping code. The high-priority issues are about *trust* (can the suite catch regressions going forward?) rather than *correctness of current shipping code*.

---

## File-by-File Findings

### `tests/conftest.py` — **keep** (11 lines)

Registers the `integration` marker via `pytest_configure`. No fixtures, no hooks beyond that. Minimal and correct.

*No action.*

**Future opportunity (not current finding):** if shared fixtures emerge (common `PaperMetadata` builder, API-key-guarded skipper, temp-vault factory), they belong here.

---

### `tests/legacy/test_arxiv.py` — **delete** (104 lines)
### `tests/legacy/test_grobid.py` — **delete** (115 lines)
### `tests/legacy/test_markdown.py` — **delete** (98 lines)
### `tests/legacy/test_synthesis.py` — **delete** (133 lines)

All four are **pre-pytest manual smoke scripts** from v0.1.0 — `print`-driven, `if __name__ == "__main__":` blocks, `sys.argv` parsing, return values instead of assertions. Already excluded from pytest via `norecursedirs = ["legacy"]` in `pyproject.toml` so they never run. The user's memory notes (`MEMORY.md`) explicitly flag them as "Consider deleting; they're superseded."

Each has a modern successor:
- `test_arxiv.py` → `tests/test_arxiv_fetcher.py`
- `test_grobid.py` → `tests/test_grobid_processor.py`
- `test_markdown.py` → `tests/test_markdown_writer.py`
- `test_synthesis.py` → `tests/test_synthesis_generator.py`

**Suggested fix:** `git rm tests/legacy/ -r` as a single commit. No code depends on them. Remove `norecursedirs = ["legacy"]` from `pyproject.toml` in the same commit (becomes unnecessary). *Priority:* **M** — housekeeping, not blocking anything.

**Caveat for Gemini:** verify no CI workflow or docs reference `tests/legacy/` before deletion. A quick `grep -r "tests/legacy" --exclude-dir=.git --exclude-dir=.venv` would catch any linger references.

---

### `tests/test_pipeline.py` — **rewrite + relocate** (137 lines) — **HIGH PRIORITY**

**This is the warning source in the baseline pytest run.**

```
PytestReturnNotNoneWarning: Test functions should return None,
but tests/test_pipeline.py::test_pipeline returned <class 'bool'>.
```

**Why it's broken:**
1. Structured exactly like the `tests/legacy/` scripts — print-driven, returns bool, runs an interactive pre-flight checks block. **Zero `assert` statements.**
2. NOT marked `@pytest.mark.integration`, so it runs on every `pytest -m "not integration"` invocation. It's only called out as "integration" in prose comments.
3. Because it returns False instead of raising when GROBID or the API key is missing, **pytest scores it as passing regardless of whether the pipeline actually worked**. The test cannot fail except via a raised exception inside `processor.process()`.
4. If GROBID + API key *are* configured, it will hit the live arXiv API, GROBID, and Anthropic — turning every local `pytest` run into a $0.01+ API call silently.

**Suggested fix:**
- **Relocate** to `scripts/smoke-pipeline.py` (or similar) — it is, genuinely, a useful manual smoke test. Just not a pytest test.
- **OR** rewrite in-place as a proper pytest integration test:
  - Add `@pytest.mark.integration` decorator
  - Replace the pre-flight `return False` paths with `pytest.skip(reason=...)`
  - Replace prints with `assert` statements against actual pipeline outcomes (was a note written? does it contain expected sections? did state update?)
  - Keep the CLI entry (`if __name__ == "__main__":`) for manual use; wrap the body in an assertions-driven function that pytest calls

**Priority:** **H** — fixing this removes the only warning in the current test run and closes a silent-API-cost leak.

---

### `tests/test_arxiv_fetcher.py` — **keep with improvements** (169 lines, 17 tests)

**What's good:** 9 pure-unit tests on `parse_arxiv_id` with solid edge-case coverage (version suffixes, URL forms, case-insensitivity, whitespace, invalid input, legacy archive/id format). Clean class-based organization.

**What needs improving:**

1. **Test efficiency (priority M):** `TestArxivFetching` + `TestArxivAuthorsFormatting` together make **10 network calls to fetch the same paper** (1706.03762). Each test calls `fetcher.fetch("1706.03762")` from scratch. Should use a `@pytest.fixture(scope="module")` to fetch once and reuse the result.

   ```python
   @pytest.fixture(scope="module")
   def attention_paper():
       return ArxivFetcher(config.vault_path).fetch("1706.03762")
   ```

2. **Weak assertion (priority L):** `test_authors_formatted_correctly` asserts `"," in author or len(author.split()) == 1` — allows "Smith, John" and "Vaswani" but rejects "John Smith". Mostly OK but the intent (testing "Lastname, Firstname" format OR mononym) could be more explicit.

3. **Integration-test dependency on network behavior (priority L):** `test_fetch_skips_already_downloaded_pdf` is order-sensitive — works only if no prior test in the module deleted the PDF. The module-scoped fixture above would make this robust.

**Verdict breakdown:**
- 9 tests **keep** (TestArxivIdParsing)
- 6 tests **improve** (refactor to shared fixture)
- 2 tests **improve** (TestArxivAuthorsFormatting — same fixture issue)

---

### `tests/test_doi_fetcher.py` — **keep** (371 lines, ~43 tests)

**What's good:** Exemplary. Section headers (`# ------`) organize the file. Mocking strategy is clean: module-level `_make_crossref_response()` + `_mock_response()` helpers. All non-live tests are fast and self-contained. Good comment on `test_doi_embedded_in_publisher_url` explains a real trade-off (can't distinguish real DOI from publisher-appended article ID).

**Minor nits:**

1. **Naming confusion (priority L):** `TestFetchIntegration` class contains heavily mocked tests — "integration" is misleading. Rename to `TestFetchEndToEndMocked` or `TestFetchOrchestration` to avoid conflating with `@pytest.mark.integration`.

2. **Redundancy with `TestRealDoi` (priority L):** The single test in `TestRealDoi` is adequate proof-of-life for live Crossref. Consider adding one for live Unpaywall too, once someone has cycles — not a current issue.

**Verdict:** ~42 **keep**, 1 **improve** (class rename). No rewrites or deletes.

This is the model to imitate for other test files.

---

### `tests/test_web_fetcher.py` — **keep with improvements** (506 lines, ~40 tests)

**What's good:** Comprehensive coverage of URL detection, unsupported-host blocking, HTML parsing helpers, PDF-link-finder heuristic, and full `fetch()` paths with mocked HTTP. `TestUnsupportedHosts` uses `@pytest.mark.parametrize` well. Error paths (timeout, 404, invalid URL) are covered.

**What needs improving:**

1. **Helper duplication (priority M):** `_mock_head()` and `_mock_get()` are redefined inside both `TestLandingPageToPdfRouting` and `TestFetchWithMockedHttp`. Hoist to a module-level fixture or a small `_helpers` module shared with `test_doi_fetcher.py`'s `_mock_response()`. A shared `tests/_mock_helpers.py` or `conftest.py` fixture would eliminate the duplication.

2. **`GOOD_HTML` class constant is verbose (priority L):** could move to a fixture file or a helper that generates padding-length HTML on demand. Not a correctness issue.

3. **Paywall detection coverage (priority L):** only two tests (`test_paywall_detected_by_class`, `test_no_paywall_for_normal_page`). Paywall heuristics are fragile; a few more test cases (body-length-based detection, "subscribe to read" text markers, etc.) would be worthwhile — though "what counts as a paywall" is a minor design question.

**Verdict:** ~37 **keep**, 3 **improve** (mostly refactoring).

---

### `tests/test_citation_context.py` — **keep with improvements** (344 lines, ~22 tests)

**What's good:** Module-level `SAMPLE_TEXT` and `NUMERIC_TEXT` fixtures are readable and realistic. Citation fixtures (`vaswani`, `bahdanau`, `devlin`) are reusable. Coverage of both author-year and numeric [N] styles matches the production extractor's two-mode design. Tests for important edge cases: off-by-one numeric matching (`[30]` not matching `[3]` pattern), missing year, empty list, DOI-as-key precedence.

**What needs improving:**

1. **Hacky placeholder citation (priority L):** in `test_does_not_match_wrong_citation_number`:
   ```python
   _placeholder = Citation(raw_text="placeholder")
   contexts = extractor.extract_contexts(text, [_placeholder, _placeholder, citation_3])
   ```
   Uses two `_placeholder` objects purely for list-index padding. Works but obscures intent. A helper like `citations_at_index(3, citation_3)` would read better, or the test should use a direct parameter if the API supports positional injection.

2. **Bibliography removal is under-tested (priority M):** `TestBibliographyRemoval` has only 2 tests, but `_remove_bibliography` is heuristic and order-sensitive. Worth adding:
   - All-caps `REFERENCES` header
   - `Bibliography` instead of `References`
   - Multiple section headers (how does it decide?)
   - Body text that contains the word "References" as prose mid-paper but no actual bibliography section

3. **`TestNumericCitations.test_context_contains_surrounding_text` (priority L):** the final assertion:
   ```python
   assert any(kw in combined.lower() for kw in ["transformer", "attention", "recurrence"])
   ```
   is testing that at least one of three keywords is in the extracted context, which is a very weak proxy for "the context captured the citing sentence." If the extractor returned only the word " " around `[2]`, this could still pass for some paper texts. Strengthen by asserting more specifically on window size or structural properties.

**Verdict:** ~18 **keep**, 3 **improve**, 1 *opportunity* (expand bibliography tests).

---

### `tests/test_markdown_writer.py` — **keep with coverage gaps** (210 lines, ~15 tests)

**What's good:** `test_markdown_has_yaml_frontmatter` actually parses the YAML with `yaml.safe_load` and asserts on the parsed dict — that's exactly the right kind of assertion (robust against whitespace/formatting changes, validates the contract). Source-note tests and article-source-link tests cover the post-v0.2.0 split-content architecture well. Filename tests cover quote removal and character sanitization.

**Coverage gaps (priority M):**

The commit history and project memory reference several markdown-writer features that have **zero test coverage**:

1. **Filename smart-truncation at word boundaries** — commit notes say "smart truncation at boundaries, single ellipsis" but no test exercises title that exceeds the length limit.
2. **Period-to-dash substitution in filenames** — `3.1 → 3-1`, `U.S.A. → U-S-A-` (per commit `4315aa3`'s ancestors). No test.
3. **Citation wikilink format** — `[[Author, Author & Author (Year) - Title]]` with full author list for disambiguation. No test.
4. **Garbage citation filtering applied to list** — `markdown_writer` receives `metadata.citations` post-filter. Not a writer concern per se, but there's no test verifying that the output list matches the filtered input.
5. **UTF-8 author name handling** — mojibake (`é → Ã©`) was a past bug (commit mentions "explicitly set response.encoding='utf-8'"). No regression test for non-ASCII author names in the frontmatter.
6. **YAML escaping for colons/quotes in title** — commit `b0b45d0` and earlier fixed YAML frontmatter edge cases. No test for titles containing `:`, `"`, or leading/trailing punctuation that YAML treats specially.

**Suggested fix:** Add ~6 tests targeting the gaps above. Each is straightforward — build a `PaperMetadata` with the pathological input, call `generate_filename` or `paper_to_markdown`, assert the output is sanitized/escaped correctly.

**Verdict:** 15 **keep**, ~6 **add** (coverage gaps).

---

### `tests/test_grobid_processor.py` — **keep with fixes** (240 lines, ~20 tests)

**What's good:** `TestExtractBodyText` (6 tests) is the gold standard of this file — uses an embedded `SAMPLE_TEI` XML string, no network, no fixture PDF, and directly verifies the critical behavior that `[N]` citation markers inside `<ref>` elements survive text extraction. Fast and focused.

**What needs fixing:**

1. **`test_processor_initialized_with_url` is environment-coupled (priority L):**
   ```python
   assert "localhost" in processor.grobid_url or "8070" in processor.grobid_url
   ```
   This asserts something about `config.grobid_url` (env-driven) rather than the processor. If a developer sets `GROBID_URL=http://grobid.mynet.com`, the test fails. **Rewrite:** pass an explicit URL like `GrobidProcessor("http://test:9999")` and assert `processor.grobid_url == "http://test:9999"`.

2. **Silent integration-test skipping (priority M):** 9 tests across `TestGrobidMetadataExtraction` and `TestGrobidCitationExtraction` depend on `tests/fixtures/sample.pdf`. If the fixture doesn't exist, they skip with a message pointing to `tests/fixtures/README.md`. **Verify that file exists; if not, either commit a test fixture (an arXiv paper with a redistributable license) or delete these tests.** Silent skips make coverage look better than it is.

3. **Weak assertions on extracted fields (priority L):** `test_extract_title` asserts `len(title) > 0 and len(title) < 500`. If GROBID returns literally `"a"`, this passes. Worth asserting title is a proper English string (contains a space, doesn't start with a digit, etc.) — or cross-checking against known metadata for the fixture PDF.

**Verdict:** 14 **keep**, 1 **rewrite** (URL test), 1 **fix-or-delete** (fixture dependency), 5 **improve** (stronger field assertions).

---

### `tests/test_token_utils.py` — **improve** (35 lines, 5 tests)

**What's good:** Covers core happy-path and empty-string cases. Token-count range assertions are appropriately tolerant of tiktoken's estimation variance.

**What needs improving:**

1. **`test_truncate_at_paragraph_boundary` name vs. body mismatch (priority M):** The test name says "at_paragraph_boundary" but asserts only `len(result) < len(long_text)` and token count. It doesn't verify the truncation actually happened *at* a `\n\n` boundary. Add:
   ```python
   assert result.endswith("word") or result.endswith("word ")  # word-boundary, not mid-word
   # OR stronger: if paragraphs exist in source, result should end at one
   ```

2. **Boundary-fallback hierarchy is untested (priority M):** `_truncate_at_boundary()` implements a 4-level fallback (paragraph → sentence → word → hard cut). Only the paragraph case is implicitly tested. Missing:
   - Text without paragraph breaks but with sentences — verify sentence-boundary cut
   - Text without sentences but with spaces — verify word-boundary cut
   - Text without any spaces — verify hard cut (edge case, but possible for heavily-encoded content)

3. **Re-truncation pass untested (priority M):** `truncate_to_token_budget` has a "if still over budget, do one more conservative pass" branch. No test exercises the path where the first truncation undershoots (which can happen when the char-ratio estimate is off).

4. **Tiktoken encoder fallback untested (priority L):** `_get_encoder` has a fallback to `cl100k_base` if gpt-4 encoding fails. Not easy to trigger in a test, but could be mocked.

**Verdict:** 2 **keep** (empty-string cases), 1 **improve** (paragraph boundary assertion), 1 **improve** (truncation test scope), 4–6 **add** (fallback coverage).

**Priority:** M overall — token-budget correctness directly affects whether synthesis runs blow the 200K context limit.

---

### `tests/test_telemetry.py` — **rewrite entirely** (29 lines, 4 tests) — **HIGH PRIORITY**

**This is the placeholder-quality file that surfaced the audit need.**

Every test is either a tautology, a non-assertion, or checks attribute existence instead of behavior. Matches the diagnosis in issue #7:

| Test | Diagnosis |
|---|---|
| `test_init_telemetry_no_otlp` | Asserts `tracer is not None` and `meter is not None`. These are module-level constants defined at import time as `trace.get_tracer("alcanzai")` — they are **always** non-None regardless of whether `init_telemetry()` ran correctly. Tautology. |
| `test_init_telemetry_idempotent` | Comment: "If it didn't raise, we consider it successful for this unit test." **No assertion.** Doesn't verify handlers aren't duplicated on re-init. |
| `test_get_logger_returns_logger` | Checks `.info`, `.debug`, `.warning`, `.error` attributes exist. Structural, not behavioral — structlog loggers always have these. |
| `test_diagnostics_sets_debug_level` | Comment: "should not raise". **No assertion** that DEBUG was actually set on the root logger. |

**Suggested rewrite:**

```python
# Use OTel's in-memory exporter
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

def test_spans_are_created_and_exported():
    """Real span flow: start_as_current_span should produce a retrievable span."""
    exporter = InMemorySpanExporter()
    # ... wire exporter, run a trivial tracer call, assert exporter.get_finished_spans() is non-empty ...
    
def test_trace_id_injected_into_logs(caplog):
    """When inside an active span, logs should carry trace_id/span_id fields."""
    # ... wrap a logger call inside a start_as_current_span, assert caplog records have trace_id ...
    
def test_init_telemetry_is_truly_idempotent():
    """Root logger handler count should not grow after repeated init_telemetry() calls."""
    import logging
    init_telemetry()
    handlers_before = len(logging.getLogger().handlers)
    init_telemetry()
    assert len(logging.getLogger().handlers) == handlers_before
    
def test_log_level_override_applied():
    init_telemetry(log_level_override="DEBUG")
    import logging
    assert logging.getLogger().level == logging.DEBUG
```

**Priority:** H — explicitly called out in issue #7 as part of instrumentation hardening. This test file is also the immediate blocker for issue #3 (local trace validation) because without real span-exporter tests, we can't prove the instrumentation works locally.

---

### `tests/test_synthesis_generator.py` — **expand heavily** (71 lines, 3 tests) — **HIGH PRIORITY**

**What's there:** 3 integration tests that hit the live Anthropic API. Each constructs the same `SynthesisGenerator` + fixture and calls `generate_quick_synthesis()`. Assertions check that the returned `Synthesis` object has non-None fields and cost is in a reasonable range.

**What's missing:** 

**Zero unit tests.** The generator has many pure functions that are trivial to test without network:

1. **`_parse_quick_synthesis_response(response_text)`** — XML tag extraction. Edge cases: missing tags, malformed tags, empty tag content, quotes embedded in memorable_quote, trailing/leading whitespace.
2. **`_calculate_cost(input_tokens, output_tokens)`** — Pure arithmetic, easily verified (1M input = $1.00, etc.).
3. **`_infer_research_area(metadata)`** — Keyword matching over a fixed dict. Test each keyword category, test fallback to "machine learning and AI".
4. **`_build_quick_synthesis_message(text, metadata, register, citation_contexts)`** — Prompt construction. Verify register params flow through, author-truncation at 3+, citation-context truncation at 10K chars.

**Live-test inefficiency (priority M):**
All 3 integration tests use function-scoped fixtures — every test makes a new API call. A `@pytest.fixture(scope="module")` would cut API costs per test run by ~3×.

**No request-shape test (priority M):**
The `client.beta.messages.create()` call has a specific shape (`betas=[SKILLS_BETA, CODE_EXECUTION_BETA]`, `container={"skills": skill_containers}`, `tools=[CODE_EXECUTION_TOOL]`). If the Anthropic SDK changes any of these keyword names, the pipeline breaks silently in production. A **mocked** test asserting on `mock_client.beta.messages.create.call_args.kwargs` would catch that regression. Example:

```python
def test_api_call_shape():
    with patch.object(generator.client.beta.messages, "create") as mock_create:
        mock_create.return_value = MagicMock(
            content=[MagicMock(text="<summary>x</summary><why_you_cared>y</why_you_cared><key_concepts>a,b</key_concepts><memorable_quote>q</memorable_quote>")],
            usage=MagicMock(input_tokens=100, output_tokens=50,
                            cache_read_input_tokens=0, cache_creation_input_tokens=0),
            stop_reason="end_turn",
        )
        generator.generate_quick_synthesis("text", metadata)
        kw = mock_create.call_args.kwargs
        assert "skills-2025-10-02" in kw["betas"]
        assert "code-execution-2025-08-25" in kw["betas"]
        assert kw["container"]["skills"]  # non-empty
```

**Verdict:** 3 **keep** (integration tests, session-scope them), ~15 **add** (unit tests for pure functions + request-shape mock).

**Priority:** H — this is where most of the recurring cost per paper lives. Silent breakage here is expensive.

---

---

## Cross-Cutting Observations

### 1. Modules entirely lacking direct test coverage

- **`paper_library/models.py`** — Pydantic models (`BibliographicEntry`, `Citation`, `PaperMetadata`, `ArticleMetadata`, `Synthesis`, `ProcessingState`). Exercised transitively by every other test, but no dedicated test file. Worth one: validation edge cases (year boundaries, required-vs-optional fields, `contexts: list[str]` default, `pdf_path: Optional[str]`, BibliographicEntry→Citation/PaperMetadata override behavior).
- **`paper_library/state.py`** / `StateManager` — deduplication logic across 3 ID types (arXiv, DOI, URL), idempotent re-runs, `--force` flag behavior. Currently only tested transitively via orchestrator integration paths. Given that state correctness gates every ingest run, worth a dedicated file.
- **`paper_library/skills_manager.py`** — no direct test file. ID caching, `invalidate_cache()`, container-construction logic. Mocked tests possible.
- **`paper_library/config.py`** — no test file. Env var parsing, path derivation. Simple but trivially testable.
- **`paper_library/cli.py`** — no test file. Click command-parsing + flag plumbing. `CliRunner` from click makes this trivially testable.

### 2. Helper duplication

Three patterns appear in multiple files:
- `_mock_response(status, json_data, content)` — in `test_doi_fetcher.py`
- `_mock_head(content_type)` / `_mock_get(content, content_type)` — duplicated in both `test_doi_fetcher.py` (implicit) and `test_web_fetcher.py` (explicit, in two classes)

Hoisting to `tests/conftest.py` (as fixtures) or `tests/_mock_helpers.py` (as plain functions) would remove ~60 lines of boilerplate and give a single source of truth for mock-response shapes.

### 3. "Weak assertion" pattern

Several tests are structural or existence-checking when they could verify behavior:
- `test_init_telemetry_idempotent` → "should not raise" (no assertion)
- `test_diagnostics_sets_debug_level` → "should not raise" (no assertion)
- `test_extract_title` (GROBID) → `0 < len(title) < 500`
- `test_authors_formatted_correctly` → `"," in author or len(author.split()) == 1`
- `test_context_contains_surrounding_text` → `any(kw in combined.lower() for kw in [...])`

None of these are broken per se, but they're the kind of tests that pass even when the behavior they're nominally protecting has regressed.

### 4. Integration-test inefficiency

Several test classes make the same network/API call per-test:
- `test_arxiv_fetcher.py` fetches `1706.03762` ten times across two classes
- `test_synthesis_generator.py` makes three live Anthropic calls per run
- `test_grobid_processor.py` sends the same `sample.pdf` through GROBID six to nine times

Module-scope fixtures would reduce both runtime (significant for GROBID — 30s per call) and spend (live API tests cost real money).

### 5. The "integration" marker is inconsistently applied

- `test_pipeline.py::test_pipeline` — hits live API + GROBID + arXiv. **Not marked.**
- `test_doi_fetcher.py::TestFetchIntegration` — class name says "Integration" but contents are fully mocked. **Shouldn't be marked, but the name misleads.**
- `test_grobid_processor.py::test_processor_initialized_with_url` — labeled "unit" in the class name, but the assertion depends on env-configured `config.grobid_url`, making it partly an environment test.

A documented convention for "what qualifies as integration" would make future PRs consistent. The rough cut seems to be "requires external state (network, disk, env)" but `config.grobid_url`-sensitivity blurs it.

### 6. Python version on the cusp

`pyproject.toml` says `requires-python = ">=3.9"` and `target-version = ['py39', ..., 'py314']` — but the venv is running 3.14 (visible in `.pyc` paths from earlier: `__pycache__/*.cpython-314.pyc`). No tests exercise version-sensitive code paths. If the project genuinely supports 3.9+, CI should run against at least the oldest target to catch inadvertent use of newer syntax (walrus operators are fine for 3.9, but e.g. PEP 604 `X | Y` type unions need 3.10+, and `orchestrator.py:169` uses `list[str]` which is 3.9+). Worth verifying CI config matches stated support.

---

## Recommended Action Queue

**Format:** each item is sized to be a single Gemini-drafted PR. Dependencies noted where relevant. File paths are absolute from repo root.

### H-priority (do first)

#### A1. Delete `tests/legacy/`
- **Remove:** `tests/legacy/test_arxiv.py`, `tests/legacy/test_grobid.py`, `tests/legacy/test_markdown.py`, `tests/legacy/test_synthesis.py`
- **Remove from `pyproject.toml`:** the `norecursedirs = ["legacy"]` line in `[tool.pytest.ini_options]` (no longer needed)
- **Verify first:** `grep -r "tests/legacy" --exclude-dir=.git --exclude-dir=.venv .` returns no matches in CI workflows, docs, or code
- **Commit message:** `Remove superseded v0.1.0 manual test scripts`
- **Dependency:** none. Can go first.

#### A2. Fix `tests/test_pipeline.py` — silent API cost leak
- **Choose one approach:**
  - **(a)** Relocate to `scripts/smoke-pipeline.py`, keep it as a manual CLI tool; remove from `tests/`
  - **(b)** Rewrite in-place:
    - Add `@pytest.mark.integration` decorator
    - Replace `return False` pre-flight exits with `pytest.skip(reason=...)`
    - Replace prints with `assert` statements on post-pipeline state (`state.is_processed(arxiv_id)` is True, a .md file exists at `config.papers_dir / f"{expected_filename}.md"` and contains "Attention" in the title, etc.)
    - Keep `if __name__ == "__main__":` for manual use
- **Recommended:** (b) — preserves the smoke test's value without the cost leak
- **Commit message:** `Fix test_pipeline.py: add integration marker, assert on outcomes`
- **Dependency:** none.

#### A3. Rewrite `tests/test_telemetry.py`
- **Delete** all 4 existing tests
- **Add:**
  - Real span-creation test using `InMemorySpanExporter` (from `opentelemetry.sdk.trace.export.in_memory_span_exporter`)
  - Trace-ID-in-logs test using pytest's `caplog` fixture
  - Actual idempotence test (handler count)
  - Actual log-level test (assert `logging.getLogger().level == logging.DEBUG` after init)
- **Also:** add a test that fails when the tracer shutdown bug from issue #7 is present (register a test-scoped atexit hook, confirm `tracer_provider.shutdown()` was called)
- **Commit message:** `Rewrite test_telemetry.py with real span/log/level assertions`
- **Dependency:** coordinates with issue #7 (instrumentation hardening). Gemini can draft; human review needed to confirm OTel SDK testing patterns are correct.

#### A4. Add unit tests to `tests/test_synthesis_generator.py`
- Add unit tests (no network) for:
  - `_parse_quick_synthesis_response(response_text)` — covers: all-tags-present, missing tag, malformed tag, empty tag, quote-stripping, key-concepts comma-splitting
  - `_calculate_cost(input, output)` — simple arithmetic, verify pricing constants
  - `_infer_research_area(metadata)` — one test per keyword category + fallback
  - `_build_quick_synthesis_message(...)` — register params in output, author truncation at >3, citation-context length cap at 10K
- Add a **mocked** integration-shape test that asserts on `client.beta.messages.create.call_args.kwargs`:
  - `betas` contains both `"skills-2025-10-02"` and `"code-execution-2025-08-25"`
  - `container["skills"]` is non-empty
  - `tools` contains the code_execution tool dict
- Change existing live integration tests to `@pytest.fixture(scope="module")` for the generator to reduce per-run API spend
- **Commit message:** `Add unit coverage and API-shape test for synthesis_generator`
- **Dependency:** none. High impact — silent breakage here costs real money.

### M-priority (do after H-priority)

#### B1. Hoist mock helpers to `tests/conftest.py`
- Extract `_mock_response(...)`, `_mock_head(...)`, `_mock_get(...)` patterns from `test_doi_fetcher.py` and `test_web_fetcher.py`
- Move to `tests/conftest.py` as `@pytest.fixture` or `tests/_mock_helpers.py` as plain callables
- Update call sites across both files
- **Commit message:** `Consolidate mock-response helpers in tests/conftest.py`

#### B2. Coverage gaps in `tests/test_markdown_writer.py`
- Add tests for:
  - Filename truncation at word boundaries when title exceeds length cap
  - Period-to-dash substitution: `"3.1"` → `"3-1"`, `"U.S.A."` → `"U-S-A-"`
  - Full Obsidian citation wikilink format `[[Author, Author & Author (Year) - Title]]`
  - UTF-8 author names (é, ü, ń — use `"Kaiser, Łukasz"` from the Vaswani author list as a real-world example)
  - YAML escaping for titles containing `:`, `"`, leading `-`, or other YAML-sensitive characters
- **Commit message:** `Add markdown_writer test coverage for filenames, UTF-8, YAML edge cases`

#### B3. Efficient integration tests in `tests/test_arxiv_fetcher.py`
- Replace per-test `fetcher.fetch(...)` calls with a `@pytest.fixture(scope="module") def attention_paper()` that fetches once
- Update 10 tests in `TestArxivFetching` and `TestArxivAuthorsFormatting` to consume the shared fixture
- **Commit message:** `Use module-scope fixture in test_arxiv_fetcher to avoid 10 redundant fetches`

#### B4. Fix environment coupling in `tests/test_grobid_processor.py`
- `test_processor_initialized_with_url` — pass an explicit URL like `"http://test:9999"` to the constructor, assert it's stored verbatim
- Strengthen weak assertions in `test_extract_title`, `test_extract_authors` — e.g. title contains a space, authors have `,` in "Lastname, First" format
- **Commit message:** `Decouple test_grobid_processor from env, strengthen field assertions`

#### B5. Boundary-fallback coverage in `tests/test_token_utils.py`
- Add tests for sentence-boundary fallback (text with `.` but no `\n\n`)
- Add tests for word-boundary fallback (text with spaces but no sentences)
- Add test for hard-cut case (text with no spaces at all — edge case)
- Strengthen `test_truncate_at_paragraph_boundary` to actually verify `\n\n` boundary was used
- Add test for the re-truncation pass (construct a case where first pass undershoots)
- **Commit message:** `Expand token_utils boundary-fallback test coverage`

#### B6. Bibliography-removal coverage in `tests/test_citation_context.py`
- Add tests for:
  - All-caps `REFERENCES` header
  - `Bibliography` instead of `References`
  - Multiple "References" mentions (how does the heuristic decide which is the bibliography?)
  - Body text containing the word "references" as prose, with no actual bibliography section
- **Commit message:** `Expand bibliography removal heuristic test coverage`

#### B7. Add `tests/test_models.py`
- Pydantic validation for each model in `paper_library/models.py`
- Edge cases: required-vs-optional fields, `contexts: list[str]` default, year boundaries, author list types
- Coverage of the `BibliographicEntry` → `Citation`/`PaperMetadata` override pattern (optional in base, required in some subclasses)
- **Commit message:** `Add direct tests for Pydantic models`

#### B8. Add `tests/test_state.py`
- Test `StateManager.load()`, `.mark_processed()`, `.is_processed()`, `.get_stats()`, `.mark_failed()`
- Verify dedup across the three ID types (arXiv/DOI/URL) doesn't cross-contaminate
- Verify `--force` behavior (at orchestrator level, consuming StateManager)
- **Commit message:** `Add direct tests for StateManager`

### L-priority (polish)

#### C1. Rename `TestFetchIntegration` in `test_doi_fetcher.py`
- Rename class → `TestFetchOrchestration` (or `TestFetchEndToEndMocked`)
- **Commit message:** `Rename misleading TestFetchIntegration class`

#### C2. Strengthen weak assertions surfaced in audit
- In `test_arxiv_fetcher.py::test_authors_formatted_correctly` — make the format check more explicit
- In `test_citation_context.py::test_context_contains_surrounding_text` — stronger than keyword-proxy
- **Commit message:** `Strengthen weak assertions in arxiv-fetcher and citation-context tests`

#### C3. CI matrix for stated Python versions
- Verify whether CI actually runs against Python 3.9, 3.10, ..., 3.14 as `target-version` claims
- If not, either add the matrix or narrow the stated support range
- **Commit message:** `Align CI Python matrix with pyproject.toml target-version` (if CI file exists) or `Narrow Python support in pyproject.toml to match CI` (if not)
- **Dependency:** requires a human to decide which direction to go (broaden CI or narrow stated support)

---

## Open Questions

Items surfaced during the audit that need human judgment before Gemini can act on them:

1. **Python version support** (see Cross-Cutting #6). Does alcanzai genuinely support 3.9+, or is the venv-resident 3.14 the real runtime? Choice: either make CI reflect 3.9 compatibility, or narrow `pyproject.toml`.

2. **`test_pipeline.py`: relocate or rewrite?** Both options in A2 are valid. A single CLI smoke-script (option a) has different semantics than a proper integration test (option b). The decision depends on whether "run `pytest` and see everything tested" is more important than "run a script to validate end-to-end before shipping". My lean is (b) because the project already has `@pytest.mark.integration` plumbing, but the user may prefer (a) for clarity.

3. **Where to file each recommended fix PR.** Options:
   - File one PR per action item (A1, A2, A3, ...) — high visibility, easy review
   - File one PR per priority tier (H, M, L) — fewer PRs but larger diffs
   - Open a tracking epic (similar to issue #2) that links individual sub-issues — mirrors the telemetry workflow
   
   My lean: **per-item PRs for H-priority** (they're logically distinct and reviewed more carefully), **per-tier for M and L** if Gemini can batch similar fixes cleanly.

4. **Is a shared test-fixture library warranted?** Beyond mock helpers (B1), some fixture objects (the `vaswani` / `bahdanau` / `devlin` citations, `PaperMetadata` sample objects) are recreated per-file. A `tests/_factories.py` with `make_paper_metadata(**overrides)` etc. would DRY things up — but might be over-engineering for the current size. Decide when B1 lands.

5. **Live-test API cost budget.** `pytest -m integration` currently runs 3 live Claude calls, ~10 arXiv calls, and ~6 GROBID calls. Per-run cost estimate: $0.05–0.15. If CI ever runs integration tests, this accumulates. A `ALCANZAI_INTEGRATION_BUDGET` env guard (fail the test session if expected-cost > $X) might be worth adding as a separate issue.

---

## Metadata

- **Audit duration:** ~1 session (partial — if cut off, resume by reading to "## File-by-File Findings" and noting which files have entries vs. not)
- **Code base state at audit:** commit `93ccde2` (after v0.2.6 issue scaffolding landed)
- **Next action:** future session should reference this document + issue #8 to pick up work. Suggested prompt shape for the exomonad/Gemini session:
  > "Open `docs/test-audit-2026-04.md`. Work through the H-priority action queue: A1 → A2 → A3 → A4. Each is sized to be one PR. For each, read the relevant test file, make the prescribed changes, run `pytest -m 'not integration'` to confirm nothing broke, and open a PR referencing issue #8 with the commit message suggested in the audit doc. Stop after A4 for my review before proceeding to M-priority."
