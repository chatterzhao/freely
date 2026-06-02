---
local_id: raw-20260518T000117Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260505T1210Z-A
platform_ids:
  github:
    issue_id: '534'
    url: https://github.com/chatterzhao/freely/issues/534
    synced_at: '2026-05-18T00:01:24Z'
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-18T00:01:17Z'
updated_at: '2026-06-02T16:45:06Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
priority: P1
source: chat-inbox
title: 消除 status 字段残留，统一为 platform_state + phase_state 双字段
completed_at: '2026-05-19T01:26:43Z'
---

## 背景

ibm-framework.md 设计的目标模型是 issue.md 只有两个状态字段：
- `platform_state` — open/closed（平台同步状态）
- `phase_state` — proposed/absorbed/dropped（治理生命周期）

`migrate-issue-phase-state` 做过一次迁移（`status` → `phase_state`），但不彻底。

## 数据现状

- 137/217 raw-* issues 仍有 `status` 字段（63%）
- 54 个 raw-* issue 同时有 `status` + `phase_state`（冗余）
- 14/229 I-* issues 仍有 `status` 字段

## 需要改动的位置

### 写入方（3处）

| 文件 | 行 | 当前 | 改为 |
|------|-----|------|------|
| `chat-inbox.py` | 202 | `status: proposed` | `phase_state: proposed` |
| `platform-adapter.py` | 361 | `"status": "proposed"` | 删除（362已有 phase_state） |
| `freely` cmd_feedback | 20076 | `status: open` | `phase_state: proposed` |

### 读取方（5处，均在 issue-sync）

| issue-sync 行 | 用途 | 改为读 phase_state |
|------|------|------|
| 236 | body 组装 | ✅ |
| 271 | labels 生成 | ✅ |
| 711 | batch closeout 判断 | ✅ |
| 768 | scan 显示 | ✅ |
| 790 | cmd_status 显示 | ✅ |

### 设计文档

| 文件 | 改动 |
|------|------|
| `ibm-framework.md` §291 | 移除 `status` 字段行 |

### 迁移脚本

二次运行 `migrate-issue-phase-state`，清理 137 个 raw-* 中的残留 `status` 字段。
I-* 的 14 个 `status` 一并处理。
