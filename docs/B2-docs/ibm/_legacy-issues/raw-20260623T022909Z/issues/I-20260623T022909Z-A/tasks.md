# Tasks

1. [x] Add importlib import at top of file
2. [x] Create `_get_pa()` cached lazy loader function
3. [x] Replace direct import at line 19: `from platform_adapter import list_open_issues` → `_get_pa().list_open_issues`
4. [x] Replace direct import at line 438: `from platform_adapter import configured_platforms` → `_get_pa().configured_platforms`
5. [x] Replace direct import at line 474: `from platform_adapter import fetch_issue_state` → `_get_pa().fetch_issue_state`
6. [x] Test: run `task-lifecycle-scan.py --project <project> --json`
7. [ ] Merge to develop via PR
