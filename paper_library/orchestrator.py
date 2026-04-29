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
from typing import Any

from opentelemetry.trace import StatusCode

from paper_library.telemetry import tracer, get_logger
from paper_library import __version__
from paper_library.config import config
from paper_library.state import StateManager
from paper_library.models import PaperMetadata, ArticleMetadata
from paper_library.arxiv_fetcher import ArxivFetcher
from paper_library.citation_context import CitationContextExtractor
from paper_library.doi_fetcher import DoiFetcher, DoiFetchError
from paper_library.web_fetcher import WebFetcher, WebFetchError, UnsupportedSourceError
from paper_library.grobid_processor import GrobidProcessor
from paper_library.synthesis_generator import SynthesisGenerator
from paper_library.markdown_writer import MarkdownWriter

logger = get_logger(__name__)


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
        self.doi_fetcher = DoiFetcher(config.vault_path, email=getattr(config, "crossref_email", None))
        self.web_fetcher = WebFetcher(config.vault_path)
        self.grobid = GrobidProcessor(config.grobid_url)
        self.synthesis_gen = SynthesisGenerator(config.anthropic_api_key)
        self.markdown_writer = MarkdownWriter()

        # Source notes directory (raw PDF text / web article content)
        self.sources_dir = config.vault_path / "Sources"
        self.sources_dir.mkdir(parents=True, exist_ok=True)

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
        with tracer.start_as_current_span(
            "process_paper",
            attributes={
                "paper.identifier": identifier,
                "paper.force_reprocess": force,
                "alcanzai.version": __version__,
            },
        ) as span:
            # Check if already processed (unless force=True)
            if not force and self.state.is_processed(identifier):
                logger.info("skipped_already_processed", identifier=identifier)
                return False

            try:
                # Step 1: Determine source type and fetch
                logger.info("fetch_started", identifier=identifier)
                fetch_result = self._fetch_paper(identifier)

                if fetch_result["type"] == "paper":
                    result = self._process_paper(
                        fetch_result["pdf_path"],
                        fetch_result["metadata"],
                        identifier,
                    )
                elif fetch_result["type"] == "article":
                    result = self._process_article(
                        fetch_result["metadata"],
                        fetch_result["content"],
                        identifier,
                    )
                elif fetch_result["type"] == "doi_only":
                    result = self._process_doi_only(fetch_result["metadata"], identifier)
                else:
                    raise ProcessingError(f"Unknown result type: {fetch_result['type']}")

                span.set_status(StatusCode.OK)
                return result

            except UnsupportedSourceError as e:
                logger.error("unsupported_source", identifier=identifier, error=str(e))
                self.state.mark_failed(identifier, f"Unsupported source: {e}")
                span.set_status(StatusCode.ERROR, str(e))
                span.record_exception(e)
                raise ProcessingError(str(e)) from e

            except Exception as e:
                self.state.mark_failed(identifier, str(e))
                logger.error("processing_failed", identifier=identifier, error=str(e))
                span.set_status(StatusCode.ERROR, str(e))
                span.record_exception(e)
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

        with tracer.start_as_current_span(
            "process_batch",
            attributes={
                "batch.size": len(identifiers),
                "batch.force": force,
            },
        ) as span:
            for i, identifier in enumerate(identifiers, 1):
                logger.info("processing_started", identifier=identifier, index=i, total=len(identifiers))

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
                        logger.error("batch_stopped_on_error", identifier=identifier, error=str(e))
                        break

            span.set_attribute("batch.succeeded", results["success"])
            span.set_attribute("batch.failed", results["failed"])
            span.set_attribute("batch.skipped", results["skipped"])

        return results

    # -------------------------------------------------------------------------
    # Fetch: detect source type and return a typed dict
    # -------------------------------------------------------------------------

    def _fetch_paper(self, identifier: str) -> dict[str, Any]:
        """
        Fetch content based on identifier type.

        Returns a dict with:
          {"type": "paper",    "pdf_path": Path, "metadata": PaperMetadata}
          {"type": "article",  "metadata": ArticleMetadata, "content": str}
          {"type": "doi_only", "metadata": PaperMetadata}  # Crossref metadata, no PDF

        Raises:
            ProcessingError: If source type cannot be determined
            UnsupportedSourceError: For blocked content types (Twitter, etc.)
            WebFetchError: If web fetching fails
        """
        # arXiv ID (e.g. "1706.03762" or "https://arxiv.org/abs/1706.03762")
        if self.arxiv_fetcher.parse_arxiv_id(identifier):
            pdf_path, metadata = self.arxiv_fetcher.fetch(identifier)
            logger.info("fetch_complete", source="arxiv", identifier=identifier, title=metadata.title)
            return {"type": "paper", "pdf_path": pdf_path, "metadata": metadata}

        # DOI (e.g. "10.1093/mind/fzae004" or "https://doi.org/10.1093/mind/fzae004")
        doi = self.doi_fetcher.parse_doi(identifier)
        if doi:
            try:
                metadata, pdf_path = self.doi_fetcher.fetch(doi)
                logger.info("fetch_complete", source="doi", identifier=identifier, title=metadata.title)
            except DoiFetchError as e:
                raise ProcessingError(f"DOI lookup failed: {e}") from e
            if pdf_path:
                return {"type": "paper", "pdf_path": pdf_path, "metadata": metadata}
            else:
                return {"type": "doi_only", "metadata": metadata}

        # Local PDF file
        path = Path(identifier)
        if path.exists() and path.suffix.lower() == ".pdf":
            metadata = PaperMetadata(
                title="[Title will be extracted from PDF]",
                authors=["Unknown"],
                year=None,  # Populated by GROBID via _merge_metadata
                pdf_path=str(path),
                source="local",
            )
            logger.info("fetch_complete", source="local", identifier=identifier)
            return {"type": "paper", "pdf_path": path, "metadata": metadata}

        # Web URL (http/https/www)
        if self.web_fetcher.is_url(identifier):
            try:
                metadata, content = self.web_fetcher.fetch(identifier)

                if getattr(metadata, "source", "") == "pdf_from_web":
                    # PDF downloaded from a URL — route through the full paper
                    # pipeline (GROBID → text → citation contexts → synthesis).
                    if not metadata.pdf_path:
                        raise ProcessingError(
                            f"PDF was detected at {identifier} but could not be saved "
                            f"(vault_path not set). Configure VAULT_PATH and retry."
                        )
                    logger.info("fetch_complete", source="pdf_from_web", identifier=identifier)
                    paper_meta = PaperMetadata(
                        title="[Extracting from PDF]",
                        authors=["Unknown"],
                        year=None,  # Populated by GROBID via _merge_metadata
                        pdf_path=metadata.pdf_path,
                        source="pdf_from_web",
                    )
                    return {
                        "type": "paper",
                        "pdf_path": Path(metadata.pdf_path),
                        "metadata": paper_meta,
                    }
                else:
                    logger.info("fetch_complete", source="web", identifier=identifier, content_len=len(content))
                    return {"type": "article", "metadata": metadata, "content": content}

            except UnsupportedSourceError:
                raise  # Let process() handle it
            except WebFetchError as e:
                raise ProcessingError(f"Failed to fetch URL: {e}") from e

        raise ProcessingError(
            f"Could not determine source type for: {identifier}\n"
            f"  Supported: arXiv ID (e.g. '1706.03762'), "
            f"DOI (e.g. '10.1093/mind/fzae004' or 'https://doi.org/...'), "
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
        logger.info("metadata_extraction_started", identifier=identifier)
        grobid_metadata = self.grobid.process(pdf_path)
        metadata = self._merge_metadata(metadata, grobid_metadata)
        logger.info("metadata_extraction_complete", identifier=identifier, n_citations=len(metadata.citations))

        # Step 3: Text extraction
        # Prefer GROBID body text: it correctly handles 2-column layout and
        # preserves [N] citation markers.
        text = grobid_metadata.body_text or ""
        if len(text) < 1000:
            logger.warning(
                "grobid_body_text_short",
                body_text_chars=len(text),
                identifier=identifier,
                hint="PDF may be scanned/image-only — OCRmyPDF preprocessing needed (v0.3.0)",
            )

        # Step 3.5: Citation context extraction
        logger.info("citation_context_extraction_started", identifier=identifier)
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
        logger.info("citation_context_extraction_complete", identifier=identifier, n_found=n_ctx, n_total=len(metadata.citations))
        formatted_contexts = ctx_extractor.format_contexts_for_synthesis(context_map)

        # Step 4: AI synthesis
        logger.info("synthesis_started", identifier=identifier)
        synthesis = self.synthesis_gen.generate_quick_synthesis(
            text, metadata, citation_contexts=formatted_contexts
        )
        logger.info("synthesis_complete", identifier=identifier, cost_usd=synthesis.cost_usd)

        # Step 5: Write vault note
        logger.info("writing_note", identifier=identifier)
        filename = self.markdown_writer.generate_filename(metadata)
        markdown = self.markdown_writer.paper_to_markdown(metadata, synthesis)
        output_dir = self.config.papers_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{filename}.md"
        output_path.write_text(markdown, encoding="utf-8")

        # Record output path on the active span (no-op when telemetry is off)
        from opentelemetry import trace
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("paper.output_path", str(output_path))

        # Step 6: Update state
        source = self._get_source_type(identifier)
        self.state.mark_processed(identifier, source)

        logger.info("processing_complete", identifier=identifier, cost_usd=synthesis.cost_usd)
        return True

    def _process_doi_only(self, metadata: PaperMetadata, identifier: str) -> bool:
        """
        DOI pipeline when no OA PDF is available.

        Uses the Crossref abstract as synthesis text. Writes a paper note
        to vault/Papers/ with a notice that synthesis is abstract-only.
        """
        text = metadata.abstract or ""
        if not text:
            text = f"No abstract available for {metadata.doi or identifier}."

        # Step 2: AI synthesis (on abstract text)
        logger.info("synthesis_started", identifier=identifier, abstract_only=True)
        synthesis = self.synthesis_gen.generate_quick_synthesis(text, metadata)
        logger.info("synthesis_complete", identifier=identifier, cost_usd=synthesis.cost_usd)

        # Step 3: Write vault note
        logger.info("writing_note", identifier=identifier)
        markdown = self.markdown_writer.paper_to_markdown(metadata, synthesis)
        filename = self.markdown_writer.generate_filename(metadata)
        output_dir = self.config.papers_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{filename}.md"
        output_path.write_text(markdown, encoding="utf-8")

        # Record output path on the active span (no-op when telemetry is off)
        from opentelemetry import trace
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("paper.output_path", str(output_path))

        # Step 4: Update state
        self.state.mark_processed(identifier, "doi")
        logger.info("processing_complete", identifier=identifier, cost_usd=synthesis.cost_usd)
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
        logger.info("synthesis_started", identifier=identifier)
        synthesis = self.synthesis_gen.generate_quick_synthesis(content, metadata)
        logger.info("synthesis_complete", identifier=identifier, cost_usd=synthesis.cost_usd)

        # Step 3: Write vault note + source note
        logger.info("writing_note", identifier=identifier)
        filename = self.markdown_writer.generate_filename(metadata)

        # Write source note (raw web content) to vault/Sources/
        source_note_name = filename + " - Source"
        source_md = self.markdown_writer.source_note_markdown(
            metadata.title, content, "web_content"
        )
        (self.sources_dir / f"{source_note_name}.md").write_text(source_md, encoding="utf-8")

        markdown = self.markdown_writer.article_to_markdown(metadata, synthesis, source_note_name=source_note_name)
        output_dir = self.config.articles_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{filename}.md"
        output_path.write_text(markdown, encoding="utf-8")

        # Record output path on the active span (no-op when telemetry is off)
        from opentelemetry import trace
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("paper.output_path", str(output_path))

        # Step 4: Update state
        self.state.mark_processed(identifier, "web")
        logger.info("processing_complete", identifier=identifier, cost_usd=synthesis.cost_usd)
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
