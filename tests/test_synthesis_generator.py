"""
Tests for Claude synthesis generation.

Run all tests: pytest tests/test_synthesis_generator.py
Run only unit tests: pytest tests/test_synthesis_generator.py -m "not integration"
Run only integration: pytest tests/test_synthesis_generator.py -m integration
"""

import pytest
from datetime import datetime

from paper_library.config import config
from paper_library.synthesis_generator import SynthesisGenerator
from paper_library.models import PaperMetadata, Synthesis


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
