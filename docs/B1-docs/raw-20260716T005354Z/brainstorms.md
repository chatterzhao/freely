---
b1_id: B1-20260716T005354Z
phase_state: completed
source_raw: raw-20260716T005354Z
---
# B1: acp_session_register all roles + worker session tracking

## Problem
1. acp_session_register (line 4070-4078): worker/reviewer 分支直接 return 0，不写 agent_working。session 创建后 session_id 丢失。
2. agent_working.py 的 acp_session_connect 已实现跨 tool 检测 + session 注册，但 worker launch 未调用。

## Decision
Fix 1: acp_session_register 移除 return 0，对所有 role 调用 agent_assign 写入。从 worktree 的 exit contract 或上下文推断 raw_key。
Fix 2(后续): Worker launch 接入 acp_session_connect。

## Candidate: C-20260716T005354Z-A promoted M-20260716T005354Z-A
