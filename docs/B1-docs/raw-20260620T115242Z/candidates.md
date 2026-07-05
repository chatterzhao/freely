# Candidates

## C-20260620T115242Z-A: legacy issue
- status: promoted
- milestone: M-20260620T115242Z-A
- promoted_issue_path: docs/issues/I-20260620T115242Z-A/issue.md
- summary: wt-close closes absorbed I-* issue; issue-sync supports parent_raw fallback
- rationale: ~30 completed I-* issues stuck open on GitHub because wt-close only closed the raw issue, never the absorbed I-*
- acceptance: Running wt-close on a raw→I absorbed chain closes both GitHub issues
- next: Materialize as I-20260620T115242Z-A, merge via PR
