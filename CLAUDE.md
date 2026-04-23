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

<!-- deciduous:start -->
## Decision Graph Workflow

**THIS IS MANDATORY. Log decisions IN REAL-TIME, not retroactively.**

### Available Slash Commands

| Command | Purpose |
|---------|---------|
| `/decision` | Manage decision graph - add nodes, link edges, sync |
| `/recover` | Recover context from decision graph on session start |
| `/work` | Start a work transaction - creates goal node before implementation |
| `/document` | Generate comprehensive documentation for a file or directory |
| `/build-test` | Build the project and run the test suite |
| `/serve-ui` | Start the decision graph web viewer |
| `/sync-graph` | Export decision graph to GitHub Pages |
| `/decision-graph` | Build a decision graph from commit history |
| `/sync` | Multi-user sync - pull events, rebuild, push |

### Available Skills

| Skill | Purpose |
|-------|---------|
| `/pulse` | Map current design as decisions (Now mode) |
| `/narratives` | Understand how the system evolved (History mode) |
| `/archaeology` | Transform narratives into queryable graph |

### The Node Flow Rule - CRITICAL

The canonical flow through the decision graph is:

```
goal -> options -> decision -> actions -> outcomes
```

- **Goals** lead to **options** (possible approaches to explore)
- **Options** lead to a **decision** (choosing which option to pursue)
- **Decisions** lead to **actions** (implementing the chosen approach)
- **Actions** lead to **outcomes** (results of the implementation)
- **Observations** attach anywhere relevant
- Goals do NOT lead directly to decisions -- there must be options first
- Options do NOT come after decisions -- options come BEFORE decisions
- Decision nodes should only be created when an option is actually chosen, not prematurely

### The Core Rule

```
BEFORE you do something -> Log what you're ABOUT to do
AFTER it succeeds/fails -> Log the outcome
CONNECT immediately -> Link every node to its parent
AUDIT regularly -> Check for missing connections
```

### Behavioral Triggers - MUST LOG WHEN:

| Trigger | Log Type | Example |
|---------|----------|---------|
| User asks for a new feature | `goal` **with -p** | "Add dark mode" |
| Exploring possible approaches | `option` | "Use Redux for state" |
| Choosing between approaches | `decision` | "Choose state management" |
| About to write/edit code | `action` | "Implementing Redux store" |
| Something worked or failed | `outcome` | "Redux integration successful" |
| Notice something interesting | `observation` | "Existing code uses hooks" |

### Document Attachments

Attach files (images, PDFs, diagrams, specs, screenshots) to decision graph nodes for rich context.

```bash
# Attach a file to a node
deciduous doc attach <node_id> <file_path>
deciduous doc attach <node_id> <file_path> -d "Architecture diagram"
deciduous doc attach <node_id> <file_path> --ai-describe

# List documents
deciduous doc list              # All documents
deciduous doc list <node_id>    # Documents for a specific node

# Manage documents
deciduous doc show <doc_id>     # Show document details
deciduous doc describe <doc_id> "Updated description"
deciduous doc describe <doc_id> --ai   # AI-generate description
deciduous doc open <doc_id>     # Open in default application
deciduous doc detach <doc_id>   # Soft-delete (recoverable)
deciduous doc gc                # Remove orphaned files from disk
```

**When to suggest document attachment:**

| Situation | Action |
|-----------|--------|
| User shares an image or screenshot | Ask: "Want me to attach this to the current goal/action node?" |
| User references an external document | Ask: "Should I attach a copy to the decision graph?" |
| Architecture diagram is discussed | Suggest attaching it to the relevant goal node |
| Files not in the project are dropped in | Attach to the most relevant active node |

**Do NOT aggressively prompt for documents.** Only suggest when files are directly relevant to a decision node. Files are stored in `.deciduous/documents/` with content-hash naming for deduplication.

### CRITICAL: Capture VERBATIM User Prompts

**Prompts must be the EXACT user message, not a summary.** When a user request triggers new work, capture their full message word-for-word.

**BAD - summaries are useless for context recovery:**
```bash
# DON'T DO THIS - this is a summary, not a prompt
deciduous add goal "Add auth" -p "User asked: add login to the app"
```

**GOOD - verbatim prompts enable full context recovery:**
```bash
# Use --prompt-stdin for multi-line prompts
deciduous add goal "Add auth" -c 90 --prompt-stdin << 'EOF'
I need to add user authentication to the app. Users should be able to sign up
with email/password, and we need OAuth support for Google and GitHub. The auth
should use JWT tokens with refresh token rotation.
EOF

# Or use the prompt command to update existing nodes
deciduous prompt 42 << 'EOF'
The full verbatim user message goes here...
EOF
```

**When to capture prompts:**
- Root `goal` nodes: YES - the FULL original request
- Major direction changes: YES - when user redirects the work
- Routine downstream nodes: NO - they inherit context via edges

**Updating prompts on existing nodes:**
```bash
deciduous prompt <node_id> "full verbatim prompt here"
cat prompt.txt | deciduous prompt <node_id>  # Multi-line from stdin
```

Prompts are viewable in the web viewer.

### CRITICAL: Maintain Connections

**The graph's value is in its CONNECTIONS, not just nodes.**

| When you create... | IMMEDIATELY link to... |
|-------------------|------------------------|
| `outcome` | The action that produced it |
| `action` | The decision that spawned it |
| `decision` | The option(s) it chose between |
| `option` | Its parent goal |
| `observation` | Related goal/action |
| `revisit` | The decision/outcome being reconsidered |

**Root `goal` nodes are the ONLY valid orphans.**

### Quick Commands

```bash
deciduous add goal "Title" -c 90 -p "User's original request"
deciduous add action "Title" -c 85
deciduous link FROM TO -r "reason"  # DO THIS IMMEDIATELY!
deciduous serve   # View live (auto-refreshes every 30s)
deciduous sync    # Export for static hosting

# Metadata flags
# -c, --confidence 0-100   Confidence level
# -p, --prompt "..."       Store the user prompt (use when semantically meaningful)
# -f, --files "a.rs,b.rs"  Associate files
# -b, --branch <name>      Git branch (auto-detected)
# --commit <hash|HEAD>     Link to git commit (use HEAD for current commit)
# --date "YYYY-MM-DD"      Backdate node (for archaeology)

# Branch filtering
deciduous nodes --branch main
deciduous nodes -b feature-auth
```

### CRITICAL: Link Commits to Actions/Outcomes

**After every git commit, link it to the decision graph!**

```bash
git commit -m "feat: add auth"
deciduous add action "Implemented auth" -c 90 --commit HEAD
deciduous link <goal_id> <action_id> -r "Implementation"
```

The `--commit HEAD` flag captures the commit hash and links it to the node. The web viewer will show commit messages, authors, and dates.

### Git History & Deployment

```bash
# Export graph AND git history for web viewer
deciduous sync

# This creates:
# - docs/graph-data.json (decision graph)
# - docs/git-history.json (commit info for linked nodes)
```

To deploy to GitHub Pages:
1. `deciduous sync` to export
2. Push to GitHub
3. Settings > Pages > Deploy from branch > /docs folder

Your graph will be live at `https://<user>.github.io/<repo>/`

### Branch-Based Grouping

Nodes are auto-tagged with the current git branch. Configure in `.deciduous/config.toml`:
```toml
[branch]
main_branches = ["main", "master"]
auto_detect = true
```

### Audit Checklist (Before Every Sync)

1. Does every **outcome** link back to what caused it?
2. Does every **action** link to why you did it?
3. Any **dangling outcomes** without parents?

### Git Staging Rules - CRITICAL

**NEVER use broad git add commands that stage everything:**
- ❌ `git add -A` - stages ALL changes including untracked files
- ❌ `git add .` - stages everything in current directory
- ❌ `git add -a` or `git commit -am` - auto-stages all tracked changes
- ❌ `git add *` - glob patterns can catch unintended files

**ALWAYS stage files explicitly by name:**
- ✅ `git add src/main.rs src/lib.rs`
- ✅ `git add Cargo.toml Cargo.lock`
- ✅ `git add .claude/commands/decision.md`

**Why this matters:**
- Prevents accidentally committing sensitive files (.env, credentials)
- Prevents committing large binaries or build artifacts
- Forces you to review exactly what you're committing
- Catches unintended changes before they enter git history

### Session Start Checklist

```bash
deciduous check-update    # Update needed? Run 'deciduous update' if yes
deciduous nodes           # What decisions exist?
deciduous edges           # How are they connected? Any gaps?
deciduous doc list        # Any attached documents to review?
git status                # Current state
```

### Multi-User Sync

Sync decisions with teammates via event logs:

```bash
# Check sync status
deciduous events status

# Apply teammate events (after git pull)
deciduous events rebuild

# Compact old events periodically
deciduous events checkpoint --clear-events
```

Events auto-emit on add/link/status commands. Git merges event files automatically.
<!-- deciduous:end -->
