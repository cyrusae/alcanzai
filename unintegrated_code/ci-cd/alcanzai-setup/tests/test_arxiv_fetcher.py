"""
Unit and integration tests for arXiv fetcher.

Run all tests: pytest tests/test_arxiv_fetcher.py
Run only unit tests: pytest tests/test_arxiv_fetcher.py -m "not integration"
Run only integration tests: pytest tests/test_arxiv_fetcher.py -m integration
"""

import pytest
from pathlib import Path

from paper_library.config import config
from paper_library.arxiv_fetcher import ArxivFetcher, ArxivError
from paper_library.models import PaperMetadata


class TestArxivIdParsing:
    """Tests for arXiv ID parsing (unit tests, fast)"""
    
    @pytest.fixture
    def fetcher(self):
        """Create a fetcher instance for each test"""
        return ArxivFetcher(config.vault_path)
    
    def test_parse_new_style_id(self, fetcher):
        """Test parsing modern arXiv ID format (YYMM.NNNNN)"""
        assert fetcher.parse_arxiv_id("2312.12345") == "2312.12345"
    
    def test_parse_with_version_suffix(self, fetcher):
        """Test that version suffix is stripped (YYMM.NNNNNvX)"""
        assert fetcher.parse_arxiv_id("1706.03762v2") == "1706.03762"
    
    def test_parse_from_abs_url(self, fetcher):
        """Test extracting ID from arXiv abstract URL"""
        url = "https://arxiv.org/abs/1706.03762"
        assert fetcher.parse_arxiv_id(url) == "1706.03762"
    
    def test_parse_from_pdf_url(self, fetcher):
        """Test extracting ID from arXiv PDF download URL"""
        url = "https://arxiv.org/pdf/1706.03762.pdf"
        assert fetcher.parse_arxiv_id(url) == "1706.03762"
    
    def test_parse_with_arxiv_prefix(self, fetcher):
        """Test extracting ID from 'arxiv:' prefixed string"""
        assert fetcher.parse_arxiv_id("arxiv:2312.12345") == "2312.12345"
    
    def test_parse_case_insensitive_prefix(self, fetcher):
        """Test that 'arXiv:' prefix (mixed case) is handled"""
        assert fetcher.parse_arxiv_id("arXiv:1706.03762") == "1706.03762"
    
    def test_parse_old_style_id(self, fetcher):
        """Test parsing legacy arXiv ID format (archive/YYMMNNN)"""
        # Old format: cs/0703001
        result = fetcher.parse_arxiv_id("cs/0703001")
        assert result == "cs/0703001"
    
    def test_parse_invalid_id_returns_none(self, fetcher):
        """Test that invalid IDs return None"""
        assert fetcher.parse_arxiv_id("not-an-id") is None
        assert fetcher.parse_arxiv_id("") is None
    
    def test_parse_with_whitespace(self, fetcher):
        """Test that leading/trailing whitespace is handled"""
        assert fetcher.parse_arxiv_id("  2312.12345  ") == "2312.12345"


class TestArxivFetching:
    """Tests for arXiv metadata and PDF fetching (integration tests, slow)"""
    
    @pytest.fixture
    def fetcher(self):
        """Create a fetcher instance"""
        return ArxivFetcher(config.vault_path)
    
    @pytest.mark.integration
    def test_fetch_valid_paper_metadata(self, fetcher):
        """Test fetching metadata from arXiv API for a well-known paper"""
        # "Attention Is All You Need" - won't be removed anytime soon
        pdf_path, metadata = fetcher.fetch("1706.03762")
        
        # Verify metadata was extracted correctly
        assert metadata.title is not None
        assert "Attention" in metadata.title.lower() or "Transformer" in metadata.title
        assert len(metadata.authors) >= 2
        assert metadata.year == 2017
        assert metadata.abstract is not None
        assert len(metadata.abstract) > 50
    
    @pytest.mark.integration
    def test_fetch_returns_correct_types(self, fetcher):
        """Test that fetch returns the expected types"""
        pdf_path, metadata = fetcher.fetch("1706.03762")
        
        assert isinstance(pdf_path, Path)
        assert isinstance(metadata, PaperMetadata)
    
    @pytest.mark.integration
    def test_fetch_downloads_pdf(self, fetcher):
        """Test that the PDF file is actually downloaded and exists"""
        pdf_path, metadata = fetcher.fetch("1706.03762")
        
        assert pdf_path.exists()
        assert pdf_path.is_file()
        # PDF should be reasonably large (at least 100KB)
        assert pdf_path.stat().st_size > 100000
    
    @pytest.mark.integration
    def test_fetch_pdf_filename_format(self, fetcher):
        """Test that PDF is saved with correct naming convention"""
        pdf_path, metadata = fetcher.fetch("1706.03762")
        
        # Should follow pattern: arxiv_YYMM.NNNNN.pdf
        assert pdf_path.name.startswith("arxiv_")
        assert pdf_path.name.endswith(".pdf")
    
    @pytest.mark.integration
    def test_fetch_sets_metadata_fields(self, fetcher):
        """Test that all important metadata fields are populated"""
        pdf_path, metadata = fetcher.fetch("1706.03762")
        
        # These should be set by the fetcher
        assert metadata.arxiv_id == "1706.03762"
        assert metadata.source == "arxiv"
        assert metadata.pdf_path is not None
    
    @pytest.mark.integration
    def test_fetch_with_version_suffix(self, fetcher):
        """Test that fetch works with versioned arXiv IDs"""
        # Fetch should strip version and work anyway
        pdf_path, metadata = fetcher.fetch("1706.03762v2")
        
        # Should have fetched the paper
        assert metadata.title is not None
        assert metadata.arxiv_id == "1706.03762"  # Version stripped
    
    @pytest.mark.integration
    def test_fetch_invalid_id_raises_error(self, fetcher):
        """Test that fetching an invalid ID raises ArxivError"""
        with pytest.raises(ArxivError):
            fetcher.fetch("0000.00000")  # Non-existent paper
    
    @pytest.mark.integration
    def test_fetch_skips_already_downloaded_pdf(self, fetcher):
        """Test that fetching twice doesn't re-download PDF"""
        # First fetch
        pdf_path1, metadata1 = fetcher.fetch("1706.03762")
        original_mtime = pdf_path1.stat().st_mtime
        
        # Second fetch - should skip downloading
        pdf_path2, metadata2 = fetcher.fetch("1706.03762")
        
        assert pdf_path1 == pdf_path2
        assert pdf_path2.stat().st_mtime == original_mtime  # File wasn't rewritten


class TestArxivAuthorsFormatting:
    """Tests for author name formatting from arXiv API"""
    
    @pytest.fixture
    def fetcher(self):
        return ArxivFetcher(config.vault_path)
    
    @pytest.mark.integration
    def test_authors_formatted_correctly(self, fetcher):
        """Test that authors are formatted as 'Lastname, Firstname'"""
        pdf_path, metadata = fetcher.fetch("1706.03762")
        
        # Authors from arXiv come as "Firstname Lastname"
        # We should format them as "Lastname, Firstname"
        for author in metadata.authors:
            # Each author should have comma (or be single-name, which is rare)
            assert "," in author or len(author.split()) == 1
    
    @pytest.mark.integration
    def test_multiple_authors(self, fetcher):
        """Test that papers with multiple authors are handled"""
        pdf_path, metadata = fetcher.fetch("1706.03762")
        
        # This paper has multiple authors
        assert len(metadata.authors) > 1
