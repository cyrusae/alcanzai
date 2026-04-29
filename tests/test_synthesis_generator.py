"""
Tests for Claude synthesis generation.

Run all tests: pytest tests/test_synthesis_generator.py
Run only unit tests: pytest tests/test_synthesis_generator.py -m "not integration"
Run only integration: pytest tests/test_synthesis_generator.py -m integration
"""

import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch

from paper_library.config import config
from paper_library.synthesis_generator import SynthesisGenerator, DEFAULT_REGISTER
from paper_library.models import PaperMetadata, ArticleMetadata, Synthesis


# ---------------------------------------------------------------------------
# Unit tests — no network required
# ---------------------------------------------------------------------------

class TestParseQuickSynthesisResponse:
    """_parse_quick_synthesis_response: XML tag extraction."""

    @pytest.fixture
    def gen(self):
        return SynthesisGenerator.__new__(SynthesisGenerator)

    def test_all_tags_present_returns_full_dict(self, gen):
        response = (
            "<summary>This paper proposes X.</summary>"
            "<why_you_cared>Relevant because Y.</why_you_cared>"
            "<key_concepts>attention, transformer, NLP</key_concepts>"
            "<memorable_quote>\"All you need is attention.\"</memorable_quote>"
        )
        result = gen._parse_quick_synthesis_response(response)
        assert result["summary"] == "This paper proposes X."
        assert result["why_you_cared"] == "Relevant because Y."
        assert result["key_concepts"] == ["attention", "transformer", "NLP"]
        assert result["memorable_quote"] == "All you need is attention."

    def test_missing_tag_returns_empty_string(self, gen):
        result = gen._parse_quick_synthesis_response("<summary>Only this.</summary>")
        assert result["summary"] == "Only this."
        assert result["why_you_cared"] == ""
        assert result["key_concepts"] == []
        assert result["memorable_quote"] == ""

    def test_key_concepts_split_on_comma(self, gen):
        response = "<key_concepts>  alpha ,  beta , gamma  </key_concepts>"
        result = gen._parse_quick_synthesis_response(response)
        assert result["key_concepts"] == ["alpha", "beta", "gamma"]

    def test_single_key_concept(self, gen):
        response = "<key_concepts>sole concept</key_concepts>"
        result = gen._parse_quick_synthesis_response(response)
        assert result["key_concepts"] == ["sole concept"]

    def test_memorable_quote_strips_surrounding_quotes(self, gen):
        result = gen._parse_quick_synthesis_response(
            '<memorable_quote>"Quoted text here."</memorable_quote>'
        )
        assert result["memorable_quote"] == "Quoted text here."

    def test_multiline_summary(self, gen):
        response = "<summary>Line one.\nLine two.</summary>"
        result = gen._parse_quick_synthesis_response(response)
        assert "Line one." in result["summary"]
        assert "Line two." in result["summary"]

    def test_empty_response_returns_empty_fields(self, gen):
        result = gen._parse_quick_synthesis_response("")
        assert result["summary"] == ""
        assert result["key_concepts"] == []


class TestCalculateCost:
    """_calculate_cost: pricing arithmetic."""

    @pytest.fixture
    def gen(self):
        return SynthesisGenerator.__new__(SynthesisGenerator)

    def test_zero_tokens_is_zero_cost(self, gen):
        assert gen._calculate_cost(0, 0) == 0.0

    def test_input_only_cost(self, gen):
        # 1M input tokens at $1.00/Mtok = $1.00
        assert gen._calculate_cost(1_000_000, 0) == pytest.approx(1.0, abs=0.001)

    def test_output_only_cost(self, gen):
        # 1M output tokens at $5.00/Mtok = $5.00
        assert gen._calculate_cost(0, 1_000_000) == pytest.approx(5.0, abs=0.001)

    def test_mixed_cost_rounded_to_four_decimals(self, gen):
        # 10k input + 1k output
        # 10_000/1_000_000 * 1.00 + 1_000/1_000_000 * 5.00
        # = 0.01 + 0.005 = 0.015
        result = gen._calculate_cost(10_000, 1_000)
        assert result == pytest.approx(0.015, abs=0.0001)
        # Must be rounded to 4 decimal places max
        assert len(str(result).rstrip("0").split(".")[-1]) <= 4

    def test_pricing_constants_are_plausible(self, gen):
        assert gen.INPUT_PRICE_PER_MTOK > 0
        assert gen.OUTPUT_PRICE_PER_MTOK > 0
        # Output should cost more than input (standard Anthropic pricing)
        assert gen.OUTPUT_PRICE_PER_MTOK > gen.INPUT_PRICE_PER_MTOK


class TestInferResearchArea:
    """_infer_research_area: keyword matching and fallback."""

    @pytest.fixture
    def gen(self):
        return SynthesisGenerator.__new__(SynthesisGenerator)

    def _meta(self, title: str) -> PaperMetadata:
        return PaperMetadata(title=title, authors=[], year=2024)

    def test_nlp_keyword_matches(self, gen):
        # Must avoid ML keywords (neural/learning/model/training/deep) which are
        # checked first in the keyword dict — use a title with only NLP signals.
        assert gen._infer_research_area(self._meta("Text translation with attention")) \
            == "natural language processing"

    def test_vision_keyword_matches(self, gen):
        # Same priority note: avoid ML keywords; use only CV signals.
        assert gen._infer_research_area(self._meta("Object detection in satellite imagery")) \
            == "computer vision"

    def test_rl_keyword_matches(self, gen):
        assert gen._infer_research_area(self._meta("Policy gradient reinforcement methods")) \
            == "reinforcement learning"

    def test_ml_keyword_matches(self, gen):
        assert gen._infer_research_area(self._meta("Deep learning training dynamics")) \
            == "machine learning"

    def test_unknown_falls_back_to_default(self, gen):
        area = gen._infer_research_area(self._meta("A study of ancient Roman aqueducts"))
        assert area == "machine learning and AI"

    def test_interpretability_keyword_matches(self, gen):
        assert gen._infer_research_area(
            self._meta("Mechanistic interpretability of transformer circuits")
        ) == "interpretability"


class TestBuildQuickSynthesisMessage:
    """_build_quick_synthesis_message: message content and edge cases."""

    @pytest.fixture
    def gen(self):
        return SynthesisGenerator.__new__(SynthesisGenerator)

    def _meta(self, authors=None) -> PaperMetadata:
        return PaperMetadata(
            title="Attention Is All You Need",
            authors=authors or ["Vaswani, Ashish", "Shazeer, Noam"],
            year=2017,
        )

    def test_contains_title_and_year(self, gen):
        msg = gen._build_quick_synthesis_message("body text", self._meta(), DEFAULT_REGISTER)
        assert "Attention Is All You Need" in msg
        assert "2017" in msg

    def test_two_authors_listed_in_full(self, gen):
        msg = gen._build_quick_synthesis_message("text", self._meta(), DEFAULT_REGISTER)
        assert "Vaswani, Ashish" in msg
        assert "Shazeer, Noam" in msg

    def test_four_authors_truncated_to_et_al(self, gen):
        many = ["A, B", "C, D", "E, F", "G, H"]
        msg = gen._build_quick_synthesis_message("text", self._meta(many), DEFAULT_REGISTER)
        assert "et al." in msg
        assert "C, D" not in msg  # only first author should appear

    def test_register_axes_appear_in_message(self, gen):
        reg = {"jargon": "heavy", "structure": "formal", "depth": "assume-knowledge"}
        msg = gen._build_quick_synthesis_message("text", self._meta(), reg)
        assert "jargon=heavy" in msg
        assert "structure=formal" in msg
        assert "depth=assume-knowledge" in msg

    def test_citation_contexts_included_when_provided(self, gen):
        contexts = "Smith et al. (2020): 'Relevant sentence here.'"
        msg = gen._build_quick_synthesis_message("text", self._meta(), DEFAULT_REGISTER,
                                                  citation_contexts=contexts)
        assert "Citation contexts" in msg
        assert "Smith et al." in msg

    def test_citation_contexts_truncated_at_10k_chars(self, gen):
        long_contexts = "a" * 15_000
        msg = gen._build_quick_synthesis_message("text", self._meta(), DEFAULT_REGISTER,
                                                  citation_contexts=long_contexts)
        # The rendered section should not contain the full 15k of 'a's
        assert len(msg) < 15_000 + 2_000  # 2k slack for message template
        assert "truncated" in msg

    def test_empty_citation_contexts_omitted(self, gen):
        msg = gen._build_quick_synthesis_message("text", self._meta(), DEFAULT_REGISTER,
                                                  citation_contexts=None)
        assert "Citation contexts" not in msg

    def test_placeholder_citation_contexts_omitted(self, gen):
        msg = gen._build_quick_synthesis_message(
            "text", self._meta(), DEFAULT_REGISTER,
            citation_contexts="No citation contexts extracted.",
        )
        assert "Citation contexts" not in msg


class TestApiRequestShape:
    """Mocked integration test: verifies the shape of the API call without a network."""

    def test_api_call_uses_correct_betas_and_tools(self):
        """client.beta.messages.create must be called with both required betas
        and the code_execution tool — a missing beta breaks the skills API."""
        gen = SynthesisGenerator.__new__(SynthesisGenerator)
        gen.client = MagicMock()
        gen._skills_manager = MagicMock()
        gen._skills_manager.get_skill_containers.return_value = [
            {"type": "custom", "skill_id": "skill_abc", "version": "latest"}
        ]

        # Build a plausible API response mock
        mock_response = MagicMock()
        mock_response.content = [MagicMock(type="text", text=(
            "<summary>Test summary.</summary>"
            "<why_you_cared>Relevant.</why_you_cared>"
            "<key_concepts>A, B, C</key_concepts>"
            "<memorable_quote>Quote.</memorable_quote>"
        ))]
        mock_response.usage.input_tokens = 100
        mock_response.usage.output_tokens = 50
        gen.client.beta.messages.create.return_value = mock_response

        metadata = PaperMetadata(title="Test", authors=["Author, A"], year=2024)
        gen.generate_quick_synthesis("some paper text", metadata)

        call_kwargs = gen.client.beta.messages.create.call_args.kwargs
        # Both beta flags are required
        assert SynthesisGenerator.SKILLS_BETA in call_kwargs["betas"]
        assert SynthesisGenerator.CODE_EXECUTION_BETA in call_kwargs["betas"]
        # code_execution tool must be present
        tool_types = [t.get("type") for t in call_kwargs.get("tools", [])]
        assert "code_execution_20250825" in tool_types
        # Skills container must be non-empty
        container = call_kwargs.get("container", {})
        assert container.get("skills"), "container.skills must be non-empty"


# ---------------------------------------------------------------------------
# Integration tests (live API — skipped by default)
# ---------------------------------------------------------------------------

class TestSynthesisGenerator:
    """Tests for synthesis generation using Claude"""

    @pytest.fixture
    def generator(self):
        """Create generator instance, skip if API key not available"""
        if not config.anthropic_api_key:
            pytest.skip("ANTHROPIC_API_KEY not set in environment")
        return SynthesisGenerator(config.anthropic_api_key)

    @pytest.fixture
    def sample_metadata(self):
        """Sample paper metadata for testing"""
        return PaperMetadata(
            title="Attention Is All You Need",
            authors=["Vaswani, Ashish", "Shazeer, Noam"],
            year=2017,
            abstract="The dominant sequence transduction models are based on complex recurrent or convolutional neural networks.",
        )

    @pytest.fixture
    def sample_text(self):
        """Sample paper text for synthesis"""
        return """
        The Transformer is the first transduction model relying entirely on self-attention
        to compute representations of its input and output without using sequence-aligned
        RNNs or convolution.
        """

    @pytest.mark.integration
    def test_generate_quick_synthesis_returns_synthesis_object(
        self, generator, sample_metadata, sample_text
    ):
        """Test that synthesis generation returns proper Synthesis object"""
        synthesis = generator.generate_quick_synthesis(sample_text, sample_metadata)
        assert isinstance(synthesis, Synthesis)

    @pytest.mark.integration
    def test_synthesis_has_all_required_fields(self, generator, sample_metadata, sample_text):
        """Test that synthesis contains all required fields"""
        synthesis = generator.generate_quick_synthesis(sample_text, sample_metadata)

        assert synthesis.summary is not None
        assert len(synthesis.summary) > 0
        assert synthesis.why_you_cared is not None
        assert synthesis.key_concepts is not None
        assert synthesis.memorable_quote is not None

    @pytest.mark.integration
    def test_synthesis_tracks_cost(self, generator, sample_metadata, sample_text):
        """Test that synthesis records API cost"""
        synthesis = generator.generate_quick_synthesis(sample_text, sample_metadata)
        assert synthesis.cost_usd >= 0
        assert synthesis.cost_usd < 1.0
