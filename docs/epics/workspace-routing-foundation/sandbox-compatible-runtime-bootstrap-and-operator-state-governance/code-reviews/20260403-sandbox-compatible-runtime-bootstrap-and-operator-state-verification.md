# Verification: sandbox-compatible-runtime-bootstrap-and-operator-state-governance

- issue_id: `I-20260403-2245-A`
- title: `Sandbox-compatible runtime bootstrap and operator-state governance`
- reviewer: `codex`
- scope: runtime bootstrap fallback and ps-less degraded readiness only
- verdict: `pass_for_verification`

## Summary

- Freely now has a lawful project-scoped operator-state bootstrap path when the default `$FREELY_HOME` is unwritable.
- Runtime process discovery no longer hard-fails `start` reuse when `/bin/ps` is unavailable; the command degrades to truthful reduced evidence instead.
- The implementation stays within the narrow runtime/operator-state owner and does not reopen broader tool-boundary or project-command umbrellas.

## Evidence Read

- `docs/pre-brainstorms/20260403-2245--sandbox-compatible-runtime-bootstrap-and-operator-state/brainstorms.md`
- `docs/pre-brainstorms/20260403-2245--sandbox-compatible-runtime-bootstrap-and-operator-state/candidates.md`
- `docs/epics/workspace-routing-foundation/sandbox-compatible-runtime-bootstrap-and-operator-state-governance/issues/sandbox-compatible-runtime-bootstrap-and-operator-state-governance.md`
- `docs/epics/workspace-routing-foundation/sandbox-compatible-runtime-bootstrap-and-operator-state-governance/prd.md`
- `docs/epics/workspace-routing-foundation/sandbox-compatible-runtime-bootstrap-and-operator-state-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/sandbox-compatible-runtime-bootstrap-and-operator-state-governance/tasks.md`
- `docs/progress/workspace-routing-foundation/p-sandbox-compatible-runtime-bootstrap-and-operator-state-governance.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-start-attaches-when-ps-is-unavailable`

## Verification

1. `bash docs/system/workspace/scripts/tests/test-freely-start-attaches-when-ps-is-unavailable`
2. `./bin/governance-check`
3. Manual read-through of candidate -> issue -> progress -> runtime script linkage

## Findings

- No finding: the runtime slice now preserves lawful bootstrap and degraded readiness semantics under sandbox constraints.

## Residual Risks

- The broader `$FREELY_HOME` ownership split between shared global state and future richer project-local fallback remains intentionally narrow in this slice.
- `status`/`live-status` surfaces may still need follow-on work if future sandboxes remove more process evidence than `/bin/ps` alone.
