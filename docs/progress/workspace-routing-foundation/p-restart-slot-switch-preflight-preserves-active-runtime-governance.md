# Progress: restart-slot-switch-preflight-preserves-active-runtime-governance

- issue_id: `I-20260405-2055-A`
- issue_path: `docs/epics/workspace-routing-foundation/restart-slot-switch-preflight-preserves-active-runtime-governance/issues/restart-slot-switch-preflight-preserves-active-runtime-governance.md`
- title: `Restart slot-switch preflight preserves active runtime governance`
- phase_state: `in_verification`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/restart-slot-switch-preflight-20260405-0605`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260405-0605-feature-restart-slot-switch-preflight`
- updated_at: `2026-04-05`
- closure_status: `verification_in_progress`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- Materialized a new follow-on owner instead of reopening the completed startup-lock or project-command owners.
- `runtime/freely` now preflights shared codex slot-switch readiness before restart stops the current project runtime.
- The lane also hardens restart-adjacent helper behavior required to keep that preserved-runtime contract truthful under supervision churn.
- Focused runtime regressions and governance checks have passed in the feature worktree; guarded pre-merge integration is still pending.

## Evidence So Far

1. `bash -n docs/system/workspace/scripts/runtime/freely`
2. `bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
3. `bash docs/system/workspace/scripts/tests/test-freely-restart-preserves-runtime-on-active-slot-switch-lock`
4. `bash docs/system/workspace/scripts/tests/test-freely-session-rotation`
5. `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch-serialization`
6. `bash docs/system/workspace/scripts/tests/test-ai-cli-login-triggers-auth-change-wake`
7. `bash docs/system/workspace/scripts/tests/test-ai-cli-login-does-not-block-on-auth-change-wake`
8. `bash docs/system/workspace/scripts/tests/test-freely-checkpoint-governance`
9. `bash docs/system/workspace/scripts/tests/test-freely-checkpoint-drift-escalation`
10. `bash docs/system/workspace/scripts/tests/test-freely-codex-current-slot-does-not-capture-switch-warning`
11. `git diff --check`
12. `./bin/governance-check`

## Next Action

- Commit this feature lane with the new owner documents and focused runtime/test changes.
- Create a fresh `test-pre-merge-*` worktree from current `develop`, merge this feature into it, and replay the verification subset there before guarded merge to `develop`.
