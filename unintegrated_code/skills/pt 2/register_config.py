"""
Register configuration management for alcanzai.

Handles loading and managing register presets from config files
and command-line arguments.

Python concepts:
- TOML configuration files
- Dataclasses for configuration
- Environment variable handling
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional
try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib  # Fallback for Python 3.9-3.10


@dataclass
class RegisterConfig:
    """
    Register configuration for synthesis.
    
    Defines three orthogonal axes that control synthesis output:
    - jargon: How much technical terminology to use
    - structure: Sentence complexity and formality
    - depth: How much explanation to provide
    """
    jargon: str = "selective"      # none | selective | heavy
    structure: str = "mixed"       # conversational | mixed | formal
    depth: str = "balanced"        # hand-holding | balanced | assume-knowledge
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary for skill loader."""
        return {
            "jargon": self.jargon,
            "structure": self.structure,
            "depth": self.depth
        }
    
    @classmethod
    def from_dict(cls, config: Dict[str, str]) -> "RegisterConfig":
        """Create from dictionary."""
        return cls(
            jargon=config.get("jargon", "selective"),
            structure=config.get("structure", "mixed"),
            depth=config.get("depth", "balanced")
        )


@dataclass
class AlcanzaiConfig:
    """
    Complete alcanzai configuration.
    
    Includes register presets and other settings.
    """
    # Default register
    register: RegisterConfig = field(default_factory=RegisterConfig)
    
    # Named presets for common use cases
    presets: Dict[str, RegisterConfig] = field(default_factory=dict)
    
    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "AlcanzaiConfig":
        """
        Load configuration from TOML file.
        
        Args:
            config_path: Path to config.toml file
                        If None, looks in standard locations:
                        1. ./alcanzai.toml (project directory)
                        2. ~/.config/alcanzai/config.toml (user config)
                        3. ~/.alcanzai.toml (user home)
        
        Returns:
            AlcanzaiConfig instance
        """
        # Find config file
        if config_path is None:
            config_path = cls._find_config_file()
        
        # If no config found, use defaults
        if config_path is None or not config_path.exists():
            return cls._create_default()
        
        # Load TOML
        with open(config_path, 'rb') as f:
            data = tomllib.load(f)
        
        # Parse register section
        register = RegisterConfig.from_dict(data.get("register", {}))
        
        # Parse presets
        presets = {}
        for name, preset_data in data.get("presets", {}).items():
            presets[name] = RegisterConfig.from_dict(preset_data)
        
        return cls(register=register, presets=presets)
    
    @classmethod
    def _find_config_file(cls) -> Optional[Path]:
        """
        Search for config file in standard locations.
        
        Returns:
            Path to config file, or None if not found
        """
        search_paths = [
            Path.cwd() / "alcanzai.toml",                    # Project directory
            Path.home() / ".config" / "alcanzai" / "config.toml",  # XDG config
            Path.home() / ".alcanzai.toml",                  # User home
        ]
        
        for path in search_paths:
            if path.exists():
                return path
        
        return None
    
    @classmethod
    def _create_default(cls) -> "AlcanzaiConfig":
        """
        Create default configuration with common presets.
        
        Returns:
            AlcanzaiConfig with default presets
        """
        presets = {
            # Learning mode: accessible with lots of explanation
            "learning": RegisterConfig(
                jargon="selective",
                structure="conversational",
                depth="hand-holding"
            ),
            
            # Partner-shareable: maximum accessibility
            "partner": RegisterConfig(
                jargon="none",
                structure="conversational",
                depth="hand-holding"
            ),
            
            # Literature review: expert efficiency
            "litreview": RegisterConfig(
                jargon="heavy",
                structure="formal",
                depth="assume-knowledge"
            ),
            
            # Quick scan: efficient but still clear
            "scan": RegisterConfig(
                jargon="heavy",
                structure="mixed",
                depth="balanced"
            ),
            
            # Default: balanced across all axes
            "default": RegisterConfig(
                jargon="selective",
                structure="mixed",
                depth="balanced"
            )
        }
        
        return cls(
            register=RegisterConfig(),  # Use defaults
            presets=presets
        )
    
    def get_register(self, preset: Optional[str] = None) -> RegisterConfig:
        """
        Get register configuration.
        
        Args:
            preset: Name of preset to use, or None for default
        
        Returns:
            RegisterConfig instance
        
        Raises:
            ValueError: If preset doesn't exist
        """
        if preset is None:
            return self.register
        
        if preset not in self.presets:
            available = ", ".join(self.presets.keys())
            raise ValueError(
                f"Unknown preset: {preset}\n"
                f"Available presets: {available}"
            )
        
        return self.presets[preset]
    
    def save(self, config_path: Path):
        """
        Save configuration to TOML file.
        
        Args:
            config_path: Path to save config.toml
        """
        # Ensure parent directory exists
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Build TOML structure
        data = {
            "register": self.register.to_dict(),
            "presets": {
                name: preset.to_dict()
                for name, preset in self.presets.items()
            }
        }
        
        # Write TOML (using simple approach since we have simple structure)
        with open(config_path, 'w') as f:
            f.write("# alcanzai configuration\n\n")
            
            # Write default register
            f.write("[register]\n")
            for key, value in data["register"].items():
                f.write(f'{key} = "{value}"\n')
            f.write("\n")
            
            # Write presets
            for preset_name, preset_data in data["presets"].items():
                f.write(f"[presets.{preset_name}]\n")
                for key, value in preset_data.items():
                    f.write(f'{key} = "{value}"\n')
                f.write("\n")


def create_default_config(config_path: Path):
    """
    Create a default configuration file.
    
    Args:
        config_path: Where to save the config file
    """
    config = AlcanzaiConfig._create_default()
    config.save(config_path)
    print(f"Created default configuration: {config_path}")


# Example config file content (for documentation)
EXAMPLE_CONFIG = """# alcanzai configuration

# Default register settings (used unless overridden)
[register]
jargon = "selective"      # none | selective | heavy
structure = "mixed"       # conversational | mixed | formal
depth = "balanced"        # hand-holding | balanced | assume-knowledge

# Preset configurations for common use cases
[presets.learning]
jargon = "selective"
structure = "conversational"
depth = "hand-holding"

[presets.partner]
jargon = "none"
structure = "conversational"
depth = "hand-holding"

[presets.litreview]
jargon = "heavy"
structure = "formal"
depth = "assume-knowledge"

[presets.scan]
jargon = "heavy"
structure = "mixed"
depth = "balanced"

[presets.default]
jargon = "selective"
structure = "mixed"
depth = "balanced"
"""
