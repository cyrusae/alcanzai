"""
Processing state management.

This module handles reading and writing the processing_state.json file
to track which papers have been processed and avoid duplicates.

Python concepts:
- Context managers (with statement)
- JSON serialization
- File I/O
- Class methods
"""

import json
from pathlib import Path
from typing import Optional

from paper_library.config import config
from paper_library.models import ProcessingState


class StateManager:
    """
    Manages the processing state file.
    
    This is a singleton pattern - there's only one state file,
    so we always work with the same instance.
    
    Usage:
        state = StateManager.load()
        if not state.is_processed("2312.12345"):
            # Process the paper
            state.mark_processed("2312.12345", "arxiv")
            state.save()
    """
    
    def __init__(self, state_file: Path):
        """
        Initialize the state manager.
        
        Args:
            state_file: Path to the processing_state.json file
        """
        self.state_file = state_file
        self._state: Optional[ProcessingState] = None
    
    @classmethod
    def load(cls) -> "StateManager":
        """
        Load the processing state from disk.
        
        This is a class method (@classmethod) so you can call it without
        creating an instance first: StateManager.load()
        
        Returns:
            StateManager instance with loaded state
        """
        manager = cls(config.processing_state_file)
        manager._load_state()
        return manager
    
    def _load_state(self) -> None:
        """
        Internal method to load state from JSON file.
        
        If the file doesn't exist, creates a new empty state.
        """
        # Check if file exists
        if not self.state_file.exists():
            # Create new empty state
            self._state = ProcessingState()
            return
        
        # Read and parse JSON
        try:
            # Path.read_text() reads the entire file as a string
            data = json.loads(self.state_file.read_text())
            
            # Convert sets from lists (JSON doesn't have sets)
            # The ** syntax "unpacks" the dictionary into keyword arguments
            # It's like doing: ProcessingState(processed_dois=data["processed_dois"], ...)
            self._state = ProcessingState(
                processed_dois=set(data.get("processed_dois", [])),
                processed_arxiv_ids=set(data.get("processed_arxiv_ids", [])),
                processed_urls=set(data.get("processed_urls", [])),
                failed=data.get("failed", {}),
            )
        except Exception as e:
            # If something goes wrong, start fresh
            print(f"Warning: Could not load state file: {e}")
            print("Starting with empty state")
            self._state = ProcessingState()
    
    def save(self) -> None:
        """
        Save the current state to disk.
        
        This converts our ProcessingState model to JSON and writes it.
        """
        # Ensure parent directory exists
        # parents=True creates any missing parent directories
        # exist_ok=True doesn't error if directory already exists
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert state to dictionary
        # Pydantic's model_dump() creates a dict from the model
        data = self._state.model_dump()
        
        # Convert sets to lists for JSON (JSON doesn't support sets)
        # list() converts a set to a list
        data["processed_dois"] = list(data["processed_dois"])
        data["processed_arxiv_ids"] = list(data["processed_arxiv_ids"])
        data["processed_urls"] = list(data["processed_urls"])
        
        # Convert datetime to string (JSON doesn't support datetime)
        if data.get("last_updated"):
            # .isoformat() converts datetime to ISO 8601 string: "2024-01-06T10:30:00"
            data["last_updated"] = data["last_updated"].isoformat()
        
        # Write to file
        # indent=2 makes the JSON human-readable with 2-space indentation
        self.state_file.write_text(json.dumps(data, indent=2))
    
    @property
    def state(self) -> ProcessingState:
        """
        Get the current processing state.
        
        This is a property so you can access it like:
            manager.state.is_processed("123")
        instead of:
            manager.state().is_processed("123")
        """
        if self._state is None:
            self._load_state()
        return self._state
    
    def is_processed(self, identifier: str) -> bool:
        """Convenience method to check if already processed."""
        return self.state.is_processed(identifier)
    
    def mark_processed(self, identifier: str, source: str) -> None:
        """Convenience method to mark as processed and save."""
        self.state.mark_processed(identifier, source)
        self.save()
    
    def mark_failed(self, identifier: str, error: str) -> None:
        """Convenience method to mark as failed and save."""
        self.state.mark_failed(identifier, error)
        self.save()
    
    def get_stats(self) -> dict[str, int]:
        """
        Get processing statistics.
        
        Returns:
            Dictionary with counts of processed papers by source
        """
        return {
            "arxiv": len(self.state.processed_arxiv_ids),
            "doi": len(self.state.processed_dois),
            "web": len(self.state.processed_urls),
            "failed": len(self.state.failed),
            "total": (
                len(self.state.processed_arxiv_ids)
                + len(self.state.processed_dois)
                + len(self.state.processed_urls)
            ),
        }
