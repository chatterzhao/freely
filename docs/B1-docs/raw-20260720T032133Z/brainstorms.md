- b1_id: B1-20260720T032133Z
- phase_state: completed
- source_raw: raw-20260720T032133Z
- produced_candidate: C-20260720T032133Z-A
- created_at: 2026-07-20

# B1_IBM: Manager prompt 委派 vs 插话决策规则

## Input
- Manager prompt L17091 只有"不可重复委派"，无替代动作指引
- Manager AI 不知已委派后该用 a2a_task.py prompt，而非 a2a-exit --state submitted
- 根因：语义控制缺失，非硬编码问题

## Problem
- Manager 每轮对同 raw_key 重复创建 submitted，而非在已有对话中追加 prompt
- agent_working 已有正确分配，但 Manager 不知如何利用
- a2a_task.py prompt 工具已定义（manager-agent.md L85），但 prompt 模板未引导使用

## Decision: 增强 prompt 模板
- 表格增加 task_id 列（查 a2a_tasks 获取）
- 替换"不可重复"为决策规则：已委派→prompt跟进 / 已失败→标记后重试 / 未委派→submitted
- 不改代码逻辑，纯 prompt 语义增强
