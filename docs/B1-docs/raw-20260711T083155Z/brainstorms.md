---
b1_id: B1-20260711T083155Z
phase_state: completed
source_raw: raw-20260711T083155Z
source_url: https://github.com/chatterzhao/freely/issues/3882
produced_candidate: C-20260711T083155Z-A
created_at: 2026-07-11
---

# B1_IBM: A2A→SSE→ACP 消息投递链修复 + SQLite 友好校验

## Input
- 来源: raw-20260711T083155Z, GitHub #3882
- 问题: Manager→Worker A2A 消息发出去后 Worker 收不到。消息链断裂点: A2A Server 存储消息后不发 SSE → watchdog_sse 不处理 message_added 事件 → 消息静默丢失。
- 次生问题: AI agent 写错 A2A 格式时 SQLite 无拦截，空内容静默写入，agent 不知道失败原因。

## Problem
1. **消息投递断裂**: A2A Server messages handler (POST /tasks/{id}/messages) 只写 SQLite，不发 SSE。watchdog_sse 只处理 input-required 状态变更，不认识 message_added 事件。Manager 用 a2a_task.py prompt 发消息后，Worker 永远收不到。
2. **无校验层**: a2a_tasks 表所有字段 DEFAULT ''，AI 写空内容/非法 role/不存在 task 时全部静默成功。Agent 不知道写错了，更不知道怎么改。
3. **role 无约束**: role 字段可以是任意值，没有枚举校验。

## Brainstorm

### Option A: 完整修复（推荐）
**A2A Server**: messages handler 存储后 emit SSE message_added
**watchdog_sse**: 新增 message_added 事件处理 → 查 a2a_tasks.raw_key → 查 agent_working.session_id → ACP session/prompt 投递
**freely_db_manager**: 3 层 SQLite 校验 gate（content 非空 / role 合法 / task 存在），每层返回结构化错误 {valid, error, fix_hint, example}
**a2a_task.py**: update_message() 失败时打印 fix_hint + example 到 stderr

优点: 全链路打通 + 每个断点都有友好提示
缺点: 4 文件改动

### Option B: 最小修复
只在 A2A Server 加 SSE emit，watchdog 加简单 handler，不加强校验。

优点: 改动最小
缺点: AI 写错格式时仍然静默失败，下次还会犯同样错误

## Decision: Option A
完整修复。消息投递是 agent 协作的基础设施——断了就等于 Manager 是聋哑人。友好校验让 AI 知道自己写错了什么、怎么改，避免重复犯错。

## Candidate
- candidate_id: C-20260711T083155Z-A
- status: promoted
- milestone: M-20260711T083155Z-A
