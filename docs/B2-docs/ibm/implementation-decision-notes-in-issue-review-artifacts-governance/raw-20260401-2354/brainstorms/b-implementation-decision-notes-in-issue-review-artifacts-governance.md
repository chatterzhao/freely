# Brainstorm: implementation-decision-notes-in-issue-review-artifacts-governance

## Key Decisions

1. Canonical landing surface stays in issue-bound `code-reviews/`
- do not add a parallel `decision-summaries/` tree
- decision notes belong to the same artifact family that already carries verification verdicts and residual risks

2. Gate against presence + structure, not prose quality
- the merge gate should not try to grade “thoughtfulness”
- it should only enforce that owner-bound implementation changes carry a recoverable decision note surface

3. Reuse owner issue truth
- the gate must resolve the current owner issue and then look under that issue’s `verification_artifact_dir`
- avoid repository-wide scans or filename heuristics beyond the owner issue’s declared review directory

4. Keep the note minimal
- `decision`
- `why_this`
- `alternatives_considered`
- `boundary_non_goals`
- `residual_risk`

## Why Not Progress

- `progress` is the execution-state log for dev-loop, not the canonical explanation surface for a specific develop-bound implementation batch
- the same issue may have many progress rewrites before one merge-worthy implementation decision lands

## Why Not PRD

- `prd.md` freezes issue-level contract, not branch-local implementation choice
- forcing every implementation decision back into `prd.md` would either create churn or blur issue contract with batch-local tradeoffs

## Why Not New Directory

- it would create a parallel truth family
- it would require new owner resolution rules even though `verification_artifact_dir` already exists
- it would make reviewer workflow worse by splitting “what was verified” from “why this implementation was chosen”
