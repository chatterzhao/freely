---
local_id: raw-20260708T202424Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260708T202424Z-A
platform_ids:
  github:
    issue_id: '3829'
    url: https://github.com/chatterzhao/freely/issues/3829
    synced_at: ''
  gitee:
    issue_id: IJZS0N
    url: https://gitee.com/zhaoquan/freely/issues/IJZS0N
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-08T20:24:45Z'
updated_at: '2026-07-08T20:24:45Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题

### 1. Bridge 全量启动浪费资源
Daemon 启动时为所有 agent-table 中的 tool（claude/opencode/cline）各开一个 ACP bridge。但 reviewer（cline）可能数小时无任务——bridge 空闲 180s 超时自杀，日志只写 "server stdout closed"，无明确原因。

### 2. 无任务时无休眠/关闭机制
未使用的 bridge 没有睡眠或优雅关闭机制。活跃 bridge 靠 60s ping 续命，但无 session 的 bridge 无 ping → 超时退出。

### 3. 无自动唤醒
Bridge 退出后没有自动重启机制。当 Manager 需要委派 Reviewer 时，对应的 bridge 已死，无法响应。

### 4. 日志不清晰
空闲退出不打印原因。应该打印：
- "no task for <slot>, idle 180s — shutting down, restart on next task"
- 或者先睡眠再被唤醒，而不是直接退出

## 修复

### 1. Lazy-start bridge
不预先全开 bridge。按需启动：
- Manager bridge (claude) — daemon 启动时开（Manager 总在工作）
- Worker bridge (opencode) — Manager 委派 worker 时才开
- Reviewer bridge (cline) — 有 review 任务时才开

### 2. 空闲休眠/优雅关闭
- Bridge 空闲 180s → 打印 `idle 180s, shutting down — will restart on next task` → 退出
- 或：空闲 180s → 打印 `idle, entering sleep` → 保留进程但释放资源 → 被 task 唤醒

### 3. 任务自动唤醒
- agent-working 表 + agent-table.toml pool 字段知道谁空闲、谁在哪个工位
- Manager 委派任务时检查 bridge 状态 → 如已死 → 自动重启 bridge → 再委派
- A2A task 提交时触发 bridge 唤醒

### 4. agent-table pool 利用
- Manager 委派前查 agent-table-query --next-free worker
- agent-working 记录每个 worker 的 session_id、worktree
- Worker/Reviewer 被唤醒时从 agent-working 读取自己的任务上下文

## 验收
- Daemon 启动后只启动 Manager bridge，不启动 Worker/Reviewer bridge
- Manager 委派 Worker 时自动启动 Worker bridge
- Bridge 空闲退出打印明确日志
- Bridge 退出后能被下一次委派自动唤醒
