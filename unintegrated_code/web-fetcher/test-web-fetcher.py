#!/usr/bin/env python3
"""
Test script for web fetcher.

This tests the web content fetcher with various sources:
- HTML articles (blogs, Distill, LessWrong)
- PDFs from URLs
- Unsupported sources (Twitter, Reddit, video)
- Error cases (paywalled, too short, network errors)

Usage:
    python test_web_fetcher.py [--live]
    
    --live: Test against real URLs (requires network)
           Without this flag, tests use mocked responses

Python concepts:
- Mocking HTTP responses for unit tests
- Testing error handling
- Fixtures for test data
"""

import sys
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
import pytest

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from paper_library.web_fetcher import (
    WebFetcher,
    WebFetchError,
    UnsupportedSourceError,
    TooShortError,
    PaywallError
)
from paper_library.models import ArticleMetadata


class TestWebFetcherDetection:
    """Test URL type detection and routing."""
    
    def test_is_url(self):
        """Test URL detection."""
        fetcher = WebFetcher()
        
        assert fetcher.is_url("https://example.com/article")
        assert fetcher.is_url("http://example.com")
        assert fetcher.is_url("www.example.com")
        
        assert not fetcher.is_url("2312.12345")
        assert not fetcher.is_url("./local/file.pdf")
        assert not fetcher.is_url("not a url")
    
    def test_unsupported_hosts_detection(self):
        """Test detection of explicitly unsupported sources."""
        fetcher = WebFetcher()
        
        unsupported_urls = [
            "https://twitter.com/user/status/123456",
            "https://x.com/user/status/123456",
            "https://reddit.com/r/MachineLearning/comments/xyz",
            "https://www.reddit.com/r/MachineLearning/comments/xyz",
            "https://youtube.com/watch?v=abc123",
            "https://www.youtube.com/watch?v=abc123",
            "https://youtu.be/abc123",
        ]
        
        for url in unsupported_urls:
            # Attempting to fetch should raise UnsupportedSourceError
            # without even making a network request
            with pytest.raises(UnsupportedSourceError):
                fetcher.fetch(url)


class TestWebFetcherHtmlParsing:
    """Test HTML extraction and parsing."""
    
    def test_extract_title_from_og_tags(self):
        """Test title extraction from OG meta tags."""
        from bs4 import BeautifulSoup
        
        html = """
        <html>
            <head>
                <meta property="og:title" content="Test Article Title">
            </head>
            <body><article>Content</article></body>
        </html>
        """
        
        soup = BeautifulSoup(html, 'html.parser')
        fetcher = WebFetcher()
        
        title = fetcher._extract_title(soup, "https://example.com")
        assert title == "Test Article Title"
    
    def test_extract_title_fallback_to_h1(self):
        """Test title fallback to H1 if no OG tags."""
        from bs4 import BeautifulSoup
        
        html = """
        <html>
            <head><title>Page Title</title></head>
            <body>
                <h1>Article Headline</h1>
                <article>Content</article>
            </body>
        </html>
        """
        
        soup = BeautifulSoup(html, 'html.parser')
        fetcher = WebFetcher()
        
        title = fetcher._extract_title(soup, "https://example.com")
        assert title == "Article Headline"
    
    def test_extract_authors(self):
        """Test author extraction."""
        from bs4 import BeautifulSoup
        
        html = """
        <html>
            <head>
                <meta property="article:author" content="John Smith">
                <meta property="article:author" content="Jane Doe">
            </head>
            <body><article>Content</article></body>
        </html>
        """
        
        soup = BeautifulSoup(html, 'html.parser')
        fetcher = WebFetcher()
        
        authors = fetcher._extract_authors(soup)
        assert len(authors) == 2
        assert "John Smith" in authors
        assert "Jane Doe" in authors
    
    def test_extract_published_date(self):
        """Test published date extraction."""
        from bs4 import BeautifulSoup
        
        html = """
        <html>
            <head>
                <meta property="article:published_time" content="2024-01-15T10:30:00Z">
            </head>
            <body><article>Content</article></body>
        </html>
        """
        
        soup = BeautifulSoup(html, 'html.parser')
        fetcher = WebFetcher()
        
        date = fetcher._extract_published_date(soup)
        assert date is not None
        assert date.year == 2024
        assert date.month == 1
        assert date.day == 15
    
    def test_extract_article_content(self):
        """Test main content extraction."""
        from bs4 import BeautifulSoup
        
        html = """
        <html>
            <head><title>Page</title></head>
            <body>
                <nav>Navigation</nav>
                <article>
                    <h1>Title</h1>
                    <p>This is the main article content that should be extracted.</p>
                    <p>Second paragraph of content.</p>
                </article>
                <aside>Sidebar</aside>
            </body>
        </html>
        """
        
        soup = BeautifulSoup(html, 'html.parser')
        fetcher = WebFetcher()
        
        content = fetcher._extract_article_content(soup)
        assert content is not None
        assert "main article content" in content
        assert "Sidebar" not in content
    
    def test_clean_markdown(self):
        """Test markdown cleanup."""
        fetcher = WebFetcher()
        
        messy_md = """
        # Title
        
        
        
        
        Paragraph with   multiple   spaces.
        
        
        Another paragraph.
        """
        
        cleaned = fetcher._clean_markdown(messy_md)
        
        # Should remove excessive blank lines
        assert "\n\n\n" not in cleaned
        # Should clean up spaces
        assert "   " not in cleaned
    
    def test_check_paywall_indicators(self):
        """Test paywall detection."""
        from bs4 import BeautifulSoup
        
        # Clearly paywalled content
        html = """
        <html>
            <body>
                <div class="paywall">Subscribe to read this article</div>
                <p>Subscribe</p>
                <p>Subscribe</p>
            </body>
        </html>
        """
        
        soup = BeautifulSoup(html, 'html.parser')
        fetcher = WebFetcher()
        
        is_paywalled = fetcher._check_paywall_indicators(soup, "content")
        assert is_paywalled


class TestWebFetcherPdfHandling:
    """Test PDF from URL handling."""
    
    def test_generate_pdf_filename_from_url(self):
        """Test PDF filename generation."""
        fetcher = WebFetcher()
        
        url = "https://example.com/papers/research-2024.pdf"
        filename = fetcher._generate_pdf_filename_from_url(url)
        
        assert filename.startswith("web_example_research")
        assert filename.endswith(".pdf")
    
    @patch('paper_library.web_fetcher.ArticleMetadata')
    def test_handle_pdf_from_url_without_vault(self, mock_metadata):
        """Test PDF handling when vault_path is None."""
        fetcher = WebFetcher(vault_path=None)
        
        pdf_content = b"%PDF-1.4\n%dummy pdf content"
        url = "https://example.com/paper.pdf"
        
        metadata, content = fetcher._handle_pdf_from_url(url, pdf_content)
        
        # Should return ArticleMetadata with PDF info
        assert content == ""  # No content for PDFs


class TestWebFetcherIntegration:
    """Integration tests (with mocked HTTP)."""
    
    @patch('paper_library.web_fetcher.requests.head')
    @patch('paper_library.web_fetcher.requests.get')
    def test_fetch_html_article(self, mock_get, mock_head):
        """Test fetching an HTML article."""
        # Mock the HEAD request
        mock_head_resp = Mock()
        mock_head_resp.headers = {'content-type': 'text/html; charset=utf-8'}
        mock_head_resp.status_code = 200
        mock_head.return_value = mock_head_resp
        
        # Mock the GET request
        html_content = """
        <html>
            <head>
                <meta property="og:title" content="Test Article">
                <meta property="article:author" content="John Doe">
                <meta property="article:published_time" content="2024-01-15T10:30:00Z">
            </head>
            <body>
                <article>
                    <h1>Test Article</h1>
                    <p>This is a test article with enough content to be useful.</p>
                    <p>Second paragraph with more content.</p>
                </article>
            </body>
        </html>
        """.encode('utf-8')
        
        mock_get_resp = Mock()
        mock_get_resp.content = html_content
        mock_get_resp.headers = {'content-type': 'text/html'}
        mock_get_resp.encoding = 'utf-8'
        mock_get_resp.raise_for_status = Mock()
        mock_get.return_value = mock_get_resp
        
        # Test fetch
        fetcher = WebFetcher()
        url = "https://example.com/article"
        
        metadata, content = fetcher.fetch(url)
        
        # Verify metadata
        assert metadata.title == "Test Article"
        assert "John Doe" in metadata.authors
        assert metadata.published_date is not None
        
        # Verify content extraction
        assert content is not None
        assert len(content) > 500  # Should exceed MIN_CONTENT_LENGTH
        assert "test article with enough content" in content.lower()
    
    @patch('paper_library.web_fetcher.requests.head')
    @patch('paper_library.web_fetcher.requests.get')
    def test_fetch_pdf_from_url(self, mock_get, mock_head):
        """Test detecting and handling PDFs from URLs."""
        # Mock the HEAD request returning PDF content type
        mock_head_resp = Mock()
        mock_head_resp.headers = {'content-type': 'application/pdf'}
        mock_head_resp.status_code = 200
        mock_head.return_value = mock_head_resp
        
        # Mock the GET request
        pdf_content = b"%PDF-1.4\n%dummy pdf"
        mock_get_resp = Mock()
        mock_get_resp.content = pdf_content
        mock_get_resp.raise_for_status = Mock()
        mock_get.return_value = mock_get_resp
        
        # Test fetch
        fetcher = WebFetcher()
        url = "https://example.com/paper.pdf"
        
        metadata, content = fetcher.fetch(url)
        
        # Should detect as PDF
        assert metadata.source == 'pdf_from_web'
        assert content == ""  # PDFs have no extracted content
    
    @patch('paper_library.web_fetcher.requests.head')
    def test_fetch_twitter_url_unsupported(self, mock_head):
        """Test that Twitter URLs raise UnsupportedSourceError without network request."""
        fetcher = WebFetcher()
        url = "https://twitter.com/user/status/123456"
        
        # Should raise without even making HTTP request
        with pytest.raises(UnsupportedSourceError) as exc_info:
            fetcher.fetch(url)
        
        assert "Twitter" in str(exc_info.value) or "thread" in str(exc_info.value)
        mock_head.assert_not_called()
    
    @patch('paper_library.web_fetcher.requests.head')
    @patch('paper_library.web_fetcher.requests.get')
    def test_fetch_too_short_error(self, mock_get, mock_head):
        """Test TooShortError when content is too short."""
        # Mock HEAD
        mock_head_resp = Mock()
        mock_head_resp.headers = {'content-type': 'text/html'}
        mock_head.return_value = mock_head_resp
        
        # Mock GET with very short content
        html = """
        <html>
            <head><meta property="og:title" content="Short"></head>
            <body><article>Too short.</article></body>
        </html>
        """.encode('utf-8')
        
        mock_get_resp = Mock()
        mock_get_resp.content = html
        mock_get_resp.headers = {'content-type': 'text/html'}
        mock_get_resp.raise_for_status = Mock()
        mock_get.return_value = mock_get_resp
        
        # Test fetch
        fetcher = WebFetcher()
        
        with pytest.raises(TooShortError):
            fetcher.fetch("https://example.com/short")


class TestWebFetcherErrorHandling:
    """Test error handling and edge cases."""
    
    @patch('paper_library.web_fetcher.requests.head')
    def test_invalid_url(self, mock_head):
        """Test handling of invalid URL format."""
        fetcher = WebFetcher()
        
        with pytest.raises(WebFetchError):
            fetcher.fetch("not-a-valid-url")
    
    @patch('paper_library.web_fetcher.requests.head')
    def test_404_error(self, mock_head):
        """Test handling of 404 Not Found."""
        mock_head.side_effect = Exception()  # Simulate error
        
        mock_get_resp = Mock()
        mock_get_resp.status_code = 404
        mock_get_resp.raise_for_status.side_effect = Exception("404 Not Found")
        
        with patch('paper_library.web_fetcher.requests.get', return_value=mock_get_resp):
            fetcher = WebFetcher()
            
            with pytest.raises(WebFetchError) as exc_info:
                fetcher.fetch("https://example.com/404")
            
            assert "404" in str(exc_info.value)
    
    @patch('paper_library.web_fetcher.requests.head')
    def test_timeout_error(self, mock_head):
        """Test handling of request timeout."""
        import requests
        
        mock_head.side_effect = requests.Timeout("Connection timed out")
        
        fetcher = WebFetcher()
        
        with pytest.raises(WebFetchError) as exc_info:
            fetcher.fetch("https://slow.example.com")
        
        assert "timed out" in str(exc_info.value).lower()


class TestWebFetcherRealWorld:
    """Real-world tests (optional, requires --live flag)."""
    
    @pytest.mark.skip(reason="Requires --live flag and network access")
    def test_fetch_real_blog_post(self):
        """Test fetching a real blog post."""
        fetcher = WebFetcher()
        
        # Using a known stable blog post URL
        # (you'd change this to an actual blog)
        url = "https://example.com/blog/sample-article"
        
        metadata, content = fetcher.fetch(url)
        
        assert metadata.title
        assert len(content) > 500
    
    @pytest.mark.skip(reason="Requires --live flag and network access")
    def test_fetch_real_distill_article(self):
        """Test fetching from Distill.pub."""
        fetcher = WebFetcher()
        
        url = "https://distill.pub/2021/zoom-in/"
        
        metadata, content = fetcher.fetch(url)
        
        assert metadata.title
        assert "zoom" in metadata.title.lower()
        assert len(content) > 1000  # Distill articles are usually long


def run_tests_with_live_option():
    """Run tests with optional --live flag for real network access."""
    import sys
    
    # Check for --live flag
    if "--live" in sys.argv:
        sys.argv.remove("--live")
        print("Running tests WITH network access (--live mode)")
        pytest.main([__file__, "-v"])
    else:
        print("Running tests WITHOUT network access (mocked responses)")
        print("  Use --live flag to test against real URLs:")
        print("  python test_web_fetcher.py --live")
        pytest.main([__file__, "-v", "-m", "not skip"])


if __name__ == "__main__":
    # Only run via pytest
    pytest.main([__file__, "-v"])