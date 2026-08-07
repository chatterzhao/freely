---
local_id: raw-20260701T045911Z11Z
kind: raw
- phase_state: dropped
absorbed_into: M-20260701T045911Z-A
platform_ids:
  github:
    issue_id: '3685'
    url: https://github.com/chatterzhao/freely/issues/3685
    synced_at: ''
  gitee:
    issue_id: IJY1C4
    url: https://gitee.com/zhaoquan/freely/issues/IJY1C4
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-01T04:59:48Z'
updated_at: '2026-07-01T04:59:48Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n
## 现状

agent-table.toml 定义了 reviewer，A2A SSE 已实现，freely-cycle 已能检测 input-required 并建议 dispatch_reviewer。但 reviewer 从未作为独立 agent 启动，也不在 workflow 每步介入。

## 已实现（部分或完整）
- agent-table.toml: 每个 agent 有 paired reviewer ✅
- agent-table-query --get-reviewer: 可查询 reviewer slot ✅
- A2A SSE: _notify_sse() + /tasks/{id}/stream 端点 ✅
- freely-cycle: 检测 input-required → 建议 dispatch_reviewer ✅
- pr-review-guarded: 已用 reviewer slot ✅

## 缺失
1. reviewer 不作为独立 ACP agent 启动 — 只是 pr-review-guarded 的 --reviewer flag
2. A2A task 只有 manager/worker 角色，没有 reviewer
3. workflow 10 个步骤，reviewer 只在 step 7 出现一次
4. SSE 推送了但 runtime 没用它做路由
5. input-required 没有分类路由（什么时候→reviewer，什么时候→manager）
6. freely-cycle 建议了 dispatch_reviewer 但没有代码执行
7. worker pool=10 只用 worker_01
8. reviewer slot 和 worker 是同一个 tool

## 修复方向
1. Reviewer 成为独立 agent — 有独立 ACP session，独立 slot
2. Workflow 每步设 input-required → SSE 推送 → runtime 路由到 reviewer
3. Reviewer 审查该步输出 → 给出 guidance → worker 继续下一步
4. 不同类型 input-required 路由到不同 agent
