# IBM Brainstorm - structured-closeout-gate-context-and-review-evidence-governance

## Core framing

这条 owner 修的不是“门禁缺失”，而是“门禁 contract 没有在 runtime state 中完整可恢复”。

## Candidate implementation shape

### A. Structured closeout fields

- keep the existing `Closeout-Gate` command as compatibility output only
- add first-class fields for target lane, promotion gate, adequacy requirement, and review-artifact policy
- treat these fields as part of the verification contract, not cleanup-local state

### B. Consumer alignment

- delegated intake and workcell state persist the same structured fields
- cleanup replay reads structured fields directly
- merge-gate diagnostics and worker guidance reuse the same wording and field names

### C. Compatibility boundary

- older snapshots without structured closeout fields fail closed into retained continuation
- no break-glass or hidden fallback to permissive parsing

## Risks

- if the field set is too broad, this owner will drift back into a generic test-orchestration design
- if the field set is too narrow, operators will still not know why fresh staged review evidence is required
- if compatibility logic becomes too implicit, the repo will keep carrying two competing closeout truths
