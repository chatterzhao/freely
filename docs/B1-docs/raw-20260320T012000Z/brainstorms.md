# 研究：主管型插话处理 agent

## Context

- 日期：2026-03-20 01:20 PDT
- 触发：上一版 `interruption direct-answer dispatcher` 证明了必须有独立 interruption control plane，但它对“后台 AI 进程在做什么”仍主要靠 runtime 规则识别，不符合“主管应自主判断自己回答还是委派”的目标。

## 主问题

需要回答：

1. 如何保证任意插话都被第一时间注意到。
2. 如何让“主管自己答 or 委派出去”主要由 AI 判断，而不是大量硬编码话术。
3. 如何避免长出第二个平权主管。

## 已形成的判断

### 1. 第一时间注意到仍应由独立 control plane 保证

这部分不能退回给主主管长循环。

正确结构仍是：

- raw intake durable 落盘
- interruption dispatcher 立即发现
- dispatcher 拉起主管型插话处理 agent

### 2. dispatcher 负责拉起，不负责理解

dispatcher 的职责应收窄为：

- watch intake
- claim 前置协调
- 调 handler
- 回写结果

不要再让 dispatcher 自己理解插话内容。

### 3. handler 应使用极小决策词典

AI 不是要在这里直接生成完整长期规划，而只是先判断 ownership。

当前最小可行词典：

- `manager_answer_ai_process_status`
- `delegate_general`

这不是穷举所有话术，而是穷举“主管是否直接回答”的所有权决策。

### 4. 主管直答的判断依据是职责，不是关键词

像“看看后台 AI 在做什么”之所以应由主管自己答，不是因为命中了“后台”或“AI”，而是因为它属于：

- manager-owned
- runtime visibility
- high-attention / low-business-value

所以 handler prompt 应强调：

- 根据主管职责判断
- 不要靠关键词表
- 不要扩 scope

### 5. 非主管直答的问题，先 claim 再 delegate

第一版不需要让 interruption manager agent 自己完成完整委派。

最小行为是：

- claim
- 标成 `delegate_general`
- 回到主主管或后续下游链

## 初步结论

- Freely 应从 “规则直答 dispatcher” 升级为 “dispatcher + manager-triage handler”。
- 第一版 handler 只做极小决策词典，不直接承担完整主线排班。
- 这样既避免硬编码穷举，也避免把 control plane 扩张成第二主管。
