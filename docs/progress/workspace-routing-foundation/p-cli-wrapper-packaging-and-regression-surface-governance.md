# Progress: cli-wrapper-packaging-and-regression-surface-governance

- issue_id: `I-20260405-2358-C`
- issue_path: `docs/epics/workspace-routing-foundation/cli-wrapper-packaging-and-regression-surface-governance/issues/cli-wrapper-packaging-and-regression-surface-governance.md`
- title: `CLI wrapper packaging and regression-surface governance`
- phase_state: `in_verification`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/cli-command-audit-20260406-0015`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260406-0015-feature-cli-command-audit`
- updated_at: `2026-04-06`
- closure_status: `open`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- Full `bin/` command audit proved a bounded packaging/regression layer is still broken even when the underlying features exist.
- This owner is addressing the highest-leverage subset first: runnable wrapper executable bits, `freely ai --help` shell noise, and worktree-sensitive auth-change wake regression coverage.
- Project-target bootstrap/status drift and runtime control-plane instability remain explicitly out of scope for this lane.
- The current lane has already repaired the audited executable-bit gaps, cleaned the `ai --help` surface, and stabilized auth-change wake regression coverage with focused verification written to the issue-bound review artifact.

## Active Plan

1. Prepare the lane for guarded merge with current verification evidence.
2. Keep project-target bootstrap/status drift and runtime control-plane findings parked for their own follow-on owners.
