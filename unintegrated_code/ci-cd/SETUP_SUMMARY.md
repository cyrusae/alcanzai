# Testing, Code Quality & Infrastructure Summary

## What We Built

You now have a complete professional development setup for alcanzai:

### 1. pytest Test Suite (670+ lines)

**Why?** Auto-discovery, better reporting, CI/CD ready, separates unit vs integration tests.

**Files created:**
- `tests/test_arxiv_fetcher.py` - ID parsing, metadata extraction, PDF download
- `tests/test_grobid_processor.py` - PDF processing, metadata extraction, citations
- `tests/test_synthesis_generator.py` - Claude API integration, parsing, cost tracking
- `tests/test_markdown_writer.py` - Obsidian note generation, formatting, filenames

**Key features:**
- Unit tests (fast, no dependencies) run by default
- Integration tests (slow, need services) marked with `@pytest.mark.integration`
- Fixtures for reusable setup (fetcher, processor, sample data)
- Clear assertion messages for debugging

**Quick commands:**
```bash
pytest tests/                              # All tests
pytest tests/ -m "not integration"        # Fast unit tests only
pytest tests/ -v                           # Verbose output
pytest tests/test_arxiv_fetcher.py        # Specific file
```

### 2. Command-Line Interface (CLI)

**Why?** Replace test_pipeline.py with a proper CLI entry point. More discoverable, follows Python conventions.

**File:** `paper_library/cli.py`

**Commands:**
```bash
alcanzai ingest 1706.03762              # Import single paper
alcanzai ingest https://arxiv.org/...   # Import from URL
alcanzai batch papers.txt               # Batch import from file
alcanzai stats                          # Show import statistics
alcanzai validate                       # Check configuration
```

**Registration:** Added to `pyproject.toml` under `[project.scripts]`

### 3. Pre-commit Hooks

**Why?** Automatic code quality checks before each commit. Prevents bad code from being committed.

**File:** `.pre-commit-config.yaml`

**What it does:**
- Black: Auto-formats your code
- Ruff: Finds bugs and style issues (auto-fixes many)
- Whitespace: Removes trailing whitespace
- YAML: Validates YAML files
- Large files: Prevents accidentally committing huge files

**Setup (one-time):**
```bash
uv sync --all-extras
pre-commit install
```

**Then:** Every `git commit` runs the hooks automatically

**If hooks fail:** Fix the issues and commit again

### 4. Dev Container

**Why?** Complete isolated development environment. Same setup for everyone, reproducible, CI/CD ready.

**Files:**
- `.devcontainer/devcontainer.json` - Container configuration
- `.devcontainer/postCreateCommand.sh` - Initialization script

**What's inside:**
- Python 3.11 (official Microsoft image)
- All dependencies pre-installed
- Docker-in-Docker (to run GROBID)
- VS Code extensions configured (Python, Pylance, Black, Ruff)
- GROBID and CouchDB ports forwarded
- Pre-commit hooks ready

**Setup (one-time):**
1. Install Docker Desktop
2. Install VS Code + Remote Containers extension
3. Open project in VS Code
4. Press `Ctrl+Shift+P`, type "Reopen in Container"
5. Wait ~2-5 minutes for first build
6. Terminal opens inside container, ready to use

**Why VS Code devcontainers?**
- Seamless integration - feels like local development
- All extensions work inside container
- Git integration works automatically
- Easy debugging

### 5. Documentation

**File:** `DEVELOPER.md` (comprehensive guide)

Covers:
- pytest testing guide (running, writing, common patterns)
- Black & Ruff usage (formatting, linting, fixing)
- Pre-commit hooks (how they work, setup, workflow)
- Dev container setup and workflow
- Full development workflow (edit → test → commit → push)
- Troubleshooting

---

## The Testing Mindset

### Test Categories

**Unit Tests** (fast, no external dependencies):
```
✓ No network calls
✓ No GROBID/Claude API calls
✓ Test individual methods/functions
✓ Run in seconds
✓ Run first while developing
```

**Integration Tests** (slow, require services):
```
✓ Make actual API calls (arXiv, Claude, CrossRef, etc)
✓ Use GROBID service
✓ Test components together
✓ Run in minutes
✓ Run before committing to main
```

**Running:** 
```bash
pytest -m "not integration"    # Quick feedback while coding
pytest                          # Full suite before pushing
```

### Test Structure Pattern

Each test file follows this structure:

```python
class TestComponentName:
    """Test suite for a component"""
    
    @pytest.fixture
    def component(self):
        """Setup - runs before each test"""
        return SomeComponent(config)
    
    def test_specific_behavior(self, component):
        """Test one thing, clearly"""
        result = component.do_something()
        assert result == expected
```

---

## The Code Quality Workflow

### Before (Manual)
1. Write code
2. Remember to format it
3. Remember to check for bugs
4. Try to commit, realize code is messy
5. Fix and commit

### After (Automated with Pre-commit)
1. Write code
2. Try to commit
3. Pre-commit hooks run automatically:
   - Black formats your code
   - Ruff finds bugs and auto-fixes some
   - Other checks pass
4. Commit succeeds (good code only)

**One-time setup:**
```bash
pre-commit install
```

**Then:** Every commit is automatically checked

---

## The Development Workflow (New)

### With Dev Container (Recommended)

```bash
# 1. Open project in VS Code
#    Press Ctrl+Shift+P → "Reopen in Container"
#    Wait for container to build (~2-5 min first time)

# 2. Edit code in VS Code (runs in container automatically)

# 3. Terminal opens inside container
#    Run tests: pytest tests/ -m "not integration"
#    Format: black paper_library/
#    Lint: ruff check paper_library/
#    Import paper: alcanzai ingest 1706.03762

# 4. Commit code
#    git add .
#    git commit -m "Add feature"
#    # Pre-commit hooks run automatically

# 5. Push to repo
#    git push origin feature-branch
```

### Without Dev Container (Traditional Local Setup)

```bash
# 1. Setup (once)
uv sync --all-extras
pre-commit install

# 2. Activate venv
source .venv/bin/activate

# 3. Edit code, test, commit (same as above)
```

---

## Key Commands Cheat Sheet

### Testing
```bash
pytest tests/                          # Run all tests
pytest tests/ -v                       # Verbose
pytest tests/ -m "not integration"    # Fast unit tests only
pytest tests/test_arxiv_fetcher.py    # Specific file
pytest --lf                            # Last failed
pytest -x                              # Stop on first failure
```

### Code Quality
```bash
black paper_library/ tests/            # Format code
ruff check paper_library/ tests/       # Find issues
ruff check --fix paper_library/        # Auto-fix issues
pre-commit run --all-files             # Run all hooks manually
```

### Running alcanzai
```bash
alcanzai validate                      # Check setup
alcanzai ingest 1706.03762             # Import paper
alcanzai batch papers.txt              # Batch import
alcanzai stats                         # Show stats
```

### Git
```bash
git add .
git commit -m "Description"            # Pre-commit hooks run
git push origin feature-branch
```

---

## Next Steps (After This Setup)

### Immediate (This Week)
1. ✅ Run `uv sync --all-extras`
2. ✅ Run `pre-commit install`
3. ✅ Run `pytest tests/ -m "not integration"` (verify fast tests work)
4. ✅ Update your `.env` with `ANTHROPIC_API_KEY`
5. ✅ Try: `alcanzai ingest 1706.03762`

### Short Term (Next Week)
1. Run full test suite: `pytest tests/` (integration tests)
2. Try devcontainer setup if you want to
3. Add a few more unit tests as you add features
4. Get comfortable with the workflow

### Medium Term (Next Month)
1. Set up GitHub Actions CI/CD (auto-run tests on push)
2. Add code coverage tracking
3. Add type hints with mypy
4. Consider pytest-benchmark for performance testing

### Long Term (As you scale)
1. Performance profiling
2. Load testing
3. Documentation generation (sphinx)
4. Release process automation

---

## FAQ

**Q: Why both Black and Ruff?**
A: They're complementary. Black formats (style), Ruff catches bugs. Think of Black as "prettier" and Ruff as "ESLint" from JavaScript.

**Q: Do I have to use pre-commit hooks?**
A: No, but it's highly recommended. They save you from committing bad code. You can still commit without them with `--no-verify`, but why would you?

**Q: Should I use the dev container?**
A: Highly recommended if you're on Mac/Linux/Windows with Docker Desktop. It's the most reproducible setup. But traditional local setup works fine too.

**Q: How often should I run tests?**
A: While developing: `pytest -m "not integration"` (fast, frequent). Before committing: `pytest` (all tests). Before pushing: `pytest` + check code coverage.

**Q: What if a test is flaky (sometimes passes, sometimes fails)?**
A: Usually means it depends on timing or external service state. Mark with `@pytest.mark.flaky` and investigate. For integration tests, you might need to add retries.

**Q: Can I skip pre-commit hooks?**
A: Yes: `git commit --no-verify`. But don't make it a habit—hooks exist for a reason!

**Q: What if GROBID isn't running in the dev container?**
A: The postCreateCommand script starts it, but it takes ~30 seconds. The script waits for it, but if you're impatient, run: `docker-compose up -d grobid` inside the container.

---

## Resources

- [pytest docs](https://docs.pytest.org) - Full pytest guide
- [Black docs](https://black.readthedocs.io) - Code formatter
- [Ruff docs](https://docs.astral.sh/ruff) - Linter
- [Pre-commit docs](https://pre-commit.com) - Git hooks
- [Dev Containers docs](https://containers.dev) - Dev containers
- DEVELOPER.md (in this repo) - All of the above, in one place
