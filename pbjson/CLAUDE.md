# using pbjson within alcanzai

The name of this project is `alcanzai`. It's an AI study assistant/personal research librarian/knowledge manager. Navigate the GitHub repo attached to this project to see the source code.

At the start of each conversation: 
Review pbjson.py to understand state tracking system
cat project.json

Look for any additional subsystem json files related to initial prompt: cat {subsystem}-state.json

COMMUNICATION PROTOCOL:

- Always discuss decisions, questions, and context with the user in natural language FIRST
- State tracking tools are for RECORD-KEEPING, not communication
- After explaining something to the user, use pbjson.py to record it
- Never use tool calls as a substitute for explaining things to the user
- ALWAYS call present_files() after pbjson.py to show changes to user

DECISION WORKFLOW:

- Proposals/suggestions → Discuss in conversation (no tool calls yet)
- Open questions → Ask user, then: ./pbjson.py question "description" OR ./pbjson.py question:subsystem "description"
- Agreed decisions → After user confirms: ./pbjson.py decided "decision - brief reason"
- Work completed → After finishing: ./pbjson.py built "description (search term)"
- Important context → Anytime: ./pbjson.py context "information for reference"
- Entry point files → When creating key navigation files (max 3-5): ./pbjson.py file "path - purpose (e.g., 'start here for X')"

Within a subsystem: ./pjbson.py decided:subsystem "decision about future architecture"

FIELD PURPOSES:

- what_we_decided: Architectural decisions made with user agreement
- what_we_built: Code/files completed (searchable by filename or description)
- what_we_need_to_decide: Open questions requiring user input
- what_we_resolved: Questions that have been answered (use ./pbjson.py resolve)
- important_files: Entry points only (3-5 max) - "where do I start for X task?"
- context: Background information, constraints, user preferences, anything else to remember