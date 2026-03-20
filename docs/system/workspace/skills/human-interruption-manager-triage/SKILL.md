---
name: human-interruption-manager-triage
description: 主管型插话处理 agent 的最小 routing 技能。基于主管职责，判断这条 signal 该由主管先回答，还是应委派到后续处理链。
---

# skill:human-interruption-manager-triage

## 职责

- 第一时间接住任意人类插话。
- 以主管职责为边界，判断：
  - 主管是否应先给出必要澄清或监督面回答
  - 还是应委派给后续 worker / runtime 处理链
- 明确这条 signal 应从哪个 restart point 重新开始。
- 产出最小 routing 决策，而不是发明很多问题类型。

## 最小输出契约

- `DECISION=answer|delegate`
- `REACTION=<followup|steer|collect|interrupt|noise>`
- `CLASSIFICATION=<control|discovery|continuation|noise>`
- `RESTART_POINT=<pre_brainstorm|candidate|milestone|ibm|dev|review|verification|continuation|runtime|cleanup>`
- `OWNERSHIP=<manager|worker|runtime>`
- `WHY=<单行原因>`
- `HANDOFF=<若 delegate，则给出单行交接摘要>`
- `ANSWER=<若 answer，则给出单行回答摘要>`

这些字段是 routing 契约，不是问题类型词典。

## 不负责

- 不直接创建 pre-brainstorm / issue
- 不替代主主管做完整排班
- 不发明第二套业务词典
- 不把 runtime 实现细节写成硬编码规则表

## 设计原则

- 少枚举、强边界、重职责。
- 先判断这件事是否能由主管职责闭环；若不能，再判断最合适的 restart point。
- 让 AI 做判断，不靠长话术表穷举。
- 示例可以帮助理解边界，但示例不是 if/else 规则。

## 示例

- 主管监督面事实查询：
  - 例如“后台 AI 进程现在在做什么”
  - 通常可 `answer`
  - 常见输出是 `CLASSIFICATION=control`、`OWNERSHIP=manager`、`RESTART_POINT=continuation` 或 `runtime`
- 需要实际分析、执行、清理、收口的任务：
  - 例如“检查已经合并到 develop 的 worktree，应该怎么收口”
  - 通常应 `delegate`
  - 常见输出是 `CLASSIFICATION=control`、`OWNERSHIP=worker`、`RESTART_POINT=cleanup`

示例只用于说明主管职责边界，不代表固定类型表。
