"""
Skill loader for alcanzai synthesis system.

Reads markdown skill files from /mnt/skills/user/alcanzai/ and composes them
into complete prompts for Claude API calls.

Python concepts:
- File I/O with pathlib
- String composition and templating
- Caching for performance
- Configuration management
"""

from pathlib import Path
from typing import Dict, Optional


class SkillLoader:
    """
    Load and compose skills from markdown files.
    
    Skills are organized as:
    /mnt/skills/user/alcanzai/
    ├── core/                          # Foundational skills
    │   ├── understand-academic-text-SKILL.md
    │   ├── extract-arguments-SKILL.md
    │   └── identify-terminology-SKILL.md
    ├── synthesis/                     # Output generation skills
    │   ├── quick-summary-SKILL.md
    │   ├── detailed-summary-SKILL.md
    │   └── glossary-extraction-SKILL.md
    └── register/                      # Tone/style configuration
        ├── jargon-density/
        │   ├── none.md
        │   ├── selective.md
        │   └── heavy.md
        ├── sentence-structure/
        │   ├── conversational.md
        │   ├── mixed.md
        │   └── formal.md
        └── explanation-depth/
            ├── hand-holding.md
            ├── balanced.md
            └── assume-knowledge.md
    
    Usage:
        loader = SkillLoader()
        
        # Load synthesis with register
        prompt = loader.load_synthesis_skill(
            task="quick-summary",
            register_config={
                "jargon": "selective",
                "structure": "mixed",
                "depth": "balanced"
            }
        )
        
        # Send prompt to Claude
        response = client.messages.create(
            model="claude-sonnet-4-5",
            messages=[{"role": "user", "content": prompt + paper_text}]
        )
    """
    
    # Default register configuration
    DEFAULT_REGISTER = {
        "jargon": "selective",      # Keep technical terms + inline glosses
        "structure": "mixed",       # Professional but clear
        "depth": "balanced"         # Standard academic detail
    }
    
    def __init__(self, skills_dir: Optional[Path] = None):
        """
        Initialize skill loader.
        
        Args:
            skills_dir: Path to skills directory
                       Defaults to /mnt/skills/user/alcanzai
        """
        self.skills_dir = skills_dir or Path("/mnt/skills/user/alcanzai")
        
        # Cache loaded skills to avoid re-reading files
        self._cache: Dict[str, str] = {}
    
    def load_synthesis_skill(
        self,
        task: str,
        register_config: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Load complete synthesis skill with register configuration.
        
        This composes:
        1. Register configuration (jargon, structure, depth)
        2. Task-specific skill (quick-summary, detailed-summary, etc.)
        
        Args:
            task: Synthesis task name
                  Options: "quick-summary", "detailed-summary", "glossary-extraction"
            register_config: Register settings
                           {
                               "jargon": "none" | "selective" | "heavy",
                               "structure": "conversational" | "mixed" | "formal",
                               "depth": "hand-holding" | "balanced" | "assume-knowledge"
                           }
        
        Returns:
            Complete prompt ready to send to Claude
        """
        # Use default register if none provided
        config = register_config or self.DEFAULT_REGISTER
        
        # Load register components
        register_prompt = self._load_register(config)
        
        # Load task skill
        task_prompt = self._load_task_skill(task)
        
        # Compose: register first, then task
        return f"""{register_prompt}

---

{task_prompt}"""
    
    def _load_register(self, config: Dict[str, str]) -> str:
        """
        Load and compose register configuration.
        
        Args:
            config: Register settings dict
        
        Returns:
            Composed register prompt section
        """
        # Load each register axis
        jargon = self._load_skill_file(
            f"register/jargon-density/{config['jargon']}.md"
        )
        structure = self._load_skill_file(
            f"register/sentence-structure/{config['structure']}.md"
        )
        depth = self._load_skill_file(
            f"register/explanation-depth/{config['depth']}.md"
        )
        
        # Compose into register section
        return f"""# Register Configuration

The following register settings control how you should write the synthesis:

## Jargon Density: {config['jargon'].title()}

{jargon}

---

## Sentence Structure: {config['structure'].title()}

{structure}

---

## Explanation Depth: {config['depth'].title()}

{depth}"""
    
    def _load_task_skill(self, task: str) -> str:
        """
        Load task-specific synthesis skill.
        
        Args:
            task: Task name (e.g., "quick-summary")
        
        Returns:
            Task skill content
        """
        return self._load_skill_file(f"synthesis/{task}-SKILL.md")
    
    def _load_skill_file(self, relative_path: str) -> str:
        """
        Load a single skill file with caching.
        
        Args:
            relative_path: Path relative to skills_dir
        
        Returns:
            File content
        
        Raises:
            FileNotFoundError: If skill file doesn't exist
        """
        # Check cache first
        if relative_path in self._cache:
            return self._cache[relative_path]
        
        # Build absolute path
        file_path = self.skills_dir / relative_path
        
        # Verify file exists
        if not file_path.exists():
            raise FileNotFoundError(
                f"Skill not found: {file_path}\n"
                f"Looking for: {relative_path}"
            )
        
        # Read and cache
        content = file_path.read_text(encoding='utf-8')
        self._cache[relative_path] = content
        
        return content
    
    def clear_cache(self):
        """Clear the skill file cache. Useful for development/testing."""
        self._cache.clear()
    
    def validate_register_config(self, config: Dict[str, str]) -> bool:
        """
        Validate a register configuration.
        
        Args:
            config: Register config to validate
        
        Returns:
            True if valid
        
        Raises:
            ValueError: If config is invalid
        """
        valid_options = {
            "jargon": ["none", "selective", "heavy"],
            "structure": ["conversational", "mixed", "formal"],
            "depth": ["hand-holding", "balanced", "assume-knowledge"]
        }
        
        for key, value in config.items():
            if key not in valid_options:
                raise ValueError(f"Unknown register axis: {key}")
            if value not in valid_options[key]:
                raise ValueError(
                    f"Invalid value for {key}: {value}\n"
                    f"Valid options: {', '.join(valid_options[key])}"
                )
        
        return True


# Convenience function for quick use
def load_synthesis_prompt(
    task: str,
    jargon: str = "selective",
    structure: str = "mixed",
    depth: str = "balanced"
) -> str:
    """
    Convenience function to load a synthesis prompt.
    
    Args:
        task: Synthesis task ("quick-summary", "detailed-summary", etc.)
        jargon: Jargon density ("none", "selective", "heavy")
        structure: Sentence structure ("conversational", "mixed", "formal")
        depth: Explanation depth ("hand-holding", "balanced", "assume-knowledge")
    
    Returns:
        Complete prompt ready for Claude
    
    Example:
        prompt = load_synthesis_prompt(
            task="quick-summary",
            jargon="selective",
            structure="conversational",
            depth="hand-holding"
        )
    """
    loader = SkillLoader()
    return loader.load_synthesis_skill(
        task=task,
        register_config={
            "jargon": jargon,
            "structure": structure,
            "depth": depth
        }
    )
