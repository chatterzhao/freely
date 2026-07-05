# Candidates

## C-20260623T022909Z-A
- status: promoted
- milestone: M-20260623T022909Z-A
- promoted_issue_path: docs/issues/I-20260623T022909Z-A/issue.md
- summary: Fix platform_adapter import broken by hyphenated filename in task-lifecycle-scan.py
- rationale: `from platform_adapter import` fails because file is named `platform-adapter.py`
- acceptance: task-lifecycle-scan.py runs without ImportError
- next: Merge via PR
