# 研究：高注意力直答型插话的 interruption control plane

## Context

- 日期：2026-03-20 00:52 PDT
- 触发：`freely chat "看看后台在执行什么"` 已能 durable 写入 intake，但主主管长循环不会及时 claim；对于“后台 AI 进程在做什么”这类高注意力、低业务价值的询问型插话，这种延迟不可接受。

## 主问题

需要回答：

1. 这类插话是否应该进入 pre-brainstorm / issue / worker 主线。
2. 若主主管长循环忙碌，谁来保证“及时注意到”。
3. 如何实现而不长出第二个平权主管。

## 已形成的判断

### 1. 这类插话不应升级成长期研发产物

像“看看后台 AI 进程都在做什么”这种询问：

- 注意优先级高
- 业务长期价值低
- 目标是立即得到事实答案

所以它不应默认进入：

- `pre-brainstorm`
- `issue`
- `worker worktree`

正确落点应是：

- runtime direct answer
- resolution artifact
- 必要时 manager continuity 留痕

### 2. 问题不是 CLI 收不到，而是主主管不够及时

当前链路已经能做到：

- `freely chat` durable 写入 intake

但主主管只有一个长循环进程；当它正忙于 doc-loop / canonical 收口时，新的询问型插话可能长期停在：

- `new`
- `unclaimed`
- `pending`

所以“及时注意到”不能完全依赖主主管空闲。

### 3. 应增加 interruption dispatcher，而不是第二主管

正确的最小模型是：

- 单主主管继续负责全局治理
- runtime 增加一个独立 interruption dispatcher
- dispatcher 只处理窄范围的 answer-only control query

它不是第二主管，因为它：

- 不做 milestone / issue / pre-brainstorm 路由
- 不做 worker 排班
- 不创建长期业务产物

### 4. direct-answer 查询应通过专门 skill 收口

建议新增：

- `skill:human-interruption-direct-answer`

用于定义：

- 什么样的问题属于 direct-answer control query
- 可以直接读取哪些 runtime 事实源
- 输出长什么样

### 5. 第一版只支持后台 AI 进程状态查询

为了避免 scope inflation，第一版只支持：

- “后台进程都在做什么？”
- “后台 AI 进程现在在干什么？”
- “当前有没有 AI 进程在跑？”

回答内容只基于 runtime 可直接确认的事实：

- AI PID
- 进程命令
- 运行时长 / 状态
- 最近 session id / jsonl / prompt

## 初步结论

- 这项能力应落为 runtime interruption control plane 增强，而不是 manager 第二副本。
- 第一版以 “后台 AI 进程状态直答” 为唯一支持面。
- 吸收类型是 `control`，产物是 answer-only `resolution artifact`。
