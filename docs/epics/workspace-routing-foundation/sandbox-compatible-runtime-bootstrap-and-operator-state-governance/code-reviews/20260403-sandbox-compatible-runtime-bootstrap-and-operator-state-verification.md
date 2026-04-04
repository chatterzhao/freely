# Verification: sandbox-compatible-runtime-bootstrap-and-operator-state-governance

- issue_id: `I-20260403-2245-A`
- issue_path: `docs/epics/workspace-routing-foundation/sandbox-compatible-runtime-bootstrap-and-operator-state-governance/issues/sandbox-compatible-runtime-bootstrap-and-operator-state-governance.md`
- branch: `feature/sandbox-compatible-runtime-bootstrap-and-operator-state-20260403-2245`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260403-2245-feature-sandbox-compatible-runtime-bootstrap-and-operator-state`
- verification_date: `2026-04-04`
- title: `Sandbox-compatible runtime bootstrap and operator-state governance`
- verifier: `codex`
- scope: runtime bootstrap fallback and ps-less degraded readiness only
- verdict: `pass_for_verification`

## Summary

- Freely now has a lawful project-scoped operator-state bootstrap path when the default `$FREELY_HOME` is unwritable.
- Runtime process discovery no longer hard-fails `start` reuse when `/bin/ps` is unavailable; the command degrades to truthful reduced evidence instead.
- The implementation stays within the narrow runtime/operator-state owner and does not reopen broader tool-boundary or project-command umbrellas.

## Implementation Decision Note

- decision: `Keep the runtime fix narrowly anchored in Freely's existing operator-state bootstrap and process-inspection paths by adding a lawful project-scoped fallback and ps-less degraded readiness behavior, instead of widening the change into generic sandbox bypasses or a broader runtime redesign.`
- why_this: `The real failure mode was a double dead-end in sandboxed sessions: default operator state was unwritable and /bin/ps was unavailable. Fixing those two junctions preserves lawful routing into dedicated worktrees without weakening protected-branch policy or reopening already-completed parent owners.`
- alternatives_considered: `Considered forcing explicit FREELY_HOME opt-in before any runtime command, treating ps absence as a hard command failure, or reopening broader project-command and tool-boundary owners. Those options either keep the dead-end in place or mix this narrow runtime gap with already-closed umbrellas.`
- boundary_non_goals: `This slice does not redesign worktree tooling boundaries, does not add a generic Git sandbox escape hatch, and does not promise full process observability when the sandbox intentionally withholds process evidence.`
- residual_risk: `Future sandboxes may block more than /bin/ps, and richer status/live-status truth may still need follow-on handling. This slice only guarantees lawful bootstrap and truthful degraded readiness for the currently observed constraint set.`

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
