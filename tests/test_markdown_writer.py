"""
Tests for Obsidian markdown generation.

Run all tests: pytest tests/test_markdown_writer.py
Run only unit tests: pytest tests/test_markdown_writer.py -m "not integration"
"""

import pytest
import yaml
from pathlib import Path

from paper_library.markdown_writer import MarkdownWriter
from paper_library.models import PaperMetadata, Synthesis, Citation


class TestMarkdownWriterPaper:
    """Tests for paper markdown generation"""

    @pytest.fixture
    def sample_metadata(self):
        """Sample paper metadata"""
        return PaperMetadata(
            title="Attention Is All You Need",
            authors=["Vaswani, Ashish", "Shazeer, Noam"],
            year=2017,
            arxiv_id="1706.03762",
            abstract="The dominant sequence transduction models...",
        )

    @pytest.fixture
    def sample_synthesis(self):
        """Sample synthesis data"""
        return Synthesis(
            summary="This paper introduces the Transformer.",
            why_you_cared="Foundation for modern LLMs.",
            key_concepts=["transformers", "attention-mechanism"],
            memorable_quote="The Transformer is the first transduction model.",
            cost_usd=0.0042,
        )

    def test_paper_to_markdown_produces_output(self, sample_metadata, sample_synthesis):
        """Test that markdown is generated"""
        markdown = MarkdownWriter.paper_to_markdown(sample_metadata, sample_synthesis)
        assert len(markdown) > 0
        assert isinstance(markdown, str)

    def test_markdown_contains_title(self, sample_metadata, sample_synthesis):
        """Test that markdown includes paper title"""
        markdown = MarkdownWriter.paper_to_markdown(sample_metadata, sample_synthesis)
        assert "Attention Is All You Need" in markdown

    def test_markdown_has_yaml_frontmatter(self, sample_metadata, sample_synthesis):
        """Test that YAML frontmatter is present and valid"""
        markdown = MarkdownWriter.paper_to_markdown(sample_metadata, sample_synthesis)

        lines = markdown.split("\n")
        start = lines.index("---")
        end = lines.index("---", start + 1)
        frontmatter_str = "\n".join(lines[start + 1 : end])

        frontmatter = yaml.safe_load(frontmatter_str)
        assert frontmatter is not None
        assert frontmatter["title"] == "Attention Is All You Need"
        assert frontmatter["year"] == 2017


class TestMarkdownFilenameGeneration:
    """Tests for markdown filename generation"""

    def test_filename_basic_format(self):
        """Test basic filename format"""
        metadata = PaperMetadata(title="Simple Title", authors=["Smith, John"], year=2023)

        filename = MarkdownWriter.generate_filename(metadata)

        assert filename.startswith("Smith")
        assert "(2023)" in filename
        assert "Simple Title" in filename

    def test_filename_removes_quotes(self):
        """Test that quotation marks are removed"""
        metadata = PaperMetadata(
            title='What "Should" Happen?',
            authors=["Smith, John"],
            year=2023,
        )

        filename = MarkdownWriter.generate_filename(metadata)
        assert '"' not in filename
        assert "'" not in filename

    def test_filename_removes_problematic_characters(self):
        """Test that special characters are removed"""
        metadata = PaperMetadata(
            title="Title: With / Slashes",
            authors=["Smith, John"],
            year=2023,
        )

        filename = MarkdownWriter.generate_filename(metadata)

        for char in ["/", "\\", "*", "?", "<", ">", "|"]:
            assert char not in filename
