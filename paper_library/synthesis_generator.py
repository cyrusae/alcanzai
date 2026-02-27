"""
Synthesis generator using Claude API with native Agent Skills.

This module calls Claude to generate AI summaries of papers and articles.
It produces structured syntheses with:
- Quick summary (3-4 sentences)
- Why you cared (relevance context)
- Key concepts (tags)
- Memorable quote

Skills are uploaded to Anthropic's skills API and cached locally.
The skills handle instructions; the user message provides the paper text.

Python concepts:
- API client libraries (anthropic)
- Native Agent Skills API (betas=["skills-2025-10-02"])
- Token counting and cost tracking
- Structured output parsing
"""

from datetime import datetime
from typing import Optional
import anthropic

from paper_library.models import PaperMetadata, ArticleMetadata, Synthesis
from paper_library.skills_manager import SkillsManager

# Register configuration type alias
RegisterConfig = dict[str, str]

# Default register: selective jargon, mixed structure, balanced depth
DEFAULT_REGISTER: RegisterConfig = {
    "jargon": "selective",
    "structure": "mixed",
    "depth": "balanced",
}

# Skills used for quick synthesis (max 8 per request)
QUICK_SYNTHESIS_SKILLS = [
    "understand-academic-text",
    "extract-arguments",
    "identify-terminology",
    "register-controller",
    "quick-summary",
]


class SynthesisGenerator:
    """
    Generate AI summaries using Claude with native Agent Skills.

    Uses claude-haiku-4-5 for cost-effective synthesis. Skills are uploaded
    once and cached locally — subsequent runs skip re-upload.

    Usage:
        generator = SynthesisGenerator(api_key="sk-...")
        synthesis = generator.generate_quick_synthesis(paper_text, metadata)
        print(synthesis.summary)

    With register:
        synthesis = generator.generate_quick_synthesis(
            paper_text, metadata,
            register={"jargon": "heavy", "structure": "mixed", "depth": "assume-knowledge"}
        )
    """

    # Pricing for Claude Haiku (as of Jan 2026)
    INPUT_PRICE_PER_MTOK = 1.00   # $1.00 per million input tokens
    OUTPUT_PRICE_PER_MTOK = 5.00  # $5.00 per million output tokens

    MODEL = "claude-haiku-4-5"

    # Betas and tools required for skills API
    # Skills run inside a code execution container — code_execution tool is required
    # even when skills don't execute scripts.
    SKILLS_BETA = "skills-2025-10-02"
    CODE_EXECUTION_BETA = "code-execution-2025-08-25"
    CODE_EXECUTION_TOOL = {"type": "code_execution_20250825", "name": "code_execution"}

    def __init__(self, api_key: str):
        """
        Initialize the synthesis generator.

        Args:
            api_key: Anthropic API key
        """
        self.client = anthropic.Anthropic(api_key=api_key)
        self._skills_manager = SkillsManager(api_key=api_key)

    def generate_quick_synthesis(
        self,
        text: str,
        metadata: PaperMetadata | ArticleMetadata,
        max_tokens: int = 1500,
        register: Optional[RegisterConfig] = None,
        citation_contexts: Optional[str] = None,
    ) -> Synthesis:
        """
        Generate a quick synthesis using native Agent Skills.

        Produces four structured sections:
        - 3-4 sentence summary
        - 3-4 sentence "why you cared"
        - 5-8 key concept tags
        - 1 memorable quote from the paper

        Skills handle the detailed instructions; the user message provides
        paper text and register configuration.

        Args:
            text: Full text of the paper/article
            metadata: Paper metadata (title, authors, etc.)
            max_tokens: Maximum tokens for Claude's response
            register: Writing style config with keys jargon, structure, depth.
                     Defaults to selective/mixed/balanced.

        Returns:
            Synthesis object with generated content
        """
        reg = register or DEFAULT_REGISTER

        # Build container with required skills
        skill_containers = self._skills_manager.build_skill_containers(QUICK_SYNTHESIS_SKILLS)

        # Build lean user message (skills handle the detailed instructions)
        message = self._build_quick_synthesis_message(text, metadata, reg, citation_contexts)

        # Call Claude with skills
        response = self.client.beta.messages.create(
            model=self.MODEL,
            max_tokens=max_tokens,
            betas=[self.CODE_EXECUTION_BETA, self.SKILLS_BETA],
            container={"skills": skill_containers},
            tools=[self.CODE_EXECUTION_TOOL],
            messages=[{"role": "user", "content": message}],
        )

        # The model reads skill files first (multi-step), then produces output.
        # The synthesis XML is in the last text block, not the first.
        text_blocks = [block.text for block in response.content if hasattr(block, "text")]
        response_text = text_blocks[-1] if text_blocks else ""
        synthesis_data = self._parse_quick_synthesis_response(response_text)

        cost = self._calculate_cost(
            response.usage.input_tokens,
            response.usage.output_tokens,
        )

        return Synthesis(
            summary=synthesis_data["summary"],
            why_you_cared=synthesis_data["why_you_cared"],
            key_concepts=synthesis_data["key_concepts"],
            memorable_quote=synthesis_data["memorable_quote"],
            generated_at=datetime.now(),
            model_used=self.MODEL,
            cost_usd=cost,
        )

    def _build_quick_synthesis_message(
        self,
        text: str,
        metadata: PaperMetadata | ArticleMetadata,
        register: RegisterConfig,
        citation_contexts: Optional[str] = None,
    ) -> str:
        """
        Build the lean user message for quick synthesis.

        The skills carry the detailed instructions; this message provides:
        - Paper identity (title, authors, year)
        - Register configuration
        - Paper text

        Args:
            text: Paper text
            metadata: Paper metadata
            register: Register configuration dict

        Returns:
            User message string
        """
        text_length = len(text)
        text_preview = text[:50000]

        if len(metadata.authors) > 3:
            authors_str = f"{metadata.authors[0]} et al."
        else:
            authors_str = ", ".join(metadata.authors)

        research_area = self._infer_research_area(metadata)

        jargon = register.get("jargon", "selective")
        structure = register.get("structure", "mixed")
        depth = register.get("depth", "balanced")

        year = getattr(metadata, "year", None) or (
            getattr(metadata, "published_date", None) and metadata.published_date.year
        ) or "Unknown"

        # Include citation contexts if extracted (helps ground why_you_cared).
        # Hard cap at ~10 k chars (~2 500 tokens) so we can't blow the 200 k
        # context limit even for papers with dense numeric citation lists.
        context_section = ""
        if citation_contexts and citation_contexts != "No citation contexts extracted.":
            MAX_CONTEXT_CHARS = 10_000
            if len(citation_contexts) > MAX_CONTEXT_CHARS:
                # Trim at a newline boundary so we don't cut mid-entry
                cutoff = citation_contexts.rfind("\n", 0, MAX_CONTEXT_CHARS)
                citation_contexts = citation_contexts[: cutoff if cutoff != -1 else MAX_CONTEXT_CHARS]
                citation_contexts += "\n\n...(citation contexts truncated)"
            context_section = f"""
Citation contexts (how this paper uses its key sources):
---
{citation_contexts}
---
"""

        return f"""Generate a quick synthesis of this academic paper.

Paper: "{metadata.title}"
Authors: {authors_str}
Year: {year}
Research area: {research_area}

Register: jargon={jargon}, structure={structure}, depth={depth}

Paper text ({text_length} characters):
---
{text_preview}
---
{context_section}
Use the quick-summary skill format with <summary>, <why_you_cared>, <key_concepts>, and <memorable_quote> XML tags."""

    def _infer_research_area(self, metadata: PaperMetadata | ArticleMetadata) -> str:
        """
        Infer the research area from metadata.

        Args:
            metadata: Paper metadata

        Returns:
            Research area string
        """
        title_lower = metadata.title.lower()
        venue_lower = (getattr(metadata, "venue", None) or "").lower()

        keywords = {
            "machine learning": ["neural", "learning", "model", "training", "deep"],
            "natural language processing": ["language", "nlp", "text", "translation", "llm"],
            "computer vision": ["vision", "image", "visual", "detection", "segmentation"],
            "reinforcement learning": ["reinforcement", "agent", "policy", "reward", "rl"],
            "interpretability": ["interpretability", "explainable", "transparency", "understanding"],
        }

        for area, terms in keywords.items():
            if any(term in title_lower or term in venue_lower for term in terms):
                return area

        return "machine learning and AI"

    def _parse_quick_synthesis_response(self, response_text: str) -> dict[str, any]:
        """
        Parse Claude's structured response.

        Extracts content from XML-style tags:
        <summary>...</summary>
        <why_you_cared>...</why_you_cared>
        <key_concepts>...</key_concepts>
        <memorable_quote>...</memorable_quote>

        Args:
            response_text: Claude's response

        Returns:
            Dictionary with parsed fields
        """
        import re

        def extract_tag(tag_name: str, text: str) -> str:
            pattern = f"<{tag_name}>(.*?)</{tag_name}>"
            match = re.search(pattern, text, re.DOTALL)
            if match:
                return match.group(1).strip()
            return ""

        summary = extract_tag("summary", response_text)
        why_you_cared = extract_tag("why_you_cared", response_text)
        key_concepts_raw = extract_tag("key_concepts", response_text)
        memorable_quote = extract_tag("memorable_quote", response_text)

        key_concepts = [
            concept.strip()
            for concept in key_concepts_raw.split(",")
            if concept.strip()
        ]

        memorable_quote = memorable_quote.strip('"').strip("'").strip()

        return {
            "summary": summary,
            "why_you_cared": why_you_cared,
            "key_concepts": key_concepts,
            "memorable_quote": memorable_quote,
        }

    def _calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate the cost of an API call.

        Args:
            input_tokens: Number of input tokens used
            output_tokens: Number of output tokens generated

        Returns:
            Cost in USD
        """
        input_cost = (input_tokens / 1_000_000) * self.INPUT_PRICE_PER_MTOK
        output_cost = (output_tokens / 1_000_000) * self.OUTPUT_PRICE_PER_MTOK
        return round(input_cost + output_cost, 4)

    def generate_detailed_summary(
        self,
        text: str,
        metadata: PaperMetadata,
        max_tokens: int = 4000,
        register: Optional[RegisterConfig] = None,
    ) -> str:
        """
        Generate a detailed section-by-section summary using the detailed-summary skill.

        Args:
            text: Full paper text
            metadata: Paper metadata
            max_tokens: Maximum tokens for response
            register: Writing style configuration

        Returns:
            Detailed summary as markdown string
        """
        reg = register or DEFAULT_REGISTER

        skill_containers = self._skills_manager.build_skill_containers(
            [
                "understand-academic-text",
                "extract-arguments",
                "identify-terminology",
                "register-controller",
                "detailed-summary",
            ]
        )

        if len(metadata.authors) > 3:
            authors_str = f"{metadata.authors[0]} et al."
        else:
            authors_str = ", ".join(metadata.authors)

        jargon = reg.get("jargon", "selective")
        structure = reg.get("structure", "mixed")
        depth = reg.get("depth", "balanced")
        text_preview = text[:50000]

        year = getattr(metadata, "year", None) or (
            getattr(metadata, "published_date", None) and metadata.published_date.year
        ) or "Unknown"

        message = f"""Generate a detailed section-by-section summary of this academic paper.

Paper: "{metadata.title}"
Authors: {authors_str}
Year: {year}

Register: jargon={jargon}, structure={structure}, depth={depth}

Paper text ({len(text)} characters):
---
{text_preview}
---

Use the detailed-summary skill format with <detailed_summary> XML tags."""

        response = self.client.beta.messages.create(
            model=self.MODEL,
            max_tokens=max_tokens,
            betas=[self.CODE_EXECUTION_BETA, self.SKILLS_BETA],
            container={"skills": skill_containers},
            tools=[self.CODE_EXECUTION_TOOL],
            messages=[{"role": "user", "content": message}],
        )

        # Model reads skill files first (multi-step), output is in the last text block
        text_blocks = [block.text for block in response.content if hasattr(block, "text")]
        return text_blocks[-1] if text_blocks else ""

    def generate_glossary(
        self,
        text: str,
        metadata: PaperMetadata | ArticleMetadata,
        max_tokens: int = 3000,
        register: Optional[RegisterConfig] = None,
    ) -> str:
        """
        Extract a technical glossary from the paper using the glossary-extraction skill.

        Args:
            text: Full paper text
            metadata: Paper metadata
            max_tokens: Maximum tokens for response
            register: Writing style configuration

        Returns:
            Glossary as markdown string
        """
        reg = register or DEFAULT_REGISTER

        skill_containers = self._skills_manager.build_skill_containers(
            [
                "identify-terminology",
                "register-controller",
                "glossary-extraction",
            ]
        )

        if len(metadata.authors) > 3:
            authors_str = f"{metadata.authors[0]} et al."
        else:
            authors_str = ", ".join(metadata.authors)

        jargon = reg.get("jargon", "selective")
        depth = reg.get("depth", "balanced")
        text_preview = text[:50000]

        message = f"""Extract a technical glossary from this academic paper.

Paper: "{metadata.title}"
Authors: {authors_str}

Register: jargon={jargon}, depth={depth}

Paper text ({len(text)} characters):
---
{text_preview}
---

Use the glossary-extraction skill format with <glossary> XML tags."""

        response = self.client.beta.messages.create(
            model=self.MODEL,
            max_tokens=max_tokens,
            betas=[self.CODE_EXECUTION_BETA, self.SKILLS_BETA],
            container={"skills": skill_containers},
            tools=[self.CODE_EXECUTION_TOOL],
            messages=[{"role": "user", "content": message}],
        )

        for block in response.content:
            if hasattr(block, "text"):
                return block.text
        return response.content[0].text


# Convenience function for quick use
def generate_synthesis(
    text: str,
    metadata: PaperMetadata | ArticleMetadata,
    api_key: str,
    register: Optional[RegisterConfig] = None,
) -> Synthesis:
    """
    Convenience function to generate a synthesis.

    Args:
        text: Paper text
        metadata: Paper metadata
        api_key: Anthropic API key
        register: Optional register configuration

    Returns:
        Synthesis object
    """
    generator = SynthesisGenerator(api_key)
    return generator.generate_quick_synthesis(text, metadata, register=register)
