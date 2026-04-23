"""
Tests for paper_library/skills_manager.py.

Minimal coverage focused on the corrupt-cache tolerance (issue #21).
Broader SkillsManager tests are tracked as a separate followup.
"""
from unittest.mock import patch


class TestLoadCachedIds:
    """Regression tests for #21: corrupt skills_ids.json should not crash startup."""

    def test_corrupt_json_resets_to_empty(self, tmp_path):
        """Malformed JSON in skill_ids.json should log + reset, not raise."""
        fake_cache = tmp_path / "skill_ids.json"
        fake_cache.write_text("{ this is not valid json")

        with patch("paper_library.skills_manager.SKILL_IDS_FILE", fake_cache):
            # Import late so the patched SKILL_IDS_FILE is used
            from paper_library.skills_manager import SkillsManager

            # api_key is irrelevant for _load_cached_ids; just needs to construct
            mgr = SkillsManager(api_key="sk-test")

        assert mgr.cached_skills == []

    def test_missing_file_is_fine(self, tmp_path):
        """Absent cache file is a valid starting state."""
        fake_cache = tmp_path / "nonexistent.json"

        with patch("paper_library.skills_manager.SKILL_IDS_FILE", fake_cache):
            from paper_library.skills_manager import SkillsManager

            mgr = SkillsManager(api_key="sk-test")

        assert mgr.cached_skills == []

    def test_valid_cache_loads(self, tmp_path):
        """Well-formed cache loads correctly."""
        import json

        fake_cache = tmp_path / "skill_ids.json"
        fake_cache.write_text(json.dumps({"quick-summary": "skill_01abc"}))

        with patch("paper_library.skills_manager.SKILL_IDS_FILE", fake_cache):
            from paper_library.skills_manager import SkillsManager

            mgr = SkillsManager(api_key="sk-test")

        assert "quick-summary" in mgr.cached_skills
