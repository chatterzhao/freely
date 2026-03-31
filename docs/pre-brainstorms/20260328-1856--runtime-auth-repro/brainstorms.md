# Brainstorms - 20260328-1856--runtime-auth-repro

## Context

- source_class: `discovery`
- originating_lane: `feature/runtime-auth-repro-20260328-185604`
- current canonical judgement:
  - this lane does not justify reopening the completed auth/bootstrap owner
  - this lane also does not fit the narrower `delegated continuation already injected` boundary of `C-20260323-1835-A`
  - the surviving signal is broader continuity/control-plane drift around `resume_streak_limit`, `fresh_with_handoff`, `context compacted`, transport failures, and stale state reconciliation after worker relaunch

## Convergence

- The original branch-local repro started from auth/runtime suspicion, but the later artifact chain widened:
  - repeated `resume -> ai_exit_rc_1`
  - `fresh_with_handoff rotation_reason=resume_streak_limit`
  - `context compacted`
  - websocket / remote-compaction failures
  - `live-status` vs persisted workcell-state mismatch after relaunch
- That combination is better treated as same-family supporting evidence for the already completed continuity/rotation control-plane contract, not as a new auth/bootstrap owner and not as a writeback into global restart semantics.
- Therefore the stale worktree should not continue dev-loop implementation. Its canonical closeout is `supporting_evidence_only`, after which the retained branch-local history becomes retirement-only provenance.

## Next

- Keep the branch-local artifact set as historical provenance only.
- Route the canonical closeout to `I-20260319-0018` as broader continuity/rotation supporting evidence.
- Retire `feature/runtime-auth-repro-20260328-185604` after cleanup confirms no additional owner scope survives outside this writeback.
