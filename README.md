# *alcanzai* Paper Library

Personal research library that processes academic papers and web articles into an Obsidian vault with AI-generated summaries, citation networks, and searchable metadata.

## Features

- **Unified "Clear Your Tabs" workflow**: Process arXiv papers, DOI papers, web articles, and local PDFs
- **AI-powered synthesis**: Claude generates summaries, key concepts, and memorable quotes
- **Citation network**: Automatic extraction and linking of cited papers
- **Obsidian integration**: Output formatted for Obsidian with YAML frontmatter and wikilinks
- **Deduplication**: Track downloaded papers to avoid duplicate work

## Quick Start

### Prerequisites

- Python 3.9+ (`uv` expects 3.14)
- Docker (for GROBID service)
- Anthropic API key

### Installation

```bash
# Clone/download the project
cd alcanzai

# Get uv running
uv venv
source .venv/bin/activate

# Install with uv (recommended)
uv pip install -e .

# Or with pip
pip install -e .

# Set up configuration
cp .env.example .env
# Edit .env with your API key and vault path
# ANTHROPIC_API_KEY=...
# VAULT_PATH=...
# CROSSREF_EMAIL=you@example.com   # optional but recommended for Crossref/Unpaywall polite pools

# Start GROBID service
docker-compose up -d
```

### Usage

```python
from paper_library.orchestrator import PaperProcessor
from paper_library.state import StateManager
from paper_library.config import config

# Initialize
state = StateManager.load()
processor = PaperProcessor(config, state)

# Process a single paper
processor.process("2312.12345")  # arXiv ID
processor.process("10.1162/coli_a_00123")  # DOI
processor.process("https://example.com/article")  # Web article

# Batch process from file
with open("papers.txt") as f:
    identifiers = [line.strip() for line in f]
results = processor.process_batch(identifiers)
```

## Project Structure

```
alcanzai/
├── paper_library/          # Main package
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── models.py              # Pydantic data models
│   ├── state.py               # Processing state tracking
│   ├── grobid_processor.py    # GROBID XML parsing
│   ├── synthesis_generator.py # Claude integration
│   ├── markdown_writer.py     # Obsidian note formatting
│   ├── arxiv_fetcher.py       # arXiv API integration
│   ├── doi_fetcher.py         # DOI resolution via Crossref + Unpaywall/Semantic Scholar
│   ├── web_fetcher.py         # Web article fetching (HTML, Distill sites, PDF-from-URL)
│   ├── citation_context.py    # CitationContextExtractor: regex citation matching + context sentences
│   └── orchestrator.py        # Main processing pipeline
├── docker-compose.yml         # GROBID service
├── pyproject.toml             # Package configuration
└── vault/                     # Output directory (created on first run)
    ├── Papers/                # Academic papers
    ├── Articles/              # Web articles
    ├── PDFs/                  # Original PDF files
    └── _meta/                 # Processing state
```

## Development Status

**v0.1.0 MVP** (Running prototype!)
- [x] Configuration management
- [x] Data models
- [x] State tracking
- [x] GROBID processor
- [x] Synthesis generator
- [x] Markdown writer
- [x] arXiv fetcher
- [x] Orchestrator
- [x] Wrapper function for batch processing

**Current state** (all implemented)
- [x] DOI fetcher (Crossref metadata + Unpaywall/Semantic Scholar OA PDF)
- [x] Web fetcher (HTML articles, Distill framework sites, PDF-from-URL routing)
- [x] CLI interface (`alcanzai ingest`, `batch`, `stats`, `validate`)
- [x] Citation context extraction (regex-matched sentences around each citation)
- [x] Full branching pipeline: arXiv / DOI / web URL / PDF URL / local PDF

**v0.2+** (Future)
- PDF link finder for landing pages (e.g. PhilArchive abstract pages with download links)
- OCR for scanned PDFs (OCRmyPDF + Unpaper)
- Detailed section-by-section summaries (on-demand)
- Author pages
- Advanced citation graph features
- Move to self-hosted always-on GROBID server

---

## Possible gotchas and testing notes

### Docker on a new machine

- Install Docker if you're not on a Docker-having machine:
- For Ubuntu, `sudo snap install docker`
- To provide current account with permissions: `sudo -aG docker $USER`
- This becomes irrelevant if you have a separate GROBID server (intended behavior) but is relevant for testing on a new machine
- If it's still not working: `newgrp docker` to remind your computer to use that group
- Why yes I *did* decide to test this on a machine where I hadn't done dev work before, how could you tell

### Daily Usage

Every time you start working on the project:
```bash
cd paper-library
source .venv/bin/activate  # Activates the virtual environment
# Now 'python' works and finds paper_library

# When done:
deactivate
```

**Pro tip:** Add this to your shell profile to auto-activate:
```bash
# In ~/.zshrc or ~/.bashrc
cd() {
  builtin cd "$@"
  if [[ -f .venv/bin/activate ]]; then
    source .venv/bin/activate
  fi
}
```

Or move to a devcontainer (TODO: move to devcontainer!) to avoid this in future! 

### When testing 

(Using "Attention Is All You Need" as our canonical test paper)

``` bash
# Delete the old note first if needed (exact titles will be overwritten)
rm vault/Papers/Vaswani*.md

# Run again with --force to bypass dedup check
alcanzai ingest --force 1706.03762
```

### Apple Silicon / GROBID

`grobid/grobid:0.8.2` is an AMD64-only image. Under QEMU emulation on Apple Silicon, the default DeLFT models use TensorFlow, which crashes with signal 6 because AVX instructions are not emulated.

The fix is already in place: `grobid.yaml` at the project root forces all 19 GROBID models to `engine: "wapiti"` (no DeLFT/TensorFlow). It is mounted into the container via `docker-compose.yml`. As long as you use `docker-compose up -d`, this config is applied automatically and GROBID works correctly on Apple Silicon.

If you ever rebuild the GROBID container from scratch and see crashes in GROBID logs, verify that `./grobid.yaml` is present and that the volume mount in `docker-compose.yml` is intact.

### TODO: Continue adding gotchas...
