# Code Review: runtime-daemon-self-loop-followthrough-resume-incremental-output-evidence-verification

- date: `2026-04-25 20:25 PDT`
- issue: `I-20260421-1200-A`
- branch: `feature/runtime-resume-incremental-output-evidence-guard-20260425`
- worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260425-feature-runtime-resume-incremental-output-evidence-guard`

## Scope

Verify the followthrough fix for a canonical `develop` self-host replay seam where `resume` reused a prior Codex session/jsonl, produced no new manager continuity or exit contract, but runtime still accepted the cycle because old assistant output remained in the reused jsonl history.

## Findings

- `PASS`: `manager_cycle_has_effective_output_evidence()` no longer trusts whole-file historical Codex jsonl evidence for `resume` cycles. When `LAST_LAUNCH_KIND=resume` and a concrete `LAST_PROMPT_FILE` exists, runtime now requires effective output evidence whose jsonl event timestamp is at or after the current prompt file boundary.
- `PASS`: this closes the observed false-success seam in canonical `develop`: a reused `resume_target` can no longer let stale assistant output from an earlier cycle suppress `manager_empty_success_cycle_detected`.
- `PASS`: non-resume behavior remains intact; the existing empty-success repair path and missing-resume-evidence prompt narrowing regressions still pass after the change.

## Evidence

- `bash docs/system/workspace/scripts/tests/test-freely-manager-resume-cycle-does-not-reuse-stale-output-evidence`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-empty-success-cycle-does-not-autoresume`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-repair-missing-resume-evidence-preserves-repair-handoff`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-missing-continuity-autoresumes`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-repair-fresh-with-handoff-prompt-narrowing`
- `./bin/governance-check`

## Residual Risk

- This repair makes `resume` success evidence cycle-scoped for Codex by comparing jsonl event timestamps against the current prompt boundary. If a future tool adapter emits effective output without timestamped jsonl entries, it will need a parallel cycle-scoped evidence contract instead of inheriting the old whole-history heuristic.
