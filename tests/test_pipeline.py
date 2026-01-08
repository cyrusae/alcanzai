#!/usr/bin/env python3
"""
End-to-end test script.

This runs the complete pipeline on one arXiv paper to verify
everything works together.

Usage:
    python test_pipeline.py [arxiv_id]
    
Example:
    python test_pipeline.py 1706.03762
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from paper_library.config import config
from paper_library.state import StateManager
from paper_library.orchestrator import PaperProcessor


def test_pipeline(arxiv_id: str = "1706.03762"):
    """
    Run the full pipeline on one paper.
    
    Steps:
    1. Fetch from arXiv (API + PDF)
    2. Process with GROBID (metadata extraction)
    3. Generate synthesis with Claude
    4. Write Obsidian note
    5. Update state
    """
    
    print("\n" + "="*70)
    print("END-TO-END PIPELINE TEST")
    print("="*70)
    print()
    print(f"Paper: arXiv {arxiv_id}")
    print(f"Vault: {config.vault_path}")
    print()
    
    # Pre-flight checks
    print("Pre-flight checks:")
    
    # Check API key
    if not config.anthropic_api_key:
        print("  ✗ ANTHROPIC_API_KEY not set")
        print("    Create .env file with your API key")
        return False
    print("  ✓ Anthropic API key configured")
    
    # Check GROBID
    import requests
    try:
        response = requests.get(f"{config.grobid_url}/api/isalive", timeout=5)
        if response.status_code == 200:
            print("  ✓ GROBID service is running")
        else:
            print(f"  ✗ GROBID responded but with status {response.status_code}")
            print("    Try: docker-compose restart")
            return False
    except Exception as e:
        print(f"  ✗ GROBID service not reachable: {e}")
        print("    Start with: docker-compose up -d")
        return False
    
    # Check vault exists
    if not config.vault_path.exists():
        print(f"  → Creating vault at {config.vault_path}")
        config.vault_path.mkdir(parents=True, exist_ok=True)
    print(f"  ✓ Vault directory exists")
    
    print()
    
    # Initialize processor
    state = StateManager.load()
    processor = PaperProcessor(config, state)
    
    print("✓ Processor initialized\n")
    
    # Process the paper
    try:
        success = processor.process(arxiv_id, force=True)
        
        if success:
            print("\n" + "="*70)
            print("✓✓✓ PIPELINE TEST PASSED ✓✓✓")
            print("="*70)
            print()
            print("Next steps:")
            print("1. Check your vault for the generated note")
            print(f"   Location: {config.papers_dir}")
            print("2. Open it in Obsidian to see how it renders")
            print("3. Try processing more papers from your collection")
            print()
            print("To process multiple papers:")
            print("  python -c 'from paper_library.orchestrator import process_paper; process_paper(\"ARXIV_ID\")'")
            print()
            
            # Show stats
            stats = state.get_stats()
            print("Processing statistics:")
            print(f"  Papers processed: {stats['total']}")
            print(f"  Failed: {stats['failed']}")
            print()
            
            return True
        else:
            print("\n⊘ Paper was already processed (skipped)")
            return True
            
    except Exception as e:
        print("\n" + "="*70)
        print("✗✗✗ PIPELINE TEST FAILED ✗✗✗")
        print("="*70)
        print(f"\nError: {e}")
        print("\nDebugging tips:")
        print("1. Check error message above for specifics")
        print("2. Verify GROBID is running: docker-compose ps")
        print("3. Check API key is valid")
        print("4. Try with a different paper")
        print("5. Check network connection")
        print()
        return False


if __name__ == "__main__":
    # Use command-line arg or default to "Attention Is All You Need"
    arxiv_id = sys.argv[1] if len(sys.argv) > 1 else "1706.03762"
    
    success = test_pipeline(arxiv_id)
    sys.exit(0 if success else 1)
