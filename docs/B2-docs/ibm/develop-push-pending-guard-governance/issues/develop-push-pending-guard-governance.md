# Issue: develop-push-pending-guard-governance

- issue_id: `I-20260401-1035-A`
- title: Develop push pending guard governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `develop-push-pending-guard-governance`
- issue-name: `develop-push-pending-guard-governance`
- priority: P0
- source_candidate: `docs/B1-docs/raw-20260401T224500Z/candidates.md#c-20260401-1035-a`
- source_brainstorm: `docs/B1-docs/raw-20260401T224500Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/ibm/develop-push-pending-guard-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-develop-push-pending-guard-governance.md`
- verification_artifact_dir: `docs/B2-docs/ibm/develop-push-pending-guard-governance/code-reviews`
- depends_on:
  - `docs/B2-docs/git-worktree/protected-post-merge-acceptance-route-and-promotion-guard-governance/issues/protected-post-merge-acceptance-route-and-promotion-guard-governance.md`
  - `docs/B2-docs/ibm/active-milestone-placement-and-consumption-gate-governance/issues/active-milestone-placement-and-consumption-gate-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely already protects branch topology and develop-bound merges, but still lacks canonical truth for the interval after a local protected-branch merge and before the corresponding remote push. That gap creates two risks:

1. local `develop` can carry merge-complete truth that has not reached the remote canonical integration branch yet, and
2. post-merge acceptance, cleanup, and next-lane scheduling can continue without any explicit record of whether push is intentionally delayed or silently forgotten.

This owner fixes that governance gap without auto-pushing on behalf of the operator/runtime.

## Scope

1. Freeze canonical `develop` push states:
   - `push_pending`
   - `push_deferred`
2. Add machine-readable detection for `develop` being ahead of its tracked remote.
3. Add a small runtime-managed defer-reason truth surface so delayed push can be explicit rather than implicit.
4. Surface the new push state in:
   - `freely live-status`
   - `freely fleet-status`
   - `wt-fleet-status`
5. Teach project-level patrol truth that `develop ahead without defer reason` is a first-class standing-source drift.

## Non-Goals

1. Do not implement automatic push in hooks or runtime.
2. Do not redesign the full merge/promotion flow.
3. Do not block feature-branch local work merely because a separate repo has no remote configured.
4. Do not generalize the first slice to every branch family; start with canonical `develop`.
5. Do not turn the first slice into a repo-wide blocker in `governance-check`.

## Acceptance

1. Freely can distinguish `develop` clean, `push_pending`, and `push_deferred` without inventing a new issue-phase state.
2. A structured defer reason can be written and cleared without editing hidden files manually.
3. `live-status`, `fleet-status`, and `wt-fleet-status` expose the push state clearly enough for manager patrol to consume it.
4. The manager/patrol truth sources explicitly treat unresolved develop push debt as a standing-source governance item.
5. Hooks continue blocking illegal push, but no hook auto-pushes.

## Completion

- `docs/B1-docs/raw-20260401T224500Z/brainstorms.md`
- `docs/B1-docs/raw-20260401T224500Z/candidates.md`
- `docs/B1-docs/raw-INDEX.md`
- `docs/milestones.md`
- `docs/B2-docs/ibm/develop-push-pending-guard-governance/issues/develop-push-pending-guard-governance.md`
- `docs/B2-docs/ibm/develop-push-pending-guard-governance/pre-tests.md`
- `docs/B2-docs/ibm/develop-push-pending-guard-governance/code-reviews/20260401-develop-push-pending-guard-verification.md`
- `docs/progress/workspace-routing-foundation/p-develop-push-pending-guard-governance.md`
- `docs/LAWS.md`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/skills/multi-worktree-supervision/references/manager-reactivation-patrol.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/worktree/wt-fleet-status`
- `docs/system/workspace/scripts/tests/test-freely-live-status-develop-push-pending`
- `docs/system/workspace/scripts/tests/test-freely-fleet-status-develop-push-pending`
- `docs/system/workspace/scripts/tests/test-wt-fleet-status-develop-push-pending`

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-live-status-develop-push-pending`
- `bash docs/system/workspace/scripts/tests/test-freely-fleet-status-develop-push-pending`
- `bash docs/system/workspace/scripts/tests/test-wt-fleet-status-develop-push-pending`
- `bash docs/system/workspace/scripts/tests/test-governance-check-candidate-v2`
- `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
- `./bin/governance-check`

## Next

- `2026-04-01 10:45 PDT` canonical develop absorption is complete; this owner is closed.
- Future work may widen push-followthrough truth to other protected branch families or introduce stronger repo-wide blocking semantics, but that belongs to a new lifecycle rather than reopening this bounded develop-only slice.
