"""
Cross-cutting test: all places that embed a version string must agree.

Regression guard for the version-drift pattern identified in the
2026-04-22 code review (issue #20). If you bump the version, you need
to update only paper_library/__init__.py and the pyproject.toml version
(which stays the source of truth for pip metadata).
"""
import tomllib
from pathlib import Path

import paper_library
from paper_library.doi_fetcher import DoiFetcher


REPO_ROOT = Path(__file__).resolve().parent.parent


def _pyproject_version() -> str:
    with open(REPO_ROOT / "pyproject.toml", "rb") as f:
        return tomllib.load(f)["project"]["version"]


def test_pyproject_matches_package_version():
    assert _pyproject_version() == paper_library.__version__


def test_user_agent_includes_package_version():
    ua = DoiFetcher.HEADERS["User-Agent"]
    assert paper_library.__version__ in ua, (
        f"User-Agent {ua!r} does not contain package version "
        f"{paper_library.__version__!r}"
    )
