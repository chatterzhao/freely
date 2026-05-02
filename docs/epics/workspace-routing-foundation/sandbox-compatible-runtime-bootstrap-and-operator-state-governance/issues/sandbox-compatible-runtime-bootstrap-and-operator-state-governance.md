# Issue: sandbox-compatible-runtime-bootstrap-and-operator-state-governance

- issue_id: `I-20260403-2245-A`
- title: Sandbox-compatible runtime bootstrap and operator-state governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `sandbox-compatible-runtime-bootstrap-and-operator-state-governance`
- issue-name: `sandbox-compatible-runtime-bootstrap-and-operator-state-governance`
- priority: P0
- source_candidate: `docs/pre-brainstorms/20260403-2245--sandbox-compatible-runtime-bootstrap-and-operator-state/candidates.md#c-20260403-2245-a`
- source_brainstorm: `docs/pre-brainstorms/20260403-2245--sandbox-compatible-runtime-bootstrap-and-operator-state/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/sandbox-compatible-runtime-bootstrap-and-operator-state-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-sandbox-compatible-runtime-bootstrap-and-operator-state-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/sandbox-compatible-runtime-bootstrap-and-operator-state-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/project-command-semantics-and-restore-work-governance/issues/project-command-semantics-and-restore-work-governance.md`
  - `docs/epics/workspace-routing-foundation/global-restart-restore-memory-governance/issues/global-restart-restore-memory-governance.md`
  - `docs/epics/freely-product-architecture/worktree-tool-boundary-bootstrap-governance/issues/worktree-tool-boundary-bootstrap-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely already knows that owner development must stay in sibling feature worktrees, and it already distinguishes project-scoped command semantics from shared/global restart state. What it still lacks is a lawful runtime path for the case where the current operator sandbox cannot write the default `$FREELY_HOME` and cannot run `/bin/ps`.

Without this owner, a sandboxed session can lose both sanctioned recovery paths:

1. direct Git ownership work in the intended worktree is blocked by sandbox metadata writes,
2. `freely start/chat/status/live-status` can also fail before delegation because operator-state bootstrap or process discovery aborts.

That hidden dead-end pressures users and agents back toward protected-root edits or ad hoc bypasses. This owner closes that narrow gap without reopening broader runtime command or tool-boundary umbrellas.

## Scope

1. Define a lawful fallback for Freely operator state when the default `$FREELY_HOME` is unwritable in the current session.
2. Keep shared/global state and project-scoped fallback state explicitly separated.
3. Make process discovery and readiness degrade clearly when `/bin/ps` is unavailable instead of hard-failing unrelated command surfaces.
4. Preserve enough project-scoped evidence for start/status/live-status/chat routing to remain truthful in degraded mode.
5. Lock the behavior with focused regressions and write the contract back to workspace truth sources.

## Non-Goals

1. Do not redesign worktree tooling boundaries; that remains closed under `I-20260403-2041-A`.
2. Do not add a generic Git sandbox bypass or weaken protected-branch policy.
3. Do not reopen project command taxonomy or global restart manifest ownership.
4. Do not promise full process observability when the sandbox intentionally blocks process inspection.

## Acceptance

1. When the default `$FREELY_HOME` is not writable, Freely can still bootstrap a lawful project-scoped operator state path without editing protected branches.
2. The runtime truth distinguishes global/shared operator state from project-local fallback state.
3. `start`, `status`, `live-status`, and interruption routing surfaces do not collapse into misleading generic failure when `/bin/ps` is unavailable.
4. Degraded runtime mode is surfaced explicitly as degraded or unavailable process evidence instead of pretending the runtime is healthy.
5. Focused regressions prove both fallback bootstrap and ps-less degraded readiness semantics.
6. When `ps` is unavailable, Freely only reuses or terminates PID-file processes when it still has project ownership evidence; arbitrary live PIDs must be treated as stale.

## Completion

- `docs/pre-brainstorms/20260403-2245--sandbox-compatible-runtime-bootstrap-and-operator-state/brainstorms.md`
- `docs/pre-brainstorms/20260403-2245--sandbox-compatible-runtime-bootstrap-and-operator-state/candidates.md`
- `docs/pre-brainstorms/INDEX.md`
- `docs/milestones.md`
- `docs/epics/workspace-routing-foundation/sandbox-compatible-runtime-bootstrap-and-operator-state-governance/issues/sandbox-compatible-runtime-bootstrap-and-operator-state-governance.md`
- `docs/epics/workspace-routing-foundation/sandbox-compatible-runtime-bootstrap-and-operator-state-governance/prd.md`
- `docs/epics/workspace-routing-foundation/sandbox-compatible-runtime-bootstrap-and-operator-state-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/sandbox-compatible-runtime-bootstrap-and-operator-state-governance/tasks.md`
- `docs/progress/workspace-routing-foundation/p-sandbox-compatible-runtime-bootstrap-and-operator-state-governance.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-sandbox-operator-state-bootstrap-fallback`
- `docs/system/workspace/scripts/tests/test-freely-status-degrades-when-ps-is-unavailable`
- `docs/system/workspace/scripts/tests/test-freely-start-attaches-when-ps-is-unavailable`
- `docs/system/workspace/scripts/tests/test-freely-start-refuses-unverified-attach-when-ps-is-unavailable`
- `docs/system/workspace/scripts/tests/test-freely-start-rejects-foreign-pids-when-ps-is-unavailable`
- `docs/system/workspace/scripts/tests/test-freely-stop-ignores-foreign-pids-when-ps-is-unavailable`

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-sandbox-operator-state-bootstrap-fallback`
- `bash docs/system/workspace/scripts/tests/test-freely-status-degrades-when-ps-is-unavailable`
- `bash docs/system/workspace/scripts/tests/test-freely-start-attaches-when-ps-is-unavailable`
- `bash docs/system/workspace/scripts/tests/test-freely-start-refuses-unverified-attach-when-ps-is-unavailable`
- `bash docs/system/workspace/scripts/tests/test-freely-start-rejects-foreign-pids-when-ps-is-unavailable`
- `bash docs/system/workspace/scripts/tests/test-freely-stop-ignores-foreign-pids-when-ps-is-unavailable`
- `bash docs/system/workspace/scripts/tests/test-freely-start-requires-interruption-dispatcher-ready`
- `./bin/governance-check`

## Next

- `2026-04-04` closeout: canonical `develop` already absorbed the narrow runtime bootstrap fallback through merge `1eddbcd` and the degraded PID ownership followthrough through merge `45bed28`.
- Keep this owner closed as the bounded operator-state bootstrap and ps-less readiness record; any future sandbox gaps beyond these constraints must reopen as a new owner on current `develop`.
