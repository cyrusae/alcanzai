#!/usr/bin/env python3
#!/usr/bin/env python3
"""
Batch process papers from a text file.

Usage:
    python batch_process.py papers.txt [--force]

Options:
    --force    Reprocess papers even if already done

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


def batch_process(input_file: str, force: bool = False):
    """Process all papers from a text file."""
    
    # Read identifiers from file
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"Error: File not found: {input_file}")
        return
    
    with open(input_path) as f:
        lines = []
        for line in f:
            # Strip leading/trailing whitespace
            line = line.strip()
            
            # Skip empty lines and comment lines
            if not line or line.startswith('#'):
                continue
            
            # Remove markdown bullets (-, *, +)
            if line.startswith(('-', '*', '+')):
                line = line[1:].strip()
            
            # Handle inline comments (everything after #)
            if '#' in line:
                line = line.split('#')[0].strip()
            
            # Add if not empty after cleaning
            if line:
                lines.append(line)
        
        identifiers = lines
    
    print(f"\n{'='*70}")
    print(f"BATCH PROCESSING: {len(identifiers)} papers from {input_file}")
    if force:
        print(f"  --force enabled: Will reprocess existing papers")
    print(f"{'='*70}\n")
    
    # Initialize processor
    state = StateManager.load()
    processor = PaperProcessor(config, state)
    
    # Process batch with force flag
    results = processor.process_batch(identifiers, force=force)
    
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
    
    input_file = sys.argv[1]
    force = '--force' in sys.argv
    
    batch_process(input_file, force=force)