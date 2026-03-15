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
from typing import Optional

from paper_library.models import Citation
from paper_library.telemetry import tracer, get_logger

logger = get_logger(__name__)


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

    Handles three citation formats:
    - Numeric:       "[3]" or "[1, 3, 5]" — common in CS/ML papers (arXiv)
    - Narrative:     "Smith et al. (2023) show that..."
    - Parenthetical: "...attention mechanisms (Vaswani et al., 2017)."

    Numeric matching uses each citation's 1-based position in the bibliography
    list, which corresponds to the `[N]` marker used in the paper body.

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
        with tracer.start_as_current_span(
            'extract_citation_contexts',
            attributes={
                'citations.input_count': len(citations),
                'text.char_length': len(paper_text),
            }
        ) as span:
            # Strip bibliography so we don't match reference-list entries
            body_text = self._remove_bibliography(paper_text)
            text_len = len(body_text)

            all_contexts: dict[str, list[CitationContext]] = {}

            for idx, citation in enumerate(citations):
                patterns = self._build_citation_patterns(citation, index=idx)
                if not patterns:
                    continue  # Can't build patterns without author+year

                contexts = []
                seen_positions: set[int] = set()

                for pattern, mention_type in patterns:
                    for match in re.finditer(pattern, body_text, re.IGNORECASE):
                        # Deduplicate: skip if we already grabbed context at this spot
                        bucket = match.start() // 50
                        if bucket in seen_positions:
                            continue
                        seen_positions.add(bucket)

                        context_text = self._extract_char_context(
                            body_text, match.start(), match.end()
                        )
                        position = match.start() / text_len if text_len else 0.0
                        contexts.append(CitationContext(
                            citation=citation,
                            context_text=context_text,
                            mention_type=mention_type,
                            position=position,
                        ))

                if contexts:
                    key = (
                        citation.doi
                        or citation.title
                        or (citation.raw_text[:50] if citation.raw_text else None)
                    )
                    if key:
                        all_contexts[key] = contexts

            # After extraction:
            matched_count = len(all_contexts)
            total_contexts = sum(len(ctxs) for ctxs in all_contexts.values())
            
            span.set_attribute('citations.matched_count', matched_count)
            span.set_attribute('citations.total_context_sentences', total_contexts)
            match_rate = matched_count / len(citations) if citations else 0.0
            span.set_attribute('citations.match_rate', match_rate)

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

    def _extract_char_context(self, text: str, match_start: int, match_end: int) -> str:
        """
        Extract surrounding sentence context using character offsets.

        Looks backwards from match_start for sentence-ending punctuation,
        and forward from match_end for the end of the citing sentence.
        Returns up to context_sentences sentences (current + preceding).
        """
        # Walk backwards to find sentence boundaries
        # Sentence endings: ". " "! " "? " or start of string
        sentence_end_re = re.compile(r'[.!?]\s+')

        # Find the start of the window (go back context_sentences - 1 boundaries)
        search_region = text[:match_start]
        boundaries = [m.end() for m in sentence_end_re.finditer(search_region)]
        if len(boundaries) >= self.context_sentences:
            window_start = boundaries[-(self.context_sentences - 1)]
        else:
            window_start = 0

        # Find the end of the citing sentence (first ". " "! " "? " after match)
        tail = text[match_end:]
        end_match = sentence_end_re.search(tail)
        window_end = match_end + (end_match.end() if end_match else len(tail))

        context = text[window_start:window_end].strip()
        # Collapse internal whitespace artifacts from PDF extraction
        context = re.sub(r'\s+', ' ', context)
        if not context.endswith(('.', '!', '?')):
            context += '.'
        return context

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
        self,
        citation: Citation,
        index: Optional[int] = None,
    ) -> list[tuple[str, str]]:
        """
        Build regex patterns to find in-text mentions of this citation.

        Returns list of (pattern, mention_type) tuples.
        mention_type is "narrative", "parenthetical", or "numeric".

        Args:
            citation: The citation object.
            index:    0-based position in the bibliography list.  When provided,
                      a numeric pattern ``[N]`` (1-based) is added.  This covers
                      the bracket-style citations used in most CS/ML papers.
        """
        patterns = []

        # --- Numeric style: [N], [1, N, 3], etc. ---
        # Works regardless of whether author/year fields were parsed.
        if index is not None:
            n = index + 1  # bibliography is 1-based
            # Match [N] as a standalone number or inside a comma-separated list.
            # \b ensures we don't match [30] when looking for [3].
            patterns.append((
                rf'\[([^\]]*\b{n}\b[^\]]*)\]',
                "numeric",
            ))

        # --- Author-year styles ---
        # These only fire when GROBID successfully parsed author + year.
        if not citation.authors or not citation.year:
            return patterns  # return numeric-only if fields missing

        last_name = citation.authors[0].split(",")[0].strip()
        year = str(citation.year)

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

