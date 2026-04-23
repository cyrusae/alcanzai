"""
Unit tests for doi_fetcher.py.

All HTTP calls are mocked — no network required.
"""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from paper_library.doi_fetcher import DoiFetcher, DoiFetchError


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def _make_crossref_response(
    title="Test Paper Title",
    authors=None,
    year=2023,
    abstract="<jats:p>This is the <jats:italic>abstract</jats:italic>.</jats:p>",
    doi="10.1234/test.doi",
    journal="Test Journal",
):
    """Build a minimal Crossref works message dict."""
    if authors is None:
        authors = [{"given": "Alice", "family": "Smith"}, {"given": "Bob", "family": "Jones"}]
    return {
        "status": "ok",
        "message": {
            "title": [title],
            "author": authors,
            "published-print": {"date-parts": [[year]]},
            "abstract": abstract,
            "DOI": doi,
            "container-title": [journal],
            "volume": "12",
            "issue": "3",
            "page": "100-120",
            "relation": {},
        },
    }


def _mock_response(status_code=200, json_data=None, content=b""):
    """Return a mock requests.Response."""
    mock = MagicMock()
    mock.status_code = status_code
    mock.json.return_value = json_data or {}
    mock.content = content
    mock.raise_for_status.side_effect = (
        None if status_code < 400 else Exception(f"HTTP {status_code}")
    )
    return mock


# ---------------------------------------------------------------------------
# parse_doi
# ---------------------------------------------------------------------------

class TestParseDoi:
    def setup_method(self):
        self.fetcher = DoiFetcher()

    def test_bare_doi(self):
        assert self.fetcher.parse_doi("10.1093/mind/fzae004") == "10.1093/mind/fzae004"

    def test_doi_org_https(self):
        assert self.fetcher.parse_doi("https://doi.org/10.1093/mind/fzae004") == "10.1093/mind/fzae004"

    def test_doi_org_http(self):
        assert self.fetcher.parse_doi("http://doi.org/10.1093/mind/fzae004") == "10.1093/mind/fzae004"

    def test_dx_doi_org(self):
        assert self.fetcher.parse_doi("https://dx.doi.org/10.1093/mind/fzae004") == "10.1093/mind/fzae004"

    def test_doi_prefix(self):
        assert self.fetcher.parse_doi("doi:10.1093/mind/fzae004") == "10.1093/mind/fzae004"

    def test_trailing_punctuation_stripped(self):
        assert self.fetcher.parse_doi("10.1234/test.doi.") == "10.1234/test.doi"
        assert self.fetcher.parse_doi("10.1234/test.doi,") == "10.1234/test.doi"

    def test_with_version_suffix(self):
        # DOI suffixes can contain slashes and alphanumerics
        doi = self.fetcher.parse_doi("10.5281/zenodo.1234567")
        assert doi == "10.5281/zenodo.1234567"

    def test_arxiv_id_not_doi(self):
        assert self.fetcher.parse_doi("1706.03762") is None

    def test_plain_string_not_doi(self):
        assert self.fetcher.parse_doi("not a doi at all") is None

    def test_url_without_doi_not_matched(self):
        assert self.fetcher.parse_doi("https://example.com/article/123") is None

    def test_doi_embedded_in_publisher_url(self):
        # Publisher URLs embed the DOI in the path — we extract whatever the DOI regex
        # matches. Since DOI suffixes can themselves contain slashes, we can't distinguish
        # the real DOI from the publisher's appended article ID; the caller can try the
        # full match and fall back if the Crossref lookup fails.
        doi = self.fetcher.parse_doi("https://academic.oup.com/mind/article/10.1093/mind/fzae004/7123456")
        assert doi is not None
        assert doi.startswith("10.1093/mind/fzae004")


# ---------------------------------------------------------------------------
# Crossref parsing
# ---------------------------------------------------------------------------

class TestCrossrefParsing:
    def setup_method(self):
        self.fetcher = DoiFetcher()

    def _parse(self, **kwargs):
        data = _make_crossref_response(**kwargs)["message"]
        return self.fetcher._parse_crossref(data, kwargs.get("doi", "10.1234/test"))

    def test_title_extracted(self):
        meta = self._parse(title="My Great Paper")
        assert meta.title == "My Great Paper"

    def test_authors_extracted(self):
        meta = self._parse()
        assert meta.authors == ["Alice Smith", "Bob Jones"]

    def test_org_author(self):
        data = _make_crossref_response(authors=[{"name": "ACME Research Group"}])["message"]
        meta = self.fetcher._parse_crossref(data, "10.1234/test")
        assert meta.authors == ["ACME Research Group"]

    def test_year_from_published_print(self):
        meta = self._parse(year=2021)
        assert meta.year == 2021

    def test_abstract_jats_stripped(self):
        meta = self._parse(abstract="<jats:p>This is the <jats:italic>abstract</jats:italic>.</jats:p>")
        assert meta.abstract == "This is the abstract."

    def test_abstract_none_when_missing(self):
        data = _make_crossref_response()["message"]
        data.pop("abstract", None)
        meta = self.fetcher._parse_crossref(data, "10.1234/test")
        assert meta.abstract is None

    def test_venue_extracted(self):
        meta = self._parse(journal="Nature Machine Intelligence")
        assert meta.venue == "Nature Machine Intelligence"

    def test_doi_stored(self):
        meta = self._parse(doi="10.1234/specific.doi")
        assert meta.doi == "10.1234/specific.doi"

    def test_source_is_doi(self):
        meta = self._parse()
        assert meta.source == "doi"

    def test_volume_issue_pages(self):
        meta = self._parse()
        assert meta.volume == "12"
        assert meta.issue == "3"
        assert meta.pages == "100-120"

    def test_arxiv_id_from_relation(self):
        data = _make_crossref_response()["message"]
        data["relation"] = {
            "is-preprint-of": [{"id-type": "arxiv", "id": "arxiv:2301.12345"}]
        }
        meta = self.fetcher._parse_crossref(data, "10.1234/test")
        assert meta.arxiv_id == "2301.12345"

    def test_fallback_title_when_missing(self):
        data = _make_crossref_response()["message"]
        data["title"] = []
        meta = self.fetcher._parse_crossref(data, "10.1234/test.doi")
        assert "10.1234/test.doi" in meta.title

    def test_fallback_year_when_missing(self):
        data = _make_crossref_response()["message"]
        data.pop("published-print", None)
        data.pop("published-online", None)
        data.pop("issued", None)
        meta = self.fetcher._parse_crossref(data, "10.1234/test")
        assert meta.year is not None  # Falls back to current year


# ---------------------------------------------------------------------------
# Crossref HTTP call
# ---------------------------------------------------------------------------

class TestFetchCrossref:
    def setup_method(self):
        self.fetcher = DoiFetcher(email="test@example.com")

    def test_successful_fetch(self):
        cr_data = _make_crossref_response()
        with patch("requests.get", return_value=_mock_response(200, cr_data)):
            meta = self.fetcher._fetch_crossref("10.1234/test")
        assert meta.title == "Test Paper Title"

    def test_404_raises_doi_fetch_error(self):
        with patch("requests.get", return_value=_mock_response(404)):
            with pytest.raises(DoiFetchError, match="not found"):
                self.fetcher._fetch_crossref("10.1234/nonexistent")

    def test_network_error_raises_doi_fetch_error(self):
        import requests as req
        with patch("requests.get", side_effect=req.RequestException("timeout")):
            with pytest.raises(DoiFetchError):
                self.fetcher._fetch_crossref("10.1234/test")

    def test_email_sent_in_params(self):
        cr_data = _make_crossref_response()
        with patch("requests.get", return_value=_mock_response(200, cr_data)) as mock_get:
            self.fetcher._fetch_crossref("10.1234/test")
        call_kwargs = mock_get.call_args
        assert call_kwargs.kwargs.get("params", {}).get("mailto") == "test@example.com"


# ---------------------------------------------------------------------------
# Unpaywall + Semantic Scholar
# ---------------------------------------------------------------------------

class TestOaPdfDiscovery:
    def setup_method(self):
        self.fetcher = DoiFetcher()

    def test_unpaywall_returns_pdf_url(self):
        unpaywall_data = {
            "best_oa_location": {"url_for_pdf": "https://example.com/paper.pdf", "url": None}
        }
        with patch("requests.get", return_value=_mock_response(200, unpaywall_data)):
            url = self.fetcher._fetch_unpaywall("10.1234/test")
        assert url == "https://example.com/paper.pdf"

    def test_unpaywall_falls_back_to_url_when_no_pdf_url(self):
        unpaywall_data = {
            "best_oa_location": {"url_for_pdf": None, "url": "https://example.com/landing"}
        }
        with patch("requests.get", return_value=_mock_response(200, unpaywall_data)):
            url = self.fetcher._fetch_unpaywall("10.1234/test")
        assert url == "https://example.com/landing"

    def test_unpaywall_404_returns_none(self):
        with patch("requests.get", return_value=_mock_response(404)):
            assert self.fetcher._fetch_unpaywall("10.1234/test") is None

    def test_unpaywall_no_oa_location_returns_none(self):
        with patch("requests.get", return_value=_mock_response(200, {"best_oa_location": None})):
            assert self.fetcher._fetch_unpaywall("10.1234/test") is None

    def test_unpaywall_skipped_when_no_email_configured(self):
        """Regression for #18: no fake email to Unpaywall, no HTTP call at all."""
        fetcher = DoiFetcher()  # no email
        with patch("requests.get") as mock_get:
            result = fetcher._fetch_unpaywall("10.1234/test")
        assert result is None
        mock_get.assert_not_called()

    def test_semantic_scholar_returns_pdf_url(self):
        ss_data = {"openAccessPdf": {"url": "https://arxiv.org/pdf/2301.12345.pdf"}}
        with patch("requests.get", return_value=_mock_response(200, ss_data)):
            url = self.fetcher._fetch_semantic_scholar("10.1234/test")
        assert url == "https://arxiv.org/pdf/2301.12345.pdf"

    def test_semantic_scholar_404_returns_none(self):
        with patch("requests.get", return_value=_mock_response(404)):
            assert self.fetcher._fetch_semantic_scholar("10.1234/test") is None

    def test_find_oa_uses_unpaywall_first(self):
        unpaywall_data = {"best_oa_location": {"url_for_pdf": "https://oa.pdf", "url": None}}
        with patch.object(self.fetcher, "_fetch_unpaywall", return_value="https://oa.pdf") as mock_uw, \
             patch.object(self.fetcher, "_fetch_semantic_scholar") as mock_ss:
            url = self.fetcher._find_oa_pdf_url("10.1234/test")
        assert url == "https://oa.pdf"
        mock_ss.assert_not_called()

    def test_find_oa_falls_back_to_semantic_scholar(self):
        with patch.object(self.fetcher, "_fetch_unpaywall", return_value=None), \
             patch.object(self.fetcher, "_fetch_semantic_scholar", return_value="https://ss.pdf"):
            url = self.fetcher._find_oa_pdf_url("10.1234/test")
        assert url == "https://ss.pdf"


# ---------------------------------------------------------------------------
# PDF download
# ---------------------------------------------------------------------------

class TestPdfDownload:
    def test_pdf_saved_to_vault(self, tmp_path):
        fetcher = DoiFetcher(vault_path=tmp_path)
        pdf_bytes = b"%PDF-1.4 fake pdf content"
        with patch("requests.get", return_value=_mock_response(200, content=pdf_bytes)):
            path = fetcher._download_pdf("https://example.com/paper.pdf", "10.1234/test")
        assert path is not None
        assert path.exists()
        assert path.read_bytes() == pdf_bytes

    def test_non_pdf_content_returns_none(self, tmp_path):
        fetcher = DoiFetcher(vault_path=tmp_path)
        html_bytes = b"<html>This is a landing page</html>"
        with patch("requests.get", return_value=_mock_response(200, content=html_bytes)):
            path = fetcher._download_pdf("https://example.com/page", "10.1234/test")
        assert path is None

    def test_no_vault_path_returns_none(self):
        fetcher = DoiFetcher(vault_path=None)
        assert fetcher._download_pdf("https://example.com/paper.pdf", "10.1234/test") is None

    def test_network_error_returns_none(self, tmp_path):
        import requests as req
        fetcher = DoiFetcher(vault_path=tmp_path)
        with patch("requests.get", side_effect=req.RequestException("timeout")):
            assert fetcher._download_pdf("https://example.com/paper.pdf", "10.1234/test") is None

    def test_filename_uses_doi(self, tmp_path):
        fetcher = DoiFetcher(vault_path=tmp_path)
        pdf_bytes = b"%PDF-1.4 content"
        with patch("requests.get", return_value=_mock_response(200, content=pdf_bytes)):
            path = fetcher._download_pdf("https://example.com/paper.pdf", "10.1234/my.test.doi")
        # Dots are preserved by the sanitizer; only / and special chars become _
        assert path.name.startswith("doi_10.1234")


# ---------------------------------------------------------------------------
# Integration: full fetch() call
# ---------------------------------------------------------------------------

class TestFetchIntegration:
    def test_fetch_with_pdf(self, tmp_path):
        fetcher = DoiFetcher(vault_path=tmp_path)
        cr_data = _make_crossref_response()
        unpaywall_data = {"best_oa_location": {"url_for_pdf": "https://oa.com/paper.pdf", "url": None}}
        pdf_bytes = b"%PDF-1.4 content"

        responses = [
            _mock_response(200, cr_data),          # Crossref
            _mock_response(200, unpaywall_data),    # Unpaywall
            _mock_response(200, content=pdf_bytes), # PDF download
        ]
        with patch("requests.get", side_effect=responses):
            metadata, pdf_path = fetcher.fetch("10.1234/test")

        assert metadata.title == "Test Paper Title"
        assert pdf_path is not None
        assert pdf_path.exists()

    def test_fetch_without_pdf(self, tmp_path):
        fetcher = DoiFetcher(vault_path=tmp_path)
        cr_data = _make_crossref_response()
        no_oa = {"best_oa_location": None}

        responses = [
            _mock_response(200, cr_data),  # Crossref
            _mock_response(200, no_oa),    # Unpaywall — no OA
            _mock_response(404),           # Semantic Scholar — not found
        ]
        with patch("requests.get", side_effect=responses):
            metadata, pdf_path = fetcher.fetch("10.1234/test")

        assert metadata.title == "Test Paper Title"
        assert pdf_path is None


@pytest.mark.integration
class TestRealDoi:
    """Live network tests — skipped by default (pytest -m 'not integration')."""

    def test_crossref_attention_is_all_you_need(self):
        """The arXiv version of Attention Is All You Need has a Crossref record."""
        fetcher = DoiFetcher()
        # Crossref DOI for the NIPS 2017 proceedings version
        meta = fetcher._fetch_crossref("10.48550/arXiv.1706.03762")
        assert "attention" in meta.title.lower()
        assert meta.year == 2017
