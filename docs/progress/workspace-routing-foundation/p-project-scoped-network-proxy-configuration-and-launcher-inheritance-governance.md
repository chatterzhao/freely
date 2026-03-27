# Progress: project-scoped-network-proxy-configuration-and-launcher-inheritance-governance

- issue_id: `I-20260327-0651`
- title: Project-scoped network proxy configuration and launcher inheritance governance
- phase_state: `in_verification`
- runtime_state: `stopped`
- branch: `feature/network-proxy-config-capability-restack`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-network-proxy-config-capability-restack`
- issue_path: `docs/epics/workspace-routing-foundation/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance/issues/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "dev-loop-initial-slice"}

## Summary

- 2026-03-27 这条 proxy lane 已从 pre-brainstorm candidate `C-20260327-0651-B` materialize 成 issue-bound IBM / dev-loop 承接面。
- 当前目标是把 proxy 从 runtime hardcode 迁移到 `.freely/config.env`，并让同一个 resolver 同时服务 codex exec launcher 与 watchdog 的 OAuth/curl path。
- 目前实现已补齐 project-scoped resolver、launcher inheritance、watchdog OAuth inheritance，并移除了 localhost proxy fallback。
- 当前收口点是把无参 `freely ai switch codex` 固定为“先刷新保存的 auth inventory，再决定是否切换 usable slot”，并用 machine-readable `pre-tests.md` + verification artifact 收到可关闭状态。
- 当前这棵树已经完成 focused regression 与 governance-check，下一步是合入 `develop`、写回 completed evidence，并退休旧 proxy worktree 与 restack worktree。
