"""
arXiv paper fetcher.

This module fetches papers and metadata from arXiv.org using their API.

arXiv is a free distribution service and open-access archive for scholarly
articles in physics, mathematics, computer science, and other fields.

Python concepts:
- HTTP API calls
- XML parsing (arXiv API returns Atom XML)
- File downloading
- Regular expressions for ID parsing
"""

import re
import requests
from pathlib import Path
from typing import Optional, Tuple
from lxml import etree

from paper_library.models import PaperMetadata


class ArxivError(Exception):
    """Raised when arXiv fetching fails."""
    pass


class ArxivFetcher:
    """
    Fetch papers from arXiv by ID.
    
    Handles:
    - Metadata retrieval via arXiv API
    - PDF download
    - ID format parsing
    
    Usage:
        fetcher = ArxivFetcher(vault_path=Path("./vault"))
        pdf_path, metadata = fetcher.fetch("2312.12345")
    """
    
    # arXiv API endpoint
    API_BASE = "http://export.arxiv.org/api/query"
    PDF_BASE = "https://arxiv.org/pdf"
    
    # XML namespace for Atom feed
    NS = {
        'atom': 'http://www.w3.org/2005/Atom',
        'arxiv': 'http://arxiv.org/schemas/atom'
    }
    
    def __init__(self, vault_path: Path):
        """
        Initialize the arXiv fetcher.
        
        Args:
            vault_path: Path to vault (for storing PDFs)
        """
        self.vault_path = vault_path
        self.pdfs_dir = vault_path / "PDFs"
        
        # Ensure PDFs directory exists
        self.pdfs_dir.mkdir(parents=True, exist_ok=True)
    
    def fetch(self, arxiv_id: str) -> Tuple[Path, PaperMetadata]:
        """
        Fetch a paper from arXiv.
        
        Steps:
        1. Parse and validate arXiv ID
        2. Fetch metadata from API
        3. Download PDF
        4. Return path and metadata
        
        Args:
            arxiv_id: arXiv identifier (e.g., "2312.12345" or "1706.03762v2")
            
        Returns:
            Tuple of (pdf_path, metadata)
            
        Raises:
            ArxivError: If fetching fails
        """
        # Parse ID (handles various formats)
        clean_id = self.parse_arxiv_id(arxiv_id)
        if not clean_id:
            raise ArxivError(f"Invalid arXiv ID: {arxiv_id}")
        
        print(f"→ Fetching arXiv {clean_id}...")
        
        # Fetch metadata from API
        metadata = self._fetch_metadata(clean_id)
        
        # Download PDF
        pdf_path = self._download_pdf(clean_id)
        
        # Store PDF path in metadata
        metadata.pdf_path = str(pdf_path)
        metadata.arxiv_id = clean_id
        metadata.source = "arxiv"
        
        return pdf_path, metadata
    
    def parse_arxiv_id(self, text: str) -> Optional[str]:
        """
        Parse arXiv ID from various formats.
        
        Handles:
        - "2312.12345" (new format)
        - "1706.03762v2" (with version)
        - "https://arxiv.org/abs/2312.12345"
        - "https://arxiv.org/pdf/2312.12345.pdf"
        - "arxiv:2312.12345"
        - "arXiv:1234.5678v1"
        
        Args:
            text: Input text that might contain an arXiv ID
            
        Returns:
            Clean arXiv ID (without version) or None if not found
        """
        # Strip whitespace
        text = text.strip()
        
        # Pattern for new-style IDs: YYMM.NNNNN or YYMM.NNNNNvX
        # Example: 2312.12345 or 2312.12345v2
        new_style = r'(\d{4}\.\d{4,5})(v\d+)?'
        
        # Pattern for old-style IDs: archive/YYMMNNN
        # Example: cs/0703001 or math.DG/0312001
        old_style = r'([a-z\-]+(?:\.[A-Z]+)?/\d{7})(v\d+)?'
        
        # Try to find ID in URL format
        if 'arxiv.org' in text:
            # Extract from URL
            url_pattern = r'arxiv\.org/(?:abs|pdf)/([^\s\?#]+)'
            match = re.search(url_pattern, text)
            if match:
                text = match.group(1)
                # Remove .pdf extension if present
                text = text.replace('.pdf', '')
        
        # Remove "arxiv:" or "arXiv:" prefix
        text = re.sub(r'^arxiv:', '', text, flags=re.IGNORECASE)
        
        # Try new-style format
        match = re.search(new_style, text)
        if match:
            arxiv_id = match.group(1)  # Without version
            return arxiv_id
        
        # Try old-style format
        match = re.search(old_style, text)
        if match:
            arxiv_id = match.group(1)  # Without version
            return arxiv_id
        
        return None
    
    def _fetch_metadata(self, arxiv_id: str) -> PaperMetadata:
        """
        Fetch paper metadata from arXiv API.
        
        API returns Atom XML with structure:
        <feed>
          <entry>
            <title>Paper Title</title>
            <author><name>Author Name</name></author>
            <published>2023-12-01T00:00:00Z</published>
            <summary>Abstract text...</summary>
          </entry>
        </feed>
        
        Args:
            arxiv_id: Clean arXiv ID
            
        Returns:
            PaperMetadata object
            
        Raises:
            ArxivError: If API request fails
        """
        try:
            # Build API URL
            # id_list parameter searches by arXiv ID
            url = f"{self.API_BASE}?id_list={arxiv_id}"
            
            # Make request with timeout
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse XML
            root = etree.fromstring(response.content)
            
            # Find entry element (the paper)
            entry = root.find('atom:entry', self.NS)
            if entry is None:
                raise ArxivError(f"Paper not found: {arxiv_id}")
            
            # Extract fields
            title = self._extract_text(entry, 'atom:title')
            authors = self._extract_authors(entry)
            year = self._extract_year(entry)
            abstract = self._extract_text(entry, 'atom:summary')
            
            # Clean up title and abstract (remove extra whitespace)
            if title:
                # arXiv titles often have newlines and extra spaces
                title = " ".join(title.split())
            if abstract:
                abstract = " ".join(abstract.split())
            
            # Validate required fields
            if not title or not authors or not year:
                raise ArxivError(
                    f"Incomplete metadata from arXiv for {arxiv_id}"
                )
            
            return PaperMetadata(
                title=title,
                authors=authors,
                year=year,
                abstract=abstract,
                arxiv_id=arxiv_id
            )
            
        except requests.RequestException as e:
            raise ArxivError(f"Failed to fetch metadata from arXiv: {e}")
        except etree.XMLSyntaxError as e:
            raise ArxivError(f"Invalid XML from arXiv API: {e}")
    
    def _extract_text(self, element: etree._Element, xpath: str) -> Optional[str]:
        """
        Extract text from XML element.
        
        Args:
            element: XML element to search in
            xpath: XPath query
            
        Returns:
            Text content or None
        """
        found = element.find(xpath, self.NS)
        if found is not None and found.text:
            return found.text.strip()
        return None
    
    def _extract_authors(self, entry: etree._Element) -> list[str]:
        """
        Extract author names from entry.
        
        Authors are in <author><name>Author Name</name></author> elements.
        We format them as "Lastname, Firstname" to match GROBID format.
        
        Args:
            entry: Entry element from arXiv API
            
        Returns:
            List of formatted author names
        """
        authors = []
        
        # Find all author elements
        for author_elem in entry.findall('atom:author', self.NS):
            name_elem = author_elem.find('atom:name', self.NS)
            if name_elem is not None and name_elem.text:
                name = name_elem.text.strip()
                
                # arXiv names are typically "Firstname Lastname"
                # Convert to "Lastname, Firstname" format
                name_parts = name.split()
                if len(name_parts) >= 2:
                    # Assume last word is surname, rest is forenames
                    surname = name_parts[-1]
                    forenames = " ".join(name_parts[:-1])
                    formatted = f"{surname}, {forenames}"
                else:
                    # Single name (uncommon but possible)
                    formatted = name
                
                authors.append(formatted)
        
        return authors
    
    def _extract_year(self, entry: etree._Element) -> Optional[int]:
        """
        Extract publication year from entry.
        
        Uses <published> date field: "2023-12-01T00:00:00Z"
        
        Args:
            entry: Entry element
            
        Returns:
            Year as integer or None
        """
        published = self._extract_text(entry, 'atom:published')
        if published:
            # Date is ISO format: "2023-12-01T00:00:00Z"
            # Extract first 4 characters (year)
            try:
                return int(published[:4])
            except (ValueError, IndexError):
                pass
        
        return None
    
    def _download_pdf(self, arxiv_id: str) -> Path:
        """
        Download PDF from arXiv.
        
        PDFs are available at: https://arxiv.org/pdf/{id}.pdf
        
        Args:
            arxiv_id: Clean arXiv ID
            
        Returns:
            Path to downloaded PDF
            
        Raises:
            ArxivError: If download fails
        """
        # Build PDF URL
        pdf_url = f"{self.PDF_BASE}/{arxiv_id}.pdf"
        
        # Destination path
        # Format: PDFs/arxiv_YYMM.NNNNN.pdf
        pdf_filename = f"arxiv_{arxiv_id.replace('/', '_')}.pdf"
        pdf_path = self.pdfs_dir / pdf_filename
        
        # Skip if already downloaded
        if pdf_path.exists():
            print(f"  ✓ PDF already exists: {pdf_filename}")
            return pdf_path
        
        try:
            print(f"  → Downloading PDF from arXiv...")
            
            # Stream the download (PDFs can be large)
            # stream=True means we download in chunks
            response = requests.get(pdf_url, timeout=120, stream=True)
            response.raise_for_status()
            
            # Write to file in chunks
            with open(pdf_path, 'wb') as f:
                # Download in 8KB chunks
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"  ✓ PDF downloaded: {pdf_filename}")
            return pdf_path
            
        except requests.RequestException as e:
            # Clean up partial file if download failed
            if pdf_path.exists():
                pdf_path.unlink()
            raise ArxivError(f"Failed to download PDF: {e}")


def fetch_arxiv_paper(arxiv_id: str, vault_path: Path) -> Tuple[Path, PaperMetadata]:
    """
    Convenience function to fetch an arXiv paper.
    
    Args:
        arxiv_id: arXiv identifier
        vault_path: Path to vault
        
    Returns:
        Tuple of (pdf_path, metadata)
    """
    fetcher = ArxivFetcher(vault_path)
    return fetcher.fetch(arxiv_id)
