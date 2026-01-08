"""
Synthesis generator using Claude API.

This module calls Claude to generate AI summaries of papers and articles.
It produces structured syntheses with:
- Quick summary (3-4 sentences)
- Why you cared (relevance context)
- Key concepts (tags)
- Memorable quote

Python concepts:
- API client libraries (anthropic)
- Prompt engineering
- Token counting and cost tracking
- Structured output parsing
"""

from datetime import datetime
from typing import Optional
import anthropic

from paper_library.models import PaperMetadata, ArticleMetadata, Synthesis


class SynthesisGenerator:
    """
    Generate AI summaries using Claude.
    
    This uses Claude Haiku for cost-effective synthesis.
    The prompts are designed to produce consistent, structured output.
    
    Usage:
        generator = SynthesisGenerator(api_key="sk-...")
        synthesis = generator.generate_quick_synthesis(paper_text, metadata)
        print(synthesis.summary)
    """
    
    # Pricing for Claude Haiku (as of Jan 2026)
    # These are in USD per million tokens
    INPUT_PRICE_PER_MTOK = 1.00   # $1.00 per million input tokens
    OUTPUT_PRICE_PER_MTOK = 5.00  # $5.00 per million output tokens
    
    # Default model to use
    MODEL = "claude-haiku-4-5" # Fix to use current model -- date not necessary(?)
    
    def __init__(self, api_key: str):
        """
        Initialize the synthesis generator.
        
        Args:
            api_key: Anthropic API key
        """
        # Create Anthropic client
        # This handles authentication and API calls
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def generate_quick_synthesis(
        self,
        text: str,
        metadata: PaperMetadata | ArticleMetadata,
        max_tokens: int = 1500
    ) -> Synthesis:
        """
        Generate a quick synthesis (MVP version).
        
        This produces:
        - 3-4 sentence summary
        - 2-3 sentence "why you cared"
        - 5-8 key concept tags
        - 1 memorable quote from the paper
        
        Args:
            text: Full text of the paper/article
            metadata: Paper metadata (title, authors, etc.)
            max_tokens: Maximum tokens for Claude's response
            
        Returns:
            Synthesis object with generated content
        """
        # Build the prompt
        prompt = self._build_quick_synthesis_prompt(text, metadata)
        
        # Call Claude
        response = self.client.messages.create(
            model=self.MODEL,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        # Extract the response text
        # Claude returns a list of content blocks, we want the text
        response_text = response.content[0].text
        
        # Parse the structured response
        synthesis_data = self._parse_quick_synthesis_response(response_text)
        
        # Calculate cost
        # response.usage gives us token counts
        cost = self._calculate_cost(
            response.usage.input_tokens,
            response.usage.output_tokens
        )
        
        # Create Synthesis object
        synthesis = Synthesis(
            summary=synthesis_data["summary"],
            why_you_cared=synthesis_data["why_you_cared"],
            key_concepts=synthesis_data["key_concepts"],
            memorable_quote=synthesis_data["memorable_quote"],
            generated_at=datetime.now(),
            model_used=self.MODEL,
            cost_usd=cost
        )
        
        return synthesis
    
    def _build_quick_synthesis_prompt(
        self,
        text: str,
        metadata: PaperMetadata | ArticleMetadata
    ) -> str:
        """
        Build the prompt for quick synthesis.
        
        This uses a structured format to get consistent output.
        
        Args:
            text: Paper text
            metadata: Paper metadata
            
        Returns:
            Formatted prompt string
        """
        # Truncate text if too long (Claude has context limits)
        # For MVP, we send the full text since cost isn't a concern
        # But we'll add a note about length
        text_length = len(text)
        text_preview = text[:50000]  # First ~50k chars is usually enough
        
        # Format authors nicely
        if len(metadata.authors) > 3:
            authors_str = f"{metadata.authors[0]} et al."
        else:
            authors_str = ", ".join(metadata.authors)
        
        # Build the prompt
        # Using XML-style tags helps Claude structure its response
        prompt = f"""I need you to analyze this academic paper and provide a structured synthesis.

Paper: "{metadata.title}"
Authors: {authors_str}
Year: {metadata.year}

Please read the paper text below and provide:

1. SUMMARY: A 3-4 sentence overview of the paper's main contribution and findings. Focus on what they did and what they found.

2. WHY_YOU_CARED: 2-3 sentences explaining why this paper would be relevant to someone researching {self._infer_research_area(metadata)}. What makes it interesting or important?

3. KEY_CONCEPTS: 5-8 key terms or concepts that would be useful as tags. Use lowercase, hyphenated format (e.g., "neural-networks", "attention-mechanism"). These should be searchable concepts.

4. MEMORABLE_QUOTE: One standout sentence or phrase from the paper that captures something important. Use the exact wording from the text. Include quotation marks.

Paper text ({text_length} characters):
---
{text_preview}
---

Please format your response exactly like this:

<summary>
Your 3-4 sentence summary here.
</summary>

<why_you_cared>
Your 2-3 sentence explanation here.
</why_you_cared>

<key_concepts>
concept-1, concept-2, concept-3, concept-4, concept-5
</key_concepts>

<memorable_quote>
"Your exact quote from the paper here."
</memorable_quote>

Make sure to use the exact XML-style tags shown above."""
        
        return prompt
    
    def _infer_research_area(self, metadata: PaperMetadata | ArticleMetadata) -> str:
        """
        Infer the research area from metadata.
        
        This is a simple heuristic based on title/venue keywords.
        Used to make the "why you cared" section more relevant.
        
        Args:
            metadata: Paper metadata
            
        Returns:
            Research area string
        """
        # Simple keyword matching
        # This could be more sophisticated, but works for MVP
        title_lower = metadata.title.lower()
        venue_lower = getattr(metadata, 'venue', '').lower() if hasattr(metadata, 'venue') else ''
        
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
        
        # Default fallback
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
            """Extract content between <tag> and </tag>."""
            # Pattern matches: <tag>content</tag>
            # .*? means "match as few characters as possible" (non-greedy)
            # re.DOTALL means . matches newlines too
            pattern = f"<{tag_name}>(.*?)</{tag_name}>"
            match = re.search(pattern, text, re.DOTALL)
            if match:
                # .strip() removes leading/trailing whitespace
                return match.group(1).strip()
            return ""
        
        # Extract each field
        summary = extract_tag("summary", response_text)
        why_you_cared = extract_tag("why_you_cared", response_text)
        key_concepts_raw = extract_tag("key_concepts", response_text)
        memorable_quote = extract_tag("memorable_quote", response_text)
        
        # Parse key concepts (comma-separated list)
        # Split by comma and strip whitespace from each
        key_concepts = [
            concept.strip() 
            for concept in key_concepts_raw.split(",")
            if concept.strip()
        ]
        
        # Clean up quote (remove extra quotation marks if present)
        memorable_quote = memorable_quote.strip('"').strip("'").strip()
        
        return {
            "summary": summary,
            "why_you_cared": why_you_cared,
            "key_concepts": key_concepts,
            "memorable_quote": memorable_quote
        }
    
    def _calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate the cost of an API call.
        
        Claude charges separately for input and output tokens.
        Prices are per million tokens.
        
        Args:
            input_tokens: Number of input tokens used
            output_tokens: Number of output tokens generated
            
        Returns:
            Cost in USD
        """
        # Convert from "per million" to "per token"
        # Then multiply by token count
        input_cost = (input_tokens / 1_000_000) * self.INPUT_PRICE_PER_MTOK
        output_cost = (output_tokens / 1_000_000) * self.OUTPUT_PRICE_PER_MTOK
        
        total_cost = input_cost + output_cost
        
        return round(total_cost, 4)  # Round to 4 decimal places (0.0001 cents)
    
    def generate_detailed_summary(
        self,
        text: str,
        metadata: PaperMetadata,
        max_tokens: int = 4000
    ) -> str:
        """
        Generate a detailed section-by-section summary.
        
        This is deferred to v0.2, but the method exists for future use.
        
        Args:
            text: Full paper text
            metadata: Paper metadata
            max_tokens: Maximum tokens for response
            
        Returns:
            Detailed summary as markdown string
        """
        # TODO: Implement in v0.2
        # This would:
        # 1. Identify sections (Introduction, Methods, Results, etc.)
        # 2. Summarize each section separately
        # 3. Return structured markdown with section headers
        raise NotImplementedError("Detailed summaries deferred to v0.2")


# Convenience function for quick use
def generate_synthesis(
    text: str,
    metadata: PaperMetadata | ArticleMetadata,
    api_key: str
) -> Synthesis:
    """
    Convenience function to generate a synthesis.
    
    Args:
        text: Paper text
        metadata: Paper metadata
        api_key: Anthropic API key
        
    Returns:
        Synthesis object
    """
    generator = SynthesisGenerator(api_key)
    return generator.generate_quick_synthesis(text, metadata)
