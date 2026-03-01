# Developer Setup Guide

This guide covers setting up your development environment for alcanzai, including testing, code quality tools, and using a devcontainer.

## Quick Start (Traditional Local Setup)

```bash
# 1. Install dependencies (including dev tools)
uv sync --all-extras

# 2. Activate virtual environment
source .venv/bin/activate

# 3. Validate your setup
alcanzai validate

# 4. Run tests
pytest tests/

# 5. Set up git pre-commit hooks (optional but recommended)
pre-commit install
```

## pytest: Running Tests

### What is pytest?

`pytest` is a testing framework that automatically discovers and runs your tests. It's much cleaner than running individual test files by hand.

### Installing pytest

```bash
uv sync --all-extras  # Includes pytest in dev dependencies
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with verbose output (shows each test)
pytest tests/ -v

# Run only unit tests (fast)
pytest tests/ -m "not integration"

# Run only integration tests (requires network/services)
pytest tests/ -m integration

# Run a specific test file
pytest tests/test_arxiv_fetcher.py

# Run a specific test class
pytest tests/test_arxiv_fetcher.py::TestArxivIdParsing

# Run a specific test
pytest tests/test_arxiv_fetcher.py::TestArxivIdParsing::test_parse_new_style_id

# Run with coverage report (how much code is tested)
pytest tests/ --cov=paper_library

# Run tests and stop on first failure
pytest tests/ -x

# Run last failed tests only
pytest tests/ --lf
```

### Understanding Test Structure

The pytest tests are organized by component:

- `test_arxiv_fetcher.py` - Tests for fetching papers from arXiv
- `test_grobid_processor.py` - Tests for PDF processing with GROBID
- `test_synthesis_generator.py` - Tests for Claude API integration
- `test_markdown_writer.py` - Tests for Obsidian note generation

Each test file has:
- **Unit tests** (marked `@pytest.mark.integration` = NOT unit tests; no mark = unit tests)
  - Fast, no external dependencies
  - Test individual methods in isolation
- **Integration tests** (marked `@pytest.mark.integration`)
  - Slow, require external services (arXiv API, GROBID, Claude API)
  - Test that components work together

Run fast tests while developing:
```bash
pytest tests/ -m "not integration"
```

Run integration tests before pushing:
```bash
pytest tests/ -m integration
```

### Writing New Tests

When you add a new feature, write tests for it. Pattern:

```python
def test_my_feature_does_something():
    """Test that my new feature works correctly"""
    result = my_function("input")
    assert result == "expected_output"
```

### Common pytest Features

**Fixtures** (reusable setup):
```python
@pytest.fixture
def fetcher(self):
    return ArxivFetcher(config.vault_path)

def test_something(self, fetcher):  # Injected automatically
    pdf_path, metadata = fetcher.fetch("1706.03762")
```

**Parametrization** (test multiple inputs):
```python
@pytest.mark.parametrize("arxiv_id,expected_year", [
    ("1706.03762", 2017),
    ("2312.12345", 2023),
])
def test_fetch_year(self, arxiv_id, expected_year):
    _, metadata = fetcher.fetch(arxiv_id)
    assert metadata.year == expected_year
```

**Skipping tests**:
```python
@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass
```

---

## Code Quality: Black & Ruff

### What Are They?

- **Black**: Automatic code formatter (like `prettier` for JavaScript)
- **Ruff**: Fast linter that finds bugs and style issues (replaces flake8, pylint, etc)

### Installing

```bash
uv sync --all-extras  # Includes both
```

### Running Manually

```bash
# Format all code (modifies files in-place)
black paper_library/ tests/

# Check for issues (doesn't modify files)
ruff check paper_library/ tests/

# Auto-fix issues that ruff can fix
ruff check --fix paper_library/ tests/

# Format + lint in one command
black paper_library/ tests/ && ruff check --fix paper_library/ tests/
```

### Pre-commit Hooks: Automatic Code Quality

**What?** Git hooks that run automatically before each commit, preventing you from committing bad code.

**Setup:**
```bash
# Install pre-commit tool
uv sync --all-extras

# Install the hooks (one-time setup)
pre-commit install

# Verify it's installed
cat .git/hooks/pre-commit
```

**How it works:**
```bash
# When you commit:
git commit -m "My changes"

# Pre-commit hooks run automatically:
#   1. Black formats your code
#   2. Ruff checks for issues
#   3. Other checks (trailing whitespace, etc)
#
# If anything fails, commit is blocked
# Fix the issues and commit again
```

**Manually run hooks:**
```bash
# Run on all files
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files

# Skip hooks for a commit (not recommended!)
git commit --no-verify
```

**What hooks are configured?**
See `.pre-commit-config.yaml`:
- Black (code formatter)
- Ruff (linter + formatter)
- Trailing whitespace remover
- End-of-file fixer
- YAML validator
- Large file detector

---

## Dev Container: Complete Isolated Environment

A **devcontainer** is a Docker container that serves as your complete development environment. Benefits:

- **Isolation**: Your project can't break your system
- **Consistency**: Everyone on the team has identical setup
- **Reproducibility**: Same tools, same versions, same behavior
- **Easy cleanup**: Delete container, start fresh
- **CI/CD ready**: Same environment as deployment

### Prerequisites

- **Docker**: [Install Docker Desktop](https://www.docker.com/products/docker-desktop)
- **VS Code**: [Install Visual Studio Code](https://code.visualstudio.com)
- **Dev Containers extension**: Install in VS Code (search "Remote - Containers")

### Using the Dev Container

**Option 1: VS Code (Recommended)**

1. Open the project in VS Code
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
3. Type "Reopen in Container"
4. Wait for container to build and start (~2-5 minutes first time)
5. Terminal opens inside container (ready to use!)

**Option 2: Command Line**

```bash
# Build and run container
devcontainer open .

# Or if you prefer Docker directly:
docker-compose up -d grobid
# Then work in your editor with GROBID accessible
```

### What's in the Dev Container?

See `.devcontainer/devcontainer.json`:
- Python 3.11 (official Microsoft image)
- Git support
- Docker-in-Docker (to run GROBID)
- VS Code extensions pre-configured:
  - Python language support
  - Pylance (IntelliSense)
  - Black formatter
  - Ruff linter
- Pre-commit hooks ready to use
- GROBID and CouchDB ports forwarded

### Dev Container Workflow

```bash
# Inside VS Code terminal (running in container):

# Install dependencies
uv sync --all-extras

# Run tests
pytest tests/

# Try processing a paper
alcanzai ingest 1706.03762

# Format code
black paper_library/

# Check with ruff
ruff check paper_library/
```

### Rebuilding Container

If you change dependencies in `pyproject.toml`:

```bash
# In VS Code command palette:
# "Dev Containers: Rebuild Container"

# Or from command line:
devcontainer rebuild .
```

### Environment Variables in Container

The container loads `.env` file automatically. Create it:

```bash
# Copy the template
cp .env.example .env

# Edit it with your actual API keys
nano .env
```

Inside the container, `alcanzai validate` checks your setup.

---

## Full Workflow: Start to Commit

```bash
# 1. Set up (first time only)
uv sync --all-extras
pre-commit install

# 2. Edit code (e.g., add a new feature)
# ... make changes to paper_library/something.py ...

# 3. Write tests for the feature
# ... add tests to tests/test_something.py ...

# 4. Run tests locally
pytest tests/ -m "not integration"

# 5. Format and lint (automatic with pre-commit, but you can do manually)
black paper_library/ tests/
ruff check --fix paper_library/ tests/

# 6. Commit
git add paper_library/ tests/
git commit -m "Add new feature: description"
# Pre-commit hooks run automatically
# If they fail, fix and try again

# 7. Run full test suite before pushing
pytest tests/

# 8. Push to repo
git push origin feature-branch
```

---

## Troubleshooting

### "pytest: command not found"
```bash
# You didn't install dev dependencies
uv sync --all-extras
source .venv/bin/activate
```

### "GROBID not running"
```bash
# Start GROBID
docker-compose up -d grobid

# Wait ~30 seconds, then verify
curl http://localhost:8070/api/isalive
```

### "Pre-commit hook failed"
Look at the error message. Usually:
- Black formatted your code: Just commit again
- Ruff found an issue: Read the error and fix it manually
- Whitespace issue: Ruff usually fixes it automatically

### "Dev container won't start"
```bash
# Rebuild the container
devcontainer rebuild .

# Or nuke and start fresh
docker-compose down -v
devcontainer rebuild .
```

### "My .env file isn't being loaded"
- Make sure you're using `uv sync` (not pip)
- Make sure `.env` is in the project root (same dir as `pyproject.toml`)
- Restart your terminal or VS Code

---

## Resources

- [pytest documentation](https://docs.pytest.org)
- [Black documentation](https://black.readthedocs.io)
- [Ruff documentation](https://docs.astral.sh/ruff)
- [Pre-commit documentation](https://pre-commit.com)
- [Dev Containers documentation](https://containers.dev)
- [Docker documentation](https://docs.docker.com)

## Next Steps

Once you're comfortable with testing:

1. **Add more tests** for edge cases and error handling
2. **Set up CI/CD** (GitHub Actions) to run tests automatically on push
3. **Add type hints** with mypy for additional safety
4. **Performance testing** with pytest-benchmark (future)

Good luck! 🚀
