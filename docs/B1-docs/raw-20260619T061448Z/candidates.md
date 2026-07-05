# Candidates: A2A server h11 noise suppression

## C-20260619T061448Z-A
- title: Suppress h11 non-HTTP noise via uvicorn log config
- status: promoted
- promoted_issue_path: docs/issues/I-20260619T061448Z-A/issue.md
- milestone: M-20260619T061448Z-A
- summary: |
    A2A server logs 40+ "Invalid HTTP request received" warnings from h11
    when non-HTTP probes connect. Content-Length bug already fixed.
    Fix adds custom uvicorn log_config setting h11 logger to ERROR.
