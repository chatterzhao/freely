# Tasks: fix get_config → python3 reader
- issue_id: I-20260630T143515Z-A
## Task 1: Fix config.toml reader
- Replace grep+sed with python3 one-liner
## Task 2: Fix PROJECT_ROOT → project
- init context uses $project, not $PROJECT_ROOT
