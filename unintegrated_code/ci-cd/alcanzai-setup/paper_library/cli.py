"""
Command-line interface for alcanzai.

Usage:
    alcanzai ingest 2312.12345              # Ingest a single paper
    alcanzai batch papers.txt               # Batch ingest from file
    alcanzai stats                          # Show processing statistics
    alcanzai validate                       # Check configuration
"""

import click
from pathlib import Path

from paper_library.config import config
from paper_library.state import StateManager
from paper_library.orchestrator import PaperProcessor


@click.group()
def cli():
    """alcanzai - Your personal research librarian"""
    pass


@cli.command()
@click.argument('identifier', required=True)
@click.option('--force', is_flag=True, help='Reprocess even if already imported')
def ingest(identifier: str, force: bool = False):
    """Ingest a single paper into your vault.
    
    IDENTIFIER can be:
    - arXiv ID: 2312.12345
    - URL: https://arxiv.org/abs/2312.12345
    - File path: /path/to/paper.pdf
    """
    state = StateManager.load()
    processor = PaperProcessor(config, state)
    
    try:
        processor.process(identifier, force=force)
        click.secho(f"\n✓ Successfully imported: {identifier}", fg='green')
    except Exception as e:
        click.secho(f"\n✗ Failed to import {identifier}", fg='red')
        click.secho(f"  Error: {e}", fg='red')
        raise SystemExit(1)


@cli.command()
@click.argument('file', type=click.File('r'), required=True)
@click.option('--force', is_flag=True, help='Reprocess papers even if already imported')
def batch(file, force: bool = False):
    """Batch ingest papers from a text file."""
    identifiers = []
    for line in file:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line[0] in ('-', '*', '+'):
            line = line[1:].strip()
        if '#' in line:
            line = line.split('#')[0].strip()
        if line:
            identifiers.append(line)
    
    if not identifiers:
        click.secho("No identifiers found in file", fg='yellow')
        return
    
    click.secho(f"\nBatch importing {len(identifiers)} papers...\n", fg='blue')
    
    state = StateManager.load()
    processor = PaperProcessor(config, state)
    results = processor.process_batch(identifiers, force=force)
    
    click.secho(f"\nBatch complete:", fg='blue')
    click.secho(f"  ✓ Imported: {results['success']}", fg='green')
    click.secho(f"  ⊘ Skipped:  {results['skipped']}", fg='yellow')
    click.secho(f"  ✗ Failed:   {results['failed']}", fg='red')
    click.secho("")


@cli.command()
def stats():
    """Show processing statistics."""
    state = StateManager.load()
    stats_dict = state.get_stats()
    
    click.secho("\nPaper Library Statistics", fg='blue', bold=True)
    click.secho("=" * 40)
    click.echo(f"  arXiv papers:      {stats_dict['arxiv']:3d}")
    click.echo(f"  DOI papers:        {stats_dict['doi']:3d}")
    click.echo(f"  Web articles:      {stats_dict['web']:3d}")
    click.secho("-" * 40)
    click.echo(f"  Total imported:    {stats_dict['total']:3d}")
    
    if stats_dict['failed'] > 0:
        click.echo(f"  Failed imports:    {stats_dict['failed']:3d}")
    
    click.echo()
    click.secho(f"Vault location: {config.vault_path}")
    click.echo()


@cli.command()
def validate():
    """Validate your configuration."""
    click.secho("\nValidating configuration...\n", fg='blue')
    
    checks_passed = 0
    checks_failed = 0
    
    if config.anthropic_api_key:
        click.secho("✓ ANTHROPIC_API_KEY is set", fg='green')
        checks_passed += 1
    else:
        click.secho("✗ ANTHROPIC_API_KEY not set", fg='red')
        checks_failed += 1
    
    if config.vault_path.exists():
        click.secho(f"✓ Vault directory exists: {config.vault_path}", fg='green')
        checks_passed += 1
    else:
        click.secho(f"✗ Vault directory not found: {config.vault_path}", fg='red')
        config.vault_path.mkdir(parents=True, exist_ok=True)
        click.secho(f"✓ Created vault directory", fg='green')
        checks_passed += 1
    
    click.echo()
    if checks_failed == 0:
        click.secho("✓ All required checks passed!", fg='green', bold=True)
    else:
        click.secho(f"✗ {checks_failed} check(s) failed", fg='red', bold=True)
        raise SystemExit(1)
    
    click.echo()


if __name__ == '__main__':
    cli()
