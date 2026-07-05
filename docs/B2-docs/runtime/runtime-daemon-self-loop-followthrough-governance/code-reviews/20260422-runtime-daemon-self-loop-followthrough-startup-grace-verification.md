# Verification: runtime-daemon-self-loop-followthrough-governance startup grace followthrough

- issue_id: `I-20260421-1200-A`
- issue_path: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- verification_date: `2026-04-22`
- verifier: `codex`
- source_branch: `feature/manager-bootstrap-prompt-build-grace-20260422`
- protected_test_branch: `test-pre-merge-20260422-manager-bootstrap-prompt-build-grace`

## Scope Verdict

- `PASS`: canonical `develop` replay after the benign Codex timeout fix no longer collapsed into `tool_runtime_failure`, but it still exposed a narrower control-plane seam: `ensure-manager` could restart a daemon-owned manager before `ai_launch_begin` if startup stayed between `L010 supervisor_started` and `L020 prompt_build_begin` longer than the initial bootstrap grace.
- `PASS`: `supervisor_startup_lifecycle_in_flight()` now treats `L010` as startup-in-flight evidence, so a newly started manager remains protected while pre-prompt worker recovery, fleet inspection, or other bounded startup work is still underway.
- `PASS`: `docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-during-pre-prompt-startup` proves `ensure-manager` no longer relaunches a running/starting supervisor just because `LAST_STATE_UPDATED_AT` is old while the lifecycle trace still shows fresh `L010` startup truth.
- `PASS`: the existing prompt-build grace regression still passes, so the broader startup-lifecycle guard now covers both sides of the same bounded launch window instead of regressing the already-protected `L020` to `L022` segment.
- `PENDING`: canonical `develop` still needs another daemon replay proving Freely can autonomously pick a task, complete it, merge upward, retire the temporary lane, and move on to the next task without another runtime repair.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-during-pre-prompt-startup`
2. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-during-prompt-build`
3. `bash -n docs/system/workspace/scripts/runtime/freely`
4. `./bin/governance-check`

## Implementation Decision Note

- decision: `Extend startup-lifecycle keepalive protection to begin at L010 supervisor_started, not only after prompt build has already begun.`
- why_this: `The failing develop replay showed the manager was doing legitimate startup work before prompt build, so increasing a blind time-based grace or adding broader retries would hide the real state signal. The lifecycle trace already records L010; consuming that truth is the smallest repair.`
- alternatives_considered: `Increase FREELY_MANAGER_BOOTSTRAP_AI_GRACE_SECS globally; treat every supervisor without ai.pid as launch-in-flight for a long fixed timeout; bypass idle-supervisor restart entirely during daemon bootstrap.`
- boundary_non_goals: `No tool/slot policy changes, no broadened recovery redesign, no new task-selection behavior, and no claim that canonical self-host acceptance is complete before develop replay proves one full autonomous task/merge/retirement/next-task cycle.`
- residual_risk: `If another pre-ai startup stage appears before L010 or outside the existing lifecycle checkpoints, canonical replay may still expose a different bounded keepalive seam that needs its own explicit trace-based guard.`
