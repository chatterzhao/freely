---
b1_id: B1-20260625T153111Z
phase_state: completed
source_raw: raw-20260625T153111Z
source_url: https://github.com/chatterzhao/freely/issues/3508
produced_candidate: C-20260625T153111Z-A
created_at: 2026-06-25
---

# B1_IBM: agent-table.toml 多 agent 分身注册

## Input
- source: raw-20260625T153111Z (GitHub #3508)
- 需求: 声明所有 agent 实例，Manager/Wroker/Reviewer 按表分配 slot

## Problem
- 当前 AI_TOOL 是 config.toml 里的单值，所有工位用同一个 tool+slot
- 设计上 Worker/Reviewer/Manager 应该用不同模型/CLI 工具
- 需要一种方式声明"有哪些 agent、各用什么 slot"

## Brainstorm
### Option A: agent-table.toml + pool 模式
- [[agent_pools]] 声明池，count=N 自动编号
- wt-create 读表分配空闲 worker
- Manager 巡逻读表查空闲 worker
- 扩容改 count 一行

### Option B: 在 config.toml 里直接加多行
- 扁平结构，所有 agent 实例在同一文件
- 缺点: 和现有字段混在一起，不够清晰

## Decision: Option A
- 独立文件 agent-table.toml，职责单一
- pool 模式支持一键扩容
- {role}_slot 对应终端 alias

## Candidate
- candidate_id: C-20260625T153111Z-A
- status: promoted
- milestone: M-20260625T153111Z-A
