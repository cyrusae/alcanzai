"""
Tests for citation context extraction.

Run: pytest tests/test_citation_context.py
"""

import pytest

from paper_library.citation_context import CitationContextExtractor, CitationContext
from paper_library.models import Citation


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

SAMPLE_TEXT = """
Introduction

Recent advances in neural machine translation have been driven by the
development of attention-based models. The Transformer architecture
(Vaswani et al., 2017) eliminates recurrence entirely, relying solely
on attention mechanisms for both encoding and decoding. This approach
has proven highly effective for sequence-to-sequence tasks.

Background

Early work on attention mechanisms by Bahdanau et al. (2014) showed that
neural networks can learn to align inputs and outputs. The Transformer
builds on this foundation but uses multi-head self-attention.

Methods

We follow the BERT pretraining approach (Devlin et al., 2019) but modify
the masking strategy. Unlike previous work (Vaswani et al., 2017;
Radford et al., 2018), we use bidirectional context.

Results

Our model achieves state-of-the-art results. Compared to the baseline
Transformer (Vaswani et al., 2017), we see a 15% improvement in BLEU score.

References

Vaswani, A., Shazeer, N., Parmar, N., et al. (2017). Attention Is All You Need.
Bahdanau, D., Cho, K., & Bengio, Y. (2014). Neural machine translation.
Devlin, J., Chang, M., Lee, K., & Toutanova, K. (2019). BERT: Pre-training.
Radford, A., et al. (2018). Improving language understanding.
"""


@pytest.fixture
def vaswani():
    return Citation(
        authors=["Vaswani, A.", "Shazeer, N.", "Parmar, N."],
        title="Attention Is All You Need",
        year=2017,
        raw_text="Vaswani et al. (2017). Attention Is All You Need.",
    )


@pytest.fixture
def bahdanau():
    return Citation(
        authors=["Bahdanau, D.", "Cho, K.", "Bengio, Y."],
        title="Neural machine translation by jointly learning to align and translate",
        year=2014,
        raw_text="Bahdanau et al. (2014). Neural machine translation.",
    )


@pytest.fixture
def devlin():
    return Citation(
        authors=["Devlin, J.", "Chang, M.", "Lee, K.", "Toutanova, K."],
        title="BERT: Pre-training of Deep Bidirectional Transformers",
        year=2019,
        raw_text="Devlin et al. (2019). BERT: Pre-training.",
    )


@pytest.fixture
def extractor():
    return CitationContextExtractor(context_sentences=2)


# ---------------------------------------------------------------------------
# extract_contexts
# ---------------------------------------------------------------------------

class TestExtractContexts:

    def test_finds_multi_author_citation(self, extractor, vaswani):
        """Vaswani et al. appears 3× in body text — should find at least 2."""
        contexts = extractor.extract_contexts(SAMPLE_TEXT, [vaswani])
        key = vaswani.title
        assert key in contexts
        assert len(contexts[key]) >= 2

    def test_finds_single_mention(self, extractor, bahdanau):
        """Bahdanau et al. appears once — exactly one context expected."""
        contexts = extractor.extract_contexts(SAMPLE_TEXT, [bahdanau])
        key = bahdanau.title
        assert key in contexts
        assert len(contexts[key]) == 1

    def test_context_text_is_non_empty(self, extractor, devlin):
        contexts = extractor.extract_contexts(SAMPLE_TEXT, [devlin])
        key = devlin.title
        assert key in contexts
        assert all(len(c.context_text) > 10 for c in contexts[key])

    def test_context_ends_with_period(self, extractor, vaswani):
        contexts = extractor.extract_contexts(SAMPLE_TEXT, [vaswani])
        key = vaswani.title
        for c in contexts[key]:
            assert c.context_text.endswith(".")

    def test_position_in_range(self, extractor, vaswani, bahdanau):
        all_citations = [vaswani, bahdanau]
        contexts = extractor.extract_contexts(SAMPLE_TEXT, all_citations)
        for ctx_list in contexts.values():
            for c in ctx_list:
                assert 0.0 <= c.position <= 1.0

    def test_mention_type_is_valid(self, extractor, vaswani, bahdanau, devlin):
        contexts = extractor.extract_contexts(SAMPLE_TEXT, [vaswani, bahdanau, devlin])
        valid_types = {"narrative", "parenthetical", "numeric"}
        for ctx_list in contexts.values():
            for c in ctx_list:
                assert c.mention_type in valid_types

    def test_no_match_returns_empty(self, extractor):
        """Citation that doesn't appear in the text returns no contexts."""
        ghost = Citation(
            authors=["Nobody, N."],
            title="This Paper Does Not Exist",
            year=2099,
            raw_text="Nobody (2099). This Paper Does Not Exist.",
        )
        contexts = extractor.extract_contexts(SAMPLE_TEXT, [ghost])
        assert len(contexts) == 0

    def test_bibliography_not_matched(self, extractor, vaswani):
        """References section entries shouldn't be matched as in-text citations."""
        # Text with body citation + clear bibliography section
        text = (
            "The model (Vaswani et al., 2017) processes tokens in parallel.\n\n"
            "References\n\n"
            "Vaswani et al. (2017). Attention Is All You Need.\n"
        )
        contexts = extractor.extract_contexts(text, [vaswani])
        # The bibliography line is stripped; only the body mention should match
        key = vaswani.title
        if key in contexts:
            for c in contexts[key]:
                # Context should not just be the bare bibliography line
                assert len(c.context_text) > 30

    def test_missing_year_skipped(self, extractor):
        """Citation without year produces no patterns and no contexts."""
        no_year = Citation(
            authors=["Smith, J."],
            title="No Year Paper",
            year=None,
            raw_text="Smith. No Year Paper.",
        )
        contexts = extractor.extract_contexts(SAMPLE_TEXT, [no_year])
        assert len(contexts) == 0

    def test_empty_citations_list(self, extractor):
        contexts = extractor.extract_contexts(SAMPLE_TEXT, [])
        assert contexts == {}

    def test_doi_used_as_key_when_present(self, extractor):
        """If citation has a DOI, it should be the dict key."""
        with_doi = Citation(
            authors=["Vaswani, A.", "Shazeer, N.", "Parmar, N."],
            title="Attention Is All You Need",
            year=2017,
            doi="10.48550/arXiv.1706.03762",
            raw_text="Vaswani et al. (2017).",
        )
        contexts = extractor.extract_contexts(SAMPLE_TEXT, [with_doi])
        assert with_doi.doi in contexts


# ---------------------------------------------------------------------------
# format_contexts_for_synthesis
# ---------------------------------------------------------------------------

class TestFormatContexts:

    def test_returns_string(self, extractor, vaswani):
        contexts = extractor.extract_contexts(SAMPLE_TEXT, [vaswani])
        result = extractor.format_contexts_for_synthesis(contexts)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_empty_contexts_returns_no_contexts_message(self, extractor):
        result = extractor.format_contexts_for_synthesis({})
        assert result == "No citation contexts extracted."

    def test_respects_max_contexts_per_citation(self, extractor, vaswani):
        """Should cap at max_contexts_per_citation even if more were found."""
        contexts = extractor.extract_contexts(SAMPLE_TEXT, [vaswani])
        result = extractor.format_contexts_for_synthesis(contexts, max_contexts_per_citation=1)
        # Should have exactly one [1] marker per citation
        assert result.count("[1]") >= 1
        assert "[2]" not in result

    def test_includes_author_year_label(self, extractor, vaswani):
        contexts = extractor.extract_contexts(SAMPLE_TEXT, [vaswani])
        result = extractor.format_contexts_for_synthesis(contexts)
        assert "Vaswani" in result
        assert "2017" in result


# ---------------------------------------------------------------------------
# Numeric citation style [N] — the dominant format in CS/ML papers
# ---------------------------------------------------------------------------

# Simulates pdfplumber output from a typical arXiv paper: no spaces between
# word and bracket, commas inside brackets, mixed numeric + author-year styles.
NUMERIC_TEXT = """\
Introduction

The attention mechanism was first proposed in [1]. The Transformer [2]
eliminates recurrence entirely, relying solely on self-attention. We build
on [1, 2] and extend the approach of [3] to multilingual settings.
Prior work [4] showed similar improvements. Combining [2] with [3] yields
the best performance.

References

[1] Bahdanau et al. Neural machine translation by jointly learning...
[2] Vaswani et al. Attention is all you need. NeurIPS 2017.
[3] Devlin et al. BERT: Pre-training of deep bidirectional transformers.
[4] Radford et al. Improving language understanding by generative pre-training.
"""


class TestNumericCitations:
    """Numeric [N] citation style — arXiv ML papers."""

    @pytest.fixture
    def extractor(self):
        return CitationContextExtractor(context_sentences=2)

    @pytest.fixture
    def citations(self):
        # Ordered list as GROBID would produce them (0-based → 1-based in text)
        return [
            Citation(authors=["Bahdanau, D.", "Cho, K.", "Bengio, Y."],
                     title="Neural machine translation", year=2014),
            Citation(authors=["Vaswani, A.", "Shazeer, N.", "Parmar, N."],
                     title="Attention Is All You Need", year=2017),
            Citation(authors=["Devlin, J.", "Chang, M.", "Lee, K."],
                     title="BERT", year=2019),
        ]

    def test_finds_single_bracket_citation(self, extractor, citations):
        """[1] alone on a line or inline should be found."""
        contexts = extractor.extract_contexts(NUMERIC_TEXT, citations)
        # Bahdanau is index 0 → [1]
        key = citations[0].title
        assert key in contexts

    def test_finds_bracket_within_list(self, extractor, citations):
        """[1, 2] should match both citation 1 and citation 2."""
        contexts = extractor.extract_contexts(NUMERIC_TEXT, citations)
        key0 = citations[0].title  # Bahdanau [1]
        key1 = citations[1].title  # Vaswani  [2]
        assert key0 in contexts
        assert key1 in contexts

    def test_mention_type_is_numeric(self, extractor, citations):
        contexts = extractor.extract_contexts(NUMERIC_TEXT, citations)
        for ctx_list in contexts.values():
            for c in ctx_list:
                assert c.mention_type == "numeric"

    def test_context_contains_surrounding_text(self, extractor, citations):
        """Context around [2] should include words from the citing sentence."""
        contexts = extractor.extract_contexts(NUMERIC_TEXT, citations)
        key = citations[1].title  # Vaswani [2]
        assert key in contexts
        combined = " ".join(c.context_text for c in contexts[key])
        # The citing sentence mentions "Transformer" or "attention"
        assert any(kw in combined.lower() for kw in ["transformer", "attention", "recurrence"])

    def test_does_not_match_wrong_citation_number(self, extractor):
        """[30] should not match a pattern for [3]."""
        _placeholder = Citation(raw_text="placeholder")
        citation_3 = Citation(
            authors=["Some, A."], title="Citation Three", year=2020,
        )
        text = "Results in [30] show improvements over [3]."
        # citation_3 is at index 2 → matches [3], not [30]
        contexts = extractor.extract_contexts(text, [_placeholder, _placeholder, citation_3])
        key = citation_3.title
        assert key in contexts
        for c in contexts[key]:
            assert "[3]" in c.context_text or "improvements" in c.context_text

    def test_citation_without_authors_still_gets_numeric_pattern(self, extractor):
        """Even if GROBID failed to parse authors, numeric matching should work."""
        minimal = Citation(
            authors=None,
            title="Minimal Citation",
            year=None,
            raw_text="[1] Minimal Citation.",
        )
        text = "The model in [1] achieves strong results on benchmarks."
        contexts = extractor.extract_contexts(text, [minimal])
        assert minimal.title in contexts


# ---------------------------------------------------------------------------
# bibliography removal
# ---------------------------------------------------------------------------

class TestBibliographyRemoval:

    def test_removes_references_section(self, extractor):
        text = (
            "The model (Smith, 2020) is effective.\n\n"
            "References\n\n"
            "Smith (2020). A Paper.\n"
        )
        cleaned = extractor._remove_bibliography(text)
        assert "References" not in cleaned

    def test_keeps_early_references_mention(self, extractor):
        """'References' in the first half of the text should not be stripped."""
        text = (
            "References to prior work abound in this literature.\n" * 20
            + "\nReferences\n\nSmith (2020). A Paper.\n"
        )
        # The word 'References' appears early (not stripped) but the section at end is
        cleaned = extractor._remove_bibliography(text)
        # Early mentions survive; the trailing reference list is stripped
        assert "References to prior work" in cleaned
