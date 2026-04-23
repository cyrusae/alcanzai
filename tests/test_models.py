"""
Tests for paper_library/models.py.

Currently covers ProcessingState behavior that was previously untested
(mark_processed dispatch, is_processed cross-set lookup). Broader model
validation coverage is tracked as a separate test-audit followup.
"""
import pytest
from paper_library.models import ProcessingState


class TestProcessingStateMarkProcessed:
    """Dispatch + error handling for mark_processed."""

    def test_arxiv_routes_to_arxiv_set(self):
        state = ProcessingState()
        state.mark_processed("1706.03762", "arxiv")
        assert "1706.03762" in state.processed_arxiv_ids
        assert "1706.03762" not in state.processed_dois

    def test_doi_routes_to_doi_set(self):
        state = ProcessingState()
        state.mark_processed("10.1093/mind/fzae004", "doi")
        assert "10.1093/mind/fzae004" in state.processed_dois

    def test_web_routes_to_urls_set(self):
        state = ProcessingState()
        state.mark_processed("https://example.com/article", "web")
        assert "https://example.com/article" in state.processed_urls

    def test_local_routes_to_local_paths_set(self):
        """Regression for silent no-op on local-PDF source (issue #17)."""
        state = ProcessingState()
        state.mark_processed("/home/me/paper.pdf", "local")
        assert "/home/me/paper.pdf" in state.processed_local_paths

    def test_unknown_source_raises(self):
        """Regression for silent no-op on unknown source (issue #17)."""
        state = ProcessingState()
        with pytest.raises(ValueError, match="Unknown source"):
            state.mark_processed("whatever", "unknown")

    def test_typo_source_raises(self):
        state = ProcessingState()
        with pytest.raises(ValueError):
            state.mark_processed("id", "arXiv")  # wrong case

    def test_is_processed_across_all_sets(self):
        state = ProcessingState()
        state.mark_processed("1706.03762", "arxiv")
        state.mark_processed("/home/me/paper.pdf", "local")
        assert state.is_processed("1706.03762")
        assert state.is_processed("/home/me/paper.pdf")
        assert not state.is_processed("unseen")
