# Candidates: replace inline sqlite3 with freely-db-cli

## C-20260617T063755Z-A: legacy issue
- title: Replace inline sqlite3 session query with freely-db-cli
- status: promoted
- promoted_issue_path: docs/issues/I-20260617T063755Z-B/issue.md
- milestone: M-20260617T063755Z-A
- summary: |
    Added --tool-like to freely-db-cli session.get-active and
    freed_db_manager.py. Replaced 12-line sqlite3 heredoc in freely
    with single CLI call. Last direct sqlite3 in runtime eliminated.
