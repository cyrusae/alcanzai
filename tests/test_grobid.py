#!/usr/bin/env python3
"""
Test script for GROBID processor.

This script tests the GROBID processor with a sample PDF.
You'll need:
1. GROBID running (docker-compose up -d)
2. A test PDF file
3. Your .env file configured

Usage:
    python test_grobid.py /path/to/paper.pdf
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import paper_library
sys.path.insert(0, str(Path(__file__).parent))

from paper_library.config import config
from paper_library.grobid_processor import GrobidProcessor


def test_grobid(pdf_path: str):
    """Test GROBID processing on a single PDF."""
    
    print(f"Testing GROBID processor with: {pdf_path}\n")
    
    # Initialize processor
    processor = GrobidProcessor(config.grobid_url)
    print(f"✓ GROBID URL: {config.grobid_url}")
    
    # Process PDF
    print(f"→ Sending PDF to GROBID (this may take 30-60 seconds)...")
    try:
        metadata = processor.process(Path(pdf_path))
        print("✓ Processing complete!\n")
        
        # Display results
        print("=" * 70)
        print("EXTRACTED METADATA")
        print("=" * 70)
        print(f"\nTitle: {metadata.title}")
        print(f"\nAuthors ({len(metadata.authors)}):")
        for i, author in enumerate(metadata.authors, 1):
            print(f"  {i}. {author}")
        
        print(f"\nYear: {metadata.year}")
        
        if metadata.venue:
            print(f"Venue: {metadata.venue}")
        
        if metadata.volume or metadata.issue or metadata.pages:
            pub_info = []
            if metadata.volume:
                pub_info.append(f"Vol. {metadata.volume}")
            if metadata.issue:
                pub_info.append(f"Issue {metadata.issue}")
            if metadata.pages:
                pub_info.append(f"pp. {metadata.pages}")
            print(f"Publication: {', '.join(pub_info)}")
        
        if metadata.doi:
            print(f"DOI: {metadata.doi}")
        
        if metadata.abstract:
            print(f"\nAbstract ({len(metadata.abstract)} chars):")
            # Show first 200 chars
            abstract_preview = metadata.abstract[:200]
            if len(metadata.abstract) > 200:
                abstract_preview += "..."
            print(f"  {abstract_preview}")
        
        print(f"\nCitations: {len(metadata.citations)} found")
        if metadata.citations:
            print("\nFirst 3 citations:")
            for i, citation in enumerate(metadata.citations[:3], 1):
                # Show first 100 chars of raw text
                cite_preview = citation.raw_text[:100]
                if len(citation.raw_text) > 100:
                    cite_preview += "..."
                print(f"  [{i}] {cite_preview}")
        
        print("\n" + "=" * 70)
        print("✓ Test passed! GROBID processor working correctly.")
        print("=" * 70)
        
        return metadata
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Is GROBID running? Check with: docker-compose ps")
        print("2. If not, start it: docker-compose up -d")
        print("3. Wait 30 seconds for GROBID to initialize")
        print("4. Try again")
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_grobid.py /path/to/paper.pdf")
        print("\nExample:")
        print("  python test_grobid.py ~/Downloads/paper.pdf")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    if not Path(pdf_path).exists():
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)
    
    test_grobid(pdf_path)
