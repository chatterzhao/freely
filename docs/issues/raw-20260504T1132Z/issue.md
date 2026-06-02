---
local_id: raw-20260504T1132Z
issue_title: raw key 格式规范重构：统一为 YYYYMMDDTHHMMZ 分钟精度
kind: raw
phase_state: absorbed
absorbed_into: I-20260504T1132Z-A
platform_ids:
  github:
    issue_id: '203'
    url: https://github.com/chatterzhao/freely/issues/203
primary_platform: github
created_at: '2026-05-04T11:32:00Z'
updated_at: '2026-06-02T17:03:44Z'
intake_id: 20260504T1132Z-raw-key-format
author: human
channel: github
session_refs: []
platform_state: closed
---

## 问题

当前三套 raw key 命名并存，互相不兼容：

- GitHub: `RAW-20260504T1145Z` (ISO 8601, T/Z 分隔)
- 本地: `raw-20260503-0200` (YYYYMMDD-HHMM)
- chat DB: `20260503105742` (14 位秒精度)

## 影响

pre-push.sh、wt-create、task-lifecycle-scan.py 中的 regex 只认本地格式。GitHub 格式的分支被 pre-push hook 拒绝。

## 目标

统一为 `YYYYMMDDTHHMMZ` 格式（ISO 8601 紧凑型，分钟精度），与 GitHub issue-sync 格式一致。

## 约束

- 历史数据保持原格式不动
- 代码同时兼容新旧两种格式
- 新创建的 raw/I-*/branch/pre-brainstorm 使用新格式
