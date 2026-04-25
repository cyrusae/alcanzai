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


class BibliographicEntry(BaseModel):
    """
    Base class for any bibliographic reference.
    
    Represents the core metadata that applies to any cited work,
    whether it's a paper we're processing or a citation from a bibliography.
    
    This shared base enables:
    - Consistent metadata extraction from GROBID
    - Easy promotion of Citation → PaperMetadata for citation graphs
    - Reusable formatting/display logic
    
    Python concepts:
    - Class inheritance: Citation and PaperMetadata extend this base
    - Optional fields: Most fields can be None if GROBID can't extract them
    """
    # Core identifying fields
    # For main papers: typically required; for citations: often present but can be None
    title: Optional[str] = None
    authors: Optional[list[str]] = None
    year: Optional[int] = None
    
    # Publication details
    # GROBID extracts these from <monogr> elements for both
    # main papers and citations
    venue: Optional[str] = None      # Journal or conference name
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    
    # Identifiers
    doi: Optional[str] = None
    arxiv_id: Optional[str] = None
    
    # Content
    abstract: Optional[str] = None
    
    # Raw source text
    # For citations: the full text GROBID extracted from bibliography
    # For main papers: typically None (we have the PDF)
    raw_text: Optional[str] = None


class Citation(BibliographicEntry):
    """
    A citation extracted from a paper's bibliography.
    
    Inherits all bibliographic fields from BibliographicEntry,
    adds citation-specific metadata.
    
    Example:
        citation = Citation(
            raw_text="Smith et al. (2023). Neural Models of Syntax. Nature, 123(4), pp. 567-890.",
            authors=["Smith, J.", "Jones, A."],
            title="Neural Models of Syntax",
            year=2023,
            venue="Nature",
            volume="123",
            issue="4",
            pages="567-890",
            mention_count=1
        )
    
    Future: Can be "promoted" to PaperMetadata when we process the cited paper,
    enabling the citation graph feature.
    """
    # How many times this citation is mentioned in the parent paper
    mention_count: int = 1

    # Context sentences extracted from the body of the citing paper.
    # Each string is 1-3 sentences showing how this citation was used.
    # Populated by CitationContextExtractor during processing.
    contexts: list[str] = Field(default_factory=list)

    # Future fields for citation graph (Phase 2):
    # citation_key: Optional[str] = None  # For Pandoc/BibTeX integration
    # processed: bool = False             # Have we processed this paper?
    # parent_paper_id: Optional[str] = None  # DOI/arXiv of citing paper


class PaperMetadata(BibliographicEntry):
    """
    A paper we're actively processing for the vault.
    
    Inherits all bibliographic fields from BibliographicEntry,
    adds processing-specific metadata and the paper's own bibliography.
    
    This is extracted from the PDF (via GROBID) or from APIs (arXiv, DOI).
    
    For main papers, title/authors/year are REQUIRED (we validate in GROBID processor).
    """
    # Title and authors are required for papers we're processing.
    # Year is optional: some legitimate inputs (preprints, working papers,
    # institutional technical reports) don't carry a publication date in
    # their metadata. Better to let the paper into the vault with year=None
    # than to block ingestion on a missing field the user couldn't fill
    # in anyway.
    title: str
    authors: list[str]
    year: Optional[int] = None
    
    # Bibliography of this paper
    # Citations now have full metadata (venue, volume, etc.)
    citations: list[Citation] = Field(default_factory=list)
    
    # File paths
    pdf_path: Optional[str] = None

    # Full body text extracted by GROBID (clean, 2-column-aware).
    # Preferred over pdfplumber output for synthesis and citation context matching.
    body_text: Optional[str] = None

    # Processing metadata
    # These track when and how the paper was processed
    processed_at: Optional[datetime] = None
    source: Optional[str] = None  # e.g., "arxiv", "doi", "grobid", "local"


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

    # Local path if the article was a PDF downloaded from a URL.
    # Set by WebFetcher when it saves the file; used by orchestrator
    # to route the item through GROBID instead of the HTML article path.
    pdf_path: Optional[str] = None

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
    processed_local_paths: set[str] = Field(default_factory=set)

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
            identifier: DOI, arXiv ID, URL, or local file path

        Returns:
            True if already processed, False otherwise
        """
        # The `in` operator checks if item is in a set (very fast)
        return (
            identifier in self.processed_dois
            or identifier in self.processed_arxiv_ids
            or identifier in self.processed_urls
            or identifier in self.processed_local_paths
        )

    def mark_processed(self, identifier: str, source: str) -> None:
        """
        Mark a paper as successfully processed.

        Args:
            identifier: DOI, arXiv ID, URL, or local file path
            source: Where it came from. One of:
                    "arxiv", "doi", "web", "local"

        Raises:
            ValueError: If source is not one of the supported types.
                        Previously this silently no-op'd on unknown source,
                        causing identifiers to vanish from dedup tracking.
        """
        if source == "arxiv":
            self.processed_arxiv_ids.add(identifier)
        elif source == "doi":
            self.processed_dois.add(identifier)
        elif source == "web":
            self.processed_urls.add(identifier)
        elif source == "local":
            self.processed_local_paths.add(identifier)
        else:
            raise ValueError(
                f"Unknown source: {source!r}. "
                f"Expected one of 'arxiv', 'doi', 'web', 'local'."
            )

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