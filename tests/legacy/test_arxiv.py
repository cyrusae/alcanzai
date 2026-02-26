#!/usr/bin/env python3
"""
Test script for arXiv fetcher.

This tests fetching papers from arXiv.

Usage:
    python test_arxiv.py [arxiv_id]
    
Example:
    python test_arxiv.py 1706.03762  # Attention Is All You Need
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from paper_library.config import config
from paper_library.arxiv_fetcher import ArxivFetcher


def test_arxiv(arxiv_id: str = "1706.03762"):
    """Test arXiv fetching with a paper ID."""
    
    print(f"Testing arXiv Fetcher\n")
    print(f"Paper ID: {arxiv_id}")
    print(f"Vault: {config.vault_path}\n")
    
    # Initialize fetcher
    fetcher = ArxivFetcher(config.vault_path)
    print("✓ Fetcher initialized")
    
    # Test ID parsing
    print("\n→ Testing ID parsing...")
    test_cases = [
        "1706.03762",
        "1706.03762v2",
        "https://arxiv.org/abs/1706.03762",
        "https://arxiv.org/pdf/1706.03762.pdf",
        "arxiv:1706.03762",
        "arXiv:1706.03762v1",
    ]
    
    for test_id in test_cases:
        parsed = fetcher.parse_arxiv_id(test_id)
        print(f"  '{test_id}' → '{parsed}'")
    
    # Fetch paper
    print(f"\n→ Fetching paper {arxiv_id}...")
    print("  (This downloads metadata + PDF, may take 10-30 seconds)")
    
    try:
        pdf_path, metadata = fetcher.fetch(arxiv_id)
        
        print("\n✓ Fetch complete!")
        
        # Display results
        print("\n" + "=" * 70)
        print("FETCHED METADATA")
        print("=" * 70)
        print(f"\nTitle: {metadata.title}")
        print(f"\nAuthors ({len(metadata.authors)}):")
        for i, author in enumerate(metadata.authors[:5], 1):
            print(f"  {i}. {author}")
        if len(metadata.authors) > 5:
            print(f"  ... and {len(metadata.authors) - 5} more")
        
        print(f"\nYear: {metadata.year}")
        print(f"arXiv ID: {metadata.arxiv_id}")
        
        if metadata.abstract:
            print(f"\nAbstract ({len(metadata.abstract)} chars):")
            abstract_preview = metadata.abstract[:250]
            if len(metadata.abstract) > 250:
                abstract_preview += "..."
            print(f"  {abstract_preview}")
        
        print(f"\nPDF: {pdf_path}")
        print(f"  Size: {pdf_path.stat().st_size / 1024:.1f} KB")
        print(f"  Exists: {pdf_path.exists()}")
        
        print("\n" + "=" * 70)
        print("✓ Test passed! arXiv fetcher working correctly.")
        print("=" * 70)
        
        return pdf_path, metadata
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check internet connection")
        print("2. Verify arXiv ID is valid")
        print("3. Try a different paper")
        return None


if __name__ == "__main__":
    # Use command-line arg or default
    arxiv_id = sys.argv[1] if len(sys.argv) > 1 else "1706.03762"
    
    test_arxiv(arxiv_id)
