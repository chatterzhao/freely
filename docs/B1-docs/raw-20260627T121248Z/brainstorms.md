---
b1_id: B1-20260627T121248Z
phase_state: completed
source_raw: raw-20260627T121248Z48Z
source_url: https://github.com/chatterzhao/freely/issues/3593
produced_candidate: C-20260627T121248Z-A
created_at: 2026-06-27
---

# B1_IBM: a2a_tasks worker_pid + a2a_server manager 修复

## Input
- 来源: raw-20260627T121248Z48Z (GitHub #3593)
- 症状: 
  1. --worker-pid 基础设施存在但 insert 时未传入
  2. a2a_server.py 仍硬编码 `agent_id == "manager"`

## Problem

WT2 (a2a-tasks) 已修复 worker 查询端（`LIKE 'worker_%'`），但：
1. `freely` insert 时未传 `--worker-pid`（`a2a_task.py set_worker_pid` 已实现但从未调用）
2. `a2a_server.py:415` 仍用 `agent_id == "manager"`（应为 `startswith("manager")`）

## Brainstorm

两处都是简单替换，唯一方案。

## Decision
直接修复。worker_pid 在 insert 后调用 `set_worker_pid`，manager 检查改为 `startswith`。

## Candidate
- candidate_id: C-20260627T121248Z-A
- status: promoted
- milestone: M-20260627T121248Z-A
