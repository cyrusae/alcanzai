"""
Direct unit tests for paper_library/models.py.

Tests Pydantic validation, field defaults, type coercion, and the
BibliographicEntry → Citation / PaperMetadata inheritance pattern.
No external services required.

Run: pytest tests/test_models.py -m "not integration"
"""

import pytest
from datetime import datetime
from pydantic import ValidationError

from paper_library.models import (
    BibliographicEntry,
    Citation,
    PaperMetadata,
    ArticleMetadata,
    Synthesis,
    ProcessingState,
)


# ---------------------------------------------------------------------------
# BibliographicEntry
# ---------------------------------------------------------------------------

class TestBibliographicEntry:
    """Base model: all fields optional, round-trip, no required fields."""

    def test_empty_construction_succeeds(self):
        entry = BibliographicEntry()
        assert entry.title is None
        assert entry.authors is None
        assert entry.year is None

    def test_all_fields_round_trip(self):
        entry = BibliographicEntry(
            title="Attention Is All You Need",
            authors=["Vaswani, Ashish", "Shazeer, Noam"],
            year=2017,
            venue="NeurIPS",
            volume="30",
            issue="1",
            pages="5998-6008",
            doi="10.5555/3295222.3295349",
            arxiv_id="1706.03762",
            abstract="We propose a new architecture...",
            raw_text="Vaswani et al. (2017). Attention Is All You Need.",
        )
        assert entry.title == "Attention Is All You Need"
        assert entry.year == 2017
        assert entry.doi == "10.5555/3295222.3295349"
        assert entry.arxiv_id == "1706.03762"

    def test_model_dump_excludes_none_by_default(self):
        entry = BibliographicEntry(title="Test", year=2020)
        d = entry.model_dump(exclude_none=True)
        assert "title" in d
        assert "year" in d
        assert "authors" not in d
        assert "doi" not in d

    def test_year_none_is_allowed(self):
        """year=None must be accepted (preprints, working papers)."""
        entry = BibliographicEntry(title="Preprint Paper", year=None)
        assert entry.year is None

    def test_authors_list_of_strings(self):
        entry = BibliographicEntry(authors=["Smith, J.", "Jones, A."])
        assert len(entry.authors) == 2
        assert entry.authors[0] == "Smith, J."


# ---------------------------------------------------------------------------
# Citation
# ---------------------------------------------------------------------------

class TestCitation:
    """Citation extends BibliographicEntry with mention_count and contexts."""

    def test_inherits_bibliographic_fields(self):
        citation = Citation(title="Cited Paper", year=2021)
        assert citation.title == "Cited Paper"
        assert citation.year == 2021

    def test_mention_count_defaults_to_one(self):
        citation = Citation()
        assert citation.mention_count == 1

    def test_contexts_defaults_to_empty_list(self):
        citation = Citation()
        assert citation.contexts == []
        assert isinstance(citation.contexts, list)

    def test_contexts_accepts_strings(self):
        citation = Citation(contexts=["First mention.", "Second mention."])
        assert len(citation.contexts) == 2
        assert citation.contexts[0] == "First mention."

    def test_mention_count_can_be_set(self):
        citation = Citation(mention_count=5)
        assert citation.mention_count == 5

    def test_contexts_independent_across_instances(self):
        """Default mutable default_factory must not be shared between instances."""
        c1 = Citation()
        c2 = Citation()
        c1.contexts.append("only c1")
        assert c2.contexts == []

    def test_full_citation_round_trip(self):
        citation = Citation(
            title="Neural Models of Syntax",
            authors=["Smith, J.", "Jones, A."],
            year=2023,
            venue="Nature",
            volume="123",
            issue="4",
            pages="567-890",
            mention_count=3,
            contexts=["As Smith et al. (2023) showed...", "...confirmed by [Smith23]."],
        )
        assert citation.mention_count == 3
        assert len(citation.contexts) == 2


# ---------------------------------------------------------------------------
# PaperMetadata
# ---------------------------------------------------------------------------

class TestPaperMetadata:
    """PaperMetadata: title + authors required; year optional; citations default empty."""

    def test_title_and_authors_required(self):
        with pytest.raises(ValidationError) as exc_info:
            PaperMetadata()
        errors = exc_info.value.errors()
        fields = {e["loc"][0] for e in errors}
        assert "title" in fields
        assert "authors" in fields

    def test_missing_title_raises(self):
        with pytest.raises(ValidationError):
            PaperMetadata(authors=["Author, A."])

    def test_missing_authors_raises(self):
        with pytest.raises(ValidationError):
            PaperMetadata(title="Some Paper")

    def test_year_optional(self):
        """year=None is allowed for preprints and working papers."""
        paper = PaperMetadata(title="Preprint", authors=["Author, A."])
        assert paper.year is None

    def test_citations_default_empty(self):
        paper = PaperMetadata(title="Test", authors=["A"])
        assert paper.citations == []

    def test_citations_independent_across_instances(self):
        p1 = PaperMetadata(title="P1", authors=["A"])
        p2 = PaperMetadata(title="P2", authors=["A"])
        p1.citations.append(Citation(title="Ref"))
        assert p2.citations == []

    def test_citations_accepts_citation_objects(self):
        c = Citation(title="Ref", year=2020)
        paper = PaperMetadata(title="Test", authors=["A"], citations=[c])
        assert len(paper.citations) == 1
        assert paper.citations[0].title == "Ref"

    def test_optional_fields_default_none(self):
        paper = PaperMetadata(title="T", authors=["A"])
        assert paper.pdf_path is None
        assert paper.body_text is None
        assert paper.processed_at is None
        assert paper.source is None

    def test_inherits_base_fields(self):
        """BibliographicEntry fields (doi, arxiv_id, abstract) survive in PaperMetadata."""
        paper = PaperMetadata(
            title="Transformer",
            authors=["Vaswani, A."],
            year=2017,
            doi="10.5555/test",
            arxiv_id="1706.03762",
            abstract="Abstract text.",
        )
        assert paper.doi == "10.5555/test"
        assert paper.arxiv_id == "1706.03762"
        assert paper.abstract == "Abstract text."


# ---------------------------------------------------------------------------
# ArticleMetadata
# ---------------------------------------------------------------------------

class TestArticleMetadata:
    """ArticleMetadata: url required and validated; published_date optional."""

    def test_minimal_construction(self):
        article = ArticleMetadata(
            title="Blog Post",
            authors=["Smith, J."],
            url="https://example.com/post",
        )
        assert article.title == "Blog Post"
        assert str(article.url).startswith("https://example.com")

    def test_url_required(self):
        with pytest.raises(ValidationError):
            ArticleMetadata(title="Post", authors=["A"])

    def test_invalid_url_raises(self):
        with pytest.raises(ValidationError):
            ArticleMetadata(
                title="Post",
                authors=["A"],
                url="not-a-url",
            )

    def test_published_date_optional(self):
        article = ArticleMetadata(
            title="Post", authors=["A"], url="https://example.com"
        )
        assert article.published_date is None

    def test_published_date_accepts_datetime(self):
        dt = datetime(2024, 1, 15, 12, 0, 0)
        article = ArticleMetadata(
            title="Post",
            authors=["A"],
            url="https://example.com",
            published_date=dt,
        )
        assert article.published_date == dt

    def test_source_defaults_to_web(self):
        article = ArticleMetadata(
            title="Post", authors=["A"], url="https://example.com"
        )
        assert article.source == "web"

    def test_pdf_path_defaults_to_none(self):
        article = ArticleMetadata(
            title="Post", authors=["A"], url="https://example.com"
        )
        assert article.pdf_path is None

    def test_pdf_path_can_be_set(self):
        article = ArticleMetadata(
            title="Post",
            authors=["A"],
            url="https://example.com",
            pdf_path="/tmp/article.pdf",
        )
        assert article.pdf_path == "/tmp/article.pdf"


# ---------------------------------------------------------------------------
# Synthesis
# ---------------------------------------------------------------------------

class TestSynthesis:
    """Synthesis: all four narrative fields required; generated_at defaults to now."""

    def _valid_kwargs(self, **overrides):
        base = dict(
            summary="This paper proposes X.",
            why_you_cared="Relevant because Y.",
            key_concepts=["attention", "transformer"],
            memorable_quote="All you need is attention.",
        )
        base.update(overrides)
        return base

    def test_minimal_construction(self):
        s = Synthesis(**self._valid_kwargs())
        assert s.summary == "This paper proposes X."
        assert s.cost_usd == 0.0
        assert s.detailed_summary is None

    def test_generated_at_is_set_automatically(self):
        before = datetime.now()
        s = Synthesis(**self._valid_kwargs())
        after = datetime.now()
        assert before <= s.generated_at <= after

    def test_generated_at_independent_across_instances(self):
        """default_factory must produce a fresh datetime per instance."""
        s1 = Synthesis(**self._valid_kwargs())
        s2 = Synthesis(**self._valid_kwargs())
        assert isinstance(s1.generated_at, datetime)
        assert isinstance(s2.generated_at, datetime)

    def test_summary_required(self):
        kwargs = self._valid_kwargs()
        del kwargs["summary"]
        with pytest.raises(ValidationError):
            Synthesis(**kwargs)

    def test_why_you_cared_required(self):
        kwargs = self._valid_kwargs()
        del kwargs["why_you_cared"]
        with pytest.raises(ValidationError):
            Synthesis(**kwargs)

    def test_key_concepts_required(self):
        kwargs = self._valid_kwargs()
        del kwargs["key_concepts"]
        with pytest.raises(ValidationError):
            Synthesis(**kwargs)

    def test_memorable_quote_required(self):
        kwargs = self._valid_kwargs()
        del kwargs["memorable_quote"]
        with pytest.raises(ValidationError):
            Synthesis(**kwargs)

    def test_key_concepts_is_list(self):
        s = Synthesis(**self._valid_kwargs(key_concepts=["a", "b", "c"]))
        assert isinstance(s.key_concepts, list)
        assert len(s.key_concepts) == 3

    def test_cost_usd_can_be_set(self):
        s = Synthesis(**self._valid_kwargs(cost_usd=0.0042))
        assert s.cost_usd == pytest.approx(0.0042)

    def test_model_used_default(self):
        s = Synthesis(**self._valid_kwargs())
        assert "haiku" in s.model_used.lower() or "claude" in s.model_used.lower()


# ---------------------------------------------------------------------------
# ProcessingState
# ---------------------------------------------------------------------------

class TestProcessingState:
    """ProcessingState: empty defaults, mark_processed, is_processed, mark_failed, dedup."""

    def test_empty_construction_all_sets_empty(self):
        state = ProcessingState()
        assert state.processed_dois == set()
        assert state.processed_arxiv_ids == set()
        assert state.processed_urls == set()
        assert state.processed_local_paths == set()
        assert state.failed == {}

    def test_mark_processed_arxiv(self):
        state = ProcessingState()
        state.mark_processed("1706.03762", "arxiv")
        assert "1706.03762" in state.processed_arxiv_ids
        assert state.is_processed("1706.03762")

    def test_mark_processed_doi(self):
        state = ProcessingState()
        state.mark_processed("10.5555/test", "doi")
        assert "10.5555/test" in state.processed_dois
        assert state.is_processed("10.5555/test")

    def test_mark_processed_web(self):
        state = ProcessingState()
        state.mark_processed("https://example.com/post", "web")
        assert "https://example.com/post" in state.processed_urls
        assert state.is_processed("https://example.com/post")

    def test_mark_processed_local(self):
        state = ProcessingState()
        state.mark_processed("/papers/thesis.pdf", "local")
        assert "/papers/thesis.pdf" in state.processed_local_paths
        assert state.is_processed("/papers/thesis.pdf")

    def test_mark_processed_unknown_source_raises(self):
        state = ProcessingState()
        with pytest.raises(ValueError, match="Unknown source"):
            state.mark_processed("some-id", "ftp")

    def test_is_processed_false_for_unknown(self):
        state = ProcessingState()
        assert not state.is_processed("1706.03762")

    def test_no_cross_contamination_between_source_types(self):
        """An arXiv ID stored under DOI must not appear in the arxiv set."""
        state = ProcessingState()
        state.mark_processed("1706.03762", "doi")  # stored in processed_dois
        assert state.is_processed("1706.03762")
        assert "1706.03762" not in state.processed_arxiv_ids

    def test_mark_processed_updates_last_updated(self):
        state = ProcessingState()
        before = datetime.now()
        state.mark_processed("1706.03762", "arxiv")
        assert state.last_updated >= before

    def test_mark_failed_stores_error(self):
        state = ProcessingState()
        state.mark_failed("bad-id", "Connection timed out")
        assert state.failed["bad-id"] == "Connection timed out"

    def test_mark_failed_updates_last_updated(self):
        state = ProcessingState()
        before = datetime.now()
        state.mark_failed("bad-id", "Some error")
        assert state.last_updated >= before

    def test_duplicate_mark_processed_is_idempotent(self):
        """Marking the same ID twice must not raise or duplicate entries."""
        state = ProcessingState()
        state.mark_processed("1706.03762", "arxiv")
        state.mark_processed("1706.03762", "arxiv")
        assert len(state.processed_arxiv_ids) == 1

    def test_multiple_identifiers_all_tracked(self):
        state = ProcessingState()
        state.mark_processed("1706.03762", "arxiv")
        state.mark_processed("10.5555/x", "doi")
        state.mark_processed("https://example.com", "web")
        state.mark_processed("/local.pdf", "local")
        assert state.is_processed("1706.03762")
        assert state.is_processed("10.5555/x")
        assert state.is_processed("https://example.com")
        assert state.is_processed("/local.pdf")
        assert not state.is_processed("does-not-exist")
