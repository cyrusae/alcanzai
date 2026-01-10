"""
Markdown writer for Obsidian notes.

This module converts PaperMetadata + Synthesis into formatted markdown files
for Obsidian, with YAML frontmatter and structured sections.

Python concepts:
- String formatting and templates
- YAML generation
- File path handling
- List comprehensions
"""

from datetime import datetime
from pathlib import Path
from typing import Optional

from paper_library.models import PaperMetadata, ArticleMetadata, Synthesis, Citation


class MarkdownWriter:
    """
    Write paper/article data as Obsidian-formatted markdown.
    
    Produces notes with:
    - YAML frontmatter (metadata)
    - Structured sections (title, quote, summary, etc.)
    - Wikilinks for citations
    
    Usage:
        writer = MarkdownWriter()
        markdown = writer.paper_to_markdown(metadata, synthesis)
        Path("note.md").write_text(markdown)
    """
    
    @staticmethod
    def paper_to_markdown(
        metadata: PaperMetadata,
        synthesis: Synthesis
    ) -> str:
        """
        Convert paper metadata + synthesis to Obsidian markdown.
        
        Generates the standard note template:
        - YAML frontmatter
        - Title + author byline
        - Memorable quote
        - Quick Refresh (summary)
        - Why You Cared
        - Key Concepts (tags)
        - Cites (citation links)
        - Cited By (placeholder)
        - Details (metadata)
        - Abstract
        - Full Citation List
        
        Args:
            metadata: Paper metadata from GROBID
            synthesis: AI-generated synthesis from Claude
            
        Returns:
            Formatted markdown string
        """
        # Build YAML frontmatter
        frontmatter = MarkdownWriter._build_paper_frontmatter(metadata, synthesis)
        
        # Build author byline
        authors_str = MarkdownWriter._format_authors_short(metadata.authors)
        
        # Build sections
        sections = []
        
        # Title + byline
        sections.append(f"# {metadata.title}\n")
        sections.append(f"**{authors_str}** â€¢ {metadata.year}\n")
        
        # Memorable quote
        sections.append("> [!quote] Memorable Quote")
        sections.append(f'> "{synthesis.memorable_quote}"\n')
        
        # Quick Refresh (summary)
        sections.append("## Quick Refresh\n")
        sections.append(f"{synthesis.summary}\n")
        
        # Why You Cared
        sections.append("## Why You Cared\n")
        sections.append(f"{synthesis.why_you_cared}\n")
        
        # Key Concepts (as inline tags)
        sections.append("## Key Concepts\n")
        concept_tags = " ".join(f"`#{concept}`" for concept in synthesis.key_concepts)
        sections.append(f"{concept_tags}\n")
        
        # Cites section (papers this paper references)
        if metadata.citations:
            sections.append("## Cites (Key Papers)\n")
            # Show top 10 citations as wikilinks
            # In Phase 2, we'll have logic to pick "key" papers
            # For now, just show first 10
            for citation in metadata.citations[:10]:
                citation_link = MarkdownWriter._format_citation_wikilink(citation)
                sections.append(f"- {citation_link}")
            
            if len(metadata.citations) > 10:
                sections.append(f"\n*({len(metadata.citations) - 10} more citations below)*")
            sections.append("")
        
        # Cited By section (placeholder)
        sections.append("## Cited By\n")
        sections.append("*This section will be populated as you process papers that cite this one.*\n")
        
        # Details section (all metadata)
        sections.append("## Details\n")
        details = MarkdownWriter._build_details_section(metadata)
        sections.append(details)
        
        # Abstract
        if metadata.abstract:
            sections.append("## Abstract\n")
            sections.append(f"{metadata.abstract}\n")
        
        # Full citation list (if we have more than what we showed)
        if metadata.citations:
            sections.append("## Full Citation List\n")
            for i, citation in enumerate(metadata.citations, 1):
                # Format citation properly from parsed fields
                formatted = MarkdownWriter._format_citation_full(citation, i)
                sections.append(formatted)
            sections.append("")
        
        # Combine everything
        markdown = frontmatter + "\n" + "\n".join(sections)
        
        return markdown
    
    @staticmethod
    def article_to_markdown(
        metadata: ArticleMetadata,
        synthesis: Synthesis,
        content: str
    ) -> str:
        """
        Convert article metadata + synthesis to Obsidian markdown.
        
        Similar to paper format but:
        - No citations section (web content doesn't have bibliography)
        - Includes original content at bottom
        - Different frontmatter fields
        
        Args:
            metadata: Article metadata from web fetcher
            synthesis: AI-generated synthesis
            content: Original article content as markdown
            
        Returns:
            Formatted markdown string
        """
        # Build YAML frontmatter
        frontmatter = MarkdownWriter._build_article_frontmatter(metadata, synthesis)
        
        # Build author byline
        authors_str = MarkdownWriter._format_authors_short(metadata.authors)
        
        # Build sections
        sections = []
        
        # Title + byline
        sections.append(f"# {metadata.title}\n")
        sections.append(f"**{authors_str}**")
        if metadata.published_date:
            sections.append(f" â€¢ {metadata.published_date.strftime('%Y-%m-%d')}")
        sections.append("\n")
        
        # Source link
        sections.append(f"**Source:** [{metadata.publisher or 'Web'}]({metadata.url})\n")
        
        # Memorable quote
        sections.append("> [!quote] Memorable Quote")
        sections.append(f'> "{synthesis.memorable_quote}"\n')
        
        # Quick Refresh
        sections.append("## Quick Refresh\n")
        sections.append(f"{synthesis.summary}\n")
        
        # Why You Cared
        sections.append("## Why You Cared\n")
        sections.append(f"{synthesis.why_you_cared}\n")
        
        # Key Concepts
        sections.append("## Key Concepts\n")
        concept_tags = " ".join(f"`#{concept}`" for concept in synthesis.key_concepts)
        sections.append(f"{concept_tags}\n")
        
        # Related Papers (placeholder)
        sections.append("## Related Papers\n")
        sections.append("*Papers referenced in this article will appear here.*\n")
        
        # Original content
        sections.append("## Original Content\n")
        sections.append(content)
        sections.append("")
        
        # Combine
        markdown = frontmatter + "\n" + "\n".join(sections)
        
        return markdown
    
    @staticmethod
    def _build_paper_frontmatter(metadata: PaperMetadata, synthesis: Synthesis) -> str:
        """
        Build YAML frontmatter for paper notes.
        
        Format:
        ---
        title: "Paper Title"
        authors: [Author1, Author2]
        year: 2023
        ...
        ---
        
        Args:
            metadata: Paper metadata
            synthesis: Synthesis data
            
        Returns:
            YAML frontmatter as string
        """
        lines = ["---"]
        
        # Required fields
        # Escape quotes in title for YAML
        title_escaped = metadata.title.replace('"', '\\"')
        lines.append(f'title: "{title_escaped}"')
        
        # Authors as YAML list
        # Format: [Author1, Author2, Author3]
        authors_yaml = ", ".join(f'"{author}"' for author in metadata.authors)
        lines.append(f"authors: [{authors_yaml}]")
        
        lines.append(f"year: {metadata.year}")
        
        # Optional fields
        if metadata.venue:
            lines.append(f'venue: "{metadata.venue}"')
        if metadata.volume:
            lines.append(f'volume: "{metadata.volume}"')
        if metadata.issue:
            lines.append(f'issue: "{metadata.issue}"')
        if metadata.pages:
            lines.append(f'pages: "{metadata.pages}"')
        if metadata.doi:
            lines.append(f'doi: "{metadata.doi}"')
        if metadata.arxiv_id:
            lines.append(f'arxiv: "{metadata.arxiv_id}"')
        
        # Type and status
        lines.append('type: "paper"')
        lines.append('status: "unread"')  # User can change this later
        
        # Processing metadata
        lines.append(f'added: "{datetime.now().strftime("%Y-%m-%d")}"')
        
        # Tags from synthesis
        if synthesis.key_concepts:
            tags_yaml = "\n".join(f"  - {concept}" for concept in synthesis.key_concepts)
            lines.append("tags:")
            lines.append(tags_yaml)
        
        lines.append("---")
        
        return "\n".join(lines)
    
    @staticmethod
    def _build_article_frontmatter(metadata: ArticleMetadata, synthesis: Synthesis) -> str:
        """
        Build YAML frontmatter for article notes.
        
        Args:
            metadata: Article metadata
            synthesis: Synthesis data
            
        Returns:
            YAML frontmatter as string
        """
        lines = ["---"]
        
        lines.append(f'title: "{metadata.title}"')
        
        authors_yaml = ", ".join(f'"{author}"' for author in metadata.authors)
        lines.append(f"authors: [{authors_yaml}]")
        
        if metadata.publisher:
            lines.append(f'publisher: "{metadata.publisher}"')
        
        lines.append(f'url: "{metadata.url}"')
        
        lines.append('type: "article"')
        lines.append('status: "unread"')
        
        if metadata.published_date:
            lines.append(f'published: "{metadata.published_date.strftime("%Y-%m-%d")}"')
        
        lines.append(f'added: "{datetime.now().strftime("%Y-%m-%d")}"')
        
        # Tags
        if synthesis.key_concepts:
            tags_yaml = "\n".join(f"  - {concept}" for concept in synthesis.key_concepts)
            lines.append("tags:")
            lines.append(tags_yaml)
        
        lines.append("---")
        
        return "\n".join(lines)
    
    @staticmethod
    def _format_authors_short(authors: list[str]) -> str:
        """
        Format author list for byline.
        
        Rules:
        - 1 author: "Smith"
        - 2 authors: "Smith & Jones"
        - 3 authors: "Smith, Jones & Chen"
        - 4+ authors: "Smith et al."
        
        Args:
            authors: List of author names
            
        Returns:
            Formatted string
        """
        if not authors:
            return "Unknown"
        
        if len(authors) == 1:
            return authors[0]
        elif len(authors) == 2:
            return f"{authors[0]} & {authors[1]}"
        elif len(authors) == 3:
            return f"{authors[0]}, {authors[1]} & {authors[2]}"
        else:
            return f"{authors[0]} et al."
    
    @staticmethod
    def _format_citation_wikilink(citation: Citation) -> str:
        """
        Format a citation as an Obsidian wikilink.
        
        Format: [[Author, Author & Author (Year) - Title]]
        
        This creates a "forward reference" - the link will work once
        we process that paper. Until then, Obsidian shows it as a
        "future note".
        
        Args:
            citation: Citation object
            
        Returns:
            Wikilink string
        """
        # Try to construct from parsed fields
        if citation.authors and citation.year and citation.title:
            # Format authors
            if len(citation.authors) == 1:
                authors_str = citation.authors[0]
            elif len(citation.authors) == 2:
                authors_str = f"{citation.authors[0]} & {citation.authors[1]}"
            elif len(citation.authors) >= 3:
                # Use all authors for disambiguation
                # "Smith, Jones & Chen" not "Smith et al."
                authors_str = ", ".join(citation.authors[:-1]) + f" & {citation.authors[-1]}"
            else:
                authors_str = "Unknown"
            
            # Truncate title if too long
            title = citation.title
            if len(title) > 60:
                title = title[:60] + "..."
            
            return f"[[{authors_str} ({citation.year}) - {title}]]"
        
        # Fallback: use raw text (but truncate)
        raw_truncated = citation.raw_text[:80]
        if len(citation.raw_text) > 80:
            raw_truncated += "..."
        
        return f"[[{raw_truncated}]]"
    
    @staticmethod
    def _build_details_section(metadata: PaperMetadata) -> str:
        """
        Build the Details section with all metadata.
        
        Args:
            metadata: Paper metadata
            
        Returns:
            Formatted details string
        """
        lines = []
        
        # Publication info
        if metadata.venue:
            pub_parts = [metadata.venue]
            if metadata.volume:
                pub_parts.append(f"Vol. {metadata.volume}")
            if metadata.issue:
                pub_parts.append(f"Issue {metadata.issue}")
            if metadata.pages:
                pub_parts.append(f"pp. {metadata.pages}")
            lines.append(f"**Published:** {', '.join(pub_parts)}")
        
        # DOI
        if metadata.doi:
            lines.append(f"**DOI:** [{metadata.doi}](https://doi.org/{metadata.doi})")
        
        # arXiv
        if metadata.arxiv_id:
            lines.append(f"**arXiv:** [{metadata.arxiv_id}](https://arxiv.org/abs/{metadata.arxiv_id})")
        
        # PDF link (if we have it)
        if metadata.pdf_path:
            pdf_name = Path(metadata.pdf_path).name
            lines.append(f"**PDF:** [[{pdf_name}]]")
        
        return "\n".join(lines) + "\n" if lines else ""
    
    @staticmethod
    def _format_citation_full(citation: Citation, number: int) -> str:
        """
        Format a citation for the full citation list.
        
        Tries to build from parsed fields first, falls back to raw text.
        
        Format: "1. Authors (Year). Title. Venue."
        
        Args:
            citation: Citation object
            number: Citation number
            
        Returns:
            Formatted citation string
        """
        # Try to build from parsed fields
        if citation.authors and citation.year and citation.title:
            # Format authors (handle multiple)
            if len(citation.authors) == 1:
                authors_str = citation.authors[0]
            elif len(citation.authors) == 2:
                authors_str = f"{citation.authors[0]} & {citation.authors[1]}"
            elif len(citation.authors) > 2:
                # Show first 3 authors + et al if more
                if len(citation.authors) <= 3:
                    authors_str = ", ".join(citation.authors[:-1]) + f" & {citation.authors[-1]}"
                else:
                    authors_str = ", ".join(citation.authors[:3]) + " et al."
            else:
                authors_str = "Unknown"
            
            # Build citation parts
            parts = [f"{number}. {authors_str} ({citation.year})."]
            parts.append(f"{citation.title}.")
            
            # Add venue information if available
            if citation.venue:
                venue_parts = [citation.venue]
                
                # Add volume and issue
                if citation.volume:
                    vol_str = f"Vol. {citation.volume}"
                    if citation.issue:
                        vol_str += f"({citation.issue})"
                    venue_parts.append(vol_str)
                
                # Add pages
                if citation.pages:
                    venue_parts.append(f"pp. {citation.pages}")
                
                # Join venue parts with commas
                parts.append(", ".join(venue_parts) + ".")
            
            # Add DOI if available
            if citation.doi:
                parts.append(f"DOI: {citation.doi}")
            
            return " ".join(parts)
        
        # Fallback to cleaned raw text
        # At least remove the excessive concatenation issues
        if not citation.raw_text:
            # No raw text either - this is a very incomplete citation
            # Use whatever fields we have
            parts = [f"{number}."]
            if citation.title:
                parts.append(citation.title)
            if citation.authors:
                parts.append(f"({', '.join(citation.authors[:3])})")
            if citation.year:
                parts.append(f"({citation.year})")
            return " ".join(parts) if len(parts) > 1 else f"{number}. [Incomplete citation]"
        
        raw = citation.raw_text
        import re
        
        # Add space before uppercase after lowercase (JimmyLei Ba â†’ Jimmy Lei Ba)
        raw = re.sub(r'([a-z])([A-Z])', r'\1 \2', raw)
        
        # Fix specific common patterns
        raw = re.sub(r'ar Xiv', 'arXiv', raw)  # Fix arXiv spacing
        raw = re.sub(r'ar\s*Xiv', 'arXiv', raw, flags=re.IGNORECASE)
        
        # Clean up multiple spaces
        raw = re.sub(r'\s+', ' ', raw)
        
        return f"{number}. {raw}"

    @staticmethod
    def generate_filename(metadata: PaperMetadata | ArticleMetadata) -> str:
        """
        Generate a filename for the note.
        
        Format: "FirstAuthor et al (Year) - Title"
        Max length: 80 characters (including .md extension)
        
        Sanitization:
        - Removes quotes (problematic in YAML)
        - Replaces periods with spaces (except in et al.)
        - Removes special characters
        - Smart truncation at sentence/clause boundaries
        
        Args:
            metadata: Paper or article metadata
            
        Returns:
            Filename without extension (no .md)
        """
        import re
        
        # Get first author's last name
        if metadata.authors:
            # Authors are formatted as "Lastname, Firstname"
            # Split on comma and take first part
            first_author = metadata.authors[0].split(",")[0].strip()
        else:
            first_author = "Unknown"
        
        # Format: "Author et al (Year)"
        if len(metadata.authors) > 1:
            author_part = f"{first_author} et al"
        else:
            author_part = first_author
        
        year = getattr(metadata, 'year', datetime.now().year)
        
        # Clean title
        title = metadata.title
        
        # Remove quotes (break YAML and look messy)
        title = title.replace('"', '').replace("'", '')
        
        # Replace periods with dashes (all of them - safer for cross-platform filenames)
        # "Part 3.1" â†’ "Part 3-1"
        # "U.S.A." â†’ "U-S-A-"  
        title = title.replace('.', '-')
        
        # Replace colons with dashes (more filename-friendly)
        title = title.replace(':', ' -')
        
        # Clean up multiple dashes
        title = re.sub(r'-+', '-', title)
        
        # Remove other problematic characters
        for char in ['/', '\\', '*', '?', '<', '>', '|', '\n', '\r', '\t']:
            title = title.replace(char, '')
        
        # Collapse multiple spaces
        title = re.sub(r'\s+', ' ', title).strip()
        
        # Build filename
        prefix = f"{author_part} ({year}) - "
        
        # Smart truncation
        max_length = 77  # 80 - 3 for .md
        if len(prefix + title) > max_length:
            # Available space for title
            available = max_length - len(prefix)
            
            # Try to truncate at a good boundary (space, dash, colon)
            truncated = title[:available]
            
            # Look for last space/dash in the truncated part
            last_space = max(truncated.rfind(' '), truncated.rfind('-'))
            
            if last_space > available * 0.7:  # If we found a boundary past 70% mark
                title = truncated[:last_space].strip()
            else:
                # Just hard truncate
                title = truncated.strip()
            
            # No ellipsis - just let the truncation be clean
            # Windows doesn't like extra periods before .md
        
        filename = prefix + title
        
        # Final sanity check - remove any remaining problematic chars
        filename = re.sub(r'[^\w\s\-().]', '', filename)
        
        return filename