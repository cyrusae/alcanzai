"""
Web content fetcher.

This module fetches and processes web content (articles, blog posts, research pages).

Handles:
- HTML articles (blog posts, Distill.pub, LessWrong, etc.)
- PDFs from URLs (downloads and routes to PDF handler)
- Metadata extraction (OG tags, article tags)
- HTML to markdown conversion
- Graceful failure with helpful error messages

Deliberately excludes (with error messages):
- Twitter/X threads
- Reddit threads  
- Videos
- Paywalled content

Python concepts:
- HTTP requests with content negotiation
- HTML parsing with BeautifulSoup
- Metadata extraction from OG/article tags
- HTML to markdown conversion
- Graceful error handling with context
"""

import re
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import urlparse, urljoin
from datetime import datetime
from markdownify import markdownify as md
from opentelemetry import trace
from opentelemetry.trace import SpanKind, StatusCode

from paper_library.telemetry import tracer, get_logger
from paper_library.models import ArticleMetadata

logger = get_logger(__name__)


class WebFetchError(Exception):
    """Base class for web fetcher errors."""
    pass


class UnsupportedSourceError(WebFetchError):
    """Raised when URL points to unsupported content type."""
    pass


class TooShortError(WebFetchError):
    """Raised when extracted content is too short to be useful."""
    pass


class PaywallError(WebFetchError):
    """Raised when content appears to be behind a paywall."""
    pass


class WebFetcher:
    """
    Fetch and process web content.
    
    This handles:
    1. **URL type detection** - PDF vs HTML vs unsupported
    2. **PDF routing** - detects PDFs in URLs, downloads for GROBID
    3. **HTML parsing** - extracts metadata and content
    4. **Graceful failure** - helpful error messages for edge cases
    
    Supported sources:
    - Blog posts (Medium, personal blogs)
    - Research articles (non-PDF versions)
    - Distill.pub articles
    - LessWrong posts
    - Academic blog posts
    - Any article with HTML + OG metadata
    
    Explicitly unsupported (with helpful errors):
    - Twitter/X threads (use thread archiver)
    - Reddit threads (variable quality)
    - Videos (need transcription)
    - Paywalled content (access required)
    
    Usage:
        fetcher = WebFetcher()
        metadata, content = fetcher.fetch("https://example.com/article")
    """
    
    # User agent to avoid being blocked
    # Many sites block scrapers that don't identify themselves
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # Minimum content length to consider an extraction successful
    # Less than this = probably extracted metadata, not actual article
    MIN_CONTENT_LENGTH = 500  # characters
    
    # Maximum content length to process
    # Some pages are huge (e.g., full discussion threads)
    MAX_CONTENT_LENGTH = 500_000  # ~125k tokens, safe for Claude Haiku
    
    # Hosts that are definitely NOT articles
    # These get explicit "unsupported" errors instead of parsing attempts
    UNSUPPORTED_HOSTS = {
        'twitter.com': 'Twitter/X threads',
        'x.com': 'Twitter/X threads',
        'reddit.com': 'Reddit threads',
        'www.reddit.com': 'Reddit threads',
        'youtube.com': 'YouTube videos',
        'www.youtube.com': 'YouTube videos',
        'youtu.be': 'YouTube videos',
        'linkedin.com': 'LinkedIn posts',
        'www.linkedin.com': 'LinkedIn posts',
    }
    
    def __init__(self, vault_path: Optional[Path] = None):
        """
        Initialize the web fetcher.
        
        Args:
            vault_path: Optional path to vault (for storing PDFs from URLs)
        """
        self.vault_path = vault_path
        if vault_path:
            self.pdfs_dir = vault_path / "PDFs"
            self.pdfs_dir.mkdir(parents=True, exist_ok=True)
    
    def fetch(self, url: str) -> Tuple['ArticleMetadata', str]:
        """
        Fetch a web page and extract metadata + content.
        
        This is the main entry point. It:
        1. Validates the URL
        2. Detects content type
        3. Routes to appropriate handler (PDF, HTML, or error)
        4. Returns metadata + markdown content
        
        Args:
            url: URL to fetch
            
        Returns:
            Tuple of (ArticleMetadata, markdown_content)
            
        Raises:
            UnsupportedSourceError: For Twitter, Reddit, videos, etc.
            TooShortError: If content is too short to be useful
            PaywallError: If content appears paywalled
            WebFetchError: For other fetching issues
        """
        # Validate URL format
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                raise WebFetchError(f"Invalid URL: {url}")
        except Exception as e:
            raise WebFetchError(f"Could not parse URL: {e}")

        with tracer.start_as_current_span(
            'fetch_web',
            kind=SpanKind.CLIENT,
            attributes={
                'web.url': url,
                'web.domain': parsed.netloc,
            }
        ) as span:
            try:
                logger.info("fetching_web", url=url)
                
                # Check for explicitly unsupported hosts
                hostname = parsed.netloc.lower()
                for unsupported_host, description in self.UNSUPPORTED_HOSTS.items():
                    if hostname.endswith(unsupported_host.replace('www.', '')):
                        raise UnsupportedSourceError(
                            f"Cannot process {description} yet (v0.2 feature). "
                            f"URL: {url}\n"
                            f"Try: Take a screenshot, save as PDF, or use a dedicated archiver."
                        )
                
                # Detect content type and fetch
                content_type, content = self._fetch_with_type_detection(url)
                span.set_attribute('web.content_type', 'pdf' if content_type == "application/pdf" else 'html')
                
                if content_type == "application/pdf":
                    # Route to PDF handler
                    metadata, content_str = self._handle_pdf_from_url(url, content)
                elif content_type.startswith("text/html"):
                    # Parse as HTML article
                    metadata, content_str = self._handle_html(url, content)
                else:
                    # Unknown content type
                    raise WebFetchError(
                        f"Unknown content type: {content_type}\n"
                        f"Supported: HTML articles, PDFs\n"
                        f"URL: {url}"
                    )
                
                span.set_attribute('web.content_length_chars', len(content_str))
                span.set_attribute('web.title', metadata.title or '')
                span.set_status(StatusCode.OK)
                return metadata, content_str
                
            except Exception as e:
                span.set_status(StatusCode.ERROR, str(e))
                span.record_exception(e)
                raise
    
    def _fetch_with_type_detection(self, url: str) -> Tuple[str, bytes]:
        """
        Fetch URL with content-type detection.
        
        Uses HEAD request first to check type, then GET if needed.
        This saves bandwidth for PDFs (we know not to parse them).
        
        Args:
            url: URL to fetch
            
        Returns:
            Tuple of (content_type_header, content_bytes)
            
        Raises:
            WebFetchError: If fetch fails
        """
        try:
            # Try HEAD first to get content type without downloading everything
            head_response = requests.head(
                url,
                headers=self.HEADERS,
                timeout=15,
                allow_redirects=True
            )
            
            content_type = head_response.headers.get('content-type', 'text/html').lower()
            
            # If it's a PDF, we know what to do
            if 'application/pdf' in content_type:
                # Download the PDF
                get_response = requests.get(
                    url,
                    headers=self.HEADERS,
                    timeout=30,
                    stream=False
                )
                get_response.raise_for_status()
                return 'application/pdf', get_response.content
            
            # Otherwise, get the full content for parsing
            get_response = requests.get(
                url,
                headers=self.HEADERS,
                timeout=30
            )
            get_response.raise_for_status()
            
            # Force UTF-8 encoding (prevents mojibake)
            get_response.encoding = 'utf-8'
            
            return get_response.headers.get('content-type', 'text/html'), get_response.content
            
        except requests.Timeout:
            raise WebFetchError(f"Request timed out: {url}")
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                raise WebFetchError(f"Page not found (404): {url}")
            elif e.response.status_code == 403:
                raise PaywallError(f"Access forbidden (403): {url}\nMay be paywalled or restricted.")
            elif e.response.status_code == 429:
                raise WebFetchError("Rate limited (429). Wait and try again.")
            else:
                raise WebFetchError(f"HTTP error {e.response.status_code}: {url}")
        except requests.RequestException as e:
            raise WebFetchError(f"Failed to fetch {url}: {e}")
    
    def _handle_pdf_from_url(self, url: str, pdf_content: bytes) -> Tuple['ArticleMetadata', str]:
        """
        Handle a PDF found at a URL.
        
        Two strategies:
        1. If vault_path set: Download PDF to vault, return metadata for arXiv-style processing
        2. If no vault: Create a minimal ArticleMetadata with URL reference
        
        For now (MVP), we return ArticleMetadata to keep web fetcher output consistent.
        The orchestrator can detect this is a PDF and route to GROBID if needed.
        
        Args:
            url: Original URL
            pdf_content: PDF bytes
            
        Returns:
            Tuple of (ArticleMetadata with pdf_path, empty_string)
        """
        logger.info("pdf_detected", url=url)
        
        # Optionally save to vault
        pdf_path = None
        if self.vault_path:
            # Generate filename from URL
            filename = self._generate_pdf_filename_from_url(url)
            pdf_path = self.pdfs_dir / filename
            
            # Save PDF
            pdf_path.write_bytes(pdf_content)
            logger.info("pdf_saved", filename=filename)

        # Create minimal metadata.
        # pdf_path is set when vault_path was provided; the orchestrator
        # uses it to route this item through GROBID instead of the article path.
        metadata = ArticleMetadata(
            title="PDF from URL",  # Will be overwritten by GROBID
            authors=["Unknown"],
            url=url,
            published_date=None,  # GROBID extracts the real date; don't fake it
            publisher=None,
            content=None,
            pdf_path=str(pdf_path) if pdf_path else None,
            source="pdf_from_web",
        )
        
        # Return empty content string (GROBID will extract this)
        return metadata, ""
    
    def _handle_html(self, url: str, html_content: bytes) -> Tuple['ArticleMetadata', str]:
        """
        Parse HTML page and extract article metadata + content.
        
        Steps:
        1. Parse HTML with BeautifulSoup
        2. Extract metadata (OG tags, article tags)
        3. Extract article content using heuristics
        4. Convert to markdown
        5. Validate content length
        6. Check for paywall indicators
        
        Args:
            url: Original URL
            html_content: HTML bytes
            
        Returns:
            Tuple of (ArticleMetadata, markdown_content)
            
        Raises:
            TooShortError: If content too short
            PaywallError: If paywall detected
        """
        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract metadata
        title = self._extract_title(soup, url)
        authors = self._extract_authors(soup)
        published_date = self._extract_published_date(soup)
        publisher = self._extract_publisher(soup)
        
        # Extract main article content
        content_html = self._extract_article_content(soup)
        
        if not content_html:
            # Before giving up entirely, check if this is a landing page with a
            # PDF download link (PhilArchive, SSRN, etc. with no article body).
            pdf_link = self._find_pdf_link_on_page(soup, url)
            if pdf_link:
                logger.info("landing_page_pdf_link_found", url=pdf_link)
                try:
                    pdf_content_type, pdf_bytes = self._fetch_with_type_detection(pdf_link)
                    if "application/pdf" in pdf_content_type:
                        return self._handle_pdf_from_url(pdf_link, pdf_bytes)
                except WebFetchError:
                    pass
            raise TooShortError(
                f"Could not extract article content from {url}\n"
                f"Is this a real article? Try saving as PDF instead."
            )
        
        # Convert HTML to markdown
        content_md = md(content_html, heading_style="atx")
        
        # Clean up markdown
        content_md = self._clean_markdown(content_md)
        
        # Check length — before giving up, look for a PDF download link.
        # Abstract/repository pages (PhilArchive, SSRN, ACL Anthology…) serve
        # minimal HTML but link to the full PDF.
        if len(content_md) < self.MIN_CONTENT_LENGTH:
            pdf_link = self._find_pdf_link_on_page(soup, url)
            if pdf_link:
                logger.info("landing_page_pdf_link_found", url=pdf_link)
                try:
                    pdf_content_type, pdf_bytes = self._fetch_with_type_detection(pdf_link)
                    if "application/pdf" in pdf_content_type:
                        return self._handle_pdf_from_url(pdf_link, pdf_bytes)
                except WebFetchError:
                    pass  # fall through to TooShortError
            raise TooShortError(
                f"Extracted content too short ({len(content_md)} chars, need {self.MIN_CONTENT_LENGTH}). "
                f"This might be paywalled, a listing page, or not an article. "
                f"URL: {url}"
            )
        
        # Check for paywall indicators
        if self._check_paywall_indicators(soup, content_md):
            raise PaywallError(
                f"This page appears to be paywalled or restricted: {url}\n"
                f"Try accessing with institutional credentials or find an open access version."
            )
        
        # Truncate if too long
        if len(content_md) > self.MAX_CONTENT_LENGTH:
            content_md = content_md[:self.MAX_CONTENT_LENGTH]
            logger.warning("content_truncated", max_length=self.MAX_CONTENT_LENGTH)
        
        logger.info("content_extracted", length=len(content_md))
        
        # Create metadata
        metadata = ArticleMetadata(
            title=title,
            authors=authors,
            url=url,
            published_date=published_date,
            publisher=publisher,
            source="web"
        )
        
        return metadata, content_md
    
    def _extract_title(self, soup, url: str) -> str:
        """
        Extract article title from page.
        
        Tries in order:
        1. og:title meta tag (most reliable)
        2. article:title meta tag
        3. <h1> tag (common for blog posts)
        4. <title> tag (fallback)
        5. Domain name (last resort)
        """
        # OG title (most reliable)
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            return og_title['content'].strip()
        
        # Article title
        article_title = soup.find('meta', property='article:title')
        if article_title and article_title.get('content'):
            return article_title['content'].strip()
        
        # H1 (common for blog posts)
        h1 = soup.find('h1')
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True)
        
        # HTML title tag
        title_tag = soup.find('title')
        if title_tag and title_tag.get_text(strip=True):
            title_text = title_tag.get_text(strip=True)
            # Remove trailing " | Domain" or " - Domain"
            title_text = title_text.split('|')[0].split('-')[0].strip()
            if title_text:
                return title_text
        
        # Fallback: domain name
        parsed = urlparse(url)
        return parsed.netloc.replace('www.', '').replace('.com', '').title()
    
    def _extract_authors(self, soup) -> list[str]:
        """
        Extract author names from page.

        Tries in order:
        1. <meta name="author"> (standard HTML, widely used)
        2. article:author Open Graph meta tags
        3. JSON-LD schema.org author field
        4. <d-byline> Distill-framework element (transformer-circuits.pub, distill.pub)
        5. <a rel="author"> link elements
        6. Common author CSS classes (byline, author-name, etc.)
        """
        import json as _json

        authors = []

        # 1. Standard HTML meta author
        meta_author = soup.find('meta', attrs={'name': 'author'})
        if meta_author and meta_author.get('content', '').strip():
            authors.append(meta_author['content'].strip())

        # 2. Open Graph article:author
        if not authors:
            for m in soup.find_all('meta', property='article:author'):
                if m.get('content', '').strip():
                    authors.append(m['content'].strip())

        # 3. JSON-LD schema.org (covers many academic/blog sites)
        if not authors:
            for script in soup.find_all('script', type='application/ld+json'):
                try:
                    data = _json.loads(script.string or '')
                    # May be a single object or a list
                    items = data if isinstance(data, list) else [data]
                    for item in items:
                        raw = item.get('author', [])
                        if isinstance(raw, dict):
                            raw = [raw]
                        for a in raw:
                            name = a.get('name', '').strip() if isinstance(a, dict) else str(a).strip()
                            if name:
                                authors.append(name)
                    if authors:
                        break
                except Exception:
                    continue

        # 4. Distill framework <d-byline> (transformer-circuits.pub, distill.pub)
        if not authors:
            byline = soup.find('d-byline')
            if byline:
                # Authors are in <div class="authors-affiliations"> > <p class="author">
                for p in byline.find_all('p', class_='author'):
                    name = p.get_text(strip=True)
                    if name:
                        authors.append(name)
                # Fallback: any <a> inside d-byline
                if not authors:
                    for a in byline.find_all('a'):
                        name = a.get_text(strip=True)
                        if name and len(name) < 60:
                            authors.append(name)

        # 5. rel="author" links
        if not authors:
            for a in soup.find_all('a', rel='author'):
                name = a.get_text(strip=True)
                if name and len(name) < 80:
                    authors.append(name)

        # 6. Common CSS class patterns
        if not authors:
            for cls in ['byline', 'author-name', 'post-author', 'entry-author', 'author']:
                el = soup.find(class_=cls)
                if el:
                    text = el.get_text(strip=True)
                    # Trim trailing noise ("• date", "Posted by", etc.)
                    for sep in ('•', '|', 'Posted', 'by ', '\n'):
                        text = text.split(sep)[0]
                    text = text.strip()
                    if text and len(text) < 100:
                        authors.append(text)
                        break

        # Deduplicate preserving order
        seen: set[str] = set()
        unique: list[str] = []
        for a in authors:
            if a and a not in seen:
                seen.add(a)
                unique.append(a)

        return unique or ["Unknown"]
    
    def _extract_published_date(self, soup) -> Optional[datetime]:
        """
        Extract publication date from page.
        
        Tries:
        1. article:published_time meta tag (ISO format)
        2. datePublished schema.org (ISO format)
        3. Common date patterns in meta tags
        
        Returns None if not found.
        """
        # OG article:published_time
        pub_time = soup.find('meta', property='article:published_time')
        if pub_time and pub_time.get('content'):
            try:
                return datetime.fromisoformat(pub_time['content'].replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                pass
        
        # Schema.org datePublished
        date_published = soup.find('meta', property='datePublished')
        if date_published and date_published.get('content'):
            try:
                return datetime.fromisoformat(date_published['content'].replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                pass
        
        return None
    
    def _extract_publisher(self, soup) -> Optional[str]:
        """
        Extract publisher/site name.
        
        Tries:
        1. og:site_name
        2. article:publisher
        3. Common site name patterns
        """
        # OG site name
        site_name = soup.find('meta', property='og:site_name')
        if site_name and site_name.get('content'):
            return site_name['content'].strip()
        
        # Publisher
        publisher = soup.find('meta', property='article:publisher')
        if publisher and publisher.get('content'):
            return publisher['content'].strip()
        
        return None
    
    def _extract_article_content(self, soup) -> Optional[str]:
        """
        Extract main article content from HTML.
        
        Tries to find the actual article text, avoiding:
        - Navigation/header/footer
        - Sidebars and ads
        - Comments
        
        Strategy:
        1. Look for semantic <article> tag
        2. Look for common article container classes
        3. Fall back to largest text block
        
        Returns HTML string of article content.
        """
        # Remove script/style tags (they're not content)
        for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            tag.decompose()

        # Strip data-URI images — they produce massive base64 blobs in markdown.
        # Keep img tags with real URLs so alt text and captions are preserved.
        for img in soup.find_all('img'):
            src = img.get('src', '')
            if src.startswith('data:'):
                img.decompose()
        
        # Try semantic <article> tag first
        article = soup.find('article')
        if article:
            return str(article)

        # Try Distill framework custom elements (distill.pub, transformer-circuits.pub)
        for tag_name in ['d-article', 'd-body']:
            distill_article = soup.find(tag_name)
            if distill_article:
                span = trace.get_current_span()
                if span.is_recording():
                    span.set_attribute('web.is_distill', True)
                return str(distill_article)

        # Try common article container classes
        common_containers = [
            {'class': 'article-content'},
            {'class': 'post-content'},
            {'class': 'entry-content'},
            {'class': 'article-body'},
            {'class': 'content'},
            {'id': 'main-content'},
            {'class': 'main-content'},
        ]
        
        for selector in common_containers:
            container = soup.find(attrs=selector)
            if container:
                return str(container)
        
        # Fall back to largest <div> or <section> (crude but often works)
        largest = None
        largest_size = 0
        
        for tag in soup.find_all(['div', 'section']):
            text_length = len(tag.get_text(strip=True))
            if text_length > largest_size and text_length > 200:
                largest = tag
                largest_size = text_length
        
        return str(largest) if largest else None
    
    def _clean_markdown(self, markdown: str) -> str:
        """
        Clean up markdown from HTML conversion.
        
        Removes:
        - Excessive blank lines
        - URL artifacts
        - HTML entities that weren't converted
        - Trailing whitespace
        """
        import re
        
        # Remove excessive blank lines (3+ becomes 2)
        markdown = re.sub(r'\n\n\n+', '\n\n', markdown)
        
        # Remove trailing whitespace from lines
        markdown = '\n'.join(line.rstrip() for line in markdown.split('\n'))
        
        # Remove completely blank lines at start/end
        markdown = markdown.strip()
        
        return markdown
    
    def _check_paywall_indicators(self, soup, content_md: str) -> bool:
        """
        Check if page appears to be paywalled.
        
        Looks for:
        - "Subscribe" prominent in content
        - Very short content (metadata extracted but not article)
        - Paywall warning classes
        """
        # Check for paywall warnings
        paywall_indicators = [
            'paywall',
            'subscribe-wall',
            'metered-paywall',
            'limited-access'
        ]
        
        html_text = str(soup).lower()
        if any(indicator in html_text for indicator in paywall_indicators):
            return True
        
        # Check if content is mostly subscribe prompts
        if content_md.count('subscribe') > 5 and len(content_md) < 1000:
            return True
        
        return False
    
    def _find_pdf_link_on_page(self, soup, base_url: str) -> Optional[str]:
        """
        Scan an HTML page for a PDF download link.

        Used when a landing/abstract page (PhilArchive, SSRN, ACL Anthology,
        etc.) doesn't serve full article text itself but links to the PDF.

        Scoring:
          3 pts — href ends in .pdf
          2 pts — href path contains /pdf/, /download/, or 'pdf' before any '?'
          1 pt  — link text matches download/PDF pattern

        Returns the absolute URL of the best candidate, or None if nothing
        plausible is found.  The caller is responsible for verifying the link
        is actually a PDF (e.g. via content-type header).
        """
        _PDF_TEXT = re.compile(
            r'\b(download(\s+pdf)?|full[\s\-]?text(\s+pdf)?|view\s+pdf|get\s+pdf|pdf)\b',
            re.IGNORECASE,
        )

        candidates: list[tuple[int, str]] = []

        for a_tag in soup.find_all('a', href=True):
            href = a_tag.get('href', '').strip()
            if not href or href.startswith('#') or href.startswith('javascript:'):
                continue

            abs_url = urljoin(base_url, href)
            if not abs_url.startswith(('http://', 'https://')):
                continue

            href_lower = href.lower()
            path_part = href_lower.split('?')[0]  # ignore query string for path checks

            if path_part.endswith('.pdf'):
                candidates.append((3, abs_url))
            elif '/pdf/' in path_part or '/download/' in path_part or path_part.endswith('/pdf'):
                candidates.append((2, abs_url))
            elif 'pdf' in path_part:
                candidates.append((1, abs_url))
            else:
                link_text = a_tag.get_text(strip=True)
                if _PDF_TEXT.search(link_text):
                    candidates.append((1, abs_url))

        if not candidates:
            return None

        # Stable descending sort: highest score first, document order preserved
        # among ties.
        candidates.sort(key=lambda x: -x[0])
        return candidates[0][1]

    def _generate_pdf_filename_from_url(self, url: str) -> str:
        """
        Generate a filename for a PDF downloaded from URL.
        
        Format: web_<domain>_<slug>.pdf
        
        Args:
            url: Original URL
            
        Returns:
            Filename for PDF
        """
        from datetime import datetime
        parsed = urlparse(url)
        
        # Extract domain
        domain = parsed.netloc.replace('www.', '').split('.')[0]
        
        # Extract last path component as slug (if meaningful)
        slug = parsed.path.rstrip('/').split('/')[-1]
        slug = slug[:30] if slug else "document"
        
        # Add timestamp for uniqueness
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        return f"web_{domain}_{slug}_{timestamp}.pdf"
    
    def is_url(self, text: str) -> bool:
        """
        Check if text looks like a URL.
        
        Args:
            text: Text to check
            
        Returns:
            True if text appears to be a URL
        """
        text = text.strip()
        return text.startswith(('http://', 'https://', 'www.'))