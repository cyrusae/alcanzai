"""
Citation context extraction.

This module finds where citations are mentioned in paper text and extracts
the surrounding context (typically 1-3 sentences). This helps understand:
- Why the paper cited this work
- How they used the cited work
- What claims they're supporting with the citation

Python concepts:
- Regular expressions for pattern matching
- Text windowing and context extraction
- Citation format detection
"""

import re
from typing import Optional
from dataclasses import dataclass

from paper_library.models import Citation


@dataclass
class CitationContext:
    """
    Context where a citation appears in the paper.
    
    Attributes:
        citation: The citation object
        context_text: Surrounding sentences (usually 1-3 sentences)
        mention_type: How the citation appears (e.g., "(Author, Year)" or "[42]")
        position: Approximate position in paper (0.0 = start, 1.0 = end)
    """
    citation: Citation
    context_text: str
    mention_type: str  # "narrative", "parenthetical", "numeric"
    position: float  # 0.0 to 1.0


class CitationContextExtractor:
    """
    Extract contexts where citations are mentioned in paper text.
    
    This handles multiple citation formats:
    - Narrative: "Smith et al. (2023) show that..."
    - Parenthetical: "...attention mechanisms (Vaswani et al., 2017)."
    - Numeric: "...as shown previously [42]."
    
    Usage:
        extractor = CitationContextExtractor()
        contexts = extractor.extract_contexts(paper_text, citations)
        
        for context in contexts:
            print(f"{context.citation.authors[0]}: {context.context_text}")
    """
    
    def __init__(self, context_sentences: int = 2):
        """
        Initialize the extractor.
        
        Args:
            context_sentences: Number of sentences to include around citation
                              (1 = just the sentence with citation, 2 = before+current, etc.)
        """
        self.context_sentences = context_sentences
    
    def extract_contexts(
        self, 
        paper_text: str, 
        citations: list[Citation]
    ) -> dict[str, list[CitationContext]]:
        """
        Extract contexts for all citations in the paper.
        
        Args:
            paper_text: Full text of the paper
            citations: List of citations from bibliography
            
        Returns:
            Dictionary mapping citation key (doi or title) to list of contexts
            Each citation might appear multiple times in the paper.
        """
        # Split text into sentences for context extraction
        sentences = self._split_into_sentences(paper_text)
        
        # Build citation patterns for each citation
        citation_patterns = {}
        for citation in citations:
            patterns = self._build_citation_patterns(citation)
            citation_patterns[citation] = patterns
        
        # Find mentions for each citation
        all_contexts = {}
        
        for citation, patterns in citation_patterns.items():
            contexts = []
            
            # Search through sentences for mentions
            for i, sentence in enumerate(sentences):
                for pattern, mention_type in patterns:
                    if re.search(pattern, sentence, re.IGNORECASE):
                        # Found a mention! Extract context
                        context_text = self._extract_context_window(
                            sentences, i, self.context_sentences
                        )
                        
                        # Calculate position in paper (0.0 to 1.0)
                        position = i / len(sentences) if sentences else 0.0
                        
                        contexts.append(CitationContext(
                            citation=citation,
                            context_text=context_text,
                            mention_type=mention_type,
                            position=position
                        ))
                        break  # Only count once per sentence
            
            # Store contexts if we found any
            if contexts:
                # Use DOI as key if available, otherwise title
                key = citation.doi or citation.title or citation.raw_text[:50]
                all_contexts[key] = contexts
        
        return all_contexts
    
    def _split_into_sentences(self, text: str) -> list[str]:
        """
        Split text into sentences.
        
        This is a simple heuristic that works for most academic papers.
        We split on periods followed by whitespace and capital letters.
        
        Args:
            text: Full text to split
            
        Returns:
            List of sentences
        """
        # Remove bibliography section if present (reduces false matches)
        text = self._remove_bibliography(text)
        
        # Simple sentence splitting
        # Split on: ". " or ".\n" followed by capital letter or number
        sentences = re.split(r'\.\s+(?=[A-Z0-9])', text)
        
        # Clean up sentences
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return sentences
    
    def _remove_bibliography(self, text: str) -> str:
        """
        Remove bibliography/references section from text.
        
        This prevents false matches with citation text in the bibliography.
        We use heuristics to find where the bibliography starts.
        
        Args:
            text: Full paper text
            
        Returns:
            Text with bibliography removed
        """
        # Common bibliography section headers
        bibliography_markers = [
            r'\nReferences\n',
            r'\nREFERENCES\n',
            r'\nBibliography\n',
            r'\nBIBLIOGRAPHY\n',
            r'\nWorks Cited\n',
            r'\n\d+\.\s+References\n',  # "7. References"
        ]
        
        # Find the earliest bibliography marker
        earliest_pos = len(text)
        
        for marker in bibliography_markers:
            match = re.search(marker, text)
            if match:
                # Only remove if it's in the latter half of the paper
                # (avoids false positives in introduction)
                if match.start() > len(text) * 0.5:
                    earliest_pos = min(earliest_pos, match.start())
        
        # Truncate at bibliography
        if earliest_pos < len(text):
            text = text[:earliest_pos]
        
        return text
    
    def _build_citation_patterns(self, citation: Citation) -> list[tuple[str, str]]:
        """
        Build regex patterns to find mentions of this citation.
        
        Returns multiple patterns because citations can be formatted different ways:
        - "Smith et al. (2023)"  [narrative]
        - "(Smith et al., 2023)"  [parenthetical]
        - "Smith and Jones (2023)"  [two authors]
        - "Smith, Jones, and Chen (2023)"  [three authors]
        
        Args:
            citation: Citation to build patterns for
            
        Returns:
            List of (pattern, mention_type) tuples
        """
        patterns = []
        
        if not citation.authors or not citation.year:
            # Can't build good patterns without author+year
            return patterns
        
        # Extract first author's last name
        first_author = citation.authors[0]
        # Authors are formatted as "Lastname, Firstname"
        last_name = first_author.split(',')[0].strip()
        
        year = str(citation.year)
        
        # Pattern 1: Narrative citation - "Smith et al. (2023)"
        if len(citation.authors) > 2:
            pattern = rf'\b{re.escape(last_name)}\s+et\s+al\.?\s*\({year}\)'
            patterns.append((pattern, "narrative"))
        
        # Pattern 2: Two authors - "Smith and Jones (2023)"
        if len(citation.authors) == 2:
            second_author = citation.authors[1].split(',')[0].strip()
            pattern = rf'\b{re.escape(last_name)}\s+(?:and|&)\s+{re.escape(second_author)}\s*\({year}\)'
            patterns.append((pattern, "narrative"))
        
        # Pattern 3: Single author - "Smith (2023)"
        if len(citation.authors) == 1:
            pattern = rf'\b{re.escape(last_name)}\s*\({year}\)'
            patterns.append((pattern, "narrative"))
        
        # Pattern 4: Parenthetical citation - "(Smith et al., 2023)"
        if len(citation.authors) > 2:
            pattern = rf'\({re.escape(last_name)}\s+et\s+al\.?,?\s*{year}\)'
            patterns.append((pattern, "parenthetical"))
        
        # Pattern 5: Parenthetical with two authors
        if len(citation.authors) == 2:
            second_author = citation.authors[1].split(',')[0].strip()
            pattern = rf'\({re.escape(last_name)}\s+(?:and|&)\s+{re.escape(second_author)},?\s*{year}\)'
            patterns.append((pattern, "parenthetical"))
        
        # Pattern 6: Parenthetical single author
        if len(citation.authors) == 1:
            pattern = rf'\({re.escape(last_name)},?\s*{year}\)'
            patterns.append((pattern, "parenthetical"))
        
        return patterns
    
    def _extract_context_window(
        self, 
        sentences: list[str], 
        index: int, 
        window_size: int
    ) -> str:
        """
        Extract context window around a sentence.
        
        Args:
            sentences: List of all sentences
            index: Index of sentence containing citation
            window_size: Number of sentences to include (2 = current + previous)
            
        Returns:
            Context text (multiple sentences joined)
        """
        # Calculate window boundaries
        start = max(0, index - (window_size - 1))
        end = min(len(sentences), index + 1)
        
        # Extract and join sentences
        context_sentences = sentences[start:end]
        context_text = ". ".join(context_sentences)
        
        # Ensure it ends with period
        if not context_text.endswith('.'):
            context_text += '.'
        
        return context_text
    
    def format_contexts_for_synthesis(
        self,
        contexts: dict[str, list[CitationContext]],
        max_contexts_per_citation: int = 2
    ) -> str:
        """
        Format contexts for inclusion in synthesis prompt.
        
        Args:
            contexts: Dictionary of citation contexts
            max_contexts_per_citation: Maximum contexts to include per citation
            
        Returns:
            Formatted string for prompt
        """
        if not contexts:
            return "No citation contexts extracted."
        
        formatted = []
        
        for key, context_list in contexts.items():
            # Get citation info from first context
            citation = context_list[0].citation
            
            # Format citation reference
            if citation.authors and citation.year:
                first_author = citation.authors[0].split(',')[0]
                if len(citation.authors) > 1:
                    cite_ref = f"{first_author} et al. ({citation.year})"
                else:
                    cite_ref = f"{first_author} ({citation.year})"
            else:
                cite_ref = citation.title[:50] if citation.title else "Unknown"
            
            formatted.append(f"\n{cite_ref}:")
            
            # Add contexts (limit to max_contexts_per_citation)
            for i, context in enumerate(context_list[:max_contexts_per_citation]):
                formatted.append(f'  [{i+1}] "{context.context_text}"')
        
        return "\n".join(formatted)


def extract_citation_contexts(
    paper_text: str,
    citations: list[Citation],
    context_sentences: int = 2
) -> dict[str, list[CitationContext]]:
    """
    Convenience function to extract citation contexts.
    
    Args:
        paper_text: Full paper text
        citations: List of citations from bibliography
        context_sentences: Number of sentences to include in context
        
    Returns:
        Dictionary mapping citation key to contexts
    """
    extractor = CitationContextExtractor(context_sentences)
    return extractor.extract_contexts(paper_text, citations)