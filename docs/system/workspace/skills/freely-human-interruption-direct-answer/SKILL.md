---
name: freely-human-interruption-direct-answer
description: >-
  处理高注意力、低业务价值的快速人类插话。典型场景：查询 AI 进程状态、
  简单问答。由 runtime interruption dispatcher 直接 claim 并回答。

  Use when: 用户问简单问题（状态查询、进度确认），无需进入长期主线。
  触发词："状态"、"进度"、"在干什么"、"查一下"。
loop: intake
owner: runtime
supersedes: []
---

# skill:freely-human-interruption-direct-answer

## 职责

- 处理 runtime-owned 的 answer-only interruption。
- 在不打断主主管长循环的前提下，尽快返回直接答案。
- 产出 resolution artifact，并把 intake 回写为 `absorbed`。

## 典型输入

- “看看后台进程都在做什么？”
- “后台 AI 进程现在在干什么？”
- “当前有没有跑着的 AI 进程？”

## 典型输出

- 当前是否存在后台 AI 进程
- AI 进程 PID / 命令 / 运行时长 / 状态
- 最近一次 tool session / jsonl / prompt 文件

## 不负责

- 不创建 pre-brainstorm / issue / worker worktree
- 不替代主管做项目排班
- 不解释 discovery / continuation 类插话
- 不把 answer-only 查询伪装成长期业务产物

## 边界

- 这是 runtime interruption control plane 的特例，不是第二个主管。
- 只允许处理窄范围的 direct-answer control query。
- 若查询超出 runtime 可直接回答的边界，应留给主主管或 `skill:freely-human-interruption-handling`。
