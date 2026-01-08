"""
Configuration management for the paper library.

This module loads settings from environment variables (via .env file)
and provides them to the rest of the application.

Python concepts covered:
- dataclasses: Clean way to create classes that just hold data
- pathlib.Path: Modern way to work with file paths (better than strings)
- os.getenv: Read environment variables
- dotenv: Load variables from .env file
"""

import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file into os.environ
# This happens automatically when this module is imported
load_dotenv()


@dataclass
class Config:
    """
    Application configuration loaded from environment variables.
    
    A dataclass is a special kind of Python class that:
    - Automatically creates __init__ method
    - Provides nice __repr__ for printing
    - Can have default values
    
    Usage:
        config = Config()
        print(config.anthropic_api_key)  # Access like attributes
    """
    
    # API keys and endpoints
    # os.getenv("KEY", "default") reads from environment, uses default if not set
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    grobid_url: str = os.getenv("GROBID_URL", "http://localhost:8070")
    
    # File paths
    # Path() creates a pathlib Path object, better than string manipulation
    # .resolve() converts to absolute path (e.g., ./vault -> /home/user/vault)
    vault_path: Path = Path(os.getenv("VAULT_PATH", "./vault")).resolve()
    
    # Derived paths - constructed from vault_path
    # Using @property means these are computed on-the-fly when accessed
    # They act like attributes but are actually methods
    @property
    def papers_dir(self) -> Path:
        """Directory where paper notes are stored."""
        return self.vault_path / "Papers"
    
    @property
    def articles_dir(self) -> Path:
        """Directory where article notes are stored."""
        return self.vault_path / "Articles"
    
    @property
    def pdfs_dir(self) -> Path:
        """Directory where PDF files are stored."""
        return self.vault_path / "PDFs"
    
    @property
    def meta_dir(self) -> Path:
        """Directory for metadata and processing state."""
        return self.vault_path / "_meta"
    
    @property
    def processing_state_file(self) -> Path:
        """JSON file tracking which papers have been processed."""
        return self.meta_dir / "processing_state.json"
    
    def validate(self) -> None:
        """
        Check that all required configuration is present.
        
        Raises:
            ValueError: If API key is missing or vault path doesn't exist
        """
        # Check API key
        if not self.anthropic_api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not set. "
                "Please create a .env file with your API key."
            )
        
        # Check that vault exists (create it if needed)
        if not self.vault_path.exists():
            print(f"Creating vault directory at {self.vault_path}")
            self.vault_path.mkdir(parents=True, exist_ok=True)


# Create a global config instance
# This is imported by other modules: from paper_library.config import config
config = Config()
