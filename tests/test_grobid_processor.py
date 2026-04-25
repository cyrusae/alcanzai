"""
Tests for GROBID PDF processor.

Run all tests: pytest tests/test_grobid_processor.py
Run only unit tests: pytest tests/test_grobid_processor.py -m "not integration"
Run only integration: pytest tests/test_grobid_processor.py -m integration
"""

import pytest
from pathlib import Path

from paper_library.config import config
from paper_library.grobid_processor import GrobidProcessor, GrobidError
from paper_library.models import PaperMetadata, Citation


class TestGrobidConnection:
    """Tests for GROBID service connectivity (unit tests, fast)"""

    @pytest.fixture
    def processor(self):
        """Create processor instance"""
        return GrobidProcessor(config.grobid_url)

    def test_processor_initialized_with_url(self, processor):
        """Test that processor stores GROBID URL correctly"""
        assert processor.grobid_url is not None
        assert "localhost" in processor.grobid_url or "8070" in processor.grobid_url

    def test_api_endpoint_url_constructed(self, processor):
        """Test that API endpoint URL is constructed correctly"""
        assert processor.api_url.endswith("/api/processFulltextDocument")

    @pytest.mark.integration
    def test_grobid_service_is_running(self, processor):
        """Test that GROBID service is reachable and running"""
        import requests

        try:
            response = requests.get(f"{processor.grobid_url}/api/isalive", timeout=5)
            assert response.status_code == 200
        except requests.ConnectionError:
            pytest.skip("GROBID service not running - start with: docker-compose up -d")


class TestGrobidFileHandling:
    """Tests for file handling and validation (unit tests, fast)"""

    @pytest.fixture
    def processor(self):
        return GrobidProcessor(config.grobid_url)

    def test_missing_file_raises_file_not_found(self, processor):
        """Test that processing non-existent file raises FileNotFoundError"""
        with pytest.raises(FileNotFoundError):
            processor.process(Path("/nonexistent/paper.pdf"))


class TestGrobidMetadataExtraction:
    """Tests for XML parsing and metadata extraction (integration tests, requires PDF)"""

    @pytest.fixture
    def processor(self):
        return GrobidProcessor(config.grobid_url)

    @pytest.fixture
    def sample_pdf_path(self):
        """Get path to a sample PDF for testing.

        Place any real academic paper PDF at tests/fixtures/sample.pdf.
        See tests/fixtures/README.md for details.
        """
        path = Path(__file__).parent / "fixtures" / "sample.pdf"
        if not path.exists():
            pytest.skip(f"Sample PDF not found at {path} - see tests/fixtures/README.md")
        return path

    @pytest.mark.integration
    def test_extract_title(self, processor, sample_pdf_path):
        """Test that paper title is extracted"""
        metadata = processor.process(sample_pdf_path)

        assert metadata.title is not None
        assert len(metadata.title) > 0
        assert len(metadata.title) < 500

    @pytest.mark.integration
    def test_extract_authors(self, processor, sample_pdf_path):
        """Test that author names are extracted"""
        metadata = processor.process(sample_pdf_path)

        assert len(metadata.authors) > 0
        for author in metadata.authors:
            assert len(author) > 2
            assert len(author) < 200

    @pytest.mark.integration
    def test_extract_year(self, processor, sample_pdf_path):
        """Test that publication year is extracted"""
        metadata = processor.process(sample_pdf_path)

        assert metadata.year is not None
        assert 1950 < metadata.year < 2030

    @pytest.mark.integration
    def test_extract_abstract(self, processor, sample_pdf_path):
        """Test that abstract is extracted (if present)"""
        metadata = processor.process(sample_pdf_path)

        if metadata.abstract:
            assert len(metadata.abstract) > 50

    @pytest.mark.integration
    def test_returns_paper_metadata_object(self, processor, sample_pdf_path):
        """Test that processing returns proper PaperMetadata object"""
        metadata = processor.process(sample_pdf_path)

        assert isinstance(metadata, PaperMetadata)
        assert isinstance(metadata.authors, list)
        assert isinstance(metadata.citations, list)

    @pytest.mark.integration
    def test_stores_pdf_path(self, processor, sample_pdf_path):
        """Test that PDF path is stored in metadata"""
        metadata = processor.process(sample_pdf_path)

        assert metadata.pdf_path is not None
        assert str(sample_pdf_path) in metadata.pdf_path


class TestGrobidCitationExtraction:
    """Tests for bibliography citation extraction (integration tests)"""

    @pytest.fixture
    def processor(self):
        return GrobidProcessor(config.grobid_url)

    @pytest.fixture
    def sample_pdf_path(self):
        path = Path(__file__).parent / "fixtures" / "sample.pdf"
        if not path.exists():
            pytest.skip(f"Sample PDF not found at {path} - see tests/fixtures/README.md")
        return path

    @pytest.mark.integration
    def test_citations_list_is_populated(self, processor, sample_pdf_path):
        """Test that citations are extracted from bibliography"""
        metadata = processor.process(sample_pdf_path)

        assert isinstance(metadata.citations, list)

    @pytest.mark.integration
    def test_citations_have_raw_text(self, processor, sample_pdf_path):
        """Test that each citation has raw text"""
        metadata = processor.process(sample_pdf_path)

        if len(metadata.citations) > 0:
            for citation in metadata.citations[:5]:
                assert citation.raw_text is not None
                assert len(citation.raw_text) > 0

    @pytest.mark.integration
    def test_citation_is_citation_object(self, processor, sample_pdf_path):
        """Test that citations are proper Citation objects"""
        metadata = processor.process(sample_pdf_path)

        if len(metadata.citations) > 0:
            assert isinstance(metadata.citations[0], Citation)


# ---------------------------------------------------------------------------
# Body text extraction — unit tests (no GROBID service required)
# ---------------------------------------------------------------------------

SAMPLE_TEI = """<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader/>
  <text>
    <body>
      <div>
        <head>Introduction</head>
        <p>The Transformer <ref type="bibr" target="#b0">[1]</ref> eliminates recurrence.</p>
        <p>Self-attention allows parallel computation across all positions.</p>
      </div>
      <div>
        <head>Methods</head>
        <p>We use multi-head attention <ref type="bibr" target="#b1">[2]</ref> with eight heads.</p>
      </div>
    </body>
  </text>
</TEI>
"""


class TestExtractBodyText:
    """Unit tests for _extract_body_text() — no GROBID service needed."""

    @pytest.fixture
    def processor(self):
        return GrobidProcessor("http://localhost:8070")

    @pytest.fixture
    def root(self):
        from lxml import etree
        return etree.fromstring(SAMPLE_TEI.encode("utf-8"))

    def test_returns_non_empty_string(self, processor, root):
        text = processor._extract_body_text(root)
        assert isinstance(text, str)
        assert len(text) > 0

    def test_preserves_citation_markers(self, processor, root):
        """[N] markers inside <ref> elements must appear in the output."""
        text = processor._extract_body_text(root)
        assert "[1]" in text
        assert "[2]" in text

    def test_includes_paragraph_text(self, processor, root):
        text = processor._extract_body_text(root)
        assert "eliminates recurrence" in text
        assert "parallel computation" in text
        assert "multi-head attention" in text

    def test_includes_section_headings(self, processor, root):
        text = processor._extract_body_text(root)
        assert "Introduction" in text
        assert "Methods" in text

    def test_no_body_returns_empty_string(self, processor):
        from lxml import etree
        empty_tei = b"""<?xml version="1.0"?>
        <TEI xmlns="http://www.tei-c.org/ns/1.0"><teiHeader/><text/></TEI>"""
        root = etree.fromstring(empty_tei)
        assert processor._extract_body_text(root) == ""

    def test_collapses_whitespace(self, processor, root):
        text = processor._extract_body_text(root)
        # No double spaces in paragraph text
        assert "  " not in text


class TestCleanTitle:
    """Unit tests for _clean_title() — no GROBID service needed."""

    @pytest.fixture
    def processor(self):
        return GrobidProcessor("http://localhost:8070")

    def test_all_caps_title_converted_to_title_case(self, processor):
        assert processor._clean_title("DEEP LEARNING WITH BERT") == "Deep Learning With Bert"

    def test_mixed_case_with_acronym_left_alone(self, processor):
        """Acronyms must not be destroyed — only fully-uppercase input is title-cased."""
        result = processor._clean_title("Deep Learning with BERT")
        assert result == "Deep Learning with BERT"

    def test_mixed_case_multiple_acronyms_left_alone(self, processor):
        result = processor._clean_title("NLP Benchmarks: A Study of BERT, GPT, and LLaMA")
        assert result == "NLP Benchmarks: A Study of BERT, GPT, and LLaMA"

    def test_already_correct_title_unchanged(self, processor):
        result = processor._clean_title("Attention Is All You Need")
        assert result == "Attention Is All You Need"

    def test_strips_leading_trailing_whitespace(self, processor):
        assert processor._clean_title("  Some Title  ") == "Some Title"

    def test_collapses_internal_whitespace(self, processor):
        assert processor._clean_title("Some   Title") == "Some Title"
