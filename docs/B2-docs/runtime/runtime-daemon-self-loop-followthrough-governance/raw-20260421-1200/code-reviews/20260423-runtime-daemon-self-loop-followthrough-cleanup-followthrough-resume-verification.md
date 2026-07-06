# Verification: runtime-daemon-self-loop-followthrough-governance cleanup followthrough resume

- issue_id: `I-20260421-1200-A`
- date: `2026-04-23`
- scope: `Force manager exit-contract resume_manager replay to execute cleanup followthrough before relaunch, and materialize an exact blocker when that cleanup step fails.`

## Findings

- `FAIL`: canonical `develop` replay still entered `cleanup_governance`, but `manager_runtime_handle_exit_contract_after_ai_cycle()` could take `EXIT_KIND=resume_manager` and relaunch manager without first running the already-selected cleanup followthrough, so the retained merged lane stayed pinned and the daemon loop did not advance.
- `FAIL`: when cleanup followthrough failed on that resume path, runtime fell back to generic invalid-resume handling without preserving cleanup-followthrough failure as the exact blocker truth.
- `PASS`: the resume-manager branch now checks continuity for cleanup-followthrough intent, runs `run_cleanup_followthrough` before relaunch, and emits explicit begin/success receipts so manager replay cannot silently skip retained-lane closeout.
- `PASS`: cleanup-followthrough failure on that path now writes manager repair handoff truth, records `LAST_EXIT_REASON=manager_exit_contract_cleanup_followthrough_failed`, emits `manager_exit_contract_cleanup_followthrough_failed`, and returns `resume_invalid`.

## Evidence

- `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-resume-triggers-cleanup-followthrough`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-cleanup-followthrough-failure-materializes-blocker`

## Status

- `PASS`: focused feature-lane regressions prove resume-manager replay now consumes cleanup-followthrough intent before relaunch and fails closed with exact blocker truth when that closeout step breaks.
- `PENDING`: guarded premerge plus canonical `develop` daemon replay still must prove this repair clears the retained cleanup lane and lets Freely continue toward the next task instead of staying pinned in cleanup governance.

## Implementation Decision Note

- decision: `Treat cleanup-followthrough intent as higher priority than manager relaunch whenever exit-contract replay resolves to resume_manager.`
- why_this: `The failing replay was not a general resume-target problem anymore. Runtime already had a concrete cleanup-governance continuation selected, but the exit-contract branch could bypass that work and re-enter manager patrol, recreating the same retained-lane loop. Running cleanup first is the smallest truthful repair.`
- alternatives_considered: `Keep relaunch-first behavior and rely on another patrol round to notice cleanup again; widen the fix into a generic continuity-priority refactor; allow cleanup-followthrough failure to collapse into opaque resume_invalid without exact blocker evidence.`
- boundary_non_goals: `No redesign of continuation ranking, no broad cleanup-governance rewrite, no retirement policy expansion beyond the active retained-lane replay seam, and no claim that canonical develop success-standard acceptance is complete before the next protected replay proves it.`
- residual_risk: `If canonical replay surfaces another retained-lane blocker after cleanup followthrough begins, the daemon loop may still stop for a narrower reason, but it should now stop with exact cleanup-followthrough blocker evidence instead of silently relaunching manager.`
