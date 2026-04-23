"""
Tests for web content fetcher.

Mocked tests run without network access and are fast.
Integration tests hit real URLs — marked @pytest.mark.integration
and skipped by default (run with: pytest -m integration).

Run mocked tests only:
    pytest tests/test_web_fetcher.py -m "not integration"

Run everything including live network:
    pytest tests/test_web_fetcher.py -m integration
"""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest
import requests

from paper_library.web_fetcher import (
    PaywallError,
    TooShortError,
    UnsupportedSourceError,
    WebFetchError,
    WebFetcher,
)
from paper_library.models import ArticleMetadata


# ---------------------------------------------------------------------------
# URL detection
# ---------------------------------------------------------------------------

class TestUrlDetection:

    def test_http_url_recognised(self):
        assert WebFetcher().is_url("https://example.com/article")

    def test_http_prefix_recognised(self):
        assert WebFetcher().is_url("http://example.com")

    def test_www_prefix_recognised(self):
        assert WebFetcher().is_url("www.example.com")

    def test_arxiv_id_not_url(self):
        assert not WebFetcher().is_url("2312.12345")

    def test_local_path_not_url(self):
        assert not WebFetcher().is_url("./local/file.pdf")

    def test_plain_string_not_url(self):
        assert not WebFetcher().is_url("not a url")


# ---------------------------------------------------------------------------
# Unsupported host detection (no network — raises before any HTTP call)
# ---------------------------------------------------------------------------

class TestUnsupportedHosts:

    @pytest.mark.parametrize("url", [
        "https://twitter.com/user/status/123456",
        "https://x.com/user/status/123456",
        "https://reddit.com/r/MachineLearning/comments/xyz",
        "https://www.reddit.com/r/MachineLearning/comments/xyz",
        "https://youtube.com/watch?v=abc123",
        "https://www.youtube.com/watch?v=abc123",
        "https://youtu.be/abc123",
        "https://linkedin.com/posts/user/xyz",
    ])
    def test_unsupported_url_raises_before_network(self, url):
        """Should raise UnsupportedSourceError without making any HTTP call."""
        fetcher = WebFetcher()
        with patch("paper_library.web_fetcher.requests.head") as mock_head:
            with pytest.raises(UnsupportedSourceError):
                fetcher.fetch(url)
            mock_head.assert_not_called()


# ---------------------------------------------------------------------------
# HTML parsing helpers
# ---------------------------------------------------------------------------

class TestHtmlParsing:

    @pytest.fixture
    def fetcher(self):
        return WebFetcher()

    def _soup(self, html: str):
        from bs4 import BeautifulSoup
        return BeautifulSoup(html, "html.parser")

    def test_title_from_og_tag(self, fetcher):
        soup = self._soup('<html><head><meta property="og:title" content="OG Title"></head><body><article>x</article></body></html>')
        assert fetcher._extract_title(soup, "https://example.com") == "OG Title"

    def test_title_fallback_to_h1(self, fetcher):
        soup = self._soup("<html><head><title>Page</title></head><body><h1>H1 Heading</h1><article>content</article></body></html>")
        assert fetcher._extract_title(soup, "https://example.com") == "H1 Heading"

    def test_title_fallback_to_title_tag(self, fetcher):
        soup = self._soup("<html><head><title>Title Tag | Site</title></head><body></body></html>")
        title = fetcher._extract_title(soup, "https://example.com")
        assert "Title Tag" in title

    def test_authors_from_meta_tags(self, fetcher):
        soup = self._soup("""
            <html><head>
                <meta property="article:author" content="Alice Smith">
                <meta property="article:author" content="Bob Jones">
            </head><body></body></html>
        """)
        authors = fetcher._extract_authors(soup)
        assert "Alice Smith" in authors
        assert "Bob Jones" in authors

    def test_authors_defaults_to_unknown(self, fetcher):
        soup = self._soup("<html><body></body></html>")
        assert fetcher._extract_authors(soup) == ["Unknown"]

    def test_published_date_from_og_tag(self, fetcher):
        soup = self._soup('<html><head><meta property="article:published_time" content="2024-01-15T10:30:00Z"></head><body></body></html>')
        date = fetcher._extract_published_date(soup)
        assert date is not None
        assert date.year == 2024
        assert date.month == 1
        assert date.day == 15

    def test_published_date_none_when_missing(self, fetcher):
        soup = self._soup("<html><body></body></html>")
        assert fetcher._extract_published_date(soup) is None

    def test_article_content_prefers_article_tag(self, fetcher):
        soup = self._soup("""
            <html><body>
                <nav>Navigation</nav>
                <article><p>This is the main article content that should be extracted.</p></article>
                <aside>Sidebar</aside>
            </body></html>
        """)
        content = fetcher._extract_article_content(soup)
        assert content is not None
        assert "main article content" in content
        assert "Sidebar" not in content

    def test_article_content_excludes_nav_and_footer(self, fetcher):
        soup = self._soup("""
            <html><body>
                <nav>Nav links</nav>
                <article><p>Real content here.</p></article>
                <footer>Footer links</footer>
            </body></html>
        """)
        content = fetcher._extract_article_content(soup)
        assert "Nav links" not in (content or "")
        assert "Footer links" not in (content or "")

    def test_clean_markdown_removes_excessive_blank_lines(self, fetcher):
        messy = "# Title\n\n\n\n\nParagraph."
        cleaned = fetcher._clean_markdown(messy)
        assert "\n\n\n" not in cleaned

    def test_clean_markdown_strips_trailing_whitespace(self, fetcher):
        messy = "Line one.   \nLine two.  "
        cleaned = fetcher._clean_markdown(messy)
        for line in cleaned.split("\n"):
            assert line == line.rstrip()

    def test_paywall_detected_by_class(self, fetcher):
        soup = self._soup('<html><body><div class="paywall">Subscribe</div></body></html>')
        assert fetcher._check_paywall_indicators(soup, "content")

    def test_no_paywall_for_normal_page(self, fetcher):
        soup = self._soup("<html><body><article><p>Normal content here.</p></article></body></html>")
        assert not fetcher._check_paywall_indicators(soup, "Normal content here with lots of text.")


# ---------------------------------------------------------------------------
# PDF landing page link finder
# ---------------------------------------------------------------------------

class TestPdfLinkFinder:
    """Tests for _find_pdf_link_on_page — no network calls needed."""

    @pytest.fixture
    def fetcher(self):
        return WebFetcher()

    def _soup(self, html: str):
        from bs4 import BeautifulSoup
        return BeautifulSoup(html, "html.parser")

    def test_href_ending_in_pdf_is_found(self, fetcher):
        soup = self._soup(
            '<html><body><a href="/files/paper.pdf">Full paper</a></body></html>'
        )
        url = fetcher._find_pdf_link_on_page(soup, "https://philarchive.org/abstract/SMITH")
        assert url == "https://philarchive.org/files/paper.pdf"

    def test_absolute_pdf_href_is_returned_unchanged(self, fetcher):
        soup = self._soup(
            '<html><body><a href="https://cdn.example.com/paper.pdf">Download</a></body></html>'
        )
        url = fetcher._find_pdf_link_on_page(soup, "https://example.com/abstract")
        assert url == "https://cdn.example.com/paper.pdf"

    def test_link_text_download_pdf_is_found(self, fetcher):
        soup = self._soup(
            '<html><body><a href="/get?id=42">Download PDF</a></body></html>'
        )
        url = fetcher._find_pdf_link_on_page(soup, "https://papers.ssrn.com/abstract=42")
        assert url == "https://papers.ssrn.com/get?id=42"

    def test_link_text_pdf_alone_is_found(self, fetcher):
        soup = self._soup(
            '<html><body><a href="/view/42">PDF</a></body></html>'
        )
        url = fetcher._find_pdf_link_on_page(soup, "https://example.com/abstract/42")
        assert url is not None

    def test_href_with_pdf_in_path_is_found(self, fetcher):
        """ACL Anthology style: /pdf/2021.acl-long.1"""
        soup = self._soup(
            '<html><body><a href="/pdf/2021.acl-long.1">PDF</a></body></html>'
        )
        url = fetcher._find_pdf_link_on_page(soup, "https://aclanthology.org/2021.acl-long.1")
        assert url == "https://aclanthology.org/pdf/2021.acl-long.1"

    def test_no_pdf_links_returns_none(self, fetcher):
        soup = self._soup(
            '<html><body><a href="/about">About</a><a href="/contact">Contact</a></body></html>'
        )
        assert fetcher._find_pdf_link_on_page(soup, "https://example.com") is None

    def test_anchor_only_links_are_skipped(self, fetcher):
        soup = self._soup(
            '<html><body><a href="#section">PDF mention</a></body></html>'
        )
        assert fetcher._find_pdf_link_on_page(soup, "https://example.com") is None

    def test_javascript_links_are_skipped(self, fetcher):
        soup = self._soup(
            '<html><body><a href="javascript:void(0)">Download PDF</a></body></html>'
        )
        assert fetcher._find_pdf_link_on_page(soup, "https://example.com") is None

    def test_direct_pdf_href_outscores_link_text_only(self, fetcher):
        """Href ending in .pdf should win over a link that only has matching text."""
        soup = self._soup(
            '''<html><body>
                <a href="/generic-link">Download PDF</a>
                <a href="/paper.pdf">Full paper</a>
            </body></html>'''
        )
        url = fetcher._find_pdf_link_on_page(soup, "https://example.com/abstract")
        assert url is not None and url.endswith(".pdf")

    def test_query_string_not_confused_with_pdf_path(self, fetcher):
        """A ?format=pdf query param should still be found (path without .pdf, but 'pdf' in full href)."""
        soup = self._soup(
            '<html><body><a href="/download?format=pdf&id=99">Download PDF</a></body></html>'
        )
        url = fetcher._find_pdf_link_on_page(soup, "https://example.com/abstract")
        # Should be found via link text, not confused by query string
        assert url is not None


# ---------------------------------------------------------------------------
# Landing page → PDF pipeline integration (mocked)
# ---------------------------------------------------------------------------

class TestLandingPageToPdfRouting:
    """Verify that _handle_html() routes to the PDF pipeline on short content."""

    def _mock_head(self, content_type="text/html; charset=utf-8"):
        resp = Mock()
        resp.headers = {"content-type": content_type}
        resp.status_code = 200
        return resp

    def _mock_get(self, content, content_type="text/html"):
        resp = Mock()
        resp.content = content
        resp.headers = {"content-type": content_type}
        resp.encoding = "utf-8"
        resp.raise_for_status = Mock()
        return resp

    @patch("paper_library.web_fetcher.requests.head")
    @patch("paper_library.web_fetcher.requests.get")
    def test_landing_page_with_pdf_link_returns_pdf_metadata(self, mock_get, mock_head):
        """A short page containing a PDF link should produce pdf_from_web metadata."""
        landing_html = b"""
        <html>
          <head><title>Paper Abstract</title></head>
          <body>
            <p>Abstract: This paper studies attention mechanisms.</p>
            <a href="/papers/attention.pdf">Download PDF</a>
          </body>
        </html>
        """
        pdf_bytes = b"%PDF-1.4\n%dummy pdf content"

        # Sequence: HEAD for landing page, GET for landing page,
        # HEAD for PDF link, GET for PDF link
        mock_head.side_effect = [
            self._mock_head("text/html"),          # landing page HEAD
            self._mock_head("application/pdf"),    # PDF link HEAD
        ]
        mock_get.side_effect = [
            self._mock_get(landing_html, "text/html"),   # landing page GET
            self._mock_get(pdf_bytes, "application/pdf"), # PDF GET
        ]

        metadata, content = WebFetcher().fetch("https://example.com/abstract/42")

        assert metadata.source == "pdf_from_web"
        assert content == ""

    @patch("paper_library.web_fetcher.requests.head")
    @patch("paper_library.web_fetcher.requests.get")
    def test_short_page_without_pdf_link_still_raises(self, mock_get, mock_head):
        """A short page with no PDF link should still raise TooShortError."""
        short_html = b"""
        <html><head><title>Stub</title></head>
        <body><p>Very little content here.</p></body>
        </html>
        """
        mock_head.return_value = self._mock_head("text/html")
        mock_get.return_value = self._mock_get(short_html, "text/html")

        with pytest.raises(TooShortError):
            WebFetcher().fetch("https://example.com/stub")


# ---------------------------------------------------------------------------
# PDF handling
# ---------------------------------------------------------------------------

class TestPdfHandling:

    def test_pdf_filename_format(self):
        fetcher = WebFetcher()
        name = fetcher._generate_pdf_filename_from_url("https://example.com/papers/research-2024.pdf")
        assert name.startswith("web_example_research")
        assert name.endswith(".pdf")

    def test_pdf_filename_is_deterministic(self):
        """Regression for #15: same URL must produce the same filename across calls.

        Previously a timestamp suffix made every call produce a unique filename,
        breaking PDF cache dedup and leaving orphan files in vault/PDFs on
        --force reprocessing."""
        fetcher = WebFetcher()
        url = "https://example.com/papers/attention.pdf"
        assert fetcher._generate_pdf_filename_from_url(url) == \
            fetcher._generate_pdf_filename_from_url(url)

    def test_pdf_from_url_returns_empty_content(self):
        fetcher = WebFetcher(vault_path=None)
        metadata, content = fetcher._handle_pdf_from_url(
            "https://example.com/paper.pdf",
            b"%PDF-1.4\n%dummy",
        )
        assert content == ""
        assert metadata.source == "pdf_from_web"

    def test_pdf_from_url_has_no_faked_date(self):
        """Regression for #14: published_date must be None when not extracted."""
        fetcher = WebFetcher(vault_path=None)
        metadata, _ = fetcher._handle_pdf_from_url(
            "https://example.com/paper.pdf",
            b"%PDF-1.4\n%dummy",
        )
        assert metadata.published_date is None


# ---------------------------------------------------------------------------
# Integration tests with mocked HTTP
# ---------------------------------------------------------------------------

class TestFetchWithMockedHttp:
    """Full fetch() calls with HTTP mocked out."""

    # Needs to exceed WebFetcher.MIN_CONTENT_LENGTH (500 chars) after HTML→markdown
    GOOD_HTML = """
        <html>
            <head>
                <meta property="og:title" content="Test Article">
                <meta property="article:author" content="John Doe">
                <meta property="article:published_time" content="2024-01-15T10:30:00Z">
            </head>
            <body>
                <article>
                    <h1>Test Article</h1>
                    <p>This is a test article with enough content to pass the minimum length check.
                    We need a fair amount of prose here because the MIN_CONTENT_LENGTH is 500 characters
                    and HTML-to-markdown conversion strips tags, so the raw HTML must be substantially
                    longer than the threshold to survive the conversion.</p>
                    <p>Second paragraph adds more content so we exceed 500 characters easily. The quick
                    brown fox jumped over the lazy dog. Sphinx of black quartz judge my vow. Pack my
                    box with five dozen liquor jugs. How vexingly quick daft zebras jump.</p>
                    <p>Third paragraph: lorem ipsum dolor sit amet consectetur adipiscing elit sed do
                    eiusmod tempor incididunt ut labore et dolore magna aliqua ut enim ad minim veniam
                    quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
                </article>
            </body>
        </html>
    """.encode("utf-8")

    def _mock_head(self, content_type="text/html; charset=utf-8"):
        resp = Mock()
        resp.headers = {"content-type": content_type}
        resp.status_code = 200
        return resp

    def _mock_get(self, content, content_type="text/html"):
        resp = Mock()
        resp.content = content
        resp.headers = {"content-type": content_type}
        resp.encoding = "utf-8"
        resp.raise_for_status = Mock()
        return resp

    @patch("paper_library.web_fetcher.requests.head")
    @patch("paper_library.web_fetcher.requests.get")
    def test_fetch_html_article_returns_metadata_and_content(self, mock_get, mock_head):
        mock_head.return_value = self._mock_head()
        mock_get.return_value = self._mock_get(self.GOOD_HTML)

        metadata, content = WebFetcher().fetch("https://example.com/article")

        assert isinstance(metadata, ArticleMetadata)
        assert metadata.title == "Test Article"
        assert "John Doe" in metadata.authors
        assert metadata.published_date is not None
        assert len(content) > 500
        assert "test article" in content.lower()

    @patch("paper_library.web_fetcher.requests.head")
    @patch("paper_library.web_fetcher.requests.get")
    def test_fetch_pdf_from_url(self, mock_get, mock_head):
        mock_head.return_value = self._mock_head("application/pdf")
        mock_get.return_value = self._mock_get(b"%PDF-1.4\n%dummy", "application/pdf")

        metadata, content = WebFetcher().fetch("https://example.com/paper.pdf")

        assert metadata.source == "pdf_from_web"
        assert content == ""

    @patch("paper_library.web_fetcher.requests.head")
    def test_fetch_twitter_raises_unsupported_without_http(self, mock_head):
        with pytest.raises(UnsupportedSourceError) as exc_info:
            WebFetcher().fetch("https://twitter.com/user/status/123456")
        mock_head.assert_not_called()
        assert "Twitter" in str(exc_info.value) or "thread" in str(exc_info.value).lower()

    @patch("paper_library.web_fetcher.requests.head")
    @patch("paper_library.web_fetcher.requests.get")
    def test_fetch_too_short_content_raises(self, mock_get, mock_head):
        short_html = b"""
        <html><head><meta property="og:title" content="Stub"></head>
        <body><article>Hi.</article></body></html>
        """
        mock_head.return_value = self._mock_head()
        mock_get.return_value = self._mock_get(short_html)

        with pytest.raises(TooShortError):
            WebFetcher().fetch("https://example.com/stub")

    @patch("paper_library.web_fetcher.requests.head")
    def test_fetch_timeout_raises_web_fetch_error(self, mock_head):
        mock_head.side_effect = requests.Timeout("timed out")

        with pytest.raises(WebFetchError) as exc_info:
            WebFetcher().fetch("https://slow.example.com/article")
        assert "timed out" in str(exc_info.value).lower()

    @patch("paper_library.web_fetcher.requests.head")
    @patch("paper_library.web_fetcher.requests.get")
    def test_fetch_404_raises_web_fetch_error(self, mock_get, mock_head):
        mock_head.return_value = self._mock_head()
        resp_404 = Mock()
        resp_404.headers = {"content-type": "text/html"}
        err = requests.HTTPError()
        err.response = Mock()
        err.response.status_code = 404
        resp_404.raise_for_status.side_effect = err
        mock_get.return_value = resp_404

        with pytest.raises(WebFetchError) as exc_info:
            WebFetcher().fetch("https://example.com/gone")
        assert "404" in str(exc_info.value)

    def test_invalid_url_raises_web_fetch_error(self):
        with pytest.raises(WebFetchError):
            WebFetcher().fetch("not-a-valid-url")


# ---------------------------------------------------------------------------
# Integration tests — real network (marked, skipped by default)
# ---------------------------------------------------------------------------

class TestRealNetwork:
    """Live network tests. Run with: pytest -m integration"""

    @pytest.mark.integration
    def test_fetch_transformer_circuits_article(self):
        """Mechanistic Interpretability essay — server-rendered Distill-style HTML."""
        fetcher = WebFetcher()
        metadata, content = fetcher.fetch(
            "https://transformer-circuits.pub/2022/mech-interp-essay/index.html"
        )
        assert metadata.title
        assert len(content) > 1000

    @pytest.mark.integration
    def test_fetch_distill_article(self):
        """Distill.pub article — canonical Distill-style HTML."""
        fetcher = WebFetcher()
        metadata, content = fetcher.fetch("https://distill.pub/2021/gnn-intro/")
        assert metadata.title
        assert len(content) > 1000
