"""
Paper processing orchestrator.

This module coordinates the entire pipeline:
1. Fetch paper/article (from arXiv, web, local file, etc.)
2. For PDFs: Process with GROBID (extract metadata)
3. For articles: Use extracted content directly
4. Generate synthesis with Claude
5. Write Obsidian note
6. Update processing state

The pipeline branches based on source type:
- PDFs (arXiv, local, PDF-from-URL): GROBID → synthesis → paper note
- Web articles (HTML): synthesis → article note

Python concepts:
- Coordination/orchestration patterns
- Error handling and recovery
- State management
- File path manipulation
"""

from pathlib import Path
from typing import Any, Optional, Union
import pdfplumber

from paper_library.config import config
from paper_library.state import StateManager
from paper_library.models import PaperMetadata, ArticleMetadata
from paper_library.arxiv_fetcher import ArxivFetcher
from paper_library.citation_context import CitationContextExtractor
from paper_library.web_fetcher import WebFetcher, WebFetchError, UnsupportedSourceError
from paper_library.grobid_processor import GrobidProcessor
from paper_library.synthesis_generator import SynthesisGenerator
from paper_library.markdown_writer import MarkdownWriter


class ProcessingError(Exception):
    """Raised when paper processing fails."""
    pass


class PaperProcessor:
    """
    Orchestrate the paper/article processing pipeline.

    Handles both PDFs (via GROBID) and web articles (direct synthesis).

    Usage:
        state = StateManager.load()
        processor = PaperProcessor(config, state)

        # Process single item — any source type
        processor.process("2312.12345")                              # arXiv
        processor.process("https://transformer-circuits.pub/...")   # Web article
        processor.process("./local_paper.pdf")                      # Local PDF

        # Batch with mixed sources
        results = processor.process_batch([
            "2312.12345",
            "https://transformer-circuits.pub/2022/mech-interp-essay/",
            "./papers/local.pdf"
        ])
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
        self.web_fetcher = WebFetcher(config.vault_path)
        self.grobid = GrobidProcessor(config.grobid_url)
        self.synthesis_gen = SynthesisGenerator(config.anthropic_api_key)
        self.markdown_writer = MarkdownWriter()

    def process(self, identifier: str, force: bool = False) -> bool:
        """
        Process a single paper or article from any source.

        Supports:
        - arXiv ID: "2312.12345" or "https://arxiv.org/abs/2312.12345"
        - Web URL: "https://transformer-circuits.pub/..." (HTML or PDF)
        - Local PDF: "/path/to/paper.pdf"
        - (Future) DOI: "10.1162/coli_a_00123"

        Args:
            identifier: Paper/article identifier
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
            print("Step 1: Fetching content...")
            fetch_result = self._fetch_paper(identifier)

            if fetch_result["type"] == "paper":
                return self._process_paper(
                    fetch_result["pdf_path"],
                    fetch_result["metadata"],
                    identifier,
                )
            elif fetch_result["type"] == "article":
                return self._process_article(
                    fetch_result["metadata"],
                    fetch_result["content"],
                    identifier,
                )
            else:
                raise ProcessingError(f"Unknown result type: {fetch_result['type']}")

        except UnsupportedSourceError as e:
            print(f"\n{'='*70}")
            print(f"✗ UNSUPPORTED SOURCE: {identifier}")
            print(f"{'='*70}")
            print(f"{e}\n")
            self.state.mark_failed(identifier, f"Unsupported source: {e}")
            raise ProcessingError(str(e)) from e

        except Exception as e:
            self.state.mark_failed(identifier, str(e))
            print(f"\n{'='*70}")
            print(f"✗ FAILED: {identifier}")
            print(f"  Error: {e}")
            print(f"{'='*70}\n")
            raise ProcessingError(f"Failed to process {identifier}: {e}") from e

    def process_batch(
        self,
        identifiers: list[str],
        stop_on_error: bool = False,
        force: bool = False,
    ) -> dict:
        """
        Process multiple papers/articles.

        Args:
            identifiers: List of identifiers (arXiv IDs, URLs, local paths — mixed OK)
            stop_on_error: If True, stop on first error. Otherwise continue.
            force: If True, reprocess even if already done

        Returns:
            {"success": int, "failed": int, "skipped": int, "errors": list}
        """
        results = {"success": 0, "failed": 0, "skipped": 0, "errors": []}

        print(f"\n{'='*70}")
        print(f"BATCH PROCESSING: {len(identifiers)} items")
        if force:
            print(f"  --force enabled: Reprocessing all items")
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

        print(f"\n{'='*70}")
        print(f"BATCH COMPLETE")
        print(f"{'='*70}")
        print(f"  ✓ Processed: {results['success']}")
        print(f"  ⊘ Skipped:   {results['skipped']}")
        print(f"  ✗ Failed:    {results['failed']}")

        if results["errors"]:
            print(f"\nErrors:")
            for ident, err in results["errors"]:
                truncated = err[:100] + "..." if len(err) > 100 else err
                print(f"  • {ident}: {truncated}")

        print(f"{'='*70}\n")
        return results

    # -------------------------------------------------------------------------
    # Fetch: detect source type and return a typed dict
    # -------------------------------------------------------------------------

    def _fetch_paper(self, identifier: str) -> dict[str, Any]:
        """
        Fetch content based on identifier type.

        Returns a dict with:
          {"type": "paper", "pdf_path": Path, "metadata": PaperMetadata}
          {"type": "article", "metadata": ArticleMetadata, "content": str}

        Raises:
            ProcessingError: If source type cannot be determined
            UnsupportedSourceError: For blocked content types (Twitter, etc.)
            WebFetchError: If web fetching fails
        """
        # arXiv ID (e.g. "1706.03762" or "https://arxiv.org/abs/1706.03762")
        if self.arxiv_fetcher.parse_arxiv_id(identifier):
            print("  → arXiv paper detected")
            pdf_path, metadata = self.arxiv_fetcher.fetch(identifier)
            print(f"  ✓ Fetched: {metadata.title}")
            return {"type": "paper", "pdf_path": pdf_path, "metadata": metadata}

        # Local PDF file
        path = Path(identifier)
        if path.exists() and path.suffix.lower() == ".pdf":
            print("  → Local PDF detected")
            metadata = PaperMetadata(
                title="[Title will be extracted from PDF]",
                authors=["Unknown"],
                year=2024,
                pdf_path=str(path),
                source="local",
            )
            return {"type": "paper", "pdf_path": path, "metadata": metadata}

        # Web URL (http/https/www)
        if self.web_fetcher.is_url(identifier):
            print("  → Web URL detected")
            try:
                metadata, content = self.web_fetcher.fetch(identifier)

                if not content or getattr(metadata, "source", "") == "pdf_from_web":
                    # PDF at a URL — saved to vault/PDFs/ by web_fetcher
                    print("  → PDF from URL, routing through GROBID")
                    # pdf_path: web_fetcher saves it to vault/PDFs/ but doesn't
                    # return the path yet (known limitation). For now, treat as
                    # an article so synthesis can run on whatever content we have.
                    # TODO: return saved path from _handle_pdf_from_url
                    return {"type": "article", "metadata": metadata, "content": content}
                else:
                    print(f"  ✓ Extracted {len(content)} chars of web content")
                    return {"type": "article", "metadata": metadata, "content": content}

            except UnsupportedSourceError:
                raise  # Let process() print the friendly message
            except WebFetchError as e:
                raise ProcessingError(f"Failed to fetch URL: {e}") from e

        raise ProcessingError(
            f"Could not determine source type for: {identifier}\n"
            f"  Supported: arXiv ID (e.g. '1706.03762'), "
            f"web URL (e.g. 'https://transformer-circuits.pub/...'), "
            f"or local PDF path (e.g. './paper.pdf')"
        )

    # -------------------------------------------------------------------------
    # Two processing pipelines
    # -------------------------------------------------------------------------

    def _process_paper(
        self,
        pdf_path: Path,
        metadata: PaperMetadata,
        identifier: str,
    ) -> bool:
        """
        Full PDF pipeline: GROBID → text → citation contexts → synthesis → vault.
        """
        # Step 2: GROBID metadata extraction
        print("\nStep 2: Extracting metadata with GROBID...")
        grobid_metadata = self.grobid.process(pdf_path)
        metadata = self._merge_metadata(metadata, grobid_metadata)
        print(f"  ✓ Extracted {len(metadata.citations)} citations")

        # Step 3: Text extraction (pdfplumber)
        print("\nStep 3: Extracting text from PDF...")
        text = self._extract_text(pdf_path)
        print(f"  ✓ Extracted {len(text)} characters")
        if len(text) < 1000:
            print(
                f"  ⚠ Warning: very short text ({len(text)} chars) — "
                f"PDF may be scanned/image-only. "
                f"Synthesis will rely on model's prior knowledge rather than paper content."
            )

        # Step 3.5: Citation context extraction
        print("\nStep 3.5: Extracting citation contexts...")
        ctx_extractor = CitationContextExtractor()
        context_map = ctx_extractor.extract_contexts(text, metadata.citations)
        for citation in metadata.citations:
            key = (
                citation.doi
                or citation.title
                or (citation.raw_text[:50] if citation.raw_text else None)
            )
            if key and key in context_map:
                citation.contexts = [c.context_text for c in context_map[key]]
        n_ctx = sum(1 for c in metadata.citations if c.contexts)
        print(f"  ✓ Found contexts for {n_ctx}/{len(metadata.citations)} citations")
        formatted_contexts = ctx_extractor.format_contexts_for_synthesis(context_map)

        # Step 4: AI synthesis
        print("\nStep 4: Generating AI synthesis...")
        synthesis = self.synthesis_gen.generate_quick_synthesis(
            text, metadata, citation_contexts=formatted_contexts
        )
        print(f"  ✓ Generated synthesis (cost: ${synthesis.cost_usd:.4f})")

        # Step 5: Write vault note
        print("\nStep 5: Writing Obsidian note...")
        markdown = self.markdown_writer.paper_to_markdown(metadata, synthesis)
        filename = self.markdown_writer.generate_filename(metadata)
        output_dir = self.config.papers_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{filename}.md"
        output_path.write_text(markdown, encoding="utf-8")
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

    def _process_article(
        self,
        metadata: ArticleMetadata,
        content: str,
        identifier: str,
    ) -> bool:
        """
        Article pipeline: synthesis → vault (no GROBID, no citation contexts).
        """
        # Step 2: AI synthesis
        print("\nStep 2: Generating AI synthesis...")
        synthesis = self.synthesis_gen.generate_quick_synthesis(content, metadata)
        print(f"  ✓ Generated synthesis (cost: ${synthesis.cost_usd:.4f})")

        # Step 3: Write vault note
        print("\nStep 3: Writing Obsidian note...")
        markdown = self.markdown_writer.article_to_markdown(metadata, synthesis, content)
        filename = self.markdown_writer.generate_filename(metadata)
        output_dir = self.config.articles_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{filename}.md"
        output_path.write_text(markdown, encoding="utf-8")
        print(f"  ✓ Written to: {output_path.relative_to(self.config.vault_path)}")

        # Step 4: Update state
        print("\nStep 4: Updating state...")
        self.state.mark_processed(identifier, "web")
        print(f"  ✓ Marked as processed")

        print(f"\n{'='*70}")
        print(f"✓ SUCCESS: {identifier}")
        print(f"{'='*70}\n")
        return True

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    def _merge_metadata(
        self,
        base: PaperMetadata,
        grobid: PaperMetadata,
    ) -> PaperMetadata:
        """
        Merge metadata from fetcher and GROBID.

        GROBID is more detailed, so we prefer it when available.
        Source-specific fields (arXiv ID, pdf_path) are preserved from base.
        """
        merged = PaperMetadata(
            title=grobid.title or base.title,
            authors=grobid.authors or base.authors,
            year=grobid.year or base.year,
            abstract=grobid.abstract or base.abstract,
            venue=grobid.venue or getattr(base, "venue", None),
            volume=grobid.volume,
            issue=grobid.issue,
            pages=grobid.pages,
            doi=grobid.doi or base.doi,
            citations=grobid.citations,
            pdf_path=base.pdf_path,
            source=base.source,
        )
        # Keep arXiv ID from base (GROBID doesn't extract this)
        if hasattr(base, "arxiv_id") and base.arxiv_id:
            merged.arxiv_id = base.arxiv_id
        return merged

    def _extract_text(self, pdf_path: Path) -> str:
        """Extract text from PDF using pdfplumber."""
        try:
            text_parts = []
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
            return "\n\n".join(text_parts)
        except Exception as e:
            raise ProcessingError(f"Failed to extract text from PDF: {e}")

    def _get_source_type(self, identifier: str) -> str:
        """Return source type string for state tracking."""
        if self.arxiv_fetcher.parse_arxiv_id(identifier):
            return "arxiv"
        path = Path(identifier)
        if path.exists():
            return "local"
        if self.web_fetcher.is_url(identifier):
            return "web"
        return "unknown"


def process_paper(identifier: str, force: bool = False) -> bool:
    """
    Convenience function to process a single paper or article.

    Args:
        identifier: arXiv ID, URL, or local PDF path
        force: Reprocess even if already done

    Returns:
        True if successful
    """
    state = StateManager.load()
    processor = PaperProcessor(config, state)
    return processor.process(identifier, force=force)
