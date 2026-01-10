"""
GROBID XML processor.

This module sends PDFs to GROBID for parsing and extracts structured metadata
from the XML response.

GROBID (GeneRation Of BIbliographic Data) is a machine learning library for
extracting, parsing, and restructuring raw documents such as PDF into structured
XML/TEI encoded documents.

Python concepts:
- HTTP requests with files (multipart/form-data)
- XML parsing with lxml
- XPath queries for navigating XML
- Error handling with custom exceptions
"""

import requests
from pathlib import Path
from typing import Optional
from lxml import etree

from paper_library.models import PaperMetadata, Citation


class GrobidError(Exception):
    """Raised when GROBID processing fails."""
    pass


class GrobidProcessor:
    """
    Process PDFs with GROBID to extract structured metadata.
    
    GROBID returns XML in TEI (Text Encoding Initiative) format.
    We parse this to extract paper metadata and citations.
    
    Usage:
        processor = GrobidProcessor("http://localhost:8070")
        metadata = processor.process(Path("paper.pdf"))
        print(metadata.title, metadata.authors)
    """
    
    # XML namespaces used by GROBID/TEI
    # These are needed for XPath queries
    NS = {
        'tei': 'http://www.tei-c.org/ns/1.0'
    }
    
    def __init__(self, grobid_url: str):
        """
        Initialize the GROBID processor.
        
        Args:
            grobid_url: Base URL of GROBID service (e.g., http://localhost:8070)
        """
        self.grobid_url = grobid_url.rstrip('/')
        self.api_url = f"{self.grobid_url}/api/processFulltextDocument"
    
    def process(self, pdf_path: Path) -> PaperMetadata:
        """
        Process a PDF file with GROBID and extract metadata.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            PaperMetadata object with extracted information
            
        Raises:
            GrobidError: If GROBID processing fails
            FileNotFoundError: If PDF doesn't exist
        """
        # Validate PDF exists
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        
        # Send PDF to GROBID
        xml_content = self._call_grobid(pdf_path)
        
        # Parse XML response
        metadata = self._parse_xml(xml_content)
        
        # Store the PDF path
        metadata.pdf_path = str(pdf_path)
        
        return metadata
    
    def _call_grobid(self, pdf_path: Path) -> str:
        """
        Send PDF to GROBID API and get XML response.
        
        This uses multipart/form-data to upload the file.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            XML content as string
            
        Raises:
            GrobidError: If request fails
        """
        try:
            # Open the PDF file in binary mode
            # 'rb' means "read binary"
            with open(pdf_path, 'rb') as pdf_file:
                # Send the file as multipart/form-data
                # The 'input' field is what GROBID expects
                files = {
                    'input': (pdf_path.name, pdf_file, 'application/pdf')
                }
                
                # Make the request with a reasonable timeout
                # timeout=300 means 5 minutes (GROBID can be slow)
                response = requests.post(
                    self.api_url,
                    files=files,
                    timeout=300  # 5 minutes
                )
                
                # Check if request was successful
                # raise_for_status() raises an exception for 4xx/5xx status codes
                response.raise_for_status()
                
                # GROBID returns UTF-8 XML, but requests might guess wrong encoding
                # Force UTF-8 decoding to prevent mojibake (Ã© instead of é)
                response.encoding = 'utf-8'
                return response.text
                
        except requests.Timeout:
            raise GrobidError(f"GROBID request timed out for {pdf_path.name}")
        except requests.RequestException as e:
            raise GrobidError(f"GROBID request failed: {e}")
    
    def _parse_xml(self, xml_content: str) -> PaperMetadata:
        """
        Parse GROBID XML response into PaperMetadata.
        
        GROBID returns TEI XML with structure like:
        <TEI>
          <teiHeader>
            <fileDesc>
              <titleStmt><title>Paper Title</title></titleStmt>
              <sourceDesc>
                <biblStruct>
                  <analytic>
                    <author><persName><forename>John</forename><surname>Smith</surname></persName></author>
                    <title>Paper Title</title>
                  </analytic>
                  <monogr>
                    <title>Journal Name</title>
                    <imprint>
                      <date>2023</date>
                    </imprint>
                  </monogr>
                </biblStruct>
              </sourceDesc>
            </fileDesc>
          </teiHeader>
          <text>
            <body>...</body>
            <back>
              <div type="references">
                <listBibl>
                  <biblStruct>...</biblStruct>  <!-- Citations -->
                </listBibl>
              </div>
            </back>
          </text>
        </TEI>
        
        Args:
            xml_content: XML string from GROBID
            
        Returns:
            PaperMetadata object
            
        Raises:
            GrobidError: If XML parsing fails
        """
        try:
            # Parse XML string into an element tree
            # etree.fromstring() converts string to XML element
            root = etree.fromstring(xml_content.encode('utf-8'))
            
            # Extract metadata using XPath
            # .// means "search anywhere in the tree"
            # @type means "attribute named type"
            title = self._extract_title(root)
            authors = self._extract_authors(root)
            year = self._extract_year(root)
            abstract = self._extract_abstract(root)
            venue = self._extract_venue(root)
            volume, issue, pages = self._extract_publication_info(root)
            doi = self._extract_doi(root)
            citations = self._extract_citations(root)
            
            # Create PaperMetadata object
            # We require title, authors, and year
            # Everything else is optional
            if not title or not authors or not year:
                raise GrobidError(
                    "Could not extract required fields (title, authors, year) from GROBID output"
                )
            
            return PaperMetadata(
                title=title,
                authors=authors,
                year=year,
                abstract=abstract,
                venue=venue,
                volume=volume,
                issue=issue,
                pages=pages,
                doi=doi,
                citations=citations,
                source="grobid"
            )
            
        except etree.XMLSyntaxError as e:
            raise GrobidError(f"Invalid XML from GROBID: {e}")
    
    def _extract_title(self, root: etree._Element) -> Optional[str]:
        """
        Extract paper title from XML.
        
        XPath: //tei:titleStmt/tei:title[@type='main']
        
        Args:
            root: XML root element
            
        Returns:
            Title string or None
        """
        # XPath query: find <title type="main"> inside <titleStmt>
        # The .// means "anywhere in the tree"
        # The [@type='main'] filters for main title (not subtitle)
        title_elem = root.find('.//tei:titleStmt/tei:title[@type="main"]', self.NS)
        
        if title_elem is not None and title_elem.text:
            # .strip() removes leading/trailing whitespace
            title = title_elem.text.strip()
            # Clean up common garbage from GROBID extraction
            title = self._clean_title(title)
            return title
        
        # Fallback: try title in biblStruct (alternative location)
        title_elem = root.find('.//tei:analytic/tei:title[@type="main"]', self.NS)
        if title_elem is not None and title_elem.text:
            title = title_elem.text.strip()
            title = self._clean_title(title)
            return title
        
        return None
    
    def _clean_title(self, title: str) -> str:
        """
        Clean extracted title by removing common garbage.
        
        GROBID sometimes includes:
        - Copyright notices
        - Permission statements
        - Footnote markers
        - ALL-CAPS formatting
        
        Args:
            title: Raw title from GROBID
            
        Returns:
            Cleaned title
        """
        import re
        
        # Remove copyright/permission statements at the start
        # Pattern: "Provided ... Google hereby grants ..." etc.
        copyright_patterns = [
            r'^Provided proper attribution.*?solely for use in.*?\.',
            r'^©.*?\d{4}',  # © 2023 etc.
            r'^Copyright.*?\d{4}',
            r'^\*\s*Equal contribution.*?$',  # Footnote markers
        ]
        
        for pattern in copyright_patterns:
            title = re.sub(pattern, '', title, flags=re.IGNORECASE | re.DOTALL)
        
        # Remove leading/trailing whitespace and punctuation
        title = title.strip()
        title = title.strip('.,;:')
        
        # Remove multiple spaces
        title = re.sub(r'\s+', ' ', title)
        
        # Fix ALL-CAPS titles
        # If more than 50% of letters are uppercase, convert to title case
        if title.isupper() or sum(1 for c in title if c.isupper()) > len([c for c in title if c.isalpha()]) * 0.5:
            # Simple title case - user can manually fix acronyms later
            title = title.title()
        
        return title.strip()
    
    def _extract_authors(self, root: etree._Element) -> list[str]:
        """
        Extract author names from XML.
        
        XPath: //tei:analytic/tei:author/tei:persName
        
        Authors are formatted as "Lastname, Firstname Middlename"
        
        Args:
            root: XML root element
            
        Returns:
            List of author name strings
        """
        authors = []
        
        # Find all author elements
        # .findall() returns all matching elements (not just first)
        author_elems = root.findall('.//tei:analytic/tei:author', self.NS)
        
        for author_elem in author_elems:
            # Get persName (personal name) element
            persname = author_elem.find('tei:persName', self.NS)
            if persname is None:
                continue
            
            # Extract surname (last name)
            surname_elem = persname.find('tei:surname', self.NS)
            surname = surname_elem.text.strip() if surname_elem is not None and surname_elem.text else ""
            
            # Extract forename(s) (first/middle names)
            # There can be multiple forename elements
            forenames = []
            for forename_elem in persname.findall('tei:forename', self.NS):
                if forename_elem.text:
                    forenames.append(forename_elem.text.strip())
            
            # Format as "Lastname, Firstname Middlename"
            if surname:
                if forenames:
                    author_name = f"{surname}, {' '.join(forenames)}"
                else:
                    author_name = surname
                authors.append(author_name)
        
        return authors
    
    def _extract_year(self, root: etree._Element) -> Optional[int]:
        """
        Extract publication year from XML.
        
        XPath: //tei:monogr/tei:imprint/tei:date[@type='published']/@when
        
        Args:
            root: XML root element
            
        Returns:
            Year as integer or None
        """
        # Try to find publication date
        date_elem = root.find('.//tei:monogr/tei:imprint/tei:date[@type="published"]', self.NS)
        
        if date_elem is not None:
            # Date can be in @when attribute (ISO format: "2023-01-15")
            # or in text content
            date_str = date_elem.get('when') or date_elem.text
            
            if date_str:
                # Extract just the year (first 4 digits)
                # "2023-01-15" -> "2023"
                try:
                    year_str = date_str.strip()[:4]
                    return int(year_str)
                except (ValueError, IndexError):
                    pass
        
        return None
    
    def _extract_abstract(self, root: etree._Element) -> Optional[str]:
        """
        Extract abstract text from XML.
        
        XPath: //tei:profileDesc/tei:abstract/tei:div/tei:p
        
        Args:
            root: XML root element
            
        Returns:
            Abstract text or None
        """
        # Find abstract element
        abstract_elem = root.find('.//tei:profileDesc/tei:abstract', self.NS)
        
        if abstract_elem is not None:
            # Abstract can have multiple paragraphs
            # Join them with newlines
            paragraphs = []
            for p_elem in abstract_elem.findall('.//tei:p', self.NS):
                # itertext() gets all text content, including nested elements
                # "".join(...) concatenates all text pieces
                text = "".join(p_elem.itertext()).strip()
                if text:
                    paragraphs.append(text)
            
            if paragraphs:
                return "\n\n".join(paragraphs)
        
        return None
    
    def _extract_venue(self, root: etree._Element) -> Optional[str]:
        """
        Extract venue (journal or conference) name from XML.
        
        XPath: //tei:monogr/tei:title[@level='j']
        
        Args:
            root: XML root element
            
        Returns:
            Venue name or None
        """
        # level='j' means journal
        # level='m' would be monograph (book)
        venue_elem = root.find('.//tei:monogr/tei:title[@level="j"]', self.NS)
        
        if venue_elem is not None and venue_elem.text:
            return venue_elem.text.strip()
        
        return None
    
    def _extract_publication_info(self, root: etree._Element) -> tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Extract volume, issue, and page numbers from XML.
        
        XPath: //tei:monogr/tei:imprint
        
        Args:
            root: XML root element
            
        Returns:
            Tuple of (volume, issue, pages)
        """
        imprint = root.find('.//tei:monogr/tei:imprint', self.NS)
        
        if imprint is None:
            return None, None, None
        
        # Extract volume
        volume_elem = imprint.find('tei:biblScope[@unit="volume"]', self.NS)
        volume = volume_elem.text.strip() if volume_elem is not None and volume_elem.text else None
        
        # Extract issue
        issue_elem = imprint.find('tei:biblScope[@unit="issue"]', self.NS)
        issue = issue_elem.text.strip() if issue_elem is not None and issue_elem.text else None
        
        # Extract pages
        page_elem = imprint.find('tei:biblScope[@unit="page"]', self.NS)
        if page_elem is not None:
            # Pages can be "123-145" or separate @from/@to attributes
            from_page = page_elem.get('from')
            to_page = page_elem.get('to')
            
            if from_page and to_page:
                pages = f"{from_page}-{to_page}"
            elif page_elem.text:
                pages = page_elem.text.strip()
            else:
                pages = None
        else:
            pages = None
        
        return volume, issue, pages
    
    def _extract_doi(self, root: etree._Element) -> Optional[str]:
        """
        Extract DOI from XML.
        
        XPath: //tei:idno[@type='DOI']
        
        Args:
            root: XML root element
            
        Returns:
            DOI string or None
        """
        doi_elem = root.find('.//tei:idno[@type="DOI"]', self.NS)
        
        if doi_elem is not None and doi_elem.text:
            return doi_elem.text.strip()
        
        return None
    
    def _extract_venue_from_bibl(self, bibl: etree._Element) -> Optional[str]:
        """
        Extract venue (journal/conference) from a biblStruct citation element.
        
        Similar to _extract_venue() but works on citation elements instead of root.
        
        Args:
            bibl: biblStruct element from bibliography
            
        Returns:
            Venue name or None
        """
        venue_elem = bibl.find('.//tei:monogr/tei:title[@level="j"]', self.NS)
        
        if venue_elem is not None and venue_elem.text:
            return venue_elem.text.strip()
        
        return None
    
    def _extract_publication_info_from_bibl(self, bibl: etree._Element) -> tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Extract volume, issue, and page numbers from a biblStruct citation element.
        
        Similar to _extract_publication_info() but works on citation elements.
        
        Args:
            bibl: biblStruct element from bibliography
            
        Returns:
            Tuple of (volume, issue, pages)
        """
        imprint = bibl.find('.//tei:monogr/tei:imprint', self.NS)
        
        if imprint is None:
            return None, None, None
        
        # Extract volume
        volume_elem = imprint.find('tei:biblScope[@unit="volume"]', self.NS)
        volume = volume_elem.text.strip() if volume_elem is not None and volume_elem.text else None
        
        # Extract issue
        issue_elem = imprint.find('tei:biblScope[@unit="issue"]', self.NS)
        issue = issue_elem.text.strip() if issue_elem is not None and issue_elem.text else None
        
        # Extract pages
        page_elem = imprint.find('tei:biblScope[@unit="page"]', self.NS)
        if page_elem is not None:
            # Pages can be "123-145" or separate @from/@to attributes
            from_page = page_elem.get('from')
            to_page = page_elem.get('to')
            
            if from_page and to_page:
                pages = f"{from_page}-{to_page}"
            elif page_elem.text:
                pages = page_elem.text.strip()
            else:
                pages = None
        else:
            pages = None
        
        return volume, issue, pages
    
    def _calculate_garbage_score(self, citation: Citation) -> int:
        """
        Score how likely a citation is garbage (0-100).
        
        Strategy:
        1. Start with baseline trust based on parsed fields (lower is better)
        2. Check for mutually-exclusive garbage categories:
           - Algorithmic pseudocode
           - Mathematical notation
           - Figure/table captions
           - Biographical text
        3. Each category scores independently, caps raised if multiple signals
        
        Thresholds:
        - >60: Definitely garbage, reject
        - 40-60: Suspicious (keep for now, could tune later)
        - <40: Probably legitimate
        
        Args:
            citation: Citation object with parsed fields + raw_text
            
        Returns:
            Score from 0-100 (higher = more likely garbage)
        """
        import re
        
        score = 0
        
        # Handle missing raw_text (shouldn't happen but be safe)
        if not citation.raw_text:
            # If we have no text to analyze, rely purely on parsed fields
            if not citation.title and not citation.authors:
                return 100  # No data at all = garbage
            return 0  # Has parsed fields, keep it
        
        text = citation.raw_text.lower()
        
        # === BASELINE TRUST (from parsed fields) ===
        # Citations with well-formed metadata are more trustworthy
        
        if not citation.authors:
            score += 15  # Missing authors is somewhat suspicious
        
        # Year handling: soft boundaries for humanities + future work
        if not citation.year:
            score += 10  # Missing year is suspicious
        else:
            # Soft suspicion for unusual years (not hard boundaries)
            if citation.year < 1800:
                score += 5  # Old citations are fine (classics, medieval) but slightly unusual
            elif citation.year > 2027:  # Current year + 1
                score += 15  # Future publications are more suspicious
        
        # === CATEGORY 1: ALGORITHMIC PSEUDOCODE ===
        # Very strong signals - algorithmic/programming content
        algo_score = 0
        
        algo_keywords = [
            'let ', 'for i =', 'for i >', 'for j =', 'for every',
            'as follows:', 'construct', 'recall that', 'we now',
            'independently and uniformly'
        ]
        algo_score += sum(15 for kw in algo_keywords if kw in text)
        
        # LaTeX set notation is a dead giveaway for pseudocode
        if re.search(r'\\\s*\{', text):  # "\ {" 
            algo_score += 25
        
        # Ellipsis formatting from algorithms (". . ." or "...")
        if '. . .' in text or '...' in text:
            algo_score += 10
        
        if algo_score > 0:
            score += min(60, algo_score)
        
        # === CATEGORY 2: MATHEMATICAL NOTATION ===
        # Dense math expressions with operators
        math_score = 0
        
        # Plus and equals are VERY strong signals (few legitimate titles use them)
        plus_count = text.count('+')
        equals_count = text.count('=')
        
        if plus_count >= 3:
            math_score += 20
        if equals_count >= 2:
            math_score += 25  # Equals is especially strong
        
        # LaTeX subscript/superscript patterns (x_1, y^2, etc.)
        latex_subs = len(re.findall(r'[a-z]_[0-9{]|[a-z]\^[0-9{]', text))
        math_score += min(20, latex_subs * 5)
        
        # Symbol-to-word ratio (high ratio = likely math)
        words = len(re.findall(r'\b[a-z]{3,}\b', text))  # Real words (3+ letters)
        symbols = len(re.findall(r'[=+\-*/^_{}[\]()]', text))
        
        if words > 0:
            ratio = symbols / words
            if ratio > 0.5:  # More symbols than words
                math_score += 15
        
        if math_score > 0:
            score += min(60, math_score)
        
        # === CATEGORY 3: FIGURE/TABLE CAPTIONS ===
        # Figure references, experimental parameters
        figure_score = 0
        
        # Figure/table references
        if re.search(r'figure\s+\d+|fig\.\s*\([a-z]\)', text, re.IGNORECASE):
            figure_score += 30
        if re.search(r'table\s+\d+', text, re.IGNORECASE):
            figure_score += 30
        
        # Experimental notation (N=10000, etc.)
        if re.search(r'\bn\s*=\s*\d{3,}', text, re.IGNORECASE):
            figure_score += 25
        
        # Subfigure labels like "(a) (b) (c)"
        if re.search(r'\([a-d]\)\s*\([a-d]\)', text):
            figure_score += 20
        
        # Hyperparameter notation - check DENSITY not just presence
        hyperparam_count = len(re.findall(r'-[a-z]\d+-|[a-z]-[a-z]|\d+k(?:\s|$)', text, re.IGNORECASE))
        if hyperparam_count > 5:  # Many hyperparameters = likely garbage
            figure_score += 40
        elif hyperparam_count > 2:
            figure_score += 20
        
        if figure_score > 0:
            score += min(60, figure_score)
        
        # === CATEGORY 4: BIOGRAPHICAL TEXT ===
        # Author biographies that GROBID mistakes for citations
        bio_score = 0
        
        bio_phrases = [
            'graduated from', 'was born', 'attended', 'pursued a degree',
            'is an american', 'currently resides', 'majored in',
            'the person attended', 'the person was born', 'she graduated',
            'he graduated', 'is a successful'
        ]
        
        bio_signal_count = sum(1 for phrase in bio_phrases if phrase in text)
        bio_score = bio_signal_count * 30
        
        # Raise cap if multiple bio signals (e.g., Kenny B. with 4 signals)
        if bio_signal_count >= 3:
            score += min(80, bio_score)  # Raise cap to 80
        elif bio_score > 0:
            score += min(60, bio_score)
        
        # === TRUST ADJUSTMENT ===
        # Reduce suspicion if we have strong trust signals
        
        # Has venue information = more trustworthy
        if citation.venue:
            score = max(0, score - 10)
            
            # Recognized academic venues are very trustworthy
            trusted_venue_keywords = [
                'proceedings', 'conference', 'journal', 'nature', 'science',
                'acm', 'ieee', 'springer', 'elsevier', 'arxiv'
            ]
            if any(keyword in citation.venue.lower() for keyword in trusted_venue_keywords):
                score = max(0, score - 10)
        
        # Has authors AND reasonable year = trustworthy
        # But only for recent years (humanities citations can be old, but not future)
        if citation.authors and citation.year and 1990 <= citation.year <= 2027:
            score = max(0, score - 20)
        elif citation.authors and citation.year and citation.year < 1990:
            # Old papers with authors still get some trust (humanities use case)
            score = max(0, score - 10)
        
        return min(100, score)
    
    def _extract_citations(self, root: etree._Element) -> list[Citation]:
        """
        Extract bibliography/citations from XML.
        
        XPath: //tei:back//tei:listBibl/tei:biblStruct
        
        Each citation is stored as a Citation object with:
        - raw_text: The full citation string
        - Parsed fields (authors, title, year, doi) when available
        
        Args:
            root: XML root element
            
        Returns:
            List of Citation objects
        """
        citations = []
        
        # Find bibliography section
        # //tei:back//tei:listBibl means "find listBibl anywhere under back element"
        listbibl = root.find('.//tei:back//tei:listBibl', self.NS)
        
        if listbibl is None:
            return citations
        
        # Each biblStruct is one citation
        for bibl in listbibl.findall('tei:biblStruct', self.NS):
            # Extract raw citation text (all text concatenated)
            raw_text = "".join(bibl.itertext()).strip()
            
            # Clean up excessive whitespace
            # Replace multiple whitespace chars (spaces, tabs, newlines) with single space
            import re
            raw_text = re.sub(r'\s+', ' ', raw_text)
            
            # Skip if too short to be a real citation
            if len(raw_text) < 10:
                continue
            
            # Try to parse citation fields
            # Note: Citation parsing is complex and often incomplete
            # For MVP, we just store the raw text + whatever we can extract
            
            # Title
            title_elem = bibl.find('.//tei:title[@level="a"]', self.NS)  # article title
            if title_elem is None:
                title_elem = bibl.find('.//tei:title[@level="m"]', self.NS)  # book title
            title = title_elem.text.strip() if title_elem is not None and title_elem.text else None
            
            # Authors
            authors = []
            for author_elem in bibl.findall('.//tei:author', self.NS):
                persname = author_elem.find('tei:persName', self.NS)
                if persname is not None:
                    surname = persname.find('tei:surname', self.NS)
                    forenames = persname.findall('tei:forename', self.NS)
                    
                    if surname is not None and surname.text:
                        name_parts = [surname.text.strip()]
                        if forenames:
                            initials = [f.text[0] + "." for f in forenames if f.text]
                            name_parts.extend(initials)
                        authors.append(" ".join(name_parts))
            
            # Year
            date_elem = bibl.find('.//tei:date[@type="published"]', self.NS)
            year = None
            if date_elem is not None:
                date_str = date_elem.get('when') or date_elem.text
                if date_str:
                    try:
                        year = int(date_str[:4])
                    except (ValueError, IndexError):
                        pass
            
            # DOI
            doi_elem = bibl.find('.//tei:idno[@type="DOI"]', self.NS)
            doi = doi_elem.text.strip() if doi_elem is not None and doi_elem.text else None
            
            # Extract venue and publication info (just like for main paper)
            venue = self._extract_venue_from_bibl(bibl)
            volume, issue, pages = self._extract_publication_info_from_bibl(bibl)
            
            # Create Citation object with full bibliographic data
            citation = Citation(
                raw_text=raw_text,
                authors=authors if authors else None,
                title=title,
                year=year,
                venue=venue,
                volume=volume,
                issue=issue,
                pages=pages,
                doi=doi,
                mention_count=1  # We don't track mentions in MVP
            )
            
            # === GARBAGE DETECTION: SCORING-BASED HEURISTIC ===
            # Uses parsed fields as baseline trust + categorizes garbage types
            # Each garbage category scores independently (algo, math, figure, bio)
            
            garbage_score = self._calculate_garbage_score(citation)
            
            # Threshold: >60 = definitely garbage, reject
            # 40-60 would be "suspicious" - for now we keep these
            if garbage_score > 60:
                continue
            
            citations.append(citation)
        
        return citations