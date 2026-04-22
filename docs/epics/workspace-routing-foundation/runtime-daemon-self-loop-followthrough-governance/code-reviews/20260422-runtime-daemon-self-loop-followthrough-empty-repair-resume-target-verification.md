# Verification: runtime-daemon-self-loop-followthrough-governance empty repair resume target

- issue_id: `I-20260421-1200-A`
- date: `2026-04-22`
- scope: `Prevent manager/worker exit-contract repair relaunches from forcing Codex resume when the resolved resume target is empty or lacks verified rollout evidence.`

## Findings

- `FAIL`: canonical `develop` replay after the zero-byte session evidence fix still selected `launch_kind=resume` during `manager_exit_contract_repair` even though `.freely/run/session-state.env` recorded `LAST_TOOL_RESUME_TARGET=""`, `LAST_TOOL_SESSION_ID=""`, and `LAST_LAUNCH_KIND="resume"`.
- `FAIL`: monitor preflight correctly rejected that launch with `[ERROR] codex resume requires --tool-resume-target`, proving the remaining blocker was launch-kind selection rather than Codex session-file verification.
- `PASS`: repair relaunches now stay on `resume` only when `tool_runtime_resume_target_before_launch` resolves a non-empty target and `tool_has_resume_evidence` confirms verified rollout evidence for the active tool.
- `PASS`: when repair continuity exists but Codex resume evidence is empty, launch selection now downgrades to `fresh_with_handoff` with `missing_resume_evidence`, preserving bounded same-owner recovery without sending an empty resume target into monitor preflight.

## Evidence

- `bash docs/system/workspace/scripts/tests/test-freely-manager-repair-handoff-avoids-initial-start`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-repair-handoff-missing-resume-evidence-falls-back`
- `bash docs/system/workspace/scripts/tests/test-freely-explicit-resume-target-contract`
- `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-codex-args`

## Status

- `PASS`: bounded feature-lane regression coverage now distinguishes verified repair resumes from empty-target repair fallbacks.
- `PENDING`: guarded premerge + canonical `develop` replay still need to prove this owner reaches retained cleanup closeout, retires the temporary blocker lane, and continues to the next task.
