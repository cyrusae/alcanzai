#!/usr/bin/env python3
"""
Project state management script

Usage:
    # Main project (project.json):
    ./update.py decided "Using Discord bot - cross-platform UI"
    ./update.py built "Login component (as LoginComponent.tsx)"
    ./update.py question "SQLite or Postgres for citation index?"
    ./update.py file "src/auth.ts - handles login"
    ./update.py context "Uploaded files may be replaced with annotated versions"
    ./update.py resolve "GROBID performance" "Use GROBID for slow/comprehensive processing"
    
    # Subsystem tracking (prefix-based state files):
    ./update.py --subsystem tracking decided "Use prefix-based files not nested dirs"
    ./update.py --subsystem glossary question "How to handle domain-specific terms?"
    
    # Or shorter syntax:
    ./update.py decided:tracking "Use prefix-based files not nested dirs"
    ./update.py question:glossary "How to handle domain-specific terms?"
"""

import json
import sys
from datetime import date
from pathlib import Path

PROJECT_FILE = Path(__file__).parent / "project.json"

def get_subsystem_file(subsystem: str) -> Path:
    """Get the state file path for a subsystem"""
    return Path(__file__).parent / f"{subsystem}-state.json"

def load_project(subsystem: str = None):
    """Load project state, creating if doesn't exist
    
    Args:
        subsystem: Optional subsystem name (e.g., 'tracking', 'glossary')
                   If provided, loads {subsystem}-state.json instead of project.json
    """
    if subsystem:
        state_file = get_subsystem_file(subsystem)
    else:
        state_file = PROJECT_FILE
    
    if not state_file.exists():
        return {
            "subsystem": subsystem,  # Track which subsystem this is
            "what_we_decided": [],
            "what_we_built": [],
            "what_we_need_to_decide": [],
            "what_we_resolved": [],
            "important_files": [],
            "context": []
        }
    
    with open(state_file, 'r') as f:
        data = json.load(f)
    
    # Add what_we_resolved if it doesn't exist (backward compatibility)
    if 'what_we_resolved' not in data:
        data['what_we_resolved'] = []
    
    # Add subsystem field if missing (backward compatibility)
    if 'subsystem' not in data and subsystem:
        data['subsystem'] = subsystem
    
    return data

def save_project(data, subsystem: str = None):
    """Save project state
    
    Args:
        data: The state data to save
        subsystem: Optional subsystem name - saves to {subsystem}-state.json
    """
    if subsystem:
        state_file = get_subsystem_file(subsystem)
    else:
        state_file = PROJECT_FILE
        
    with open(state_file, 'w') as f:
        json.dump(data, f, indent=2)

def update_project(update_type, content, subsystem: str = None):
    """Add entry to appropriate section
    
    Args:
        update_type: Type of update (decided, built, question, file, context)
        content: The content to add
        subsystem: Optional subsystem name
    """
    data = load_project(subsystem)
    
    # Format entry with date
    entry = f"{date.today().isoformat()} - {content}"
    
    # Map command to field
    field_map = {
        'decided': 'what_we_decided',
        'built': 'what_we_built',
        'question': 'what_we_need_to_decide',
        'file': 'important_files',
        'context': 'context'
    }
    
    if update_type not in field_map:
        print(f"Error: Unknown type '{update_type}'")
        print(f"Valid types: {', '.join(field_map.keys())}")
        sys.exit(1)
    
    field = field_map[update_type]
    data[field].append(entry)
    
    save_project(data, subsystem)
    
    subsystem_label = f" [{subsystem}]" if subsystem else ""
    print(f"✓ Added to {field}{subsystem_label}: {content}")

def resolve_question(question_partial, decision_reference, subsystem: str = None):
    """Mark a question as resolved and link to decision
    
    Args:
        question_partial: Partial text to match the question
        decision_reference: Description of the decision made
        subsystem: Optional subsystem name
    """
    data = load_project(subsystem)
    
    # Find matching question
    matching = [q for q in data['what_we_need_to_decide'] 
                if question_partial.lower() in q.lower()]
    
    if not matching:
        subsystem_label = f" [{subsystem}]" if subsystem else ""
        print(f"❌ No question found matching{subsystem_label}: '{question_partial}'")
        print(f"\nOpen questions:")
        for q in data['what_we_need_to_decide']:
            print(f"  • {q}")
        return
    
    if len(matching) > 1:
        print("⚠️  Multiple matches found:")
        for i, q in enumerate(matching, 1):
            print(f"  {i}. {q}")
        print("\nPlease be more specific")
        return
    
    question = matching[0]
    
    # Extract just the question text (without date)
    question_text = question.split(' - ', 1)[1] if ' - ' in question else question
    
    # Create resolution entry
    resolution = f"{date.today().isoformat()} - {question_text} → Decided: {decision_reference}"
    
    # Update data
    data['what_we_need_to_decide'].remove(question)
    data['what_we_resolved'].append(resolution)
    
    save_project(data, subsystem)
    subsystem_label = f" [{subsystem}]" if subsystem else ""
    print(f"✓ Resolved{subsystem_label}: {question_text}")
    print(f"  Decision: {decision_reference}")

def parse_command_with_subsystem(arg):
    """Parse command that might include subsystem (e.g., 'decided:tracking')
    
    Returns:
        tuple: (command, subsystem) where subsystem is None if not specified
    """
    if ':' in arg:
        command, subsystem = arg.split(':', 1)
        return command, subsystem
    return arg, None

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    # Check for --subsystem flag
    subsystem = None
    args = sys.argv[1:]
    
    if args[0] == '--subsystem':
        if len(args) < 2:
            print("Error: --subsystem requires a subsystem name")
            sys.exit(1)
        subsystem = args[1]
        args = args[2:]  # Remove --subsystem and its argument
    
    if not args:
        print(__doc__)
        sys.exit(1)
    
    # Parse command (might have subsystem suffix like "decided:tracking")
    command = args[0]
    parsed_command, parsed_subsystem = parse_command_with_subsystem(command)
    
    # Subsystem from suffix takes precedence over --subsystem flag
    if parsed_subsystem:
        subsystem = parsed_subsystem
    
    if parsed_command == 'resolve':
        if len(args) < 3:
            print("Usage: ./update.py resolve <question_partial> <decision_reference>")
            print("       ./update.py --subsystem <name> resolve <question_partial> <decision_reference>")
            print("       ./update.py resolve:tracking <question_partial> <decision_reference>")
            print("\nExample:")
            print('  ./update.py resolve "GROBID performance" "Use GROBID for slow/comprehensive processing"')
            print('  ./update.py resolve:tracking "prefix vs nested" "Use prefix-based naming"')
            sys.exit(1)
        
        question_partial = args[1]
        decision_reference = args[2]
        resolve_question(question_partial, decision_reference, subsystem)
    else:
        if len(args) < 2:
            print(__doc__)
            sys.exit(1)
        
        update_type = parsed_command
        content = args[1]
        update_project(update_type, content, subsystem)

if __name__ == '__main__':
    main()