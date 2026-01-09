"""
Paper processing orchestrator.

This module coordinates the entire pipeline:
1. Fetch paper (from arXiv or local file)
2. Process with GROBID (extract metadata)
3. Generate synthesis with Claude
4. Write Obsidian note
5. Update processing state

Python concepts:
- Coordination/orchestration patterns
- Error handling and recovery
- State management
- File path manipulation
"""

from pathlib import Path
from typing import Optional, Union
import pdfplumber

from paper_library.config import config
from paper_library.state import StateManager
from paper_library.models import PaperMetadata
from paper_library.arxiv_fetcher import ArxivFetcher
from paper_library.grobid_processor import GrobidProcessor
from paper_library.synthesis_generator import SynthesisGenerator
from paper_library.markdown_writer import MarkdownWriter


class ProcessingError(Exception):
    """Raised when paper processing fails."""
    pass


class PaperProcessor:
    """
    Orchestrate the paper processing pipeline.
    
    This is the main class that ties all the components together.
    
    Usage:
        state = StateManager.load()
        processor = PaperProcessor(config, state)
        
        # Process single paper
        processor.process("2312.12345")
        
        # Process batch
        results = processor.process_batch(["2312.12345", "1706.03762"])
    """
    
    def __init__(self, config, state_manager: StateManager):
        """
        Initialize the processor.
        
        Args:
            config: Configuration object
            state_manager: State manager for tracking processed papers
        """
        self.config = config
        self.state = state_manager
        
        # Initialize components
        self.arxiv_fetcher = ArxivFetcher(config.vault_path)
        self.grobid = GrobidProcessor(config.grobid_url)
        self.synthesis_gen = SynthesisGenerator(config.anthropic_api_key)
        self.markdown_writer = MarkdownWriter()
    
    def process(self, identifier: str, force: bool = False) -> bool:
        """
        Process a single paper from any source.
        
        Supports:
        - arXiv ID: "2312.12345" or "https://arxiv.org/abs/2312.12345"
        - Local PDF: "/path/to/paper.pdf"
        - (Future) DOI: "10.1162/coli_a_00123"
        - (Future) URL: "https://example.com/article"
        
        Args:
            identifier: Paper identifier (arXiv ID or file path)
            force: If True, reprocess even if already done
            
        Returns:
            True if successful, False if skipped (already processed)
            
        Raises:
            ProcessingError: If processing fails
        """
        print(f"\n{'='*70}")
        print(f"Processing: {identifier}")
        print(f"{'='*70}\n")
        
        # Check if already processed (unless force=True)
        if not force and self.state.is_processed(identifier):
            print(f"⊘ Already processed: {identifier}")
            print(f"  Use force=True to reprocess\n")
            return False
        
        try:
            # Step 1: Determine source type and fetch
            print("Step 1: Fetching paper...")
            pdf_path, metadata = self._fetch_paper(identifier)
            print(f"  ✓ Fetched: {metadata.title}")
            
            # Step 2: Process with GROBID
            print("\nStep 2: Extracting metadata with GROBID...")
            grobid_metadata = self.grobid.process(pdf_path)
            
            # Merge GROBID results with fetched metadata
            # GROBID is more detailed, so we prefer its data when available
            metadata = self._merge_metadata(metadata, grobid_metadata)
            print(f"  ✓ Extracted {len(metadata.citations)} citations")
            
            # Step 3: Extract text for synthesis
            print("\nStep 3: Extracting text from PDF...")
            text = self._extract_text(pdf_path)
            print(f"  ✓ Extracted {len(text)} characters")
            
            # Step 4: Generate synthesis with Claude
            print("\nStep 4: Generating AI synthesis...")
            synthesis = self.synthesis_gen.generate_quick_synthesis(text, metadata)
            print(f"  ✓ Generated synthesis (cost: ${synthesis.cost_usd:.4f})")
            
            # Step 5: Write Obsidian note
            print("\nStep 5: Writing Obsidian note...")
            markdown = self.markdown_writer.paper_to_markdown(metadata, synthesis)
            filename = self.markdown_writer.generate_filename(metadata)
            
            # Write to appropriate directory
            output_dir = self.config.papers_dir
            output_dir.mkdir(parents=True, exist_ok=True)
            
            output_path = output_dir / f"{filename}.md"
            output_path.write_text(markdown, encoding='utf-8')
            print(f"  ✓ Written to: {output_path.relative_to(self.config.vault_path)}")
            
            # Step 6: Update state
            print("\nStep 6: Updating state...")
            source = self._get_source_type(identifier)
            self.state.mark_processed(identifier, source)
            print(f"  ✓ Marked as processed")
            
            print(f"\n{'='*70}")
            print(f"✓ SUCCESS: {identifier}")
            print(f"{'='*70}\n")
            
            return True
            
        except Exception as e:
            # Mark as failed in state
            self.state.mark_failed(identifier, str(e))
            
            print(f"\n{'='*70}")
            print(f"✗ FAILED: {identifier}")
            print(f"  Error: {e}")
            print(f"{'='*70}\n")
            
            # Re-raise as ProcessingError
            raise ProcessingError(f"Failed to process {identifier}: {e}") from e
    
    def process_batch(self, identifiers: list[str], stop_on_error: bool = False, force: bool = False) -> dict:
        """
        Process multiple papers.
        
        Args:
            identifiers: List of paper identifiers
            stop_on_error: If True, stop on first error. Otherwise continue.
            force: If True, reprocess even if already done
            
        Returns:
            Dictionary with results: {"success": int, "failed": int, "skipped": int}
        """
        results = {
            "success": 0,
            "failed": 0,
            "skipped": 0,
            "errors": []
        }
        
        print(f"\n{'='*70}")
        print(f"BATCH PROCESSING: {len(identifiers)} papers")
        if force:
            print(f"  --force enabled: Reprocessing all papers")
        print(f"{'='*70}\n")
        
        for i, identifier in enumerate(identifiers, 1):
            print(f"[{i}/{len(identifiers)}] Processing: {identifier}")
            
            try:
                success = self.process(identifier, force=force)
                if success:
                    results["success"] += 1
                else:
                    results["skipped"] += 1
                    
            except Exception as e:
                results["failed"] += 1
                results["errors"].append((identifier, str(e)))
                
                if stop_on_error:
                    print(f"\n✗ Stopping batch due to error")
                    break
        
        # Print summary
        print(f"\n{'='*70}")
        print(f"BATCH COMPLETE")
        print(f"{'='*70}")
        print(f"  ✓ Processed: {results['success']}")
        print(f"  ⊘ Skipped:   {results['skipped']}")
        print(f"  ✗ Failed:    {results['failed']}")
        
        if results["errors"]:
            print(f"\nErrors:")
            for identifier, error in results["errors"]:
                print(f"  • {identifier}: {error}")
        
        print(f"{'='*70}\n")
        
        return results
    
    def _fetch_paper(self, identifier: str) -> tuple[Path, PaperMetadata]:
        """
        Fetch paper based on identifier type.
        
        Detects:
        - arXiv ID (digits with dots)
        - Local file path (exists on disk)
        - Future: DOI, URL
        
        Args:
            identifier: Paper identifier
            
        Returns:
            Tuple of (pdf_path, metadata)
        """
        # Check if it's an arXiv ID
        if self.arxiv_fetcher.parse_arxiv_id(identifier):
            return self.arxiv_fetcher.fetch(identifier)
        
        # Check if it's a local file
        path = Path(identifier)
        if path.exists() and path.suffix.lower() == '.pdf':
            # For local PDFs, we have no metadata yet
            # Create minimal metadata that GROBID will fill in
            metadata = PaperMetadata(
                title="Unknown",
                authors=["Unknown"],
                year=2023,
                pdf_path=str(path),
                source="local"
            )
            return path, metadata
        
        # Future: Add DOI and URL support here
        
        raise ProcessingError(
            f"Could not determine source type for: {identifier}\n"
            f"  Supported: arXiv ID (e.g., '2312.12345'), local PDF path"
        )
    
    def _merge_metadata(
        self,
        base: PaperMetadata,
        grobid: PaperMetadata
    ) -> PaperMetadata:
        """
        Merge metadata from different sources.
        
        GROBID provides the most detail, so we prefer it when available.
        But we keep arXiv ID and other source-specific fields from base.
        
        Args:
            base: Metadata from fetcher (arXiv API, etc.)
            grobid: Metadata from GROBID
            
        Returns:
            Merged metadata
        """
        # Start with GROBID data (most complete)
        merged = PaperMetadata(
            title=grobid.title or base.title,
            authors=grobid.authors or base.authors,
            year=grobid.year or base.year,
            abstract=grobid.abstract or base.abstract,
            venue=grobid.venue or getattr(base, 'venue', None),
            volume=grobid.volume,
            issue=grobid.issue,
            pages=grobid.pages,
            doi=grobid.doi or base.doi,
            citations=grobid.citations,
            pdf_path=base.pdf_path,
            source=base.source
        )
        
        # Keep arXiv ID from base (GROBID doesn't extract this)
        if hasattr(base, 'arxiv_id') and base.arxiv_id:
            merged.arxiv_id = base.arxiv_id
        
        return merged
    
    def _extract_text(self, pdf_path: Path) -> str:
        """
        Extract text from PDF for synthesis.
        
        Uses pdfplumber for reliable text extraction.
        
        Args:
            pdf_path: Path to PDF
            
        Returns:
            Extracted text
        """
        try:
            text_parts = []
            
            with pdfplumber.open(pdf_path) as pdf:
                # Extract text from each page
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
            
            # Join pages with double newline
            full_text = "\n\n".join(text_parts)
            
            return full_text
            
        except Exception as e:
            raise ProcessingError(f"Failed to extract text from PDF: {e}")
    
    def _get_source_type(self, identifier: str) -> str:
        """
        Determine source type from identifier.
        
        Args:
            identifier: Paper identifier
            
        Returns:
            Source type: "arxiv", "local", "doi", "web"
        """
        if self.arxiv_fetcher.parse_arxiv_id(identifier):
            return "arxiv"
        
        path = Path(identifier)
        if path.exists():
            return "local"
        
        # Future: check for DOI, URL patterns
        
        return "unknown"


def process_paper(identifier: str, force: bool = False) -> bool:
    """
    Convenience function to process a single paper.
    
    Args:
        identifier: Paper identifier (arXiv ID or path)
        force: Reprocess even if already done
        
    Returns:
        True if successful
    """
    state = StateManager.load()
    processor = PaperProcessor(config, state)
    return processor.process(identifier, force=force)