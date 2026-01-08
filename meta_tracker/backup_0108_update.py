#!/usr/bin/env python3
"""
Project state management script

Usage:
    ./update.py decided "Using Discord bot - cross-platform UI"
    ./update.py built "Login component (as LoginComponent.tsx)"
    ./update.py question "SQLite or Postgres for citation index?"
    ./update.py file "src/auth.ts - handles login"
    ./update.py context "Uploaded files may be replaced with annotated versions"
    ./update.py resolve "GROBID performance" "Use GROBID for slow/comprehensive processing"
"""

import json
import sys
from datetime import date
from pathlib import Path

PROJECT_FILE = Path(__file__).parent / "project.json"

def load_project():
    """Load project state, creating if doesn't exist"""
    if not PROJECT_FILE.exists():
        return {
            "what_we_decided": [],
            "what_we_built": [],
            "what_we_need_to_decide": [],
            "what_we_resolved": [],
            "important_files": [],
            "context": []
        }
    
    with open(PROJECT_FILE, 'r') as f:
        data = json.load(f)
    
    # Add what_we_resolved if it doesn't exist (backward compatibility)
    if 'what_we_resolved' not in data:
        data['what_we_resolved'] = []
    
    return data

def save_project(data):
    """Save project state"""
    with open(PROJECT_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def update_project(update_type, content):
    """Add entry to appropriate section"""
    data = load_project()
    
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
    
    save_project(data)
    print(f"âœ“ Added to {field}: {content}")

def resolve_question(question_partial, decision_reference):
    """Mark a question as resolved and link to decision"""
    data = load_project()
    
    # Find matching question
    matching = [q for q in data['what_we_need_to_decide'] 
                if question_partial.lower() in q.lower()]
    
    if not matching:
        print(f"âŒ No question found matching: '{question_partial}'")
        print("\nOpen questions:")
        for q in data['what_we_need_to_decide']:
            print(f"  â€¢ {q}")
        return
    
    if len(matching) > 1:
        print("âš ï¸  Multiple matches found:")
        for i, q in enumerate(matching, 1):
            print(f"  {i}. {q}")
        print("\nPlease be more specific")
        return
    
    question = matching[0]
    
    # Extract just the question text (without date)
    question_text = question.split(' - ', 1)[1] if ' - ' in question else question
    
    # Create resolution entry
    resolution = f"{date.today().isoformat()} - {question_text} â†’ Decided: {decision_reference}"
    
    # Update data
    data['what_we_need_to_decide'].remove(question)
    data['what_we_resolved'].append(resolution)
    
    save_project(data)
    print(f"âœ“ Resolved: {question_text}")
    print(f"  Decision: {decision_reference}")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'resolve':
        if len(sys.argv) < 4:
            print("Usage: ./update.py resolve <question_partial> <decision_reference>")
            print("\nExample:")
            print('  ./update.py resolve "GROBID performance" "Use GROBID for slow/comprehensive processing"')
            sys.exit(1)
        
        question_partial = sys.argv[2]
        decision_reference = sys.argv[3]
        resolve_question(question_partial, decision_reference)
    else:
        if len(sys.argv) < 3:
            print(__doc__)
            sys.exit(1)
        
        update_type = sys.argv[1]
        content = sys.argv[2]
        update_project(update_type, content)

if __name__ == '__main__':
    main()