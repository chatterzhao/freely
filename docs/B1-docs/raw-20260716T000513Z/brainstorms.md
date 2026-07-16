---
b1_id: B1-20260716T000513Z
phase_state: completed
source_raw: raw-20260716T000513Z
created_at: 2026-07-16
---

# B1: agent_assign timing + worker verification contract

## Problem

### 问题 1: agent_assign 写入时机
agent_assign 只在 sync_project_tooling_from_source (line 6042) 调用，该函数仅在 wt-create tooling sync 时触发。Manager 通过 freely wt-create CLI 创建工位走不同路径，agent_assign 从未被调用。agent_working 表永远只有 __manager__。

应在 daemon 委派 worker 时调用 agent_assign：worker launch 路径检测到 submitted A2A task → 分配 worker → agent_assign 写入 → worker daemon 启动 → _resolve_current_agent_id 读到正确 role。

### 问题 2: Worker verification contract 缺失
Manager prompt 未说明委派时需写 worker-verification-contract.env。Worker daemon 启动时检查该文件（owner_issue/pre_tests_path/verification_artifact_dir），缺失则拒绝启动。

修复：在 worker launch 路径中，若 agent_assign 成功写入 agent_working，同时从 agent-table 和 milestones.md 自动推断 worker contract 所需字段。

## Decision

### Fix 1: agent_assign 调用位置
在 worker launch 函数（freely 脚本 line ~6030）中，agent_assign 调用从 sync_project_tooling_from_source 移到 worker_launch 入口处。确保在 worker daemon 启动之前写入。

### Fix 2: worker contract 自动推断
worker launch 时从 agent-table + milestones.md + 工位 B2 docs 自动推断 owner_issue/pre_tests_path/verification_artifact_dir。

## Candidate
C-20260716T000513Z-A promoted M-20260716T000513Z-A
