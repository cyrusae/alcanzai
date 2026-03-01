# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

*alcanzai* is a personal research library pipeline. It ingests academic papers (arXiv IDs, local PDFs) and web articles, processes them through GROBID (PDF → structured metadata) and Claude (AI synthesis), and writes formatted Obsidian markdown notes to a vault directory.

## Setup

```bash
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
cp env.example .env        # then edit with ANTHROPIC_API_KEY and VAULT_PATH
docker-compose up -d       # starts GROBID on localhost:8070
```

## Common Commands

```bash
# Unit tests only (fast, no external services)
pytest -m "not integration"

# Full test suite (requires GROBID running + API key set)
pytest

# End-to-end integration test (canonical smoke test)
python tests/test_pipeline.py 1706.03762

# CLI usage
alcanzai validate                    # check config
alcanzai ingest 1706.03762           # process single paper
alcanzai ingest --force 1706.03762   # reprocess (bypass dedup)
alcanzai batch papers.txt            # batch from file
alcanzai stats                       # show counts

# Lint and format
ruff check .
black .
```

When testing, "Attention Is All You Need" (arXiv `1706.03762`) is the canonical test paper. To reset it for fresh processing:
```bash
rm vault/Papers/Vaswani*.md
alcanzai ingest --force 1706.03762
```

## Architecture

### Pipeline Flow

`orchestrator.py → PaperProcessor.process()` routes inputs through a branching pipeline:

```
identifier
  → _fetch_paper()
      arXiv ID       → arxiv_fetcher.py → PDF + metadata
      DOI            → doi_fetcher.py → metadata (+ PDF if OA found)
      PDF URL        → web_fetcher.py → downloads PDF → paper path
      Web article    → web_fetcher.py → ArticleMetadata + content
      Local PDF      → stub PaperMetadata

  → if paper path (arXiv / DOI+PDF / local / pdf-from-URL):
      → _process_paper()
          → grobid.process()          # grobid_processor.py: PDF → TEI XML → PaperMetadata + Citations
          → _merge_metadata()         # prefers GROBID fields; keeps arXiv ID from fetcher
          → _extract_text()           # pdfplumber extracts body text
          → citation_context.extract_contexts()   # step 3.5: attaches context sentences to Citations
          → synthesis_gen.generate_quick_synthesis()
          → markdown_writer.paper_to_markdown()
          → writes to vault/Papers/<filename>.md

  → if article path (HTML web article):
      → _process_article()
          → synthesis_gen.generate_quick_synthesis()
          → markdown_writer.article_to_markdown()
          → writes to vault/Articles/<filename>.md

  → if doi_only path (DOI with no OA PDF found):
      → _process_doi_only()
          → synthesis on Crossref abstract text only
          → markdown_writer.paper_to_markdown()
          → writes to vault/Papers/<filename>.md (noted as abstract-only)

  → state.mark_processed()  # saves to vault/_meta/processing_state.json
```

### Key Modules

| File | Purpose |
|------|---------|
| `orchestrator.py` | Main `PaperProcessor` class; branching pipeline: paper / article / doi_only paths |
| `arxiv_fetcher.py` | Fetches metadata from arXiv API + downloads PDF to `vault/PDFs/` |
| `doi_fetcher.py` | Resolves DOIs via Crossref (metadata) + Unpaywall → Semantic Scholar (OA PDF). Returns `PaperMetadata` + optional local `pdf_path`. |
| `web_fetcher.py` | Fetches HTML articles (OG tag extraction, markdownify); detects Distill-framework sites (`d-article`); downloads PDFs from URLs; blocks unsupported hosts. |
| `citation_context.py` | `CitationContextExtractor`: regex-matches narrative and parenthetical citations in body text; strips bibliography before matching; attaches context sentences to `Citation.contexts[]` |
| `grobid_processor.py` | Sends PDF to GROBID (Docker), parses TEI XML into `PaperMetadata` + `Citation` list; includes heuristic garbage-score filter for bad citations (threshold >60) |
| `synthesis_generator.py` | Calls `claude-haiku-4-5` via skills API; parses XML-tagged response into `Synthesis` model. Accepts optional `register` config dict and `citation_contexts`. |
| `skills_manager.py` | Uploads SKILL.md directories to Anthropic's skills API; caches skill IDs in `skills/skill_ids.json` |
| `markdown_writer.py` | Renders YAML frontmatter + Obsidian-formatted note from metadata + synthesis; citation contexts rendered as blockquotes in Cites section |
| `state.py` | `StateManager` loads/saves `processing_state.json`; deduplicates by arXiv ID / DOI / URL |
| `models.py` | Pydantic models: `BibliographicEntry` → `Citation` / `PaperMetadata`; `ArticleMetadata`; `Synthesis`; `ProcessingState`. `Citation` has `contexts: list[str]`; `ArticleMetadata` has `pdf_path: Optional[str]`. |
| `config.py` | Loads `.env`; exposes `vault_path`, `papers_dir`, `pdfs_dir`, `grobid_url`, `anthropic_api_key`, `crossref_email` |
| `batch_process.py` | Wrapper around `PaperProcessor` for processing lists of identifiers from a file |

### Data Models

`BibliographicEntry` is the shared base for both `Citation` (extracted references) and `PaperMetadata` (the paper being processed). This shared base enables future promotion of citations to full papers in a citation graph.

`Synthesis` contains: `summary`, `why_you_cared`, `key_concepts` (list), `memorable_quote`, and `cost_usd` for tracking API spend.

`ProcessingState` tracks three separate sets: `processed_arxiv_ids`, `processed_dois`, `processed_urls`.

### Agent Skills

Synthesis uses the native Anthropic Agent Skills API (`betas=["skills-2025-10-02"]`). Skills live in `skills/` at the project root:

```
skills/
├── understand-academic-text/   # Paper structure parsing
├── extract-arguments/          # Thesis + evidence chain extraction
├── identify-terminology/       # Term classification + domain detection
├── register-controller/        # Writing style (9 axis reference files in registers/)
│   └── registers/              # jargon-{none,selective,heavy}.md, structure-*.md, depth-*.md
├── quick-summary/              # 4-section synthesis (summary/why/concepts/quote)
├── detailed-summary/           # Section-by-section breakdown
└── glossary-extraction/        # Technical vocabulary extraction
```

Skills are uploaded once via `SkillsManager.upload_skill()` and their IDs cached in `skills/skill_ids.json`. To force re-upload after editing SKILL.md files:
```python
manager = SkillsManager(api_key)
manager.invalidate_cache()  # clears all
manager.invalidate_cache("quick-summary")  # clears one
```

Register configuration controls writing style independently on three axes:
- `jargon`: `none` | `selective` (default) | `heavy`
- `structure`: `conversational` | `mixed` (default) | `formal`
- `depth`: `hand-holding` | `balanced` (default) | `assume-knowledge`

### External Services

- **GROBID** runs via `docker-compose.yml` on port 8070 using `grobid/grobid:0.8.2`. The API endpoint used is `/api/processFulltextDocument`. Timeout is 5 minutes per PDF.
  - **Apple Silicon**: `grobid/grobid:0.8.2` is AMD64-only. The bundled `grobid.yaml` forces all models to `engine: "wapiti"` (no DeLFT/TensorFlow), avoiding AVX crashes under QEMU. Already configured via the `docker-compose.yml` volume mount.
- **Anthropic API** uses `claude-haiku-4-5` (note: no date suffix). Synthesis uses the skills API; responses use XML-style tags for structured output parsing.
- **Crossref REST API** for DOI metadata. Set `CROSSREF_EMAIL` in `.env` to join the polite pool (faster rate limits).
- **Unpaywall / Semantic Scholar** for open-access PDF discovery. Unpaywall also uses `CROSSREF_EMAIL` as the contact email.

### Vault Structure

```
vault/
├── Papers/          # Academic paper notes (.md)
├── Articles/        # Web article notes (.md)
├── PDFs/            # Downloaded PDFs (arxiv_<id>.pdf)
└── _meta/
    └── processing_state.json
```

### What's Not Yet Implemented

- **PDF link finder for landing pages**: sites like PhilArchive show an abstract page with a PDF download link but no direct PDF URL. The pipeline cannot yet discover and follow that link.
- **OCR for scanned PDFs**: planned via OCRmyPDF + Unpaper preprocessing before GROBID.
- **Detailed section-by-section summaries**: the `detailed-summary` skill exists but on-demand invocation is not yet wired up.
- **Author pages**: citation wikilinks are written as future notes; no author-level aggregation yet.

## Code Style

- Line length: 100 (black + ruff)
- Target: Python 3.9+
- Imports: stdlib → third-party → local (`paper_library.*`)
