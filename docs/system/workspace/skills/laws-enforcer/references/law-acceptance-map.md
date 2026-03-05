# Law Acceptance Map

- Doc-loop: issue/brainstorm/map artifacts, `PRE_TEST` baseline definition (including integration acceptance intent), and milestone sync.
- Dev-loop: implementation, test-case expansion during dev/review/test, executed `TEST` evidence (including integration acceptance), docs update, progress records.
- Promotion rule: `PRE_TEST` is baseline-only; promotion/merge gates must use executed `TEST` results.
- Code-doc mismatch rule: code/test correction path first; normative doc updates require dedicated feature/worktree and linked implementation evidence.
- Third-party API rule: provider contract is external source of truth; local code/adapters must align to API contract.
- Auto-loop: route/status updates and next-issue continuity.
- Recovery: blockers/progress/recovery fields complete.
