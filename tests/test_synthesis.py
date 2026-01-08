#!/usr/bin/env python3
"""
Test script for synthesis generator.

This tests Claude API integration by generating a synthesis
for sample paper text.

Usage:
    python test_synthesis.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from paper_library.config import config
from paper_library.synthesis_generator import SynthesisGenerator
from paper_library.models import PaperMetadata


def test_synthesis():
    """Test synthesis generation with sample data."""
    
    print("Testing Synthesis Generator\n")
    
    # Create sample metadata
    # This is what we'd get from GROBID or arXiv API
    metadata = PaperMetadata(
        title="Attention Is All You Need",
        authors=["Vaswani, Ashish", "Shazeer, Noam", "Parmar, Niki"],
        year=2017,
        abstract="The dominant sequence transduction models are based on complex recurrent or convolutional neural networks...",
        venue="NeurIPS"
    )
    
    # Sample paper text (just the abstract for this test)
    # In real use, this would be the full paper text
    sample_text = """
    The dominant sequence transduction models are based on complex recurrent or 
    convolutional neural networks that include an encoder and a decoder. The best 
    performing models also connect the encoder and decoder through an attention 
    mechanism. We propose a new simple network architecture, the Transformer, based 
    solely on attention mechanisms, dispensing with recurrence and convolutions entirely. 
    
    Experiments on two machine translation tasks show these models to be superior in 
    quality while being more parallelizable and requiring significantly less time to train. 
    Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, 
    improving over the existing best results, including ensembles, by over 2 BLEU. On 
    the WMT 2014 English-to-French translation task, our model establishes a new 
    single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on 
    eight GPUs, a small fraction of the training costs of the best models from the 
    literature.
    
    The Transformer is the first transduction model relying entirely on self-attention 
    to compute representations of its input and output without using sequence-aligned 
    RNNs or convolution. In the following sections, we will describe the Transformer, 
    motivate self-attention and discuss its advantages over models such as recurrent 
    and convolutional layers.
    """
    
    print(f"Paper: {metadata.title}")
    print(f"Authors: {', '.join(metadata.authors)}")
    print(f"Year: {metadata.year}\n")
    
    # Check API key
    if not config.anthropic_api_key:
        print("✗ Error: ANTHROPIC_API_KEY not set")
        print("Please create a .env file with your API key")
        print("Example: ANTHROPIC_API_KEY=sk-ant-...")
        return
    
    print("✓ API key found")
    
    # Initialize generator
    generator = SynthesisGenerator(config.anthropic_api_key)
    print("✓ Generator initialized")
    
    # Generate synthesis
    print("\n→ Calling Claude API (this takes ~5-10 seconds)...")
    try:
        synthesis = generator.generate_quick_synthesis(sample_text, metadata)
        
        print("✓ Synthesis generated!\n")
        
        # Display results
        print("=" * 70)
        print("GENERATED SYNTHESIS")
        print("=" * 70)
        
        print("\n📝 SUMMARY:")
        print(f"   {synthesis.summary}")
        
        print("\n💡 WHY YOU CARED:")
        print(f"   {synthesis.why_you_cared}")
        
        print("\n🏷️  KEY CONCEPTS:")
        for concept in synthesis.key_concepts:
            print(f"   • {concept}")
        
        print("\n💬 MEMORABLE QUOTE:")
        print(f'   "{synthesis.memorable_quote}"')
        
        print("\n📊 METADATA:")
        print(f"   Model: {synthesis.model_used}")
        print(f"   Generated: {synthesis.generated_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Cost: ${synthesis.cost_usd:.4f}")
        
        print("\n" + "=" * 70)
        print("✓ Test passed! Synthesis generator working correctly.")
        print("=" * 70)
        
        # Cost projection
        print("\n💰 COST PROJECTION:")
        print(f"   Per paper: ${synthesis.cost_usd:.4f}")
        print(f"   24 papers: ${synthesis.cost_usd * 24:.2f}")
        print(f"   100 papers: ${synthesis.cost_usd * 100:.2f}")
        
        return synthesis
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check your API key is valid")
        print("2. Check you have API credits")
        print("3. Check network connection")
        return None


if __name__ == "__main__":
    test_synthesis()
