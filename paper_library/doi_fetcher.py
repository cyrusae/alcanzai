"""
DOI-based paper fetcher.

Resolution chain for a given DOI:
1. Crossref REST API  → bibliographic metadata (title, authors, year, abstract, etc.)
2. Unpaywall API      → best OA PDF URL (primary)
3. Semantic Scholar   → OA PDF URL (fallback)
4. Download PDF if found → caller routes to GROBID pipeline
5. If no PDF found   → caller uses abstract as synthesis text

DOI formats handled:
  "10.1093/mind/fzae004"                     bare DOI
  "https://doi.org/10.1093/mind/fzae004"     doi.org URL
  "https://dx.doi.org/10.1093/mind/fzae004"  dx.doi.org URL
  "doi:10.1093/mind/fzae004"                 doi: prefix
"""

import re
import requests
from pathlib import Path
from typing import Optional, Tuple, List
from datetime import datetime
from opentelemetry.trace import SpanKind, StatusCode
from paper_library.telemetry import tracer, get_logger
from paper_library.models import PaperMetadata

logger = get_logger(__name__)


class DoiFetchError(Exception):
    """Raised when DOI metadata lookup fails (Crossref unavailable, DOI not found, etc.)."""
    pass


class DoiFetcher:
    """
    Fetch paper metadata and open-access PDF via DOI.

    Uses Crossref for bibliographic metadata, then Unpaywall → Semantic Scholar
    for OA PDF discovery.

    Usage:
        fetcher = DoiFetcher(vault_path=config.vault_path, email="you@example.com")
        metadata, pdf_path = fetcher.fetch("10.1093/mind/fzae004")
        # pdf_path is None if no OA PDF was found
    """

    CROSSREF_BASE = "https://api.crossref.org/works"
    UNPAYWALL_BASE = "https://api.unpaywall.org/v2"
    SEMANTIC_SCHOLAR_BASE = "https://api.semanticscholar.org/graph/v1/paper"

    HEADERS = {
        "User-Agent": "alcanzai/1.0 (personal research library; https://github.com/alcanzai)"
    }

    # DOI pattern: 10.XXXX/suffix
    # Registrant code is 4-9 digits; suffix is anything except whitespace and quote chars.
    DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\"'<>]+", re.IGNORECASE)

    def __init__(self, vault_path: Optional[Path] = None, email: Optional[str] = None):
        """
        Args:
            vault_path: Vault root; PDFs are saved to vault_path/PDFs/
            email:      Contact email for Crossref and Unpaywall polite pools.
                        Optional but recommended — omitting uses the anonymous pool.
        """
        self.vault_path = vault_path
        self.email = email
        if vault_path:
            self.pdfs_dir = vault_path / "PDFs"
            self.pdfs_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def parse_doi(self, text: str) -> Optional[str]:
        """
        Extract and normalize a DOI from various input formats.

        Returns the bare DOI string (e.g. "10.1093/mind/fzae004") or None.
        """
        text = text.strip()

        # Strip known URL/prefix wrappers
        for prefix in (
            "https://doi.org/",
            "http://doi.org/",
            "https://dx.doi.org/",
            "http://dx.doi.org/",
            "doi:",
        ):
            if text.lower().startswith(prefix):
                text = text[len(prefix):]
                break

        # Match at start of (possibly stripped) text
        match = self.DOI_RE.match(text)
        if match:
            return match.group(0).rstrip(".,;)")

        # Fall back to finding DOI anywhere (handles URLs like publisher landing pages
        # that embed the DOI in the path, e.g. .../article/10.1093/mind/fzae004)
        match = self.DOI_RE.search(text)
        if match:
            return match.group(0).rstrip(".,;)")

        return None

    def fetch(self, doi: str) -> Tuple[PaperMetadata, Optional[Path]]:
        """
        Fetch bibliographic metadata and try to locate an OA PDF.

        Args:
            doi: Bare DOI string (already parsed by parse_doi)

        Returns:
            (PaperMetadata, pdf_path)  — pdf_path is None if no OA copy was found.

        Raises:
            DoiFetchError: If Crossref lookup fails entirely.
        """
        with tracer.start_as_current_span(
            'fetch_doi',
            kind=SpanKind.CLIENT,
            attributes={'doi.identifier': doi}
        ) as span:
            try:
                logger.info("doi_lookup", doi=doi)

                metadata = self._fetch_crossref(doi)
                span.set_attribute('doi.crossref_found', True)
                logger.info("crossref_metadata_found", title=metadata.title)

                pdf_path = None
                resolution_path: List[str] = ["crossref"]
                
                # Unpaywall
                pdf_url = self._fetch_unpaywall(doi)
                if pdf_url:
                    span.set_attribute('doi.unpaywall_oa_found', True)
                    resolution_path.append("unpaywall")
                else:
                    span.set_attribute('doi.unpaywall_oa_found', False)
                    # Semantic Scholar
                    pdf_url = self._fetch_semantic_scholar(doi)
                    if pdf_url:
                        span.set_attribute('doi.semantic_scholar_oa_found', True)
                        resolution_path.append("semantic_scholar")
                    else:
                        span.set_attribute('doi.semantic_scholar_oa_found', False)

                span.set_attribute('doi.resolution_path', "+".join(resolution_path))

                if pdf_url:
                    logger.info("oa_pdf_found", url=pdf_url)
                    pdf_path = self._download_pdf(pdf_url, doi)
                    if pdf_path:
                        logger.info("pdf_downloaded", filename=pdf_path.name)
                    else:
                        logger.warning("pdf_download_failed")
                else:
                    logger.info("no_oa_pdf_found")

                span.set_attribute('doi.pdf_acquired', bool(pdf_path))
                span.set_status(StatusCode.OK)
                return metadata, pdf_path
            except Exception as e:
                span.set_status(StatusCode.ERROR, str(e))
                span.record_exception(e)
                raise

    def _fetch_crossref(self, doi: str) -> PaperMetadata:
        """Fetch bibliographic metadata from the Crossref REST API."""
        params = {}
        if self.email:
            params["mailto"] = self.email

        try:
            resp = requests.get(
                f"{self.CROSSREF_BASE}/{doi}",
                headers=self.HEADERS,
                params=params,
                timeout=15,
            )
            if resp.status_code == 404:
                raise DoiFetchError(f"DOI not found in Crossref: {doi}")
            resp.raise_for_status()
        except requests.RequestException as e:
            raise DoiFetchError(f"Crossref request failed for {doi}: {e}") from e

        message = resp.json().get("message", {})
        return self._parse_crossref(message, doi)

    def _parse_crossref(self, data: dict, doi: str) -> PaperMetadata:
        """Convert a Crossref works message dict into PaperMetadata."""
        # Title
        titles = data.get("title", [])
        title = titles[0] if titles else f"DOI:{doi}"

        # Authors — Crossref gives {given, family} or {name} for org authors
        authors = []
        for author in data.get("author", []):
            given = author.get("given", "").strip()
            family = author.get("family", "").strip()
            name = author.get("name", "").strip()
            if family and given:
                authors.append(f"{given} {family}")
            elif family:
                authors.append(family)
            elif name:
                authors.append(name)

        # Year — prefer print date, then online date, then issued
        year = None
        for field in ("published-print", "published-online", "issued"):
            parts = data.get(field, {}).get("date-parts", [[]])
            if parts and parts[0]:
                year = parts[0][0]
                break

        # Abstract — strip JATS XML markup (<jats:p>, <jats:italic>, etc.)
        abstract = data.get("abstract", "") or ""
        if abstract:
            abstract = re.sub(r"<[^>]+>", "", abstract).strip()

        # Venue (journal or conference name)
        container = data.get("container-title", [])
        venue = container[0] if container else None

        # arXiv ID — sometimes present in Crossref relation metadata
        arxiv_id = None
        for _rel_type, rel_list in data.get("relation", {}).items():
            for rel in rel_list:
                if rel.get("id-type") == "arxiv":
                    arxiv_id = rel.get("id", "").replace("arxiv:", "").strip()
                    break

        return PaperMetadata(
            title=title,
            authors=authors or ["Unknown"],
            year=year or datetime.now().year,
            abstract=abstract or None,
            doi=doi,
            venue=venue,
            volume=data.get("volume"),
            issue=data.get("issue"),
            pages=data.get("page"),
            arxiv_id=arxiv_id,
            source="doi",
        )

    # ------------------------------------------------------------------
    # OA PDF discovery
    # ------------------------------------------------------------------

    def _find_oa_pdf_url(self, doi: str) -> Optional[str]:
        """Try Unpaywall, then Semantic Scholar, for an open-access PDF URL."""
        url = self._fetch_unpaywall(doi)
        if url:
            return url
        return self._fetch_semantic_scholar(doi)

    def _fetch_unpaywall(self, doi: str) -> Optional[str]:
        """Return the best OA PDF URL from Unpaywall, or None."""
        email = self.email or "research@example.com"
        try:
            resp = requests.get(
                f"{self.UNPAYWALL_BASE}/{doi}",
                params={"email": email},
                headers=self.HEADERS,
                timeout=10,
            )
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            data = resp.json()
            best = data.get("best_oa_location") or {}
            # url_for_pdf is a direct download; url may be a landing page
            return best.get("url_for_pdf") or best.get("url")
        except requests.RequestException:
            return None

    def _fetch_semantic_scholar(self, doi: str) -> Optional[str]:
        """Return an OA PDF URL from Semantic Scholar, or None."""
        try:
            resp = requests.get(
                f"{self.SEMANTIC_SCHOLAR_BASE}/DOI:{doi}",
                params={"fields": "openAccessPdf"},
                headers=self.HEADERS,
                timeout=10,
            )
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            oa_pdf = resp.json().get("openAccessPdf") or {}
            return oa_pdf.get("url")
        except requests.RequestException:
            return None

    # ------------------------------------------------------------------
    # PDF download
    # ------------------------------------------------------------------

    def _download_pdf(self, url: str, doi: str) -> Optional[Path]:
        """
        Download a PDF to vault/PDFs/ and return the local path.

        Returns None if vault_path is not set, the download fails,
        or the response doesn't appear to be a PDF.
        """
        if not self.vault_path:
            return None

        try:
            resp = requests.get(url, headers=self.HEADERS, timeout=60)
            resp.raise_for_status()

            content = resp.content

            # Verify magic bytes — some Unpaywall "pdf" URLs are landing pages
            if not content.startswith(b"%PDF"):
                return None

            safe_doi = re.sub(r"[^\w.-]", "_", doi)[:60]
            filename = f"doi_{safe_doi}.pdf"
            pdf_path = self.pdfs_dir / filename
            pdf_path.write_bytes(content)
            return pdf_path

        except requests.RequestException:
            return None
