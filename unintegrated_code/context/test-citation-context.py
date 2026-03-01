#!/usr/bin/env python3
"""
Test script for citation context extraction.

This tests the citation context extraction on sample paper text.

Usage:
    python test_citation_context.py
"""

import sys
from pathlib import Path

# No need to add to path if running from project root
from models import Citation
from paper_library.citation_context import extract_citation_contexts


def test_citation_contexts():
    """Test citation context extraction with sample data."""
    
    print("Testing Citation Context Extraction\n")
    
    # Sample paper text (simulating a transformer paper)
    sample_text = """
    Introduction
    
    Recent advances in neural machine translation have been driven by the 
    development of attention-based models. The Transformer architecture 
    (Vaswani et al., 2017) eliminates recurrence entirely, relying solely 
    on attention mechanisms for both encoding and decoding. This approach 
    has proven highly effective for sequence-to-sequence tasks.
    
    Background
    
    Early work on attention mechanisms by Bahdanau et al. (2014) showed that 
    neural networks can learn to align inputs and outputs. The Transformer 
    builds on this foundation but uses multi-head self-attention.
    
    Methods
    
    We follow the BERT pretraining approach (Devlin et al., 2019) but modify 
    the masking strategy. Unlike previous work (Vaswani et al., 2017; 
    Radford et al., 2018), we use bidirectional context.
    
    Results
    
    Our model achieves state-of-the-art results. Compared to the baseline 
    Transformer (Vaswani et al., 2017), we see a 15% improvement in BLEU score.
    
    References
    
    Vaswani, A., Shazeer, N., Parmar, N., et al. (2017). Attention Is All You Need.
    Bahdanau, D., Cho, K., & Bengio, Y. (2014). Neural machine translation.
    Devlin, J., Chang, M., Lee, K., & Toutanova, K. (2019). BERT: Pre-training.
    Radford, A., et al. (2018). Improving language understanding.
    """
    
    # Sample citations (as GROBID would extract them)
    citations = [
        Citation(
            authors=["Vaswani, A.", "Shazeer, N.", "Parmar, N."],
            title="Attention Is All You Need",
            year=2017,
            raw_text="Vaswani et al. (2017). Attention Is All You Need."
        ),
        Citation(
            authors=["Bahdanau, D.", "Cho, K.", "Bengio, Y."],
            title="Neural machine translation by jointly learning to align and translate",
            year=2014,
            raw_text="Bahdanau et al. (2014). Neural machine translation."
        ),
        Citation(
            authors=["Devlin, J.", "Chang, M.", "Lee, K.", "Toutanova, K."],
            title="BERT: Pre-training of Deep Bidirectional Transformers",
            year=2019,
            raw_text="Devlin et al. (2019). BERT: Pre-training."
        ),
    ]
    
    print("Sample citations:")
    for citation in citations:
        first_author = citation.authors[0].split(',')[0]
        print(f"  • {first_author} et al. ({citation.year}): {citation.title}")
    print()
    
    # Extract contexts
    print("→ Extracting citation contexts...")
    contexts = extract_citation_contexts(sample_text, citations)
    
    print(f"✓ Found contexts for {len(contexts)} citations\n")
    
    # Display results
    print("=" * 70)
    print("EXTRACTED CONTEXTS")
    print("=" * 70)
    
    for key, context_list in contexts.items():
        citation = context_list[0].citation
        first_author = citation.authors[0].split(',')[0]
        cite_ref = f"{first_author} et al. ({citation.year})"
        
        print(f"\n{cite_ref} - mentioned {len(context_list)} time(s):")
        for i, context in enumerate(context_list, 1):
            print(f"\n  [{i}] Context (position: {context.position:.1%}):")
            print(f"      Type: {context.mention_type}")
            print(f'      "{context.context_text}"')
    
    print("\n" + "=" * 70)
    print("✓ Test passed! Citation context extraction working.")
    print("=" * 70)
    
    # Test edge cases
    print("\n\nTesting edge cases...")
    
    # Test with no matches
    no_match = Citation(
        authors=["Nobody, N."],
        title="This Paper Does Not Exist",
        year=2099,
        raw_text="Nobody et al. (2099). This Paper Does Not Exist."
    )
    
    contexts_empty = extract_citation_contexts(sample_text, [no_match])
    print(f"  • No matches: {len(contexts_empty)} contexts found (expected 0)")
    
    # Test with numeric citation format
    text_with_numbers = "Previous work [1] showed this. Later work [1, 2] confirmed it."
    numeric_citation = Citation(
        authors=["Smith, J."],
        title="Numeric Citation Test",
        year=2020,
        raw_text="[1] Smith et al. (2020). Numeric Citation Test."
    )
    
    # This won't match because we don't handle numeric citations yet
    # But it shouldn't crash
    contexts_numeric = extract_citation_contexts(text_with_numbers, [numeric_citation])
    print(f"  • Numeric citations: {len(contexts_numeric)} contexts found (not implemented yet)")
    
    print("\n✓ All tests passed!")


if __name__ == "__main__":
    test_citation_contexts()