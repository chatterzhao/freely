# Progress: project-scoped-network-proxy-configuration-and-launcher-inheritance-governance

- issue_id: `I-20260327-0651`
- title: Project-scoped network proxy configuration and launcher inheritance governance
- phase_state: `completed`
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
- 当前这棵树已经完成 focused regression、governance-check 与 feature-lane verification artifact，issue 已达到 completed closeout 边界；下一步是把这条 lane replay 到 `develop`，然后退休旧 proxy 工位、restack 工位和临时 test-pre-merge 批次。

## 2026-03-27 Missing Config Inherit Followthrough

- A later `test-freely-session-rotation` replay exposed a same-family proxy resolver edge:
  - when `HOME` points at an isolated directory without `~/.freely/config.env`
  - resolver reads for missing project/global config returned empty input under `set -e`
  - codex launcher then exited before emitting `session id` / jsonl evidence, which degraded the intended `context_usage_threshold` path into `missing_resume_evidence`
- Repair judgement:
  - this stays inside `I-20260327-0651`, because resolver mode `inherit` is supposed to tolerate absent config files and preserve ambient env
  - the minimal fix is to treat missing config reads as empty inherited values instead of hard failures
- Verification:
  - `bash docs/system/workspace/scripts/tests/test-freely-network-proxy-resolver`
  - `bash docs/system/workspace/scripts/tests/test-freely-network-proxy-launcher-inheritance`
  - `bash docs/system/workspace/scripts/tests/test-freely-session-rotation`
