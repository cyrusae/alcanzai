# Installation Instructions

## Quick Start

You have two archive options - choose either one:

### Option 1: tar.gz (for Mac/Linux)
```bash
tar -xzf alcanzai-setup.tar.gz
cd alcanzai-setup
# Copy files to your project (see structure below)
```

### Option 2: zip (for Windows or any OS)
```bash
unzip alcanzai-setup.zip
cd alcanzai-setup
# Copy files to your project (see structure below)
```

---

## What's Inside the Archive

```
alcanzai-setup/
├── tests/                          # NEW: pytest test files
│   ├── test_arxiv_fetcher.py       # Tests for arXiv fetching
│   ├── test_grobid_processor.py    # Tests for PDF processing
│   ├── test_synthesis_generator.py # Tests for Claude API
│   └── test_markdown_writer.py     # Tests for markdown generation
│
├── paper_library/
│   └── cli.py                      # NEW: Command-line interface
│
├── .devcontainer/                  # NEW: Dev container config
│   ├── devcontainer.json
│   └── postCreateCommand.sh
│
└── .pre-commit-config.yaml         # NEW: Git pre-commit hooks
```

---

## Installation Steps

### 1. Extract Archive
```bash
# tar.gz
tar -xzf alcanzai-setup.tar.gz
cd alcanzai-setup

# OR zip
unzip alcanzai-setup.zip
cd alcanzai-setup
```

### 2. Copy Files to Your Project

**Copy the directories:**
```bash
# From inside alcanzai-setup/
cp -r tests/* /path/to/your/project/tests/
cp paper_library/cli.py /path/to/your/project/paper_library/
cp .pre-commit-config.yaml /path/to/your/project/
cp -r .devcontainer /path/to/your/project/
```

**Or on Windows:**
- Drag-and-drop `tests/` folder contents to your `tests/` directory
- Copy `paper_library/cli.py` to your `paper_library/` directory
- Copy `.pre-commit-config.yaml` to your project root
- Copy `.devcontainer/` folder to your project root

### 3. Update `pyproject.toml`

Add this section (if not already present):

```toml
[project.scripts]
alcanzai = "paper_library.cli:cli"

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "black>=24.0.0",
    "ruff>=0.6.0",
    "pre-commit>=3.0.0",
    "pyyaml>=6.0",
]
```

### 4. Delete Old Test Files

Remove the old test files that are being replaced:

```bash
rm test_arxiv.py test_grobid.py test_synthesis.py test_markdown.py test_pipeline.py
```

### 5. Install Dependencies and Set Up

```bash
# Install all dependencies including dev tools
uv sync --all-extras

# Activate virtual environment
source .venv/bin/activate    # On Windows: .venv\Scripts\activate

# Install pre-commit hooks
pre-commit install
```

### 6. Verify Installation

```bash
# Test that pytest works
pytest tests/ -m "not integration"

# Test that CLI works
alcanzai validate

# Test that pre-commit hooks work
pre-commit run --all-files
```

---

## Next Steps

1. **Edit `.env`** and add your `ANTHROPIC_API_KEY`

2. **Run the full test suite:**
   ```bash
   pytest tests/
   ```

3. **Try importing a paper:**
   ```bash
   alcanzai ingest 1706.03762
   ```

4. **Make a test commit** to verify pre-commit hooks:
   ```bash
   git add .
   git commit -m "Set up testing infrastructure"
   # Pre-commit hooks should run automatically
   ```

5. **(Optional) Set up dev container** in VS Code:
   - Install Docker Desktop
   - Install Remote - Containers extension in VS Code
   - Open project in VS Code
   - Press `Ctrl+Shift+P` → "Reopen in Container"

---

## File Structure After Installation

Your project should look like:

```
your-project/
├── paper_library/
│   ├── __init__.py
│   ├── cli.py                    # ← NEW
│   ├── config.py
│   ├── arxiv_fetcher.py
│   ├── grobid_processor.py
│   ├── synthesis_generator.py
│   └── ... other modules
│
├── tests/                        # ← UPDATED
│   ├── test_arxiv_fetcher.py     # ← NEW
│   ├── test_grobid_processor.py  # ← NEW
│   ├── test_synthesis_generator.py  # ← NEW
│   └── test_markdown_writer.py   # ← NEW
│
├── .devcontainer/               # ← NEW
│   ├── devcontainer.json
│   └── postCreateCommand.sh
│
├── .pre-commit-config.yaml       # ← NEW
├── pyproject.toml                # ← UPDATED (add CLI + dev deps)
├── docker-compose.yml
├── .env
├── DEVELOPER.md
└── ... other files
```

---

## Troubleshooting

### "pytest: command not found"
```bash
uv sync --all-extras
source .venv/bin/activate
pytest tests/ -m "not integration"
```

### "pre-commit: command not found"
```bash
uv sync --all-extras
pre-commit install
```

### "GROBID not running"
```bash
docker-compose up -d grobid
# Wait ~30 seconds
curl http://localhost:8070/api/isalive
```

### "Dev container won't start"
```bash
docker-compose down -v
devcontainer rebuild .
```

---

## File Sizes

- `alcanzai-setup.tar.gz` - 7.2 KB (compressed)
- `alcanzai-setup.zip` - 11 KB (compressed)

Both contain the same files, choose whichever works for your OS.

---

## Documentation

After installation, read:
1. **DEVELOPER.md** - Comprehensive development guide
2. **SETUP_SUMMARY.md** - Overview of what was set up
3. **ARCHITECTURE_VISUAL.md** - File structure and workflows

All three are available in the outputs folder and should be in your project.

---

## Questions?

Refer to:
- `DEVELOPER.md` - All tools documented
- `ARCHITECTURE_VISUAL.md` - Visual diagrams and quick reference
- `SETUP_SUMMARY.md` - FAQ section