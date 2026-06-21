# Candidates: Remove dead CSV code paths

## C-20260617T095105Z-B
- title: Remove dead worker_prompts_csv code paths
- status: promoted
- promoted_issue_path: docs/issues/I-20260617T095105Z-B/issue.md
- milestone: M-20260617T095105Z-B
- summary: |
    Removed CSV fallback in manager_exit_contract_kind and simplified
    _manager_auto_consume_workers. PR #2914 already removed --workers;
    CSV field always empty → these code paths never executed.
