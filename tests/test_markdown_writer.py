"""
Tests for Obsidian markdown generation.

Run all tests: pytest tests/test_markdown_writer.py
Run only unit tests: pytest tests/test_markdown_writer.py -m "not integration"
"""

import pytest
import yaml
from pathlib import Path

from paper_library.markdown_writer import MarkdownWriter
from paper_library.models import PaperMetadata, ArticleMetadata, Synthesis, Citation
from datetime import datetime


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


class TestSourceNoteMarkdown:
    """Tests for source_note_markdown() — the separate raw-content note."""

    def test_source_note_has_frontmatter(self):
        md = MarkdownWriter.source_note_markdown("My Paper", "raw text here", "pdf_text")
        assert md.startswith("---")
        assert 'type: "source"' in md
        assert 'source_type: "pdf_text"' in md

    def test_source_note_contains_content(self):
        content = "This is the full extracted text of the paper."
        md = MarkdownWriter.source_note_markdown("My Paper", content, "pdf_text")
        assert content in md

    def test_source_note_web_content_type(self):
        md = MarkdownWriter.source_note_markdown("An Article", "article text", "web_content")
        assert 'source_type: "web_content"' in md

    def test_source_note_title_in_frontmatter(self):
        md = MarkdownWriter.source_note_markdown("Attention Is All You Need", "text", "pdf_text")
        assert "Attention Is All You Need" in md


class TestPaperSourceNoteLink:
    """Tests that paper_to_markdown() includes the source note wikilink."""

    @pytest.fixture
    def sample_metadata(self):
        return PaperMetadata(
            title="Attention Is All You Need",
            authors=["Vaswani, Ashish"],
            year=2017,
            abstract="The dominant sequence transduction models...",
        )

    @pytest.fixture
    def sample_synthesis(self):
        return Synthesis(
            summary="Transformer architecture.",
            why_you_cared="Foundation for LLMs.",
            key_concepts=["transformers"],
            memorable_quote="Attention is all you need.",
            cost_usd=0.001,
        )

    def test_source_note_link_appears_when_provided(self, sample_metadata, sample_synthesis):
        md = MarkdownWriter.paper_to_markdown(
            sample_metadata, sample_synthesis,
            source_note_name="Vaswani et al (2017) - Attention Is All You Need - Source"
        )
        assert "[[Vaswani et al (2017) - Attention Is All You Need - Source]]" in md
        assert "## Source Text" in md

    def test_no_source_section_when_name_not_given(self, sample_metadata, sample_synthesis):
        md = MarkdownWriter.paper_to_markdown(sample_metadata, sample_synthesis)
        assert "## Source Text" not in md


class TestArticleSourceNoteLink:
    """Tests that article_to_markdown() uses a wikilink instead of embedded content."""

    @pytest.fixture
    def sample_article_metadata(self):
        return ArticleMetadata(
            title="Understanding Transformers",
            authors=["Jane Doe"],
            url="https://example.com/article",
            published_date=datetime(2024, 3, 15),
            publisher="Example Blog",
        )

    @pytest.fixture
    def sample_synthesis(self):
        return Synthesis(
            summary="Great article on transformers.",
            why_you_cared="Very educational.",
            key_concepts=["transformers"],
            memorable_quote="Transformers changed everything.",
            cost_usd=0.001,
        )

    def test_source_link_replaces_embedded_content(self, sample_article_metadata, sample_synthesis):
        md = MarkdownWriter.article_to_markdown(
            sample_article_metadata, sample_synthesis,
            source_note_name="Jane Doe (2024) - Understanding Transformers - Source"
        )
        assert "[[Jane Doe (2024) - Understanding Transformers - Source]]" in md
        assert "## Source Text" in md
        # The raw content string itself must NOT be embedded directly
        assert "## Original Content" not in md

    def test_no_source_section_when_name_not_given(self, sample_article_metadata, sample_synthesis):
        md = MarkdownWriter.article_to_markdown(sample_article_metadata, sample_synthesis)
        assert "## Source Text" not in md

    def test_article_still_has_synthesis_sections(self, sample_article_metadata, sample_synthesis):
        md = MarkdownWriter.article_to_markdown(
            sample_article_metadata, sample_synthesis,
            source_note_name="Some - Source"
        )
        assert "## Quick Refresh" in md
        assert "## Why You Cared" in md
        assert "## Key Concepts" in md


class TestNoneYearHandling:
    """Regression tests for R3/R4/R15: year=None should render cleanly,
    not leak 'None' or fall back to the current calendar year."""

    @pytest.fixture
    def undated_paper(self):
        return PaperMetadata(
            title="An Undated Preprint",
            authors=["Solo, One"],
            year=None,
        )

    @pytest.fixture
    def sample_synthesis(self):
        return Synthesis(
            summary="s", why_you_cared="w",
            key_concepts=["c"], memorable_quote="q", cost_usd=0.0,
        )

    def test_paper_byline_uses_nd_for_none_year(self, undated_paper, sample_synthesis):
        md = MarkdownWriter.paper_to_markdown(undated_paper, sample_synthesis)
        assert "n.d." in md
        # And definitely not the string "None"
        assert "• None" not in md

    def test_paper_frontmatter_omits_year_when_none(self, undated_paper, sample_synthesis):
        """YAML frontmatter should not include 'year: None' — omit the key instead."""
        md = MarkdownWriter.paper_to_markdown(undated_paper, sample_synthesis)
        # Extract the frontmatter block
        fm = md.split("---")[1]
        assert "year:" not in fm, f"year key should be omitted when None; got frontmatter:\n{fm}"

    def test_filename_uses_nd_for_none_year(self, undated_paper):
        name = MarkdownWriter.generate_filename(undated_paper)
        # Should use n.d. in the year slot, not a real year
        assert "(n.d.)" in name
        import datetime as dt
        assert f"({dt.datetime.now().year})" not in name


class TestArticleByline:
    """Regression tests for the article byline rendering (issue #10)."""

    @pytest.fixture
    def article_with_date(self):
        return ArticleMetadata(
            title="Test Article",
            authors=["Jane Doe"],
            url="https://example.com/article",
            published_date=datetime(2024, 3, 15),
            publisher="Example Blog",
        )

    @pytest.fixture
    def article_without_date(self):
        return ArticleMetadata(
            title="Test Article",
            authors=["Jane Doe"],
            url="https://example.com/article",
            published_date=None,
            publisher="Example Blog",
        )

    @pytest.fixture
    def sample_synthesis(self):
        return Synthesis(
            summary="s",
            why_you_cared="w",
            key_concepts=["c"],
            memorable_quote="q",
            cost_usd=0.001,
        )

    def test_byline_uses_real_bullet_not_mojibake(self, article_with_date, sample_synthesis):
        """Regression for issue #10: byline should contain a real Unicode bullet (U+2022),
        not the Windows-1252-double-encoded mojibake pattern 'â€¢'."""
        md = MarkdownWriter.article_to_markdown(article_with_date, sample_synthesis)
        # The real bullet character should appear
        assert "\u2022" in md, "expected real bullet character U+2022 in byline"
        # The mojibake sequence must NOT appear
        assert "\u00e2\u20ac\u00a2" not in md, "mojibake bullet sequence leaked into output"
        # Literal 'â€¢' form also must not appear (belt-and-braces)
        assert "â€¢" not in md

    def test_byline_omits_date_separator_when_no_date(self, article_without_date, sample_synthesis):
        """When published_date is None, no bullet+date segment should be written.
        Guards against a future change that inadvertently stringifies None as the date."""
        md = MarkdownWriter.article_to_markdown(article_without_date, sample_synthesis)
        # The bullet character is only used for the date separator; absent with no date
        assert "\u2022" not in md
        # And we definitely don't want 'None' appearing as a date
        assert "None" not in md.split("## Quick Refresh")[0]


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

    def test_filename_period_to_dash(self):
        """Periods in the title become dashes: '3.1' → '3-1', 'U.S.A.' → 'U-S-A-'."""
        metadata = PaperMetadata(
            title="Part 3.1 Analysis",
            authors=["Smith, John"],
            year=2023,
        )
        filename = MarkdownWriter.generate_filename(metadata)
        assert "3.1" not in filename
        assert "3-1" in filename

    def test_filename_acronym_periods_become_dashes(self):
        """All title periods, including those in acronyms, are replaced with dashes."""
        metadata = PaperMetadata(
            title="U.S.A. Economic Policy",
            authors=["Smith, John"],
            year=2023,
        )
        filename = MarkdownWriter.generate_filename(metadata)
        assert "U.S.A." not in filename
        # Each period replaced by a dash (collapsed runs → single dash)
        assert "U" in filename
        assert "S" in filename
        assert "A" in filename
        # No bare periods survive
        assert "." not in filename.split("(")[1]  # beyond the year portion

    def test_filename_truncated_when_too_long(self):
        """Filename (no extension) must be ≤ 77 chars when title is very long."""
        long_title = "A Very Long Title That Goes On And On And On And Will Definitely Exceed The Eighty Character Limit For Filenames"
        metadata = PaperMetadata(
            title=long_title,
            authors=["Smith, John"],
            year=2023,
        )
        filename = MarkdownWriter.generate_filename(metadata)
        assert len(filename) <= 77, f"Filename too long ({len(filename)}): {filename!r}"

    def test_filename_truncation_prefers_word_boundary(self):
        """Truncation should not leave a trailing dash or space after the cut."""
        long_title = "Neural Network Architectures for Processing Sequential Data in Modern Systems"
        metadata = PaperMetadata(
            title=long_title,
            authors=["Smith, John"],
            year=2023,
        )
        filename = MarkdownWriter.generate_filename(metadata)
        assert len(filename) <= 77
        # After stripping, the filename must not end with a bare dash or space
        assert not filename.endswith("-"), f"Filename ends with trailing dash: {filename!r}"
        assert not filename.endswith(" "), f"Filename ends with trailing space: {filename!r}"

    def test_filename_et_al_for_multiple_authors(self):
        """More than one author → 'FirstLast et al (Year) - Title'."""
        metadata = PaperMetadata(
            title="Test Paper",
            authors=["Vaswani, Ashish", "Shazeer, Noam", "Parmar, Niki"],
            year=2017,
        )
        filename = MarkdownWriter.generate_filename(metadata)
        assert "et al" in filename
        assert filename.startswith("Vaswani")

    def test_filename_single_author_no_et_al(self):
        """Single author → no 'et al'."""
        metadata = PaperMetadata(
            title="Solo Paper",
            authors=["Kaiser, Łukasz"],
            year=2020,
        )
        filename = MarkdownWriter.generate_filename(metadata)
        assert "et al" not in filename
        assert "Kaiser" in filename


class TestCitationWikilink:
    """_format_citation_wikilink: wikilink format with author/year/title fields."""

    def _make_citation(self, authors, year, title, raw_text="fallback raw"):
        return Citation(
            authors=authors,
            year=year,
            title=title,
            raw_text=raw_text,
        )

    def test_single_author_format(self):
        c = self._make_citation(["Smith, John"], 2020, "Neural Nets")
        link = MarkdownWriter._format_citation_wikilink(c)
        assert link == "[[Smith, John (2020) - Neural Nets]]"

    def test_two_author_format_uses_ampersand(self):
        c = self._make_citation(["Smith, J.", "Jones, A."], 2021, "Paper Title")
        link = MarkdownWriter._format_citation_wikilink(c)
        assert "Smith, J. & Jones, A." in link
        assert link.startswith("[[")
        assert link.endswith("]]")

    def test_three_author_format(self):
        c = self._make_citation(
            ["Vaswani, A.", "Shazeer, N.", "Parmar, N."], 2017, "Attention Is All You Need"
        )
        link = MarkdownWriter._format_citation_wikilink(c)
        assert "Vaswani, A." in link
        assert "Parmar, N." in link
        assert "&" in link

    def test_long_title_truncated_in_wikilink(self):
        long_title = "A" * 70
        c = self._make_citation(["Smith, J."], 2020, long_title)
        link = MarkdownWriter._format_citation_wikilink(c)
        # Title portion should not be the full 70 chars — it's truncated at 60
        assert long_title not in link
        assert "..." in link

    def test_fallback_to_raw_text_when_fields_missing(self):
        c = Citation(raw_text="Smith et al. (2020). No structured fields.", contexts=[])
        link = MarkdownWriter._format_citation_wikilink(c)
        assert link.startswith("[[")
        assert "Smith et al." in link

    def test_wikilink_format_double_brackets(self):
        c = self._make_citation(["Author, A."], 2022, "Some Title")
        link = MarkdownWriter._format_citation_wikilink(c)
        assert link.startswith("[[")
        assert link.endswith("]]")
        # Exactly one opening and one closing double bracket
        assert link.count("[[") == 1
        assert link.count("]]") == 1


class TestYamlFrontmatterEscaping:
    """YAML frontmatter must not break on special characters in title/author fields."""

    def _synth(self):
        return Synthesis(
            summary="s", why_you_cared="w",
            key_concepts=["c"], memorable_quote="q", cost_usd=0.0,
        )

    def _parse_frontmatter(self, md: str) -> dict:
        lines = md.split("\n")
        start = lines.index("---")
        end = lines.index("---", start + 1)
        return yaml.safe_load("\n".join(lines[start + 1:end]))

    def test_title_with_colon_produces_valid_yaml(self):
        paper = PaperMetadata(
            title="Attention: A Unified Perspective",
            authors=["Smith, J."],
            year=2022,
        )
        md = MarkdownWriter.paper_to_markdown(paper, self._synth())
        fm = self._parse_frontmatter(md)
        assert "Attention" in fm["title"]

    def test_title_with_double_quote_produces_valid_yaml(self):
        paper = PaperMetadata(
            title='What "Intelligence" Really Means',
            authors=["Smith, J."],
            year=2022,
        )
        md = MarkdownWriter.paper_to_markdown(paper, self._synth())
        fm = self._parse_frontmatter(md)
        # YAML must parse without error; title should contain the word
        assert "Intelligence" in fm["title"]

    def test_title_with_leading_dash_produces_valid_yaml(self):
        """A title starting with '-' would break YAML list parsing if unquoted."""
        paper = PaperMetadata(
            title="- An Unusual Title",
            authors=["Smith, J."],
            year=2022,
        )
        md = MarkdownWriter.paper_to_markdown(paper, self._synth())
        # Must parse without raising
        fm = self._parse_frontmatter(md)
        assert fm["title"] is not None

    def test_utf8_author_names_survive_yaml_round_trip(self):
        """Authors with non-ASCII characters must survive the YAML round-trip intact."""
        paper = PaperMetadata(
            title="Multilingual NLP",
            authors=["Kaiser, Łukasz", "Gómez, María"],
            year=2023,
        )
        md = MarkdownWriter.paper_to_markdown(paper, self._synth())
        fm = self._parse_frontmatter(md)
        author_block = str(fm["authors"])
        assert "Łukasz" in author_block
        assert "Gómez" in author_block or "María" in author_block
