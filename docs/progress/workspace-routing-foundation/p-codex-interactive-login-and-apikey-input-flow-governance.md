# Progress: codex-interactive-login-and-apikey-input-flow-governance

- issue_id: `I-20260406-1851-A`
- issue_path: `docs/epics/workspace-routing-foundation/codex-interactive-login-and-apikey-input-flow-governance/issues/codex-interactive-login-and-apikey-input-flow-governance.md`
- title: `Codex interactive login and API-key input flow governance`
- phase_state: `in_verification`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/codex-apikey-login-interactive`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-codex-apikey-login-interactive`
- updated_at: `2026-04-06`
- closure_status: `open`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- This execution lane absorbs the bounded `ai-cli` interactive login patch and the four issue-bound regressions from the pre-existing dirty worktree.
- The lane stays narrower than bundle/probe governance and separate from current-live bootstrap semantics.
- Promotion sequencing is bounded: merge this owner after `I-20260406-1829-A` has retired the old residual tree, but before `I-20260406-0901-A`, so the later reconnect lane only has to reconcile one `ai-cli` follow-on instead of two dirty side lanes.
- Focused verification still passes locally, but promotion is temporarily blocked by the current Codex sandbox because `.git/worktrees/...` is not writable in this session, so checkpoint commit / `test-pre-merge-*` creation / guarded merge cannot execute yet.

## Current Evidence

- `bash docs/system/workspace/scripts/tests/test-ai-cli-login-codex-interactive-mode-selection`
- `bash docs/system/workspace/scripts/tests/test-ai-cli-login-codex-apikey-interactive`
- `bash docs/system/workspace/scripts/tests/test-ai-cli-login-codex-apikey-direct-args`
- `bash docs/system/workspace/scripts/tests/test-ai-cli-login-codex-apikey-empty-input-fails`
- `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-codex-apikey-login-interactive --issue docs/epics/workspace-routing-foundation/codex-interactive-login-and-apikey-input-flow-governance/issues/codex-interactive-login-and-apikey-input-flow-governance.md`
- `./bin/governance-check`
- `git diff --check`
- `docs/epics/workspace-routing-foundation/codex-interactive-login-and-apikey-input-flow-governance/code-reviews/20260406-codex-interactive-login-and-apikey-input-flow-implementation-decision.md`

## Next Action

- Keep this owner queued behind `I-20260406-1829-A` for guarded promotion once a session with writable `.git/worktrees/...` is available, then merge it ahead of `I-20260406-0901-A` to minimize `ai-cli` conflict pressure on the reconnect lane.
- Once a session with writable `.git/worktrees/...` is available, materialize the feature checkpoint commit here and promote through a fresh `test-pre-merge-*` batch after `1829`.
