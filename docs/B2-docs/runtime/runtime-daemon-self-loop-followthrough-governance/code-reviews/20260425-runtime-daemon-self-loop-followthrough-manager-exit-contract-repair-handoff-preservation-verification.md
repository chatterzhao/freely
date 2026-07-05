# Verification: runtime-daemon-self-loop-followthrough-governance manager exit-contract repair handoff preservation

- issue_id: `I-20260421-1200-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- verification_date: `2026-04-25`
- verifier: `codex`
- source_branch: `feature/post-l042-followthrough-keepalive-grace-replay-20260425`
- source_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260425-feature-post-l042-followthrough-keepalive-grace-replay`

## Scope Verdict

- `PASS`: this continuation stays inside `I-20260421-1200-A`. The remaining blocker is still the runtime middleman handoff/prompt contract for manager repair relaunch, not scan ordering or manager semantic prioritization.
- `FAIL`: after prompt narrowing landed, canonical root replay still failed because runtime selected the correct `fresh_with_handoff` / `missing_resume_evidence` repair relaunch and then immediately overwrote `session-handoff.txt` with a generic rotation handoff before `build_prompt()` read it.
- `FAIL`: that made the new bounded repair prompt unreachable in the real loop even though `select_launch_kind()` and the prompt builder were individually correct. The observed control-plane seam is `select_launch_kind() -> write_session_handoff() -> build_prompt()`, not task choice.
- `PASS`: runtime now preserves an existing `manager_exit_contract_repair` or `worker_exit_contract_repair` handoff when the only reason for `fresh_with_handoff` is missing resume evidence, so the repair-specific handoff contract survives long enough for prompt build and downstream exit-contract directives to consume it.
- `PASS`: the change is deliberately narrow. Ordinary `context_compacted`, route-only, dirty-budget, and other non-repair `fresh_with_handoff` rotations still rewrite `session-handoff.txt` through the existing generic writer.
- `PASS`: focused feature-local verification passed:
  1. `bash docs/system/workspace/scripts/tests/test-freely-manager-repair-missing-resume-evidence-preserves-repair-handoff`
  2. `bash docs/system/workspace/scripts/tests/test-freely-manager-repair-fresh-with-handoff-prompt-narrowing`
  3. `bash docs/system/workspace/scripts/tests/test-freely-manager-repair-handoff-missing-resume-evidence-falls-back`
  4. `bash docs/system/workspace/scripts/tests/test-freely-worker-repair-prompt-prioritizes-exit-contract`
  5. `bash docs/system/workspace/scripts/tests/test-freely-manager-empty-success-cycle-does-not-autoresume`
  6. `./bin/governance-check`
- `PENDING`: protected `premerge-integration` replay and canonical `develop` daemon acceptance remain open. This repair is not complete until the merged root replay shows the next manager repair/fresh-with-handoff round keeping the repair handoff, writing continuity + exit contract, and continuing toward the overall autonomy loop.

## Implementation Decision Note

- decision: `Preserve existing exit-contract repair handoff across fresh_with_handoff rotations that were chosen only because resume evidence is missing.`
- why_this: `Prompt narrowing alone was insufficient because runtime erased the repair signal before prompt build. The smallest correct fix is to preserve the repair handoff only for this handoff-preserving downgrade path.`
- alternatives_considered: `Teach build_prompt() to reconstruct repair semantics from session-state alone, split repair handoff and generic rotation handoff into separate artifacts immediately, or bypass handoff rewriting for every fresh_with_handoff rotation.`
- boundary_non_goals: `No change to scan ranking, no change to manager/worker role taxonomy, no broad rewrite of session rotation semantics for context compaction or other non-repair paths.`
- residual_risk: `If canonical develop replay still loops after this handoff-preservation fix, the next blocker is likely downstream in continuity materialization, exit-contract validation, or broader runtime state-machine structure rather than in handoff signal loss.`
