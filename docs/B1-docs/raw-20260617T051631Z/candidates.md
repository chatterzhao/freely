# Candidates: Dynamic project list via adapter

## C-20260617T051631Z-A: legacy issue
- title: Replace hardcoded project list with adapter-driven discovery
- status: promoted
- promoted_issue_path: docs/issues/I-20260617T051631Z-A/issue.md
- milestone: M-20260617T051631Z-A
- summary: |
    AppShell.tsx hardcoded project list. Fix adds listProjects() to
    ProbeAdapter, implemented in MockProbeAdapter and TauriProbeAdapter.
