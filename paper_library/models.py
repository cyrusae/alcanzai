"""
Data models for papers and articles.

These define the structure of our data using Pydantic, which:
- Validates data types automatically
- Provides nice error messages
- Can serialize to/from JSON easily
- Ensures our data is always in the expected format

Python concepts:
- Type hints: str, int, list[str] tell Python what type each field should be
- Optional[T]: Means the value can be T or None
- Pydantic models: Like dataclasses but with validation
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl


class Citation(BaseModel):
    """
    A single citation from a paper's bibliography.
    
    Example:
        citation = Citation(
            raw_text="Smith et al. (2023). Neural Models of Syntax.",
            authors=["Smith, J.", "Jones, A."],
            title="Neural Models of Syntax",
            year=2023
        )
    """
    # The original citation text from the PDF
    raw_text: str
    
    # Parsed fields (may be None if extraction failed)
    # Optional[str] means "str or None"
    authors: Optional[list[str]] = None
    title: Optional[str] = None
    year: Optional[int] = None
    doi: Optional[str] = None
    
    # How many times this citation is mentioned in the paper
    mention_count: int = 1


class PaperMetadata(BaseModel):
    """
    Metadata for an academic paper.
    
    This is extracted from the PDF (via GROBID) or from APIs (arXiv, DOI).
    """
    # Required fields - these must always be present
    title: str
    authors: list[str]  # list[str] means "a list of strings"
    year: int
    
    # Optional fields - may not always be available
    # = None sets the default value if not provided
    abstract: Optional[str] = None
    doi: Optional[str] = None
    arxiv_id: Optional[str] = None
    venue: Optional[str] = None  # Journal or conference name
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    
    # Citations found in the bibliography
    # Field(default_factory=list) means "default to empty list"
    # This is needed because you can't use [] as a default in Pydantic
    citations: list[Citation] = Field(default_factory=list)
    
    # File paths
    pdf_path: Optional[str] = None
    
    # Processing metadata
    # These track when and how the paper was processed
    processed_at: Optional[datetime] = None
    source: Optional[str] = None  # e.g., "arxiv", "doi", "upload"


class ArticleMetadata(BaseModel):
    """
    Metadata for a web article (blog post, Distill.pub, etc.).
    
    Similar to PaperMetadata but for non-academic content.
    """
    title: str
    authors: list[str]
    
    # URL instead of DOI
    url: HttpUrl  # Pydantic's HttpUrl type validates that it's a real URL
    
    # Optional fields
    published_date: Optional[datetime] = None
    publisher: Optional[str] = None  # e.g., "Anthropic", "DeepMind"
    
    # The converted markdown content
    content: Optional[str] = None
    
    # Processing metadata
    processed_at: Optional[datetime] = None
    source: str = "web"


class Synthesis(BaseModel):
    """
    AI-generated summary of a paper or article.
    
    This is what Claude produces when analyzing the content.
    """
    # Quick refresh (always generated)
    summary: str  # 3-4 sentences
    why_you_cared: str  # 2-3 sentences about relevance
    key_concepts: list[str]  # 5-8 key terms
    memorable_quote: str  # One standout sentence
    
    # Detailed breakdown (optional, generated on-demand)
    detailed_summary: Optional[str] = None
    
    # Metadata about the synthesis
    generated_at: datetime = Field(default_factory=datetime.now)
    model_used: str = "claude-haiku-20250514"
    cost_usd: float = 0.0  # Track how much we spent


class ProcessingState(BaseModel):
    """
    Tracks which papers have been processed to avoid duplicates.
    
    This is saved to processing_state.json in the vault.
    """
    # Sets for fast lookup: "is this DOI already processed?"
    # set[str] means "a set of strings" (sets have unique values, no duplicates)
    processed_dois: set[str] = Field(default_factory=set)
    processed_arxiv_ids: set[str] = Field(default_factory=set)
    processed_urls: set[str] = Field(default_factory=set)
    
    # Papers that failed processing
    # dict[str, str] means "dictionary with string keys and string values"
    # Keys are identifiers (DOI, arXiv ID), values are error messages
    failed: dict[str, str] = Field(default_factory=dict)
    
    # When this state was last updated
    last_updated: datetime = Field(default_factory=datetime.now)
    
    def is_processed(self, identifier: str) -> bool:
        """
        Check if a paper has already been processed.
        
        Args:
            identifier: DOI, arXiv ID, or URL
            
        Returns:
            True if already processed, False otherwise
        """
        # The `in` operator checks if item is in a set (very fast)
        return (
            identifier in self.processed_dois
            or identifier in self.processed_arxiv_ids
            or identifier in self.processed_urls
        )
    
    def mark_processed(self, identifier: str, source: str) -> None:
        """
        Mark a paper as successfully processed.
        
        Args:
            identifier: DOI, arXiv ID, or URL
            source: Where it came from ("arxiv", "doi", "web")
        """
        if source == "arxiv":
            self.processed_arxiv_ids.add(identifier)
        elif source == "doi":
            self.processed_dois.add(identifier)
        elif source == "web":
            self.processed_urls.add(identifier)
        
        # Update timestamp
        self.last_updated = datetime.now()
    
    def mark_failed(self, identifier: str, error: str) -> None:
        """
        Mark a paper as failed processing.
        
        Args:
            identifier: DOI, arXiv ID, or URL
            error: Error message describing what went wrong
        """
        self.failed[identifier] = error
        self.last_updated = datetime.now()
