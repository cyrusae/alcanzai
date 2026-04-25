"""
Tests for StateManager atomic writes and corrupt-state recovery.

Regression guards for R2 (code review 2026-04-22, issue #11): the
state file must not silently lose processed-paper history if a write
is interrupted or if the on-disk JSON becomes corrupt.
"""

import json
from pathlib import Path

import pytest

from paper_library.models import ProcessingState
from paper_library.state import StateManager


def _make_manager(tmp_path: Path) -> StateManager:
    mgr = StateManager(tmp_path / "processing_state.json")
    mgr._state = ProcessingState()
    return mgr


class TestAtomicSave:
    """save() must write atomically via os.replace, not truncate-in-place."""

    def test_save_produces_parseable_file(self, tmp_path):
        mgr = _make_manager(tmp_path)
        mgr._state.processed_arxiv_ids.add("1706.03762")
        mgr.save()

        data = json.loads(mgr.state_file.read_text())
        assert "1706.03762" in data["processed_arxiv_ids"]

    def test_save_leaves_no_tmp_file_behind(self, tmp_path):
        mgr = _make_manager(tmp_path)
        mgr.save()

        # After a successful save, no .tmp sibling should remain.
        tmps = list(tmp_path.glob("processing_state.json*.tmp"))
        assert tmps == [], f"stray tmp files: {tmps}"

    def test_save_overwrites_existing_file_atomically(self, tmp_path):
        mgr = _make_manager(tmp_path)
        mgr._state.processed_arxiv_ids.add("first")
        mgr.save()

        mgr._state.processed_arxiv_ids.add("second")
        mgr.save()

        data = json.loads(mgr.state_file.read_text())
        assert set(data["processed_arxiv_ids"]) == {"first", "second"}

    def test_save_preserves_original_when_tmp_write_fails(self, tmp_path, monkeypatch):
        """If the tmp write blows up, the real state file must remain intact."""
        mgr = _make_manager(tmp_path)
        mgr._state.processed_arxiv_ids.add("original")
        mgr.save()
        original_bytes = mgr.state_file.read_bytes()

        # Force write_text to fail mid-save
        original_write_text = Path.write_text

        def exploding_write_text(self, *args, **kwargs):
            if self.name.endswith(".tmp"):
                raise OSError("simulated disk full")
            return original_write_text(self, *args, **kwargs)

        monkeypatch.setattr(Path, "write_text", exploding_write_text)
        mgr._state.processed_arxiv_ids.add("would-be-lost")
        with pytest.raises(OSError):
            mgr.save()

        # The on-disk file must still be the previous good copy.
        assert mgr.state_file.read_bytes() == original_bytes


class TestCorruptStateBackup:
    """_load_state() must back up a corrupt file rather than silently wipe it."""

    def test_corrupt_json_is_backed_up(self, tmp_path):
        state_file = tmp_path / "processing_state.json"
        state_file.write_text("{not valid json at all")

        mgr = StateManager(state_file)
        mgr._load_state()

        backups = list(tmp_path.glob("processing_state.corrupt.*"))
        assert len(backups) == 1, f"expected one .corrupt.* backup, got {backups}"
        # Backup should contain the original garbage, byte-for-byte
        assert backups[0].read_text() == "{not valid json at all"

    def test_corrupt_load_falls_back_to_empty_state(self, tmp_path):
        state_file = tmp_path / "processing_state.json"
        state_file.write_text("garbage")

        mgr = StateManager(state_file)
        mgr._load_state()

        assert mgr.state.processed_arxiv_ids == set()
        assert mgr.state.processed_dois == set()

    def test_missing_file_does_not_create_backup(self, tmp_path):
        """A nonexistent state file is normal (first run), not corrupt."""
        mgr = StateManager(tmp_path / "processing_state.json")
        mgr._load_state()

        backups = list(tmp_path.glob("processing_state.corrupt.*"))
        assert backups == []

    def test_valid_file_does_not_create_backup(self, tmp_path):
        mgr = _make_manager(tmp_path)
        mgr._state.processed_arxiv_ids.add("1706.03762")
        mgr.save()

        mgr2 = StateManager(mgr.state_file)
        mgr2._load_state()

        backups = list(tmp_path.glob("processing_state.corrupt.*"))
        assert backups == []
        assert "1706.03762" in mgr2.state.processed_arxiv_ids
