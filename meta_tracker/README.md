# meta_tracker folder

**What this folder is:** Tracker for the `update.py` script that maintains `project.json` and its offshoots 

**How to use it:** Manually update as the state-tracking system develops--this isn't in the main code, it's cohabitating as a monorepo for expediency's sake and will eventually get broken out into something more systematically useful.

- Update `update.py` when the script changes
- Add any additional scripts that develop
- Archive previous versions of the script 
- Keep my own copies of the .json files as backup (less trustworthy than the central project's) 
- Track eventual intentions to push *this* out as its own toolkit

### Contents:

- update.py -- Claude runs this when it updates the state files
- backup_0108_update.py -- Jan. 08 previous version, before implementing multithreading
- project.json -- Current project.json 
