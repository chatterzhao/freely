---
local_id: raw-20260618T091721Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260618T091721Z-A
platform_ids:
  github:
    issue_id: '2986'
    url: https://github.com/chatterzhao/freely/issues/2986
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-18T09:17:37Z'
updated_at: '2026-06-29T13:43:23Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 问题描述

在开发 Freely 自身的过程中，AI （Claude Code）直接跳过了项目 governance 规则：
1. 在 `develop` 分支上直接创建文件（违反 AGENTS.md L17-19, L74, L127）
2. 手动创建 raw issue 目录而非通过 `freely feedback` 命令（违反 AGENTS.md L130-131）

## 根因诊断

### 1. 项目级 AGENTS.md 没被自动加载
Claude Code 自动加载 `~/.claude/CLAUDE.md`（用户全局）和项目根 `CLAUDE.md`，但 Freely 项目只有 `AGENTS.md`，没有 `CLAUDE.md`。规则写得很清楚，但不在 AI 的初始上下文中。

### 2. Skill description 缺强制语义
`freely-chat-issue-routing` 等 skill 的描述是能力声明（"将消息路由到正确的 issue"），不是约束声明。如果加 `MUST` 前缀或强制触发条件，AI 更容易被触发。

### 3. 会话启动检查未被强制执行
AGENTS.md L71-74 要求"每次会话开始检查分支/Worktree"，但没有自动化机制来执行这一检查。

## 建议改进

1. 项目根加 `CLAUDE.md` 指向 `AGENTS.md`，让治理规则自动注入 AI 上下文
2. 关键 skill description 加强制语义（MUST invoke before...）
3. 参考外部 skill 管理最佳实践（Matt Pocock skills、JiuwenSwarm 等）

## 相关
- 根因讨论发生在 Claude Code 会话中
- 参考: https://github.com/mattpocock/skills, https://github.com/openJiuwen-ai/jiuwenswarm
