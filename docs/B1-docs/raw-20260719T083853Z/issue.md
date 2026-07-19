---
local_id: raw-20260719T083853Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260719T083853Z-A
platform_ids:
  github:
    issue_id: '4008'
    url: https://github.com/chatterzhao/freely/issues/4008
    synced_at: ''
  gitee:
    issue_id: IK21C3
    url: https://gitee.com/zhaoquan/freely/issues/IK21C3
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-19T08:39:16Z'
updated_at: '2026-07-19T08:42:27Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 根因

A2A task 创建时无应用层校验。a2a_tasks 表所有字段都是 NOT NULL 但 SQLite 不视空字符串为 NULL——worktree='' branch='' raw_key='' 全部通过。agent_working.worker_id 干脆是 nullable=True。

证据: Round 094 worker task 36fa73f1 — worktree='' branch='' raw_key='' agent_id='worker' state='input-required'

## 修复

### 应用层校验 (a2a_task.py a2a-exit handler)
1. role=worker 时 worktree/branch/raw_key 必须非空字符串 → 空则报错返回
2. 新建 task 时 state 必须为 submitted（不能是 input-required/working/completed）
3. agent_id 格式校验: worker 类 task 的 agent_id 应匹配 worker_NN 格式

### agent_working 校验 (agent_working.py agent_assign)
4. worker role 时 worker_id 必须非空且格式正确
5. DB schema: agent_working.worker_id → NOT NULL

### prompt 模板 (freely)
6. 模板含完整参数 + 应用层校验兜底（双重保障）

## 影响

Worker task 以空 worktree 创建 → Runtime worker deferred → 静默失败无报错。校验后直接拒绝 → 错误立即暴露
