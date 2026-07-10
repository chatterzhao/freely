---
local_id: raw-20260621T150316Z16Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260621T130954Z-A
platform_ids:
  github:
    issue_id: '3239'
    url: https://github.com/chatterzhao/freely/issues/3239
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-21T15:03:36Z'
updated_at: '2026-06-21T15:03:36Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

# [RAW-20260621T150316Z] feat: wt-create should clone develop .freely state to test-pre-merge worktree

## 问题

`wt-create` 创建 test-pre-merge 工位时，只通过 `sync-tooling` 复制了 `.freely/config.toml` 和 `.githooks`，没有复制 `freely.db`、`.freely/run/` 等运行时状态。

导致 test-pre-merge 工位无法独立启动 daemon 进行端到端测试——这正是 test 工位的存在意义。

## 当前逻辑

`wt-create` 第 616 行：`sync-tooling --source-project <develop> --project <test-worktree>`

`sync-tooling` (freely L5473-5505) 只复制：
- `.freely/config.toml`（改写 PROJECT_ROOT/INTENT/CONSTITUTION 路径）
- `.githooks/`

不复制：
- `freely.db`（SQLite 运行时数据库）
- `.freely/run/`（运行时状态）
- `.freely/logs/`

## 已有隔离机制

各工位的 socket/DB 已通过路径 hash 隔离：
- A2A socket: `/tmp/freely-a2a-<sha256(project_path)>`
- DB socket: `/tmp/freely-db-<sha256(project_path)>`
- DB 路径: `<project>/.freely/freely.db`

不同工位因路径不同，hash 不同，天然隔离。

## 修复方案

`wt-create` 在创建 test-pre-merge 后，复制 develop 工位的 `.freely` 完整状态：
1. 复制 `.freely/freely.db`（包含 scan 数据、A2A 任务、会话等）
2. 复制 `.freely/config.toml`（已做，需保持）
3. 不复制 `.freely/run/`（socket、pid 等临时文件，daemon 启动时重建）
4. 不复制 `.freely/logs/`（测试工位应有自己的日志）

或者更简单：`cp -r <develop>/.freely <test-worktree>/.freely` 然后清理 run/ logs/ 下临时文件。

## 验证

1. `wt-create` 后，test 工位的 `.freely/freely.db` 与 develop 一致
2. test 工位能独立 `freely daemon start` 并正常运行
3. `wt-close` 时 test 工位连同其 `.freely` 一起丢弃，不污染 develop

🤖 Generated with [Claude Code](https://claude.com/claude-code)
Co-Authored-By: Claude <noreply@anthropic.com>
