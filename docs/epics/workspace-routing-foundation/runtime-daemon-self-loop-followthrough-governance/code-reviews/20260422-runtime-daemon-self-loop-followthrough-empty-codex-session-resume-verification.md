# Verification: runtime-daemon-self-loop-followthrough-governance empty Codex session resume followthrough

- issue_id: `I-20260421-1200-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- verification_date: `2026-04-22`
- verifier: `codex`
- source_branch: `feature/codex-empty-session-resume-fallback-20260422`
- protected_test_branch: `test-pre-merge-20260422-codex-empty-session-resume-fallback`

## Scope Verdict

- `PASS`: canonical `develop` replay disproved the assumption that "session file exists" was enough resume evidence for Codex; cleanup governance hit a persisted zero-byte rollout file and the next manager resume died with `thread/resume failed: empty session file`.
- `PASS`: `docs/system/workspace/scripts/runtime/freely` now treats Codex jsonl evidence as resumable only when the file is non-empty, so both persisted resume-target reuse and observed post-cycle session persistence fall back away from empty files.
- `PASS`: `recorded_worker_has_resume_evidence()` now uses the same Codex evidence gate, preventing zero-byte `LAST_TOOL_JSONL_PATH` state from falsely advertising resumable worker truth elsewhere in runtime governance.
- `PASS`: `docs/system/workspace/scripts/tests/test-freely-explicit-resume-target-contract` now covers zero-byte observed and persisted Codex rollout files while preserving the existing non-empty explicit-resume contract.
- `PASS`: protected replay on `test-pre-merge-20260422-codex-empty-session-resume-fallback` reran the same explicit-resume contract plus owner gates, so the develop-bound promotion evidence is fresh and staged under this owner instead of inferred from feature-local output only.
- `PASS`: this remains a same-owner continuation inside `I-20260421-1200-A`; no tool-switching policy, slot policy, or broader resume-model redesign is introduced.
- `PENDING`: canonical `develop` still needs protected absorption plus daemon replay proving cleanup governance skips the empty resume target, retires the retained blocker lane, and continues to another task.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-explicit-resume-target-contract`
2. `./bin/governance-check`
3. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-explicit-resume-target-contract`
4. `./bin/test-lane premerge-integration -- ./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260422-test-pre-merge-codex-empty-session-resume-fallback --issue docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
5. `./bin/test-lane premerge-integration -- ./bin/governance-check`

## Implementation Decision Note

- decision: `Reject zero-byte Codex rollout/session jsonl files as verified resume evidence.`
- why_this: `The failing canonical replay already had the right session id; the defect was that runtime trusted an empty persisted rollout file and therefore kept choosing resume when fresh/handoff fallback was the only truthful continuation. Tightening the evidence gate is the smallest repair.`
- alternatives_considered: `Delete empty files opportunistically; special-case the exact empty-session error after resume failure; widen the repair into a broader continuity redesign or tool-switch policy change.`
- boundary_non_goals: `No new session-format parser, no wider cleanup-governance rewrite, no tool/slot policy changes, and no claim that daemon success standard is met before canonical develop replay proves task completion, merge/retirement closeout, and next-task continuation.`
- residual_risk: `If future Codex failures produce non-empty but still unusable jsonl artifacts, canonical replay may surface another narrower evidence-validity seam that needs content-aware validation beyond the current non-empty gate.`
