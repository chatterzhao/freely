# Issue: runtime-evidence-provenance-research-retirement-followthrough-governance

- issue_id: `I-20260409-1715-A`
- title: Runtime evidence provenance research retirement followthrough governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `runtime-evidence-provenance-research-retirement-followthrough-governance`
- issue-name: `runtime-evidence-provenance-research-retirement-followthrough-governance`
- priority: `P0`
- source_candidate: `docs/B1-docs/raw-20260409/candidates.md#c-20260409-1715-a`
- source_brainstorm: `docs/B1-docs/raw-20260409/brainstorms.md`
- reopen_of_issue: `docs/epics/workspace-routing-foundation/worktree-maintenance-governance/issues/worktree-maintenance-governance.md`
- reopen_reason: `real develop-bound retirement of dropped candidate C-20260407-0603-A surfaced that candidate-only cleanup evidence still fails protected push and needs a narrow same-line followthrough owner`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/runtime-evidence-provenance-research-retirement-followthrough-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-runtime-evidence-provenance-research-retirement-followthrough-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/runtime-evidence-provenance-research-retirement-followthrough-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/worktree-maintenance-governance/issues/worktree-maintenance-governance.md`
  - `docs/epics/workspace-routing-foundation/develop-push-followthrough-escalation-governance/issues/develop-push-followthrough-escalation-governance.md`
  - `docs/B1-docs/raw-20260407/candidates.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

`C-20260407-0603-A` was a real research packet, but later work proved it should stay dropped rather than reopen as a mixed-owner governance issue. The remaining develop-bound diff is now only a closure problem: record the retirement decision, carry protected-branch verification evidence, and retire the obsolete dedicated research worktree.

Because `develop` push lawfully rejects candidate-only retirement evidence, this closure needs its own narrow followthrough owner instead of pretending the dropped candidate itself is a sufficient develop-bound source.

## Scope

1. Materialize the minimal candidate -> issue -> progress -> verification chain for this retirement followthrough.
2. Keep the original `C-20260407-0603-A` dropped and historical while pointing its retirement action at this owner.
3. Retire the obsolete research worktree and record the fleet closure evidence once canonical `develop` absorbs the decision.

## Non-Goals

1. Do not reopen the dropped research packet as an active runtime evidence provenance issue.
2. Do not widen `I-20260407-0215-A` or `I-20260408-1205-A`.
3. Do not introduce new runtime, manager, or worker behavior in this lane.
4. Do not treat the old mixed-owner prototype as a canonical owner-composition rule.

## Acceptance

1. The develop-bound retirement diff carries concrete same-line issue, pre-tests, progress, and verification artifacts.
2. `C-20260407-0603-A` remains explicitly dropped and historical, with retirement handled by this owner rather than by a revived IBM issue from the old packet.
3. `./bin/pretests-gate --project <worktree> --issue docs/epics/workspace-routing-foundation/runtime-evidence-provenance-research-retirement-followthrough-governance/issues/runtime-evidence-provenance-research-retirement-followthrough-governance.md` passes.
4. `./bin/governance-check` passes.
5. The obsolete research worktree is retired after canonical `develop` absorbs the closure.

## Verification

- `./bin/pretests-gate --project <worktree> --issue docs/epics/workspace-routing-foundation/runtime-evidence-provenance-research-retirement-followthrough-governance/issues/runtime-evidence-provenance-research-retirement-followthrough-governance.md`
- `git diff --check`
- `./bin/governance-check`
- `git worktree list --porcelain`

## Next

1. next_action: `completed`
2. revisit_trigger: Any future real cross-owner absorption gap must reopen as a new bounded candidate from current canonical develop rather than reviving this closeout owner.

## Completion

- `docs/milestones.md`
- `docs/B1-docs/raw-20260407/candidates.md`
- `docs/B1-docs/raw-20260409/candidates.md`
- `docs/epics/workspace-routing-foundation/runtime-evidence-provenance-research-retirement-followthrough-governance/issues/runtime-evidence-provenance-research-retirement-followthrough-governance.md`
- `docs/progress/workspace-routing-foundation/p-runtime-evidence-provenance-research-retirement-followthrough-governance.md`
- `docs/epics/workspace-routing-foundation/runtime-evidence-provenance-research-retirement-followthrough-governance/code-reviews/20260409-runtime-evidence-provenance-research-retirement-followthrough-verification.md`
