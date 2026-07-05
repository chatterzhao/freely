---
local_id: raw-20260630T002621Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260630T002621Z-A
platform_ids:
  github:
    issue_id: '3638'
    url: https://github.com/chatterzhao/freely/issues/3638
    synced_at: ''
  gitee:
    issue_id: IJXOUY
    url: https://gitee.com/zhaoquan/freely/issues/IJXOUY
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-30T00:26:41Z'
updated_at: '2026-06-30T00:26:41Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 背景

当前 Manager-Worker 模式是收件人模式：Manager 发 task → Worker 跑全流程 → Manager 收 handoff。Worker 中间过程（B1、B2、RED、dev、GREEN）Manager 完全不可见。导致糊弄——actual_RED_output 全填 "code written before RED"，Manager 不知道。

对标 Agent Conveyor 的 cycle 模式：Manager 每轮读 Worker 的 JSONL rollout，持续旁观。发现异常立即 nudge。

## 目标

1. Manager 能轮询 Worker ACP session 的最新 transcript
2. 识别 Worker 当前所处阶段（B1/B2/RED/dev/GREEN/PR）
3. 每阶段关键节点检查产出质量（尤其 RED 的 actual_RED_output）
4. 发现异常时 mid-workflow 介入（a2a prompt nudge / 中断）
5. 支持多 Worker 并发监督

## 验收

- Manager 能看到 Worker 当前阶段和最近产出
- RED 阶段若 actual_RED_output 含占位符模式，Manager 收到 warning
- Manager 能通过 a2a prompt 向 Worker 发送中途纠正指令
- 支持多 Worker 并发监督
