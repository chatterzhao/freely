---
local_id: raw-20260626T121349Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3549'
    url: https://github.com/chatterzhao/freely/issues/3549
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-26T12:14:09Z'
updated_at: '2026-06-26T12:15:53Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260626T121349Z-A
source_candidate: docs/pre-brainstorms/20260626T121349Z--consistency-cleanup/candidates.md#C-20260626T121349Z-A
---

## 背景

近期多 agent 架构重构（agent-table.toml、AGENT_AI_TOOL、agent-id.env、reviewer-agent）后，多处文档、代码引用、传输方式未同步更新。

## 4 个子问题

### 1. agent-table-query help 文本混入旧格式

`bin/agent-table-query` 的 help 文本同时展示 `[[agents]]`（当前）和 `[[agent_pools]]`（旧，用 `count` 而非 `pool`）。应只保留 `[[agents]]` 格式与 agent-table.toml 一致。

### 2. test-pre-merge 文档描述过时

相关文档仍描述 test-pre-merge 为"禁止 add/commit/push"。实际门禁已改为：
- 允许：add, commit（reviewer 需要 commit 后 diff 比较）
- 禁止：push, merge 到其他分支

### 3. .freely/ 全局文件路径审计

`agent-id.env`、`agent-table.toml` 等全局文件在 develop 工位的 `.freely/` 下。工位的 `.freely/` 是 wt-create 克隆的快照，不含 agent-id.env。需审计所有读写这些文件的位置，确保走 develop 工位路径而非 `PROJECT_ROOT`（工位自身）。

### 4. fix-execution skill 传输方式

test-pre-merge 测完后代码传输应使用 cherry-pick（reviewer 需要 commit 历史做 diff），不再用 cp 或 git stash。需更新 `freely-fix-execution/SKILL.md`。
