# Progress: runtime-startup-authority-and-readiness-governance

- issue_id: `I-20260413-0420-A`
- issue_path: `docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/issues/runtime-startup-authority-and-readiness-governance.md`
- title: `Runtime startup authority and readiness governance`
- phase_state: `completed`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/runtime-startup-authority-and-readiness-governance-20260413`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260413-feature-runtime-startup-authority-and-readiness-governance`
- updated_at: `2026-04-13`
- closure_status: `implemented-and-verified`

## Summary

This owner replaces PID/argv startup authority with runtime-published supervisor truth:

- supervisor identity is now published under project run state and reused as the authoritative startup surface
- same-project startup keeps the lock until startup truth is written
- daemon ready no longer trusts fake supervisor hints
- stop cleanup and stop-marker preservation now align with authoritative supervisor truth

## Implementation

- added supervisor identity truth files under `.freely/run/supervisor-identities`
- changed supervisor validation and supervisor lookup to require published startup truth
- delayed start-lock release until `supervisor_started`, `workcell_state`, and identity truth are all published
- tightened daemon ready semantics to require startup truth for the current launch
- updated stop cleanup and focused regressions to the new authority contract

## Verification Evidence

- `bash docs/system/workspace/scripts/tests/test-freely-fake-supervisor-argv-does-not-validate`
- `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-ignores-fake-supervisor-argv`
- `bash docs/system/workspace/scripts/tests/test-freely-start-serializes-same-project-concurrent-starts`
- `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
- `bash docs/system/workspace/scripts/tests/test-freely-stop-terminates-all-same-project-supervisors`
- `bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
- `./bin/governance-check`
- `git diff --check`
- `docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/code-reviews/20260413-runtime-startup-authority-and-readiness-closeout-verification.md`

## Next Action

`completed`
