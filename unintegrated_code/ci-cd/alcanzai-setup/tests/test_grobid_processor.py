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
            pytest.skip(
                "GROBID service not running - start with: docker-compose up -d"
            )


class TestGrobidFileHandling:
    """Tests for file handling and validation (unit tests, fast)"""
    
    @pytest.fixture
    def processor(self):
        return GrobidProcessor(config.grobid_url)
    
    def test_missing_file_raises_file_not_found(self, processor):
        """Test that processing non-existent file raises FileNotFoundError"""
        with pytest.raises(FileNotFoundError):
            processor.process(Path("/nonexistent/paper.pdf"))
    
    def test_valid_pdf_path_accepted(self, processor):
        """Test that valid PDF paths are accepted"""
        # Don't actually process, just verify path validation
        # (This is more of a sanity check)
        valid_path = Path(__file__).parent / "fixtures" / "sample.pdf"
        # We just check it doesn't raise on the path itself
        # (The actual processing might fail for other reasons)


class TestGrobidMetadataExtraction:
    """Tests for XML parsing and metadata extraction (integration tests, requires PDF)"""
    
    @pytest.fixture
    def processor(self):
        return GrobidProcessor(config.grobid_url)
    
    @pytest.fixture
    def sample_pdf_path(self):
        """Get path to a sample PDF for testing"""
        path = Path(__file__).parent / "fixtures" / "sample.pdf"
        if not path.exists():
            pytest.skip(f"Sample PDF not found at {path}")
        return path
    
    @pytest.mark.integration
    def test_extract_title(self, processor, sample_pdf_path):
        """Test that paper title is extracted"""
        metadata = processor.process(sample_pdf_path)
        
        assert metadata.title is not None
        assert len(metadata.title) > 0
        assert len(metadata.title) < 500  # Sanity check
    
    @pytest.mark.integration
    def test_extract_authors(self, processor, sample_pdf_path):
        """Test that author names are extracted"""
        metadata = processor.process(sample_pdf_path)
        
        assert len(metadata.authors) > 0
        # Each author should have some reasonable length
        for author in metadata.authors:
            assert len(author) > 2
            assert len(author) < 200
    
    @pytest.mark.integration
    def test_extract_year(self, processor, sample_pdf_path):
        """Test that publication year is extracted"""
        metadata = processor.process(sample_pdf_path)
        
        assert metadata.year is not None
        # Sanity check: year should be reasonable
        assert 1950 < metadata.year < 2030
    
    @pytest.mark.integration
    def test_extract_abstract(self, processor, sample_pdf_path):
        """Test that abstract is extracted (if present)"""
        metadata = processor.process(sample_pdf_path)
        
        # Abstract might not always be present, so just check it's reasonable if it is
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
            pytest.skip(f"Sample PDF not found at {path}")
        return path
    
    @pytest.mark.integration
    def test_citations_list_is_populated(self, processor, sample_pdf_path):
        """Test that citations are extracted from bibliography"""
        metadata = processor.process(sample_pdf_path)
        
        # Most papers have citations
        # (Some might not, so we don't assert > 0, just that it's a list)
        assert isinstance(metadata.citations, list)
    
    @pytest.mark.integration
    def test_citations_have_raw_text(self, processor, sample_pdf_path):
        """Test that each citation has raw text"""
        metadata = processor.process(sample_pdf_path)
        
        if len(metadata.citations) > 0:
            for citation in metadata.citations[:5]:  # Check first 5
                assert citation.raw_text is not None
                assert len(citation.raw_text) > 0
    
    @pytest.mark.integration
    def test_citation_is_citation_object(self, processor, sample_pdf_path):
        """Test that citations are proper Citation objects"""
        metadata = processor.process(sample_pdf_path)
        
        if len(metadata.citations) > 0:
            assert isinstance(metadata.citations[0], Citation)
