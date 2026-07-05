---
local_id: raw-20260621T092609Z09Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260621T092609Z-A
platform_ids:
  github:
    issue_id: '3211'
    url: https://github.com/chatterzhao/freely/issues/3211
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-21T09:26:26Z'
updated_at: '2026-06-21T09:26:26Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

`freely daemon stop` 和异常崩溃后，所有 worker 的 A2A task 停留在 `working`/`submitted` 状态。下次启动时 Manager 把它们全部标 `failed`，丢失所有进行中的工作。

## 各场景存活状态分析

| 场景 | A2A task (DB) | session-state.env | JSONL | worktree | ACP bridge |
|------|--------------|-------------------|-------|----------|------------|
| 正常 stop | ✅ 保留 | ❌ 删除 (L20161) | ✅ 保留 | ✅ 保留 | ❌ 清理 |
| 崩溃/断电 | ✅ 保留 | ✅ 保留 | ✅ 保留 | ✅ 保留 | ⚠️ 残留文件 |
| 网络超时 | ✅ 保留 | ✅ 保留 | ✅ 保留 | ✅ 保留 | ✅ 活着 |

A2A server 启动时 `_restore_tasks()` (a2a_server.py L338) 会加载所有非终止状态的任务到内存。但 worker 进程不会自动重启——它们变成僵尸。

## 当前 stop 流程的问题

`stop_project_runtime` (L20005) 只做：
1. 写 stop marker
2. SIGTERM → SIGKILL 各进程
3. 删 session-state.env —— **对于非 restart 原因**

**没有更新 A2A task 状态**。worker 停留在 `working`，Manager 下次看到不知道它是"被停了"还是"真死了"。

## 正确设计：基于 A2A `input-required` 的暂停/恢复

A2A 规范中 `input-required` 是 interrupted 状态（非 terminal），语义是 "paused, awaiting external input"。daemon stop 就是外部暂停。

### 停止时

```
daemon stop / 崩溃前:
  ① working → input-required (reason="daemon_stopped" 或 "crash_detected")
  ② submitted 保持不变（下轮自然消费）
  ③ 保留 session-state.env + JSONL（不再删除）
```

### 启动时恢复决策树

```
对每个 input-required / working / submitted 的 worker:

① worktree 还在吗？
  NO → failed（工位被手动删除，无法恢复）
  YES ↓

② ACP session 还连着吗？
  YES → session/prompt "继续工作"
  NO ↓

③ JSONL + session-state.env 完好？
  YES + 同工具 → resume（恢复完整对话上下文）
  YES + 跨工具 → fork（JSONL 格式不兼容）
  NO ↓

④ fork + handoff（新 session，prompt 携带前 worker 上下文）
```

## 关键改动点

1. **`stop_project_runtime`** (L20005): 停止前更新所有 `working` worker → `input-required (reason=daemon_stopped)`
2. **`_restore_tasks`** (a2a_server.py L338): 恢复时检查 worker_pid 是否存活，死掉的标 `input-required`
3. **Manager startup**: 不在 patrol 中直接标 `failed`，而是按决策树恢复：session/prompt → resume → fork → 最后才 failed
4. **session-state.env**: 不再删除（包括非 restart 场景），crash 检测通过时间戳判断
