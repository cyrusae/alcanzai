"""
Paper Library - Personal Research Knowledge Graph

A tool for processing academic papers and web articles into an Obsidian vault
with AI-generated summaries, citation networks, and searchable metadata.

Main workflow:
    from paper_library.orchestrator import PaperProcessor
    from paper_library.state import StateManager
    from paper_library.config import config
    
    state = StateManager.load()
    processor = PaperProcessor(config, state)
    processor.process("2312.12345")  # arXiv ID
"""

__version__ = "0.1.0"

# Core components available at package level
from paper_library.config import config
from paper_library.models import (
    Citation,
    PaperMetadata,
    ArticleMetadata,
    Synthesis,
    ProcessingState,
)
from paper_library.state import StateManager

__all__ = [
    "config",
    "Citation",
    "PaperMetadata",
    "ArticleMetadata",
    "Synthesis",
    "ProcessingState",
    "StateManager",
]
