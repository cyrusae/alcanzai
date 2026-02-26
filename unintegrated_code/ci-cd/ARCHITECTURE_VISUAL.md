# Development Infrastructure Architecture

## File Organization (New Structure)

```
alcanzai/
├── paper_library/                    # Main package
│   ├── __init__.py
│   ├── cli.py                        # ← NEW: Command-line interface
│   ├── config.py
│   ├── models.py
│   ├── state.py
│   ├── arxiv_fetcher.py
│   ├── grobid_processor.py
│   ├── synthesis_generator.py
│   ├── markdown_writer.py
│   └── orchestrator.py
│
├── tests/                            # ← RESTRUCTURED: pytest-based
│   ├── conftest.py                   # (optional: shared fixtures)
│   ├── test_arxiv_fetcher.py         # ← NEW: Unit + integration tests
│   ├── test_grobid_processor.py      # ← NEW
│   ├── test_synthesis_generator.py   # ← NEW
│   ├── test_markdown_writer.py       # ← NEW
│   └── fixtures/                     # (for test data)
│
├── .devcontainer/                    # ← NEW: Dev container config
│   ├── devcontainer.json
│   └── postCreateCommand.sh
│
├── .pre-commit-config.yaml           # ← NEW: Git hooks
├── pyproject.toml                    # ← UPDATED: CLI entry point
├── docker-compose.yml                # (existing: GROBID)
├── DEVELOPER.md                      # ← NEW: Comprehensive dev guide
├── SETUP_SUMMARY.md                  # ← NEW: This setup summary
└── quickstart.sh                     # ← NEW: One-command setup

# Removed:
- test_arxiv.py (replaced by tests/test_arxiv_fetcher.py)
- test_grobid.py (replaced by tests/test_grobid_processor.py)
- test_synthesis.py (replaced by tests/test_synthesis_generator.py)
- test_markdown.py (replaced by tests/test_markdown_writer.py)
- test_pipeline.py (replaced by alcanzai CLI)
```

---

## Development Flow: Before vs After

### BEFORE (Manual Testing)
```
Write code
  ↓
Run: python test_arxiv.py
  ↓
Read output manually
  ↓
Try to remember formatting rules
  ↓
Commit (maybe with formatting issues)
  ↓
Hope code is good
```

### AFTER (Automated Quality)
```
Write code
  ↓
Run: pytest tests/ -m "not integration"    [instant feedback]
  ↓
pytest shows exactly what failed
  ↓
Try to commit: git commit -m "message"
  ↓
Pre-commit hooks run automatically:
  - Black formats code ✓
  - Ruff checks for bugs ✓
  - Trailing whitespace removed ✓
  ↓
Commit succeeds (good code only) ✓
```

---

## Tools Relationship

```
                    Your Code
                        ↓
        ┌───────────────┼───────────────┐
        ↓               ↓               ↓
   Your Tests      Code Quality    Git Integration
        ↓               ↓               ↓
   
  pytest         Black + Ruff    pre-commit hooks
  ├─ Unit tests    ├─ Format        ├─ Auto-run
  ├─ Integration   ├─ Lint          ├─ Block bad code
  ├─ Markers       └─ Fix           └─ Clean commits
  └─ Fixtures          
  
  When to use:
  • While coding: pytest -m "not integration"
  • Before commit: git commit (hooks auto-run)
  • Manual check: black/ruff check
  • Full suite: pytest (all tests)
```

---

## Environment Setup Options

### Option 1: Dev Container (Recommended)
```
✅ Most reproducible
✅ Same setup for everyone
✅ CI/CD ready
✅ Seamless VS Code integration
✅ Easy cleanup (just delete container)
❌ Requires Docker + Docker Desktop

Setup: Open in VS Code → Ctrl+Shift+P → "Reopen in Container"
```

### Option 2: Local Setup with uv
```
✅ Works on any system with Python
✅ Fast dependency installation
✅ Still reproducible (uv.lock file)
✅ No Docker needed
❌ Slightly less isolated
❌ Manual environment management

Setup: uv sync --all-extras
```

### Option 3: Old-style venv + pip
```
✅ Familiar to most Python developers
❌ Slower dependency resolution
❌ Less reproducible (no lock file)
❌ Manual dependency management

Not recommended for new projects.
```

---

## Test Architecture

### Test Classification

```
All Tests
    ├─ Unit Tests (Fast)
    │   ├─ ID parsing tests
    │   ├─ Filename generation
    │   ├─ Cost calculation
    │   └─ Response parsing
    │   
    │   Run: pytest -m "not integration"
    │   Time: < 5 seconds
    │   
    └─ Integration Tests (Slow)
        ├─ arXiv API tests
        ├─ GROBID processing tests
        ├─ Claude synthesis tests
        └─ End-to-end pipeline tests
        
        Run: pytest (with -m integration flag)
        Time: 2-5 minutes
        Requirements: Network, Docker services, API keys
```

### Test Organization

```
tests/
├── test_arxiv_fetcher.py
│   ├── TestArxivIdParsing (unit tests)
│   └── TestArxivFetching (integration tests)
│
├── test_grobid_processor.py
│   ├── TestGrobidConnection (unit tests)
│   ├── TestGrobidFileHandling (unit tests)
│   ├── TestGrobidMetadataExtraction (integration)
│   └── TestGrobidCitationExtraction (integration)
│
├── test_synthesis_generator.py
│   ├── TestSynthesisGenerator (integration)
│   ├── TestSynthesisResponseParsing (unit)
│   └── TestSynthesisCostCalculation (unit)
│
└── test_markdown_writer.py
    ├── TestMarkdownWriterPaper (unit)
    ├── TestMarkdownWriterArticle (unit)
    ├── TestMarkdownFilenameGeneration (unit)
    └── TestAuthorFormatting (unit)

Pattern: Class = group of related tests, method = individual test
```

---

## Git Workflow with Pre-commit

```
git add .
  ↓
git commit -m "description"
  ↓
[pre-commit hooks run automatically]
  ├─ Black formats code
  ├─ Ruff checks for issues
  ├─ Trailing whitespace removed
  ├─ YAML validated
  └─ Large files blocked
  ↓
  IF any hook fails:
  ├─ Commit is blocked
  ├─ You fix the issues
  └─ Try commit again
  ↓
  IF all hooks pass:
  └─ Commit succeeds ✓
  ↓
git push origin feature-branch
```

---

## Quick Reference: Commands by Task

### I want to...

**...check if my code works**
```bash
pytest tests/ -m "not integration"    # Fast feedback
```

**...check if everything works (with API calls)**
```bash
pytest tests/                          # All tests
```

**...format my code**
```bash
black paper_library/ tests/
```

**...find bugs in my code**
```bash
ruff check paper_library/
```

**...import a paper**
```bash
alcanzai ingest 1706.03762
```

**...import multiple papers**
```bash
alcanzai batch papers.txt
```

**...see my stats**
```bash
alcanzai stats
```

**...check my setup**
```bash
alcanzai validate
```

**...run everything before pushing**
```bash
pytest tests/
black paper_library/ tests/
ruff check --fix paper_library/ tests/
git push origin feature-branch
```

---

## Infrastructure Checklist

- [ ] Run `uv sync --all-extras` (install all dependencies)
- [ ] Run `pre-commit install` (set up git hooks)
- [ ] Edit `.env` and add your `ANTHROPIC_API_KEY`
- [ ] Run `alcanzai validate` (check configuration)
- [ ] Run `pytest tests/ -m "not integration"` (verify tests work)
- [ ] Try: `alcanzai ingest 1706.03762` (test end-to-end)
- [ ] (Optional) Set up dev container in VS Code

---

## Troubleshooting Quick Links

**Tests fail?** → See DEVELOPER.md "Troubleshooting"
**Pre-commit stuck?** → Check `.pre-commit-config.yaml`
**GROBID not running?** → `docker-compose up -d grobid`
**Import fails?** → Run `alcanzai validate` to debug
**Devcontainer issues?** → `devcontainer rebuild .`

---

## What's Next?

After this infrastructure is in place:

1. **Phase 2** (v0.2.0): Add DOI + web fetchers, refine synthesis
2. **Phase 3** (v0.2.5): Add GitHub Actions CI/CD (auto-run tests)
3. **Phase 4** (v0.3.0): Add type hints with mypy
4. **Phase 5** (v0.4.0+): Performance profiling, load testing

Each phase builds on this solid foundation.
