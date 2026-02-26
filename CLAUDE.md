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
# Run all tests
pytest

# Run the canonical end-to-end integration test (needs GROBID + API key)
python tests/test_pipeline.py 1706.03762

# Process a single paper programmatically
python -c "from paper_library.orchestrator import process_paper; process_paper('1706.03762')"

# Reprocess a paper (force=True bypasses deduplication check)
python -c "from paper_library.orchestrator import process_paper; process_paper('1706.03762', force=True)"

# Lint and format
ruff check .
black .
```

When testing, "Attention Is All You Need" (arXiv `1706.03762`) is the canonical test paper. To reset it for fresh processing:
```bash
rm vault/Papers/Vaswani*.md
# Then run with force=True
```

## Architecture

### Pipeline Flow

Every paper goes through these steps in `orchestrator.py → PaperProcessor.process()`:

```
identifier (arXiv ID or file path)
  → _fetch_paper()        # arxiv_fetcher.py: hits arXiv API + downloads PDF
  → grobid.process()      # grobid_processor.py: sends PDF to GROBID, parses TEI XML
  → _merge_metadata()     # prefers GROBID fields; keeps arXiv ID from fetcher
  → _extract_text()       # pdfplumber extracts text from PDF
  → synthesis_gen.generate_quick_synthesis()  # calls Claude Haiku
  → markdown_writer.paper_to_markdown()       # renders Obsidian note
  → writes to vault/Papers/<filename>.md
  → state.mark_processed()  # saves to vault/_meta/processing_state.json
```

### Key Modules

| File | Purpose |
|------|---------|
| `orchestrator.py` | Main `PaperProcessor` class; coordinates entire pipeline |
| `arxiv_fetcher.py` | Fetches metadata from arXiv API + downloads PDF to `vault/PDFs/` |
| `grobid_processor.py` | Sends PDF to GROBID (Docker), parses TEI XML into `PaperMetadata` + `Citation` list; includes heuristic garbage-score filter for bad citations (threshold >60) |
| `synthesis_generator.py` | Calls `claude-haiku-4-5` with structured prompt; parses XML-tagged response into `Synthesis` model |
| `markdown_writer.py` | Renders YAML frontmatter + Obsidian-formatted note from metadata + synthesis |
| `state.py` | `StateManager` loads/saves `processing_state.json`; deduplicates by arXiv ID / DOI / URL |
| `models.py` | Pydantic models: `BibliographicEntry` → `Citation` / `PaperMetadata`; `ArticleMetadata`; `Synthesis`; `ProcessingState` |
| `config.py` | Loads `.env`; exposes `vault_path`, `papers_dir`, `pdfs_dir`, `grobid_url`, `anthropic_api_key` |
| `batch_process.py` | Wrapper around `PaperProcessor` for processing lists of identifiers from a file |

### Data Models

`BibliographicEntry` is the shared base for both `Citation` (extracted references) and `PaperMetadata` (the paper being processed). This shared base enables future promotion of citations to full papers in a citation graph.

`Synthesis` contains: `summary`, `why_you_cared`, `key_concepts` (list), `memorable_quote`, and `cost_usd` for tracking API spend.

`ProcessingState` tracks three separate sets: `processed_arxiv_ids`, `processed_dois`, `processed_urls`.

### External Services

- **GROBID** runs via `docker-compose.yml` on port 8070. The API endpoint used is `/api/processFulltextDocument`. Timeout is 5 minutes per PDF.
- **Anthropic API** uses `claude-haiku-4-5` (note: no date suffix). Synthesis prompts use XML-style tags for structured output parsing.

### Vault Structure

```
vault/
├── Papers/          # Academic paper notes (.md)
├── Articles/        # Web article notes (.md)  [not yet fully implemented]
├── PDFs/            # Downloaded PDFs (arxiv_<id>.pdf)
└── _meta/
    └── processing_state.json
```

### What's Not Yet Implemented

`doi_fetcher.py` and `web_fetcher.py` exist as stubs/partial implementations. The orchestrator currently only supports arXiv IDs and local PDF paths.

## Code Style

- Line length: 100 (black + ruff)
- Target: Python 3.9+
- Imports: stdlib → third-party → local (`paper_library.*`)
