---
name: A2A 协议替换 Handoff 架构重构
description: 用 Google A2A 协议替换 Freely 私有 Handoff 机制，实现标准化的 Agent 间通信
issue_id: raw-20260612T000223Z
kind: raw
phase_state: absorbed
promotion_gate: C-20260612T000223Z-A
absorbed_by: I-20260612T000223Z-A
open_questions: []
acceptance_criteria:
  - A2A Server 持久化到 SQLite
  - A2A Client 通过 A2A 协议委派任务
  - 删除 Handoff exit_kind 别名逻辑
  - 删除 A2AHandoffAdapter fallback
acceptance_reviews:
  - id: a2a-vs-handoff-idn
    reviewer: self
    status: staged
    date: 2026-06-12
    findings: |
      A2A 协议是 Google 提出的 Agent 间通信标准，Handoff 是 Freely 私有方案。
      A2A 协议包含 Task、Message、Artifact 等概念，与 Handoff 的 exit_kind 映射清晰。
      结论：使用 A2A 协议替换 Handoff。
created: 2026-06-12T00:02:23Z
updated: 2026-06-12T00:02:23Z
---

# A2A 协议替换 Freely Handoff 架构重构

## 问题
Freely 当前使用私有 Handoff 机制进行 Manager-Worker 通信，不符合行业标准。

## 解决方案
使用 Google A2A（Agent-to-Agent）协议替换 Handoff 机制。

## 验收标准
见上方 acceptance_criteria。