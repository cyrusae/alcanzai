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
from dataclasses import dataclass, field

from paper_library.models import Citation


@dataclass
class CitationContext:
    """
    Context where a citation appears in the paper.

    Attributes:
        citation: The citation object
        context_text: Surrounding sentences (usually 1-3 sentences)
        mention_type: How the citation appears ("narrative" or "parenthetical")
        position: Approximate position in paper (0.0 = start, 1.0 = end)
    """
    citation: Citation
    context_text: str
    mention_type: str  # "narrative", "parenthetical"
    position: float    # 0.0 to 1.0


class CitationContextExtractor:
    """
    Extract contexts where citations are mentioned in paper text.

    Handles two citation formats:
    - Narrative: "Smith et al. (2023) show that..."
    - Parenthetical: "...attention mechanisms (Vaswani et al., 2017)."

    Numeric citations ([42]) are not yet supported.

    Usage:
        extractor = CitationContextExtractor()
        contexts = extractor.extract_contexts(paper_text, citations)
        formatted = extractor.format_contexts_for_synthesis(contexts)
    """

    def __init__(self, context_sentences: int = 2):
        """
        Args:
            context_sentences: Number of sentences to include around citation.
                               2 = the citing sentence + one before it.
        """
        self.context_sentences = context_sentences

    def extract_contexts(
        self,
        paper_text: str,
        citations: list[Citation],
    ) -> dict[str, list[CitationContext]]:
        """
        Extract contexts for all citations in the paper.

        Args:
            paper_text: Full text of the paper
            citations: List of citations from bibliography

        Returns:
            Dict mapping citation key (doi or title) to list of CitationContext objects.
            A citation may appear multiple times, so each key maps to a list.
        """
        # Split text into sentences, stripping the bibliography section first
        # to avoid matching citation text in the reference list itself
        sentences = self._split_into_sentences(paper_text)

        all_contexts: dict[str, list[CitationContext]] = {}

        for citation in citations:
            patterns = self._build_citation_patterns(citation)
            if not patterns:
                continue  # Can't build patterns without author+year

            contexts = []

            for i, sentence in enumerate(sentences):
                for pattern, mention_type in patterns:
                    if re.search(pattern, sentence, re.IGNORECASE):
                        context_text = self._extract_context_window(
                            sentences, i, self.context_sentences
                        )
                        position = i / len(sentences) if sentences else 0.0
                        contexts.append(CitationContext(
                            citation=citation,
                            context_text=context_text,
                            mention_type=mention_type,
                            position=position,
                        ))
                        break  # Only count once per sentence

            if contexts:
                # Use DOI as key if available, otherwise title, otherwise raw_text prefix
                key = (
                    citation.doi
                    or citation.title
                    or (citation.raw_text[:50] if citation.raw_text else None)
                )
                if key:
                    all_contexts[key] = contexts

        return all_contexts

    def format_contexts_for_synthesis(
        self,
        contexts: dict[str, list[CitationContext]],
        max_contexts_per_citation: int = 2,
    ) -> str:
        """
        Format extracted contexts for inclusion in the synthesis prompt.

        Args:
            contexts: Output from extract_contexts()
            max_contexts_per_citation: Cap on contexts per citation (keeps prompt lean)

        Returns:
            Formatted string ready for the synthesis message
        """
        if not contexts:
            return "No citation contexts extracted."

        lines = []

        for key, context_list in contexts.items():
            citation = context_list[0].citation

            # Short reference label
            if citation.authors and citation.year:
                first = citation.authors[0].split(",")[0]
                suffix = " et al." if len(citation.authors) > 1 else ""
                cite_ref = f"{first}{suffix} ({citation.year})"
            else:
                cite_ref = citation.title[:50] if citation.title else "Unknown"

            lines.append(f"\n{cite_ref}:")

            for i, ctx in enumerate(context_list[:max_contexts_per_citation]):
                lines.append(f'  [{i + 1}] "{ctx.context_text}"')

        return "\n".join(lines)

    # -------------------------------------------------------------------------
    # Private helpers
    # -------------------------------------------------------------------------

    def _split_into_sentences(self, text: str) -> list[str]:
        """
        Split paper text into sentences.

        Strips the bibliography section first so citation patterns
        don't match the reference list entries themselves.
        """
        text = self._remove_bibliography(text)

        # Split on period + whitespace + capital letter or digit.
        # This is a heuristic that works well for most academic papers.
        sentences = re.split(r'\.\s+(?=[A-Z0-9])', text)
        return [s.strip() for s in sentences if s.strip()]

    def _remove_bibliography(self, text: str) -> str:
        """
        Truncate text at the bibliography/references section.

        Only removes the section if it's in the latter half of the paper
        (avoids false positives when a paper discusses methodology references
        in its introduction).
        """
        markers = [
            r'\nReferences\n',
            r'\nREFERENCES\n',
            r'\nBibliography\n',
            r'\nBIBLIOGRAPHY\n',
            r'\nWorks Cited\n',
            r'\n\d+\.\s+References\n',
        ]

        earliest = len(text)
        for marker in markers:
            m = re.search(marker, text)
            if m and m.start() > len(text) * 0.5:
                earliest = min(earliest, m.start())

        return text[:earliest]

    def _build_citation_patterns(
        self, citation: Citation
    ) -> list[tuple[str, str]]:
        """
        Build regex patterns to find in-text mentions of this citation.

        Returns list of (pattern, mention_type) tuples.
        mention_type is "narrative" or "parenthetical".
        """
        if not citation.authors or not citation.year:
            return []

        last_name = citation.authors[0].split(",")[0].strip()
        year = str(citation.year)
        patterns = []

        if len(citation.authors) > 2:
            # Narrative: "Smith et al. (2023)"
            patterns.append((
                rf'\b{re.escape(last_name)}\s+et\s+al\.?\s*\({year}\)',
                "narrative",
            ))
            # Parenthetical: "(Smith et al., 2023)"
            patterns.append((
                rf'\({re.escape(last_name)}\s+et\s+al\.?,?\s*{year}\)',
                "parenthetical",
            ))

        elif len(citation.authors) == 2:
            second = citation.authors[1].split(",")[0].strip()
            # Narrative: "Smith and Jones (2023)"
            patterns.append((
                rf'\b{re.escape(last_name)}\s+(?:and|&)\s+{re.escape(second)}\s*\({year}\)',
                "narrative",
            ))
            # Parenthetical: "(Smith and Jones, 2023)"
            patterns.append((
                rf'\({re.escape(last_name)}\s+(?:and|&)\s+{re.escape(second)},?\s*{year}\)',
                "parenthetical",
            ))

        else:  # single author
            # Narrative: "Smith (2023)"
            patterns.append((
                rf'\b{re.escape(last_name)}\s*\({year}\)',
                "narrative",
            ))
            # Parenthetical: "(Smith, 2023)"
            patterns.append((
                rf'\({re.escape(last_name)},?\s*{year}\)',
                "parenthetical",
            ))

        return patterns

    def _extract_context_window(
        self,
        sentences: list[str],
        index: int,
        window_size: int,
    ) -> str:
        """
        Extract a window of sentences centered on the citing sentence.

        window_size=2 means current sentence + one before it.
        """
        start = max(0, index - (window_size - 1))
        end = min(len(sentences), index + 1)
        context = ". ".join(sentences[start:end])
        if not context.endswith("."):
            context += "."
        return context
