# Verification: runtime-daemon-self-loop-followthrough-governance manager exit-contract repair prompt narrowing

- issue_id: `I-20260421-1200-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- verification_date: `2026-04-25`
- verifier: `codex`
- source_branch: `feature/manager-exit-contract-prompt-narrowing-20260425`
- source_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260425-feature-manager-exit-contract-prompt-narrowing`

## Scope Verdict

- `PASS`: this continuation stays inside `I-20260421-1200-A`. The blocker is still the runtime middleman that decides how manager repair rounds relaunch after malformed or missing exit-contract evidence, not a new scan-priority rule or a manager/worker architecture redesign.
- `FAIL`: canonical `develop` replay after the watchdog keepalive repairs no longer stalled at `L042`, but it still failed the autonomy loop because manager could exit `rc=0` without `manager-exit-contract.env`, then re-enter on `fresh_with_handoff` with `rotation_reason=missing_resume_evidence` and receive the full broad lead-agent startup prompt again.
- `FAIL`: real runtime evidence matched that seam exactly: repeated `manager_empty_success_cycle_detected details=missing_file`, `last_launch_kind: fresh_with_handoff`, `last_rotation_reason: missing_resume_evidence`, and stale `latest_manager_continuity_generated`, which means repair selection was correct but the next prompt contract was too wide to force bounded continuity/exit-contract closeout.
- `PASS`: `build_prompt()` now narrows only this exact repair surface. When the effective role is manager, the handoff rotation reason is `manager_exit_contract_repair`, and launch selection has already downgraded to `fresh_with_handoff` because resume evidence is missing, runtime bypasses the broad `start-lead-agent.sh` startup prompt and emits a bounded repair prompt focused on:
  1. reading only `AGENTS.md`, `session-handoff.txt`, `live-status`, current scan json, and the latest manager continuity
  2. writing a fresh manager continuity first
  3. writing `manager-exit-contract.env` second
  4. avoiding broad patrol, full milestone rereads, or fleet-wide survey before those artifacts exist
- `PASS`: the narrowed repair prompt preserves the existing `manager continuity 文件：\`...\`` line so the current continuity materialization contract remains compatible with `materialize_required_manager_continuity_startup_stub()` instead of introducing another special-case artifact shape.
- `PASS`: focused feature-local verification passed:
  1. `bash docs/system/workspace/scripts/tests/test-freely-manager-repair-fresh-with-handoff-prompt-narrowing`
  2. `bash docs/system/workspace/scripts/tests/test-freely-manager-empty-success-cycle-does-not-autoresume`
  3. `bash docs/system/workspace/scripts/tests/test-freely-manager-repair-handoff-missing-resume-evidence-falls-back`
  4. `bash docs/system/workspace/scripts/tests/test-freely-worker-repair-prompt-prioritizes-exit-contract`
  5. `bash docs/system/workspace/scripts/tests/test-freely-manager-consumed-continuity-resume-focus`
  6. `./bin/governance-check`
- `PASS`: protected `premerge-integration` replay passed on `2026-04-25 20:39 PDT` in `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260425-test-pre-merge-manager-exit-contract-prompt-narrowing`:
  1. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-manager-repair-fresh-with-handoff-prompt-narrowing`
  2. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-manager-empty-success-cycle-does-not-autoresume`
  3. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-manager-repair-handoff-missing-resume-evidence-falls-back`
  4. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-worker-repair-prompt-prioritizes-exit-contract`
  5. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-manager-consumed-continuity-resume-focus`
  6. `./bin/test-lane premerge-integration -- ./bin/governance-check`
  7. `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260425-test-pre-merge-manager-exit-contract-prompt-narrowing --issue docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md --require-adequacy --target-lane premerge-integration --promotion-gate develop_merge`
- `PENDING`: canonical `develop` daemon acceptance remains open. This repair is not complete until the merged root replay shows the next manager repair/fresh-with-handoff round producing continuity + exit contract and Freely continuing toward select -> finish -> merge upward -> retire -> next task.

## Implementation Decision Note

- decision: `Narrow only the manager exit-contract repair prompt when launch selection has already downgraded to fresh_with_handoff because resume evidence is missing.`
- why_this: `The observed failure was not that runtime chose the wrong next action. It already knew this was a manager exit-contract repair round. The bug was that the broad startup prompt let manager drift back into patrol context instead of forcing bounded artifact repair.`
- alternatives_considered: `Keep broad startup prompt and rely on stronger natural-language wording, move exit-contract repair entirely into new runtime-side auto-materialization, or redesign supervision around a different multi-agent protocol before stabilizing the current artifact-driven control plane.`
- boundary_non_goals: `No change to task-source scan ordering, manager semantic prioritization, worker delegation taxonomy, or the broader startup patrol contract for non-repair rounds.`
- residual_risk: `If canonical develop replay still leaves manager without a fresh continuity or exit contract after this narrowing, the next blocker is likely downstream in runtime artifact validation or continuity consumption rather than in prompt breadth at repair relaunch.`
