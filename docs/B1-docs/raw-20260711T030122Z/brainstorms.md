---
b1_id: B1-20260711T030122Z
phase_state: completed
source_raw: raw-20260711T030122Z
source_url: https://github.com/chatterzhao/freely/issues/3879
produced_candidate: C-20260711T030122Z-A
created_at: 2026-07-11
---

# B1_IBM: Agent Docs v2 — Identity-First Unified Style

## Input
raw #3879: 三个 agent 文档风格不一致。manager-agent.md 已重构为身份优先风格，
worker-agent.md 和 reviewer-agent.md 仍是旧格式。

## Problem

1. **结构不统一**: manager 新版(身份→工具箱→工作方式→边界→交互), worker/reviewer 旧版(Tool Policy→巡逻流程→Skill列表)
2. **工具分散**: Skills/Bash/禁止三表分离, AI 需要跨多张表检索
3. **缺少封装命令的原因说明**: worker 只知道用什么, 不知道为什么必须用
4. **worker 缺少 gate 自愈指引**: 遇到 gate 拦截不知道先自己诊断, 直接上报 Manager
5. **reviewer 技术细节充足但入口不清晰**: 身份、触发方式埋在后面

## Discovery
价值判断: agent 文档是 AI 理解自己职责的唯一入口。文档质量直接决定 AI 行为质量。

## Brainstorm
### Option A: 统一三文档结构 + 补充缺失内容
保持 manager 新版结构, worker/reviewer 对齐相同风格。补充 gate 自愈、封装命令原因、与其他 agent 交互说明。

### Option B: 保持现状, 仅修 bug
只修 skill 名不一致、命令参数错误等具体问题。

## Decision: Option A
三文档统一身份优先风格。AI 读完能理解自己是谁、能做什么、不能做什么、如何与其他 agent 协作。

## Candidate
- candidate_id: C-20260711T030122Z-A
- status: promoted
- milestone: M-20260711T030122Z-A
