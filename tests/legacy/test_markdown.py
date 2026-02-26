#!/usr/bin/env python3
"""
Test script for markdown writer.

This generates a sample Obsidian note to verify formatting.

Usage:
    python test_markdown.py
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from paper_library.markdown_writer import MarkdownWriter
from paper_library.models import PaperMetadata, Synthesis, Citation


def test_markdown():
    """Test markdown generation with sample data."""
    
    print("Testing Markdown Writer\n")
    
    # Create sample citation
    sample_citation = Citation(
        raw_text="Bahdanau, D., Cho, K., & Bengio, Y. (2014). Neural machine translation by jointly learning to align and translate. arXiv preprint arXiv:1409.0473.",
        authors=["Bahdanau, D.", "Cho, K.", "Bengio, Y."],
        title="Neural machine translation by jointly learning to align and translate",
        year=2014,
        doi=None
    )
    
    # Create sample metadata (like GROBID would produce)
    metadata = PaperMetadata(
        title="Attention Is All You Need",
        authors=["Vaswani, Ashish", "Shazeer, Noam", "Parmar, Niki", "Uszkoreit, Jakob"],
        year=2017,
        abstract="The dominant sequence transduction models are based on complex recurrent or convolutional neural networks...",
        venue="Advances in Neural Information Processing Systems",
        volume="30",
        pages="5998-6008",
        arxiv_id="1706.03762",
        citations=[sample_citation] * 3,  # Repeat for demo
        pdf_path="/vault/PDFs/arxiv_1706.03762.pdf"
    )
    
    # Create sample synthesis (like Claude would produce)
    synthesis = Synthesis(
        summary="This paper introduces the Transformer architecture, which relies entirely on attention mechanisms without recurrence or convolution. The model achieves state-of-the-art results on machine translation tasks while being more parallelizable and requiring less training time.",
        why_you_cared="This is the foundational paper for modern language models like GPT and BERT. Understanding the Transformer architecture is essential for working with contemporary NLP systems.",
        key_concepts=["transformers", "attention-mechanism", "self-attention", "neural-machine-translation", "encoder-decoder"],
        memorable_quote="The Transformer is the first transduction model relying entirely on self-attention to compute representations of its input and output.",
        model_used="claude-haiku-20250514",
        cost_usd=0.0123
    )
    
    print("Sample data:")
    print(f"  Title: {metadata.title}")
    print(f"  Authors: {len(metadata.authors)}")
    print(f"  Citations: {len(metadata.citations)}")
    print()
    
    # Generate markdown
    print("→ Generating markdown...")
    markdown = MarkdownWriter.paper_to_markdown(metadata, synthesis)
    
    print("✓ Markdown generated!")
    print(f"  Length: {len(markdown)} characters")
    print(f"  Lines: {markdown.count(chr(10)) + 1}")
    print()
    
    # Generate filename
    filename = MarkdownWriter.generate_filename(metadata)
    print(f"  Filename: {filename}.md")
    print()
    
    # Display the markdown
    print("=" * 70)
    print("GENERATED MARKDOWN")
    print("=" * 70)
    print(markdown)
    print("=" * 70)
    
    # Write to file for inspection
    output_path = Path("sample_note.md")
    output_path.write_text(markdown)
    print(f"\n✓ Written to: {output_path}")
    print("  You can open this in Obsidian to see how it renders!")
    
    return markdown


if __name__ == "__main__":
    test_markdown()
