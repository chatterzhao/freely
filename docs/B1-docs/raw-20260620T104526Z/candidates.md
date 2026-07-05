# Candidates

## C-20260620T104526Z-A: legacy issue
- status: promoted
- milestone: M-20260620T104526Z-A
- promoted_issue_path: docs/issues/I-20260620T104526Z-A/issue.md
- summary: Fix session_id pass-through chain, capture worker session after launch, add SSE supervision to Manager patrol
- rationale: A2A Server has SSE infrastructure but it's unused. Store worker session_id to enable real-time supervision and session/prompt intervention.
- acceptance: Worker session_id stored in A2A task after launch; Manager patrol docs include SSE and intervention instructions
- next: Materialize as I-20260620T104526Z-A, merge via PR
