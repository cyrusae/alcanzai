#!/usr/bin/env python3
"""
End-to-end integration test for the full pipeline.

Tests the complete path: arXiv API → PDF download → GROBID → Claude synthesis
→ Obsidian note → state recording.

Run manually:
    pytest tests/test_pipeline.py -m integration
    python tests/test_pipeline.py [arxiv_id]   # script mode, shows output

Requires: ANTHROPIC_API_KEY set, GROBID running on localhost:8070.
The canonical test paper is "Attention Is All You Need" (arXiv 1706.03762).
"""

import sys
import pytest
import requests
from pathlib import Path

from paper_library.config import config
from paper_library.state import StateManager
from paper_library.orchestrator import PaperProcessor


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _grobid_is_running() -> bool:
    try:
        r = requests.get(f"{config.grobid_url}/api/isalive", timeout=5)
        return r.status_code == 200
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Integration test
# ---------------------------------------------------------------------------

@pytest.mark.integration
def test_pipeline_attention_paper(tmp_path):
    """Full pipeline smoke test on arXiv:1706.03762 (Attention Is All You Need).

    Uses a tmp_path vault to avoid polluting the real vault and to ensure the
    test is repeatable across runs without --force.
    """
    arxiv_id = "1706.03762"

    if not config.anthropic_api_key:
        pytest.skip("ANTHROPIC_API_KEY not set")

    if not _grobid_is_running():
        pytest.skip("GROBID not reachable — start with: docker-compose up -d")

    # Wire up processor against a fresh tmp vault
    from paper_library.config import Config
    test_config = Config(
        anthropic_api_key=config.anthropic_api_key,
        vault_path=tmp_path,
        grobid_url=config.grobid_url,
        crossref_email=config.crossref_email,
    )
    state = StateManager(state_file=tmp_path / "_meta" / "processing_state.json")
    processor = PaperProcessor(test_config, state)

    # Run the pipeline
    processor.process(arxiv_id, force=True)

    # --- Assertions on state ---
    assert state.is_processed(arxiv_id=arxiv_id), \
        "Paper should be marked as processed in state after ingestion"

    # --- Assertions on vault output ---
    papers_dir = tmp_path / "Papers"
    md_files = list(papers_dir.glob("*.md")) if papers_dir.exists() else []
    assert md_files, "At least one .md note should have been written to vault/Papers/"

    note_text = md_files[0].read_text(encoding="utf-8")
    # YAML frontmatter
    assert "title:" in note_text, "Note must include a 'title:' frontmatter field"
    # Paper should be recognisable as the Vaswani attention paper
    title_lower = note_text.lower()
    assert "attention" in title_lower or "transformer" in title_lower, \
        "Note should reference 'attention' or 'transformer'"
    # Synthesis must have been written
    assert "## Summary" in note_text or "## Synthesis" in note_text, \
        "Note must contain a synthesis section"


# ---------------------------------------------------------------------------
# Script mode — for manual / ad-hoc use
# ---------------------------------------------------------------------------

def _run_script(arxiv_id: str = "1706.03762") -> bool:
    """Run the pipeline and print human-friendly output. Returns True on success."""
    print("\n" + "=" * 70)
    print("END-TO-END PIPELINE SMOKE TEST")
    print("=" * 70)
    print(f"\nPaper:  arXiv {arxiv_id}")
    print(f"Vault:  {config.vault_path}\n")

    if not config.anthropic_api_key:
        print("  ✗ ANTHROPIC_API_KEY not set — create .env with your key")
        return False

    if not _grobid_is_running():
        print("  ✗ GROBID not reachable — start with: docker-compose up -d")
        return False

    config.vault_path.mkdir(parents=True, exist_ok=True)

    state = StateManager.load()
    processor = PaperProcessor(config, state)

    try:
        processor.process(arxiv_id, force=True)
        print(f"\n✓ Wrote note to {config.papers_dir}")
        print(f"✓ State recorded ({state.get_stats()['total']} total papers)")
        print("\n✓✓✓ PIPELINE TEST PASSED ✓✓✓\n")
        return True
    except Exception as e:
        print(f"\n✗ Pipeline failed: {e}")
        return False


if __name__ == "__main__":
    arxiv_id = sys.argv[1] if len(sys.argv) > 1 else "1706.03762"
    sys.exit(0 if _run_script(arxiv_id) else 1)
