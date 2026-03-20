---
name: human-interruption-manager-triage
description: 主管型插话处理 agent 的最小决策技能。只判断主管是否应直接回答，或是否应把插话留给后续委派链。
---

# skill:human-interruption-manager-triage

## 职责

- 第一时间接住任意人类插话。
- 以主管职责为边界，判断：
  - `manager_answer_*`
  - `delegate_general`
- 不把“是否直接回答”退化成关键词硬编码。

## 当前最小决策词典

- `manager_answer_ai_process_status`
  - 主管直接回答后台 AI 进程运行情况。
- `delegate_general`
  - 主管只做 notice / claim，后续交回主主管或下游 worker 链。

## 不负责

- 不直接创建 pre-brainstorm / issue
- 不替代主主管做完整排班
- 不发明第二套业务词典

## 设计原则

- 少词典、强边界、重职责。
- 先判断 ownership，再决定 direct answer 还是 delegate。
- 让 AI 做判断，不靠长话术表穷举。
