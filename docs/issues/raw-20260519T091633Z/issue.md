---
issue_id: raw-20260519T091633Z
kind: raw
priority: P1
phase_state: absorbed
absorbed_into: I-20260413-0420-A
source: feedback
created_at: '2026-05-19T09:16:33Z'
title: handoffs 积压≥5 时跳过 scan，优先处理积压
platform_ids:
  github:
    issue_id: '645'
    url: https://github.com/chatterzhao/freely/issues/645
    synced_at: '2026-05-19T09:16:42Z'
updated_at: '2026-05-30T05:39:25Z'
primary_platform: github
platform_state: closed
force_closed_at: '2026-05-19T09:24:45Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
---

## 设计

Manager 两个输入口: handoffs + scan。handoffs 积压时应优先处理,不在 prompt 里拼 scan。

### 规则

1. `append_manager_handoff_context_if_needed` 查出未消费 worker 数量
2. 数量 < 5 → 正常拼接 handoffs + scan
3. 数量 ≥ 5 → 只拼 handoffs，跳过 scan。提示"handoffs 积压 N 条，先处理积压"
4. 例外: task-mode 为 id:* → 始终拼 scan（用户明确指定）

### 为什么不是 1

Manager 可并发委派多个 worker,1 个 handoff 不构成积压。

## 涉及文件

- docs/system/workspace/scripts/runtime/freely — prompt 组装处
