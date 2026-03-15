"""
Manage native Anthropic Agent Skills for alcanzai synthesis.

Handles uploading SKILL.md directories to the skills API and caching
skill IDs between sessions in skills/skill_ids.json.

Usage:
    manager = SkillsManager(api_key="sk-...")
    containers = manager.build_skill_containers([
        "understand-academic-text",
        "quick-summary",
        "register-controller",
    ])
    # Pass containers to client.beta.messages.create
"""

import json
from pathlib import Path
from typing import Optional

import anthropic
from anthropic.lib import files_from_dir
from paper_library.telemetry import tracer, get_logger

logger = get_logger(__name__)

SKILLS_DIR = Path(__file__).parent.parent / "skills"
SKILL_IDS_FILE = SKILLS_DIR / "skill_ids.json"

# All available skills
SKILL_NAMES = [
    "understand-academic-text",
    "extract-arguments",
    "identify-terminology",
    "register-controller",
    "quick-summary",
    "detailed-summary",
    "glossary-extraction",
]

# Beta header required for skills API
SKILLS_BETA = "skills-2025-10-02"


class SkillsManager:
    """
    Manages native Agent Skills upload and caching.

    Skills are uploaded once and their IDs cached in skills/skill_ids.json.
    On subsequent runs, cached IDs are used without re-uploading.

    The skills API returns an `id` for each uploaded skill, which is then
    used as `skill_id` in the messages container parameter.
    """

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self._skill_ids: dict[str, str] = {}
        self._load_cached_ids()

    def _load_cached_ids(self) -> None:
        if SKILL_IDS_FILE.exists():
            with open(SKILL_IDS_FILE) as f:
                self._skill_ids = json.load(f)

    def _save_cached_ids(self) -> None:
        SKILL_IDS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(SKILL_IDS_FILE, "w") as f:
            json.dump(self._skill_ids, f, indent=2)

    def upload_skill(self, skill_name: str) -> str:
        """
        Upload a skill directory and return its ID.

        The directory must exist at skills/<skill_name>/ and contain a SKILL.md.
        The returned ID is cached in skills/skill_ids.json for future use.

        Args:
            skill_name: Name of the skill directory (e.g., "quick-summary")

        Returns:
            Skill ID string for use in message container

        Raises:
            FileNotFoundError: If skills/<skill_name>/ does not exist
        """
        skill_dir = SKILLS_DIR / skill_name
        if not skill_dir.exists():
            raise FileNotFoundError(f"Skill directory not found: {skill_dir}")

        display_title = skill_name.replace("-", " ").title()

        with tracer.start_as_current_span(
            "skill_upload", attributes={"skill.name": skill_name, "skill.cache_hit": False}
        ) as span:
            response = self.client.beta.skills.create(
                display_title=display_title,
                files=files_from_dir(str(skill_dir)),
                betas=[SKILLS_BETA],
            )

            # response.id is the skill ID used in container.skills[].skill_id
            skill_id = response.id
            span.set_attribute("skill.id", skill_id)

        self._skill_ids[skill_name] = skill_id
        self._save_cached_ids()
        return skill_id

    def get_skill_id(self, skill_name: str) -> str:
        """
        Get skill ID, uploading if not yet cached.

        Args:
            skill_name: Name of the skill

        Returns:
            Skill ID string
        """
        if skill_name in self._skill_ids:
            cached_id = self._skill_ids[skill_name]
            logger.debug("skill_cache_hit", skill_name=skill_name, skill_id=cached_id)
            return cached_id

        return self.upload_skill(skill_name)

    def ensure_uploaded(self, skill_names: Optional[list[str]] = None) -> dict[str, str]:
        """
        Ensure all specified skills are uploaded.

        Args:
            skill_names: Skills to ensure are uploaded. Defaults to all SKILL_NAMES.

        Returns:
            Dict mapping skill_name → skill_id
        """
        names = skill_names or SKILL_NAMES
        for name in names:
            if name not in self._skill_ids:
                self.upload_skill(name)
        return {name: self._skill_ids[name] for name in names}

    def build_skill_containers(self, skill_names: list[str]) -> list[dict]:
        """
        Build the container.skills list for beta.messages.create.

        Args:
            skill_names: Skills to include in the container

        Returns:
            List of skill container dicts with type, skill_id, version

        Example:
            containers = manager.build_skill_containers([
                "understand-academic-text",
                "quick-summary",
                "register-controller",
            ])
            response = client.beta.messages.create(
                ...
                container={"skills": containers},
                betas=["skills-2025-10-02"],
            )
        """
        containers = []
        for name in skill_names:
            skill_id = self.get_skill_id(name)
            containers.append(
                {
                    "type": "custom",
                    "skill_id": skill_id,
                    "version": "latest",
                }
            )
        return containers

    def invalidate_cache(self, skill_name: Optional[str] = None) -> None:
        """
        Remove cached skill IDs to force re-upload.

        Args:
            skill_name: Specific skill to invalidate. If None, clears all.
        """
        if skill_name:
            self._skill_ids.pop(skill_name, None)
        else:
            self._skill_ids.clear()
        self._save_cached_ids()

    @property
    def cached_skills(self) -> list[str]:
        """Names of skills currently cached (already uploaded)."""
        return list(self._skill_ids.keys())
