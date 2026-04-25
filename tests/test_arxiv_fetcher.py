"""
Unit and integration tests for arXiv fetcher.

Run all tests: pytest tests/test_arxiv_fetcher.py
Run only unit tests: pytest tests/test_arxiv_fetcher.py -m "not integration"
Run only integration tests: pytest tests/test_arxiv_fetcher.py -m integration
"""

import pytest
from pathlib import Path
from unittest.mock import patch, Mock

from paper_library.config import config
from paper_library.arxiv_fetcher import ArxivFetcher, ArxivError, _cached_pdf_is_valid
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

        assert pdf_path.name.startswith("arxiv_")
        assert pdf_path.name.endswith(".pdf")

    @pytest.mark.integration
    def test_fetch_sets_metadata_fields(self, fetcher):
        """Test that all important metadata fields are populated"""
        pdf_path, metadata = fetcher.fetch("1706.03762")

        assert metadata.arxiv_id == "1706.03762"
        assert metadata.source == "arxiv"
        assert metadata.pdf_path is not None

    @pytest.mark.integration
    def test_fetch_with_version_suffix(self, fetcher):
        """Test that fetch works with versioned arXiv IDs"""
        pdf_path, metadata = fetcher.fetch("1706.03762v2")

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
        pdf_path1, metadata1 = fetcher.fetch("1706.03762")
        original_mtime = pdf_path1.stat().st_mtime

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

        for author in metadata.authors:
            assert "," in author or len(author.split()) == 1

    @pytest.mark.integration
    def test_multiple_authors(self, fetcher):
        """Test that papers with multiple authors are handled"""
        pdf_path, metadata = fetcher.fetch("1706.03762")

        assert len(metadata.authors) > 1


class TestExtractAuthorsUnit:
    """Unit tests for _extract_authors() — no network needed."""

    NS = "http://www.w3.org/2005/Atom"

    def _make_entry(self, names: list) -> "etree._Element":
        from lxml import etree
        entry = etree.Element(f"{{{self.NS}}}entry")
        for name in names:
            author = etree.SubElement(entry, f"{{{self.NS}}}author")
            name_el = etree.SubElement(author, f"{{{self.NS}}}name")
            name_el.text = name
        return entry

    @pytest.fixture
    def fetcher(self, tmp_path):
        return ArxivFetcher(tmp_path)

    def test_plain_two_part_name(self, fetcher):
        entry = self._make_entry(["John Smith"])
        assert fetcher._extract_authors(entry) == ["Smith, John"]

    def test_three_part_name(self, fetcher):
        entry = self._make_entry(["Mary Jane Watson"])
        assert fetcher._extract_authors(entry) == ["Watson, Mary Jane"]

    def test_suffix_jr_stays_with_surname(self, fetcher):
        entry = self._make_entry(["John Smith Jr."])
        result = fetcher._extract_authors(entry)
        assert result == ["Smith Jr., John"]

    def test_suffix_sr_stays_with_surname(self, fetcher):
        entry = self._make_entry(["Robert Jones Sr."])
        result = fetcher._extract_authors(entry)
        assert result == ["Jones Sr., Robert"]

    def test_suffix_roman_numeral(self, fetcher):
        entry = self._make_entry(["James Brown III"])
        result = fetcher._extract_authors(entry)
        assert result == ["Brown III, James"]

    def test_honorific_dr_stripped(self, fetcher):
        entry = self._make_entry(["Dr. Jane Doe"])
        result = fetcher._extract_authors(entry)
        assert result == ["Doe, Jane"]

    def test_honorific_prof_stripped(self, fetcher):
        entry = self._make_entry(["Prof. Alan Turing"])
        result = fetcher._extract_authors(entry)
        assert result == ["Turing, Alan"]

    def test_single_name_returned_as_is(self, fetcher):
        entry = self._make_entry(["Madonna"])
        assert fetcher._extract_authors(entry) == ["Madonna"]

    def test_multiple_authors(self, fetcher):
        entry = self._make_entry(["Alice Smith", "Bob Jones Jr."])
        result = fetcher._extract_authors(entry)
        assert result == ["Smith, Alice", "Jones Jr., Bob"]

    def test_empty_entry_returns_empty_list(self, fetcher):
        from lxml import etree
        entry = etree.Element(f"{{{self.NS}}}entry")
        assert fetcher._extract_authors(entry) == []


class TestCachedPdfIsValid:
    """Unit tests for _cached_pdf_is_valid() helper."""

    def test_valid_pdf_returns_true(self, tmp_path):
        p = tmp_path / "paper.pdf"
        p.write_bytes(b"%PDF-1.4\n" + b"x" * 2000)
        assert _cached_pdf_is_valid(p) is True

    def test_zero_byte_file_returns_false(self, tmp_path):
        p = tmp_path / "empty.pdf"
        p.write_bytes(b"")
        assert _cached_pdf_is_valid(p) is False

    def test_too_small_returns_false(self, tmp_path):
        p = tmp_path / "tiny.pdf"
        p.write_bytes(b"%PDF-1.4\n" + b"x" * 10)
        assert _cached_pdf_is_valid(p) is False

    def test_wrong_magic_bytes_returns_false(self, tmp_path):
        p = tmp_path / "html.pdf"
        p.write_bytes(b"<html>" + b"x" * 2000)
        assert _cached_pdf_is_valid(p) is False

    def test_missing_file_returns_false(self, tmp_path):
        p = tmp_path / "nonexistent.pdf"
        assert _cached_pdf_is_valid(p) is False


class TestDownloadPdfCacheVerification:
    """_download_pdf must re-download if the cached file is corrupt/truncated."""

    @pytest.fixture
    def fetcher(self, tmp_path):
        f = ArxivFetcher(tmp_path)
        # Ensure PDFs subdirectory exists (ArxivFetcher creates it in __init__)
        return f

    def _make_mock_response(self, content: bytes):
        resp = Mock()
        resp.iter_content = lambda chunk_size: [content]
        resp.raise_for_status = Mock()
        return resp

    def test_corrupt_cache_is_replaced(self, fetcher, tmp_path):
        """A zero-byte cached file should trigger a re-download."""
        arxiv_id = "1706.03762"
        pdf_filename = f"arxiv_{arxiv_id.replace('/', '_')}.pdf"
        pdf_path = fetcher.pdfs_dir / pdf_filename

        # Place a corrupt (zero-byte) file in the cache
        pdf_path.write_bytes(b"")

        valid_pdf = b"%PDF-1.4\n" + b"x" * 2000

        with patch("paper_library.arxiv_fetcher.requests.get") as mock_get:
            mock_get.return_value = self._make_mock_response(valid_pdf)
            result = fetcher._download_pdf(arxiv_id)

        # File should now be the valid PDF
        assert result.read_bytes() == valid_pdf
        mock_get.assert_called_once()

    def test_valid_cache_is_not_re_downloaded(self, fetcher, tmp_path):
        """A valid cached file must be returned without hitting the network."""
        arxiv_id = "1706.03762"
        pdf_filename = f"arxiv_{arxiv_id.replace('/', '_')}.pdf"
        pdf_path = fetcher.pdfs_dir / pdf_filename

        valid_pdf = b"%PDF-1.4\n" + b"x" * 2000
        pdf_path.write_bytes(valid_pdf)

        with patch("paper_library.arxiv_fetcher.requests.get") as mock_get:
            result = fetcher._download_pdf(arxiv_id)

        mock_get.assert_not_called()
        assert result == pdf_path
