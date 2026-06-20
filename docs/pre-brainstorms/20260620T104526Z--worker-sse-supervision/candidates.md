# Candidates

## C-20260620T104526Z-A
- status: promoted
- milestone: M-20260620T104526Z-A
- promoted_issue_path: docs/issues/I-20260620T104526Z-A/issue.md
- summary: Fix session_id pass-through chain, capture worker session after launch, add SSE supervision to Manager patrol
- rationale: A2A Server has SSE infrastructure but it's unused. Store worker session_id to enable real-time supervision and session/prompt intervention.
- acceptance: Worker session_id stored in A2A task after launch; Manager patrol docs include SSE and intervention instructions
- next: Materialize as I-20260620T104526Z-A, merge via PR

## C-20260620T104526Z-B
- status: promoted
- milestone: M-20260620T104526Z-B
- promoted_issue_path: docs/issues/I-20260620T104526Z-B/issue.md
- summary: Add ACP bridge pass-through for real-time session/prompt delivery
- rationale: Currently session/prompt stores message on task but doesn't deliver to worker's ACP session in real-time
- acceptance: session/prompt messages delivered to active worker sessions
- next: Future follow-up (not in this PR)
