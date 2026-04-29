"""
Unit tests for paper_library/state.py (StateManager).

All tests use tmp_path to avoid touching the real vault.
No external services required.

Run: pytest tests/test_state.py -m "not integration"
"""

import json
import time
import pytest
from pathlib import Path
from unittest.mock import patch

from paper_library.state import StateManager
from paper_library.models import ProcessingState


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_manager(tmp_path: Path) -> StateManager:
    """Return a StateManager whose state file lives in tmp_path."""
    state_file = tmp_path / "_meta" / "processing_state.json"
    manager = StateManager(state_file)
    manager._state = ProcessingState()
    return manager


def _write_state(state_file: Path, data: dict) -> None:
    """Write a JSON state file to disk (parent dirs created automatically)."""
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(json.dumps(data))


# ---------------------------------------------------------------------------
# Load behaviour
# ---------------------------------------------------------------------------

class TestLoad:
    """StateManager._load_state: file-not-found, valid JSON, corrupt JSON."""

    def test_missing_file_creates_empty_state(self, tmp_path):
        state_file = tmp_path / "_meta" / "processing_state.json"
        manager = StateManager(state_file)
        manager._load_state()
        assert manager.state.processed_arxiv_ids == set()
        assert manager.state.processed_dois == set()

    def test_valid_state_file_round_trips(self, tmp_path):
        state_file = tmp_path / "_meta" / "processing_state.json"
        _write_state(state_file, {
            "processed_arxiv_ids": ["1706.03762", "2312.00001"],
            "processed_dois": ["10.5555/test"],
            "processed_urls": ["https://example.com"],
            "processed_local_paths": ["/papers/thesis.pdf"],
            "failed": {"bad-id": "timeout"},
        })
        manager = StateManager(state_file)
        manager._load_state()
        assert "1706.03762" in manager.state.processed_arxiv_ids
        assert "2312.00001" in manager.state.processed_arxiv_ids
        assert "10.5555/test" in manager.state.processed_dois
        assert "https://example.com" in manager.state.processed_urls
        assert "/papers/thesis.pdf" in manager.state.processed_local_paths
        assert manager.state.failed["bad-id"] == "timeout"

    def test_missing_keys_default_to_empty(self, tmp_path):
        """Partial state file (only some keys present) must not raise."""
        state_file = tmp_path / "_meta" / "processing_state.json"
        _write_state(state_file, {"processed_arxiv_ids": ["1706.03762"]})
        manager = StateManager(state_file)
        manager._load_state()
        assert "1706.03762" in manager.state.processed_arxiv_ids
        assert manager.state.processed_dois == set()

    def test_corrupt_json_creates_empty_state(self, tmp_path):
        """Corrupt file must fall back to empty state without raising."""
        state_file = tmp_path / "_meta" / "processing_state.json"
        state_file.parent.mkdir(parents=True, exist_ok=True)
        state_file.write_text("{ this is not valid json }")
        manager = StateManager(state_file)
        manager._load_state()
        assert manager.state.processed_arxiv_ids == set()

    def test_corrupt_json_writes_backup(self, tmp_path):
        """Corrupt file must be backed up with a timestamped name."""
        state_file = tmp_path / "_meta" / "processing_state.json"
        state_file.parent.mkdir(parents=True, exist_ok=True)
        state_file.write_text("{ this is not valid json }")
        manager = StateManager(state_file)
        manager._load_state()
        backups = list(state_file.parent.glob("*.corrupt.*"))
        assert len(backups) == 1, f"Expected 1 backup, found: {backups}"

    def test_state_property_lazy_loads(self, tmp_path):
        """Accessing .state before _load_state must trigger a load automatically."""
        state_file = tmp_path / "_meta" / "processing_state.json"
        _write_state(state_file, {"processed_arxiv_ids": ["lazy-load-id"]})
        manager = StateManager(state_file)
        # _state not set — property must call _load_state
        manager._state = None
        assert "lazy-load-id" in manager.state.processed_arxiv_ids


# ---------------------------------------------------------------------------
# Save behaviour
# ---------------------------------------------------------------------------

class TestSave:
    """StateManager.save: creates file, atomic write, round-trips sets."""

    def test_save_creates_parent_dirs(self, tmp_path):
        state_file = tmp_path / "deep" / "nested" / "state.json"
        manager = StateManager(state_file)
        manager._state = ProcessingState()
        manager.save()
        assert state_file.exists()

    def test_save_round_trips_arxiv_ids(self, tmp_path):
        manager = _make_manager(tmp_path)
        manager.state.mark_processed("1706.03762", "arxiv")
        manager.save()

        reloaded = StateManager(manager.state_file)
        reloaded._load_state()
        assert "1706.03762" in reloaded.state.processed_arxiv_ids

    def test_save_round_trips_all_source_types(self, tmp_path):
        manager = _make_manager(tmp_path)
        manager.state.mark_processed("arxiv-id", "arxiv")
        manager.state.mark_processed("10.5555/doi", "doi")
        manager.state.mark_processed("https://url.com", "web")
        manager.state.mark_processed("/local.pdf", "local")
        manager.save()

        reloaded = StateManager(manager.state_file)
        reloaded._load_state()
        assert "arxiv-id" in reloaded.state.processed_arxiv_ids
        assert "10.5555/doi" in reloaded.state.processed_dois
        assert "https://url.com" in reloaded.state.processed_urls
        assert "/local.pdf" in reloaded.state.processed_local_paths

    def test_save_round_trips_failed(self, tmp_path):
        manager = _make_manager(tmp_path)
        manager.state.mark_failed("bad-id", "Network error")
        manager.save()

        reloaded = StateManager(manager.state_file)
        reloaded._load_state()
        assert reloaded.state.failed["bad-id"] == "Network error"

    def test_atomic_write_leaves_no_tmp_file(self, tmp_path):
        """After save(), the .tmp sibling must be gone."""
        manager = _make_manager(tmp_path)
        manager.save()
        tmp_files = list(manager.state_file.parent.glob("*.tmp"))
        assert tmp_files == [], f"Leftover .tmp files: {tmp_files}"

    def test_saved_json_is_valid(self, tmp_path):
        """The written file must be parseable JSON with list values for sets."""
        manager = _make_manager(tmp_path)
        manager.state.mark_processed("1706.03762", "arxiv")
        manager.save()

        raw = json.loads(manager.state_file.read_text())
        assert isinstance(raw["processed_arxiv_ids"], list)
        assert "1706.03762" in raw["processed_arxiv_ids"]


# ---------------------------------------------------------------------------
# Convenience methods
# ---------------------------------------------------------------------------

class TestConvenienceMethods:
    """mark_processed, mark_failed, is_processed — all auto-save."""

    def test_mark_processed_saves_immediately(self, tmp_path):
        manager = _make_manager(tmp_path)
        manager.mark_processed("1706.03762", "arxiv")
        assert manager.state_file.exists()
        raw = json.loads(manager.state_file.read_text())
        assert "1706.03762" in raw["processed_arxiv_ids"]

    def test_mark_failed_saves_immediately(self, tmp_path):
        manager = _make_manager(tmp_path)
        manager.mark_failed("bad", "timeout")
        raw = json.loads(manager.state_file.read_text())
        assert raw["failed"]["bad"] == "timeout"

    def test_is_processed_delegates_to_state(self, tmp_path):
        manager = _make_manager(tmp_path)
        assert not manager.is_processed("1706.03762")
        manager.mark_processed("1706.03762", "arxiv")
        assert manager.is_processed("1706.03762")

    def test_mark_processed_unknown_source_raises(self, tmp_path):
        manager = _make_manager(tmp_path)
        with pytest.raises(ValueError, match="Unknown source"):
            manager.mark_processed("some-id", "rss")


# ---------------------------------------------------------------------------
# get_stats
# ---------------------------------------------------------------------------

class TestGetStats:
    """get_stats returns per-source counts and total."""

    def test_empty_state_all_zeros(self, tmp_path):
        manager = _make_manager(tmp_path)
        stats = manager.get_stats()
        assert stats["arxiv"] == 0
        assert stats["doi"] == 0
        assert stats["web"] == 0
        assert stats["local"] == 0
        assert stats["failed"] == 0
        assert stats["total"] == 0

    def test_counts_match_mark_processed_calls(self, tmp_path):
        manager = _make_manager(tmp_path)
        manager.state.mark_processed("a1", "arxiv")
        manager.state.mark_processed("a2", "arxiv")
        manager.state.mark_processed("d1", "doi")
        manager.state.mark_processed("w1", "web")
        manager.state.mark_failed("f1", "error")
        stats = manager.get_stats()
        assert stats["arxiv"] == 2
        assert stats["doi"] == 1
        assert stats["web"] == 1
        assert stats["local"] == 0
        assert stats["failed"] == 1
        assert stats["total"] == 4

    def test_total_excludes_failed(self, tmp_path):
        """failed entries must not be counted in 'total'."""
        manager = _make_manager(tmp_path)
        manager.state.mark_processed("a1", "arxiv")
        manager.state.mark_failed("f1", "err")
        stats = manager.get_stats()
        assert stats["total"] == 1

    def test_duplicate_ids_not_double_counted(self, tmp_path):
        """Sets deduplicate; marking the same ID twice must keep count at 1."""
        manager = _make_manager(tmp_path)
        manager.state.mark_processed("1706.03762", "arxiv")
        manager.state.mark_processed("1706.03762", "arxiv")
        stats = manager.get_stats()
        assert stats["arxiv"] == 1
        assert stats["total"] == 1


# ---------------------------------------------------------------------------
# Deduplication across sources
# ---------------------------------------------------------------------------

class TestDeduplication:
    """Identifiers are partitioned by source; no cross-set contamination."""

    def test_arxiv_id_not_visible_via_doi_check(self, tmp_path):
        manager = _make_manager(tmp_path)
        manager.state.mark_processed("1706.03762", "arxiv")
        assert "1706.03762" not in manager.state.processed_dois

    def test_same_string_in_two_sources(self, tmp_path):
        """If an arXiv ID accidentally matches a DOI string, both sets stay separate."""
        manager = _make_manager(tmp_path)
        manager.state.mark_processed("shared-string", "arxiv")
        manager.state.mark_processed("shared-string", "doi")
        assert "shared-string" in manager.state.processed_arxiv_ids
        assert "shared-string" in manager.state.processed_dois
        # is_processed returns True (found in one of the sets)
        assert manager.state.is_processed("shared-string")

    def test_is_processed_checks_all_four_sets(self, tmp_path):
        """is_processed must return True regardless of which set holds the id."""
        manager = _make_manager(tmp_path)
        for source, ident in [
            ("arxiv", "ax1"), ("doi", "d1"), ("web", "w1"), ("local", "l1")
        ]:
            manager.state.mark_processed(ident, source)
        for ident in ["ax1", "d1", "w1", "l1"]:
            assert manager.state.is_processed(ident), f"{ident} not found"
