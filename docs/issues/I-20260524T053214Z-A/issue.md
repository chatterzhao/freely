---
local_id: I-20260524T053214Z-A
kind: linked
status: completed
phase_state: completed
promoted_from: raw-20260524T053214Z
source_candidate: docs/pre-brainstorms/20260524T053214Z--acp-tool-switch-integration/candidates.md
canonical_issue_path: ''
platform_ids:
  github:
    issue_id: '2586'
    url: https://github.com/chatterzhao/freely/issues/2586
    synced_at: '2026-06-13T10:42:11Z'
primary_platform: github
last_synced_comment_at: {}
hash: ''
created_at: 2026-05-24 05:32:14+00:00
updated_at: '2026-06-13T10:42:11Z'
intake_id: ''
author: zhaoquan
channel: freely-fix-execution
session_refs: []
pre_tests_path: docs/issues/raw-20260524T053214Z/pre-tests.md
verification_artifact_dir: docs/epics/acp-tool-switch-integration/code-reviews
milestone: M-20260524T053214Z-A
milestone_state: committed
platform_state: open
---

# I-20260524T053214Z-A: ACP session 生命周期接入 tool_switch_events

- source_candidate: `docs/pre-brainstorms/20260524T053214Z--acp-tool-switch-integration/candidates.md`
- pre_tests_path: `docs/issues/raw-20260524T053214Z/pre-tests.md`
- verification_artifact_dir: `docs/epics/acp-tool-switch-integration/code-reviews`

## 问题

`tool_switch_events` 已实现但 ACP 路径未集成，导致 Freely 运行时在 bridge 重启后进入 session 死锁。

## 实现

4 个集成断点修复（commit `4c146655`）：

1. `freely:select_launch_kind()` ACP 路径 — 在 `get-active` 前调 `_tool_switch_launch_kind()`，cross_tool → fresh
2. `monitor-ai-acp.sh` — `_persist_session_to_store()` 后回写 `new_session_id` 到 `tool_switch_events`
3. `monitor-ai-acp.sh:_detect_acp_failure()` — 同时 grep bridge log + 匹配 `Internal error`
4. `freely:_acp_bridge_has_fatal_error()` — 匹配 `Session not found`
5. `run-acp-prompt.py` prompt 模式 — `session/prompt` 失败 → fallback `session/new`
6. `session-store.py` — DB 写入前必填字段校验

## 验收

见 `pre_tests_path` 中 5 项集成验收测试。
