#!/usr/bin/env python3
"""
pbjson - Project state management for Claude-assisted development

A lightweight decision and work logger for projects developed with Claude AI assistance.
Designed to work within constrained environments (like Claude's project file system)
with a single-file deployment model.

PHILOSOPHY:
    - Track decisions, not just work
    - Human-readable and git-friendly (JSON + append-only log)
    - Works in Claude projects where multi-file packages are impractical
    - Supports multi-subsystem projects with prefix-based file naming

USAGE - Basic commands:
    pbjson decided "Decision made with reasoning"          # Record architectural decision
    pbjson built "Feature built (search: term)"            # Record completed work (searchable)
    pbjson question "Open question requiring input"        # Track open decision
    pbjson file "path/to/file.py - purpose"                # Mark important entry points (max 3-5)
    pbjson context "Background info or constraint"         # Store project context
    pbjson resolve "question keyword" "The decision made"   # Move question â†’ resolution

USAGE - Multi-subsystem projects:
    # Via flag:
    pbjson --subsystem tracking decided "..."
    pbjson --subsystem glossary question "..."
    
    # Via colon syntax (shorter):
    pbjson decided:tracking "..."
    pbjson question:glossary "..."

USAGE - Custom state directory:
    pbjson --state-dir ./2023/day01 decided "..."          # Store state in specific directory
    pbjson --state-dir ../shared built "..."               # Use relative paths
    
    Useful when:
    - Using pbjson as a dependency/submodule (not copying into project root)
    - Organizing state files in folder hierarchies (e.g., by year/puzzle/domain)
    - Keeping state files alongside related code rather than at repo root

EXAMPLES:
    pbjson decided "Use Obsidian for output - fast generation + graph view"
    pbjson built "arxiv_fetcher.py (fetches from arXiv API)"
    pbjson question "Should we cache synthesis results?"
    pbjson file "paper_library/orchestrator.py - main entry point"
    pbjson context "Token cost not a concern for this project"
    pbjson resolve "caching strategy" "Cache by paper DOI, invalidate on manual edit"

STATE FILE FORMAT:
    project.json (main)              - Top-level project decisions and work
    {subsystem}-state.json           - Subsystem-specific state (e.g., meta-tracking-state.json)
    
    Each file contains:
    {
        "what_we_decided": ["2026-01-08 - Decision text"],
        "what_we_built": ["2026-01-08 - Built feature (search: keyword)"],
        "what_we_need_to_decide": ["2026-01-08 - Open question"],
        "what_we_resolved": ["2026-01-08 - Question â†’ Decision made"],
        "important_files": ["2026-01-08 - path/to/file - purpose"],
        "context": ["2026-01-08 - Background information"]
    }

PHILOSOPHY - When to use each field:
    decided:  Architectural decisions made WITH user agreement (not proposals)
    built:    Work completed; searchable by filename/feature (e.g., "built (as orchestrator.py)")
    question: Open questions needing user input or decisions
    resolved: Questions answered; shows question â†’ decision mapping
    file:     Entry points ONLY (max 3-5) - "where do I start for X task?"
    context:  Constraints, user preferences, background facts for reference

CONSTRAINTS & DESIGN:
    - Single-file tool (works in Claude project context without package structure)
    - Append-only log (git-friendly, creates natural decision history)
    - Prefix-based subsystems (no nested dirs; works with file upload limits)
    - Python stdlib only (json, sys, pathlib, datetime)
    - No external dependencies
"""

import json
import sys
from datetime import date
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any

# ============================================================================
# CONFIGURATION & STATE STRUCTURE
# ============================================================================

# State directory management
# By default, state files live alongside pbjson.py (original flat-file design).
# Can be overridden via --state-dir flag to support hierarchical project structures.
# This global variable is set once during CLI parsing and used by all state operations.
STATE_DIR: Path = Path(__file__).parent  # Default: same directory as pbjson.py


def get_project_file() -> Path:
    """
    Get the path to the main project.json state file.
    
    Uses the configured STATE_DIR, which defaults to pbjson.py's directory but
    can be overridden via --state-dir flag. This allows pbjson to work both as
    a copied tool (original design) and as a submodule/dependency.
    
    Returns:
        Path to project.json in the configured state directory
    
    Example:
        # Default behavior (STATE_DIR not overridden):
        get_project_file() → /path/to/pbjson/project.json
        
        # With --state-dir ./puzzles/2023/day01:
        get_project_file() → /path/to/puzzles/2023/day01/project.json
    """
    return STATE_DIR / "project.json"


# Field names in state files (defines the structure of all state)
STATE_FIELDS: List[str] = [
    "what_we_decided",
    "what_we_built",
    "what_we_need_to_decide",
    "what_we_resolved",
    "important_files",
    "context"
]

# Mapping from CLI commands to state fields
# This defines what each command does (e.g., "decided" adds to "what_we_decided")
COMMAND_TO_FIELD: Dict[str, str] = {
    'decided': 'what_we_decided',
    'built': 'what_we_built',
    'question': 'what_we_need_to_decide',
    'file': 'important_files',
    'context': 'context'
}

# ============================================================================
# STATE FILE I/O
# ============================================================================

def get_subsystem_file(subsystem: str) -> Path:
    """
    Get the state file path for a subsystem.
    
    Implements prefix-based file naming to work within file upload constraints
    (no nested directories allowed in some contexts). This is a core design
    pattern that allows organizing multi-subsystem projects in a flat file layout.
    
    Uses the configured STATE_DIR for file location, which can be overridden
    via --state-dir flag to support hierarchical project structures.
    
    Args:
        subsystem: Subsystem name (e.g., 'tracking', 'glossary', 'features')
    
    Returns:
        Path to {subsystem}-state.json in the configured state directory
    
    Example:
        get_subsystem_file('glossary') â†’ Path('./glossary-state.json')
        get_subsystem_file('meta-tracking') â†’ Path('./meta-tracking-state.json')
    """
    return STATE_DIR / f"{subsystem}-state.json"


def _create_empty_state(subsystem: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new empty state dictionary with all required fields.
    
    Used when initializing a new project or subsystem. Ensures all expected
    fields exist even in empty projects (prevents KeyError on first read).
    
    Args:
        subsystem: Optional subsystem name to track which file this is for
    
    Returns:
        Dictionary with all state fields initialized as empty lists
    """
    state = {
        "what_we_decided": [],
        "what_we_built": [],
        "what_we_need_to_decide": [],
        "what_we_resolved": [],
        "important_files": [],
        "context": []
    }
    
    # Track which subsystem this state belongs to (for informational purposes)
    if subsystem:
        state["subsystem"] = subsystem
    
    return state


def load_state(subsystem: Optional[str] = None) -> Dict[str, Any]:
    """
    Load project state from JSON file, creating if it doesn't exist.
    
    Handles backward compatibility for projects that gain new fields over time.
    If a state file doesn't exist yet, returns an empty state that will be
    created when save_state() is called.
    
    Args:
        subsystem: Optional subsystem name. If provided, loads {subsystem}-state.json
                   instead of project.json. This allows multi-subsystem projects to
                   track state separately.
    
    Returns:
        Dictionary containing project state with all required fields
    
    Raises:
        SystemExit: If state file exists but contains invalid JSON (with helpful error message)
    """
    if subsystem:
        state_file = get_subsystem_file(subsystem)
    else:
        state_file = get_project_file()
    
    # If file doesn't exist, return empty state
    # It will be created on the next save_state() call
    if not state_file.exists():
        return _create_empty_state(subsystem)
    
    # Load and validate
    try:
        with open(state_file, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: State file {state_file} contains invalid JSON")
        print(f"Details: {e}")
        sys.exit(1)
    
    # Ensure all fields exist (backward compatibility)
    # If someone was using an older version without 'what_we_resolved', add it
    for field in STATE_FIELDS:
        if field not in data:
            data[field] = []
    
    # Add subsystem marker if missing (backward compatibility)
    if subsystem and "subsystem" not in data:
        data["subsystem"] = subsystem
    
    return data


def save_state(state: Dict[str, Any], subsystem: Optional[str] = None) -> None:
    """
    Save project state to JSON file.
    
    Writes with pretty formatting (indent=2) for human readability and clean git diffs.
    The append-only log structure means this is safe to call repeatedlyâ€”each save
    just overwrites with new entries appended.
    
    Args:
        state: The state dictionary to save
        subsystem: Optional subsystem name. If provided, saves to {subsystem}-state.json
    
    Raises:
        SystemExit: If unable to write to file (with helpful error message)
    """
    if subsystem:
        state_file = get_subsystem_file(subsystem)
    else:
        state_file = get_project_file()
    
    try:
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)
    except IOError as e:
        print(f"Error: Could not write to {state_file}")
        print(f"Details: {e}")
        sys.exit(1)


# ============================================================================
# STATE MANAGEMENT OPERATIONS
# ============================================================================

def add_entry(update_type: str, content: str, subsystem: Optional[str] = None) -> None:
    """
    Add a dated entry to the appropriate state field.
    
    This is the core operation for recording decisions, work, questions, and context.
    Each entry is prefixed with today's date (ISO format) and appended to the 
    appropriate list. This creates an append-only log that's git-friendly and
    preserves decision history.
    
    Args:
        update_type: Type of entry ('decided', 'built', 'question', 'file', 'context')
        content: The entry text to add (should not include date; we add it)
        subsystem: Optional subsystem name. If provided, operates on {subsystem}-state.json
    
    Raises:
        SystemExit: If update_type is not recognized
    
    Side effects:
        - Loads state from file
        - Appends new entry to appropriate field
        - Saves state back to file
        - Prints confirmation to stdout
    
    Example:
        add_entry('decided', 'Use Obsidian for output', subsystem=None)
        add_entry('question', 'Cache strategy?', subsystem='features')
    """
    state = load_state(subsystem)
    
    # Format entry with ISO date prefix for sorting and git readability
    # Date format is YYYY-MM-DD, which sorts chronologically as strings
    entry = f"{date.today().isoformat()} - {content}"
    
    # Validate and map command to field
    if update_type not in COMMAND_TO_FIELD:
        print(f"Error: Unknown command '{update_type}'")
        print(f"Valid commands: {', '.join(sorted(COMMAND_TO_FIELD.keys()))}")
        sys.exit(1)
    
    field = COMMAND_TO_FIELD[update_type]
    state[field].append(entry)
    
    # Save and provide feedback
    save_state(state, subsystem)
    subsystem_label = f" [{subsystem}]" if subsystem else ""
    print(f"âœ“ Added to {field}{subsystem_label}: {content}")


def resolve_question(question_partial: str, decision_text: str, 
                    subsystem: Optional[str] = None) -> None:
    """
    Move a question from "what_we_need_to_decide" to "what_we_resolved".
    
    This operation finds a matching open question using case-insensitive partial
    matching, creates a resolution entry linking the question to the decision,
    and removes the question from the open list. The resolution preserves both
    the original question and the decision for historical reference.
    
    Args:
        question_partial: Partial text to match against open questions (case-insensitive)
        decision_text: Description of the decision that resolves the question
        subsystem: Optional subsystem name
    
    Prints:
        - Success message with question and decision
        - Error messages if question not found or if match is ambiguous
        - List of open questions if no match found
    
    Exit behavior:
        - Returns normally on success or ambiguous match (user needs to try again)
        - Does not exit on error (allows script to continue)
    
    Example:
        resolve_question('caching', 'Cache by DOI, invalidate on manual edit')
    """
    state = load_state(subsystem)
    
    # Find questions matching the partial text (case-insensitive)
    matching = [q for q in state['what_we_need_to_decide'] 
                if question_partial.lower() in q.lower()]
    
    # Handle no match
    if not matching:
        subsystem_label = f" [{subsystem}]" if subsystem else ""
        print(f"âœ— No question found matching{subsystem_label}: '{question_partial}'")
        if state['what_we_need_to_decide']:
            print(f"\nOpen questions:")
            for q in state['what_we_need_to_decide']:
                print(f"  â€¢ {q}")
        return
    
    # Handle ambiguous match (multiple questions contain the text)
    if len(matching) > 1:
        print(f"âš  Multiple matches found ({len(matching)}):")
        for i, q in enumerate(matching, 1):
            print(f"  {i}. {q}")
        print("\nPlease be more specific")
        return
    
    # Extract the question (remove the date prefix for readability)
    question = matching[0]
    question_text = question.split(' - ', 1)[1] if ' - ' in question else question
    
    # Create resolution entry with date and arrow showing the resolution
    # The arrow (â†’) visually indicates the mapping from question to decision
    resolution = f"{date.today().isoformat()} - {question_text} â†’ Decided: {decision_text}"
    
    # Update state: remove question from open list, add resolution to resolved list
    state['what_we_need_to_decide'].remove(question)
    state['what_we_resolved'].append(resolution)
    save_state(state, subsystem)
    
    # Provide feedback
    subsystem_label = f" [{subsystem}]" if subsystem else ""
    print(f"âœ“ Resolved{subsystem_label}: {question_text}")
    print(f"  Decision: {decision_text}")


# ============================================================================
# CLI PARSING & ENTRY POINT
# ============================================================================

def parse_command_with_subsystem(arg: str) -> Tuple[str, Optional[str]]:
    """
    Parse a command argument that might include subsystem suffix.
    
    Supports "command:subsystem" syntax for brevity, allowing shorter CLI calls
    like 'decided:tracking' instead of '--subsystem tracking decided'.
    Also handles standalone commands without subsystems.
    
    Args:
        arg: Command argument (e.g., 'decided' or 'decided:tracking')
    
    Returns:
        Tuple of (command, subsystem) where subsystem is None if not in the argument
    
    Example:
        parse_command_with_subsystem('decided:tracking') â†’ ('decided', 'tracking')
        parse_command_with_subsystem('decided') â†’ ('decided', None)
    """
    if ':' in arg:
        command, subsystem = arg.split(':', 1)
        return command, subsystem
    return arg, None


def main() -> None:
    """
    Main entry point for the CLI.
    
    Handles:
    - State directory configuration via --state-dir flag
    - Command parsing (with optional subsystem suffix via ':' or '--subsystem' flag)
    - Routing to appropriate operation (add_entry, resolve_question)
    - Error handling and usage display
    - Argument validation
    
    Exit codes:
        0: Success
        1: Error (invalid command, missing args, JSON error, etc.)
    
    Supported commands:
    - decided, built, question, file, context: Add entries via add_entry()
    - resolve: Move questions to resolutions via resolve_question()
    """
    # Show help if no arguments
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    # Parse --state-dir flag FIRST (must be set before any state file operations)
    # This flag allows state files to be stored in a custom directory rather than
    # alongside pbjson.py. Useful for hierarchical project structures or when using
    # pbjson as a submodule/dependency.
    args = sys.argv[1:]
    
    if args and args[0] == '--state-dir':
        if len(args) < 2:
            print("Error: --state-dir requires a directory path")
            sys.exit(1)
        
        # Set the global STATE_DIR to the specified path (resolved to absolute)
        # This affects all subsequent get_project_file() and get_subsystem_file() calls
        global STATE_DIR
        STATE_DIR = Path(args[1]).resolve()
        
        # Ensure the directory exists (create if needed)
        # This prevents confusing "file not found" errors when the directory doesn't exist
        if not STATE_DIR.exists():
            try:
                STATE_DIR.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                print(f"Error: Could not create state directory {STATE_DIR}")
                print(f"Details: {e}")
                sys.exit(1)
        
        # Verify it's actually a directory
        if not STATE_DIR.is_dir():
            print(f"Error: --state-dir path exists but is not a directory: {STATE_DIR}")
            sys.exit(1)
        
        args = args[2:]  # Remove --state-dir and its argument from args
    
    # Check for --subsystem flag (alternative to colon syntax)
    subsystem: Optional[str] = None
    
    if args and args[0] == '--subsystem':
        if len(args) < 2:
            print("Error: --subsystem requires a subsystem name")
            sys.exit(1)
        subsystem = args[1]
        args = args[2:]  # Remove --subsystem and its argument from args
    
    # Require at least a command after flag processing
    if not args:
        print(__doc__)
        sys.exit(1)
    
    # Parse command (might have subsystem suffix like "decided:tracking")
    command = args[0]
    parsed_command, parsed_subsystem = parse_command_with_subsystem(command)
    
    # Subsystem from suffix takes precedence over --subsystem flag
    if parsed_subsystem:
        subsystem = parsed_subsystem
    
    # Handle 'resolve' command (special case: needs two arguments)
    if parsed_command == 'resolve':
        if len(args) < 3:
            print("Usage: pbjson resolve <question_partial> <decision_text>")
            print("       pbjson --subsystem <n> resolve <question_partial> <decision_text>")
            print("       pbjson resolve:subsystem <question_partial> <decision_text>")
            print("\nExample:")
            print('  pbjson resolve "caching" "Cache by DOI, invalidate on manual edit"')
            print('  pbjson resolve:features "performance" "Use async processing"')
            sys.exit(1)
        
        question_partial = args[1]
        decision_text = args[2]
        resolve_question(question_partial, decision_text, subsystem)
    
    # Handle regular add_entry commands
    else:
        if len(args) < 2:
            print(__doc__)
            sys.exit(1)
        
        update_type = parsed_command
        content = args[1]
        add_entry(update_type, content, subsystem)


if __name__ == '__main__':
    main()