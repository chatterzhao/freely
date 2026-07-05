# Pre-Tests: worker-reactivation-and-local-reentry-residual-runtime-governance

## Existing Evidence

- `docs/system/workspace/scripts/tests/test-freely-chat-worker-reactivation`
- `docs/system/workspace/scripts/tests/test-freely-interruption-direct-answer`
- `docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
- `docs/B1-docs/raw-20260401/brainstorms.md`

## Completed Validation

1. focused reproduction proved the exact worker attach-reuse false-success path
2. worker local reentry required both runtime repair and fixture truth tightening
3. updated focused runtime tests now reflect the worker-side truth

## Acceptance Items

### worker-attach-reuse-requires-confirmed-ai-truth
- id: `worker-attach-reuse-requires-confirmed-ai-truth`
- requirement: worker attach/reuse no longer reports success unless the reused worker has confirmed running AI ownership tied to the current project
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-chat-worker-reactivation`

### local-reentry-shares-worker-active-runtime-predicate
- id: `local-reentry-shares-worker-active-runtime-predicate`
- requirement: local worker reentry follows the same active-runtime predicate as the repaired runtime path and rejects mismatched fixture processes
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-interruption-direct-answer`

### project-command-semantics-replay-covered
- id: `project-command-semantics-replay-covered`
- requirement: project command semantics replay covers the repaired ownership and reentry truth so the residual path does not regress silently
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-project-command-semantics`

## Acceptance Test Targets

1. `test-freely-chat-worker-reactivation`
   - stopped worker continuation path no longer settles on fake success without durable AI truth
2. `test-freely-interruption-direct-answer`
   - delegated worker continuation either:
     - triggers local reentry under the frozen active-worker predicate
     - or is explicitly re-scoped so the surviving test and runtime contract agree
3. `./bin/governance-check`

## Notes

- This issue starts as a doc-loop materialization and runtime follow-up owner.
- Closure now covers the two residual paths above.
- `test-live-status-attach-false-positive-repro` may remain a side repro script, but it is not part of this owner's required acceptance set.
