#!/usr/bin/env python3
"""
Batch process papers from a text file. 

Wrapper around orchestrator.py.

Usage:
    python batch_process.py papers.txt

File format (one per line):
    1706.03762
    2312.12345
    https://arxiv.org/abs/2203.15556
    /path/to/local.pdf
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from paper_library.config import config
from paper_library.state import StateManager
from paper_library.orchestrator import PaperProcessor


def batch_process(input_file: str):
    """Process all papers from a text file."""
    
    # Read identifiers from file
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"Error: File not found: {input_file}")
        return
    
    with open(input_path) as f:
        identifiers = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    print(f"\n{'='*70}")
    print(f"BATCH PROCESSING: {len(identifiers)} papers from {input_file}")
    print(f"{'='*70}\n")
    
    # Initialize processor
    state = StateManager.load()
    processor = PaperProcessor(config, state)
    
    # Process batch
    results = processor.process_batch(identifiers)
    
    # Final summary
    print(f"\n{'='*70}")
    print(f"BATCH COMPLETE")
    print(f"{'='*70}")
    print(f"  ✓ Processed: {results['success']}")
    print(f"  ⊘ Skipped:   {results['skipped']}")
    print(f"  ✗ Failed:    {results['failed']}")
    
    if results['errors']:
        print(f"\nErrors:")
        for identifier, error in results['errors']:
            print(f"  • {identifier}: {error}")
    
    print(f"{'='*70}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    batch_process(sys.argv[1])