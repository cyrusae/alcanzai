"""
Unit tests for paper_library.cli.

These tests cover the validate and init commands. They mock config so no
real vault or API key is needed.
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from click.testing import CliRunner

from paper_library.cli import cli


class TestValidateCommand:
    """validate is read-only: it must never create directories."""

    def test_validate_passes_when_api_key_and_vault_exist(self, tmp_path):
        """Both checks green → exit 0."""
        runner = CliRunner()
        mock_config = MagicMock()
        mock_config.anthropic_api_key = "sk-test-key"
        mock_config.vault_path = tmp_path  # tmp_path exists

        with patch("paper_library.cli.config", mock_config):
            result = runner.invoke(cli, ["validate"])

        assert result.exit_code == 0
        assert "All required checks passed" in result.output
        # validate must not create any new paths
        assert not (tmp_path / "Papers").exists()

    def test_validate_fails_when_api_key_missing(self, tmp_path):
        """Missing API key → exit 1, error message shown."""
        runner = CliRunner()
        mock_config = MagicMock()
        mock_config.anthropic_api_key = None
        mock_config.vault_path = tmp_path

        with patch("paper_library.cli.config", mock_config):
            result = runner.invoke(cli, ["validate"])

        assert result.exit_code == 1
        assert "ANTHROPIC_API_KEY" in result.output

    def test_validate_fails_when_vault_missing(self, tmp_path):
        """Non-existent vault → exit 1, no directory created, init hint shown."""
        missing_vault = tmp_path / "nonexistent_vault"
        runner = CliRunner()
        mock_config = MagicMock()
        mock_config.anthropic_api_key = "sk-test-key"
        mock_config.vault_path = missing_vault

        with patch("paper_library.cli.config", mock_config):
            result = runner.invoke(cli, ["validate"])

        assert result.exit_code == 1
        assert not missing_vault.exists(), "validate must NOT create the vault"
        assert "alcanzai init" in result.output

    def test_validate_reports_both_failures(self, tmp_path):
        """Two failures → mentions both, exits 1."""
        missing_vault = tmp_path / "nonexistent"
        runner = CliRunner()
        mock_config = MagicMock()
        mock_config.anthropic_api_key = None
        mock_config.vault_path = missing_vault

        with patch("paper_library.cli.config", mock_config):
            result = runner.invoke(cli, ["validate"])

        assert result.exit_code == 1
        assert "ANTHROPIC_API_KEY" in result.output
        assert "alcanzai init" in result.output


class TestInitCommand:
    """init creates the vault structure; safe to re-run."""

    def test_init_creates_vault_subdirectories(self, tmp_path):
        """init must create Papers, Articles, PDFs, Sources, _meta."""
        vault = tmp_path / "vault"
        runner = CliRunner()
        mock_config = MagicMock()
        mock_config.vault_path = vault

        with patch("paper_library.cli.config", mock_config):
            result = runner.invoke(cli, ["init"])

        assert result.exit_code == 0
        for subdir in ("Papers", "Articles", "PDFs", "Sources", "_meta"):
            assert (vault / subdir).exists(), f"Missing subdirectory: {subdir}"

    def test_init_is_idempotent(self, tmp_path):
        """Running init twice on an existing vault does not error."""
        vault = tmp_path / "vault"
        vault.mkdir()
        runner = CliRunner()
        mock_config = MagicMock()
        mock_config.vault_path = vault

        with patch("paper_library.cli.config", mock_config):
            result1 = runner.invoke(cli, ["init"])
            result2 = runner.invoke(cli, ["init"])

        assert result1.exit_code == 0
        assert result2.exit_code == 0

    def test_init_reports_success(self, tmp_path):
        """init output includes the vault path and a success message."""
        vault = tmp_path / "vault"
        runner = CliRunner()
        mock_config = MagicMock()
        mock_config.vault_path = vault

        with patch("paper_library.cli.config", mock_config):
            result = runner.invoke(cli, ["init"])

        assert "Vault initialized" in result.output
