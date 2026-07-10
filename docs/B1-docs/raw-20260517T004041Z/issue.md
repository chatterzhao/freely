---
local_id: raw-20260517T004041Z41Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '382'
    url: https://github.com/chatterzhao/freely/issues/382
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-17T00:40:55Z'
updated_at: '2026-05-17T00:44:09Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
force_closed_at: '2026-05-17T00:44:09Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
---

## raw-20260517T004041Z41Z

| Field | Value |
|-------|-------|
| local_id | `raw-20260517T004041Z41Z` |
| kind | `raw` |
| status | `open` |
| phase | `none` |
| canonical | `none` |
| created | 2026-05-17T00:40:41Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260517T004041Z41Z`。实现前请用 `wt-create --raw-key 20260517T004041Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P2
status: open
source: chat-inbox
created_at: "2026-05-17T00:40:41Z"
title: "agent docs 缺少 freely feedback 工具和 raw issue 创建决策指南"

## 问题

Manager 和 Worker 的 agent 定义中完全没有 `freely feedback` 工具，也没有"何时创建新 raw issue"的决策指南。

当前 agent 只能处理已有 issue/scan 条目，无法将新发现的问题转化为可追踪的 raw issue。

## 需要补充

### Manager 工具列表

| 工具 | 用途 | 条件 |
|------|------|------|
| `freely feedback --title "..." --body "..."` | 创建新 raw issue | 发现 bug、识别改进机会、需要追踪的新任务 |

### Manager 决策指南

下列情况应创建新 raw issue（而非在现有 issue 里顺手修）：
- 发现 bug 或运行时异常（如 worker 反复 launch_blocked）
- 扫描/巡逻中发现新的模式性问题需要独立追踪
- Worker 汇报的问题超出了当前工位范围，需要独立开工位
- 任何需要独立工位的改动 → `freely feedback` + `wt-create`

### Worker 决策指南

- 执行 Task 时发现不相关的 bug → 创建 raw issue 记录，不中断当前任务
- 任务依赖的前置条件不满足 → 报告给 Manager（worker_handoff_needed），Manager 决定是否创建 raw issue
- **不要**把发现的问题顺手修了——那是另一个 raw issue 的范围

## 范围

- `docs/system/workspace/agents/manager-agent.md`：工具列表 + 决策指南
- `docs/system/workspace/agents/worker-agent.md`：工具列表 + 决策指南
