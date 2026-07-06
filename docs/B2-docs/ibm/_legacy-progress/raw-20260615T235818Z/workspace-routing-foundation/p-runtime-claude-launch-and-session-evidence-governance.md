# Progress: runtime-claude-launch-and-session-evidence-governance

- issue_id: `I-20260419-2245-A`
- issue_path: `docs/B2-docs/runtime/runtime-claude-launch-and-session-evidence-governance/issues/runtime-claude-launch-and-session-evidence-governance.md`
- title: `Runtime Claude launch and session evidence governance`
- phase_state: `completed`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/fix-tool-switch-noninteractive-state-20260419-2315`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260419-2315-feature-fix-tool-switch-noninteractive-state`
- updated_at: `2026-04-19`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- Manual `say hi` replay proved the broken fallback was the Claude-family non-interactive launch syntax, not merely an unavailable upstream tool.
- The bounded implementation now feeds Claude-family print-mode prompts over stdin and only persists resume targets when verified project-local session evidence exists.
- Freely should manage only its own runtime-owned processes and evidence; unrelated manual tool launches remain outside this owner.
- Focused shell regressions and real CLI replays are already green in this feature lane.

## Verification Evidence

1. `bash docs/system/workspace/scripts/tests/test-tool-launchers-cc-stdin-add-dir`
2. `bash docs/system/workspace/scripts/tests/test-freely-claude-resume-target-requires-evidence`
3. `bash -n docs/system/workspace/scripts/runtime/tool-launchers.sh`
4. `bash -n docs/system/workspace/scripts/runtime/freely`
5. `printf 'say hi\n' | claude -p --permission-mode bypassPermissions --add-dir /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees`
6. runtime-equivalent fresh launcher replay returned `Hi.`
7. runtime-equivalent resume launcher replay with no verified evidence fell back to fresh execution and returned `hi`
8. `git diff --check`
9. `./bin/governance-check`
10. `docs/B2-docs/runtime/runtime-claude-launch-and-session-evidence-governance/code-reviews/20260419-runtime-claude-launch-and-session-evidence-verification.md`

## Current Batch Risks

1. This owner must stay narrow and not silently absorb the separate worker/supervisor self-heal truth defect seen in a later replay.
2. Claude CLI contract drift can recur later, so the truthful boundary here is launcher syntax plus session-evidence gating rather than tool-availability policy.
3. Guarded promotion still depends on the disposable premerge batch carrying the same owner evidence and focused regressions.

## Next Action

1. Run `./bin/governance-check` with the new owner chain in place.
2. Refresh the disposable `test-pre-merge-tool-switch-20260419-2359` batch with this owner evidence and rerun the focused regressions there.
3. Promote the batch into `develop`, then retire both temporary worktrees and branches.
