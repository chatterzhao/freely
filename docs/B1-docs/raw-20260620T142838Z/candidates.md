# Candidates: cgrab YAML fallback + skill format docs

## C-20260620T142838Z-A: legacy issue
- title: cgrab supports YAML format; I-* template uses bullet format
- status: promoted
- promoted_issue_path: docs/issues/I-20260620T142838Z-A/issue.md
- milestone: M-20260620T142838Z-A
- summary: |
    governance-merge-gate cgrab() only supported bullet format (- key: value),
    causing I-* files with YAML frontmatter to have all fields cleared during
    canonical resolution. Fix adds YAML fallback. Skill template updated to
    use bullet format with explanatory comment.
