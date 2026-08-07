---
local_id: raw-20260516T014923Z39Z
kind: raw
phase_state: dropped
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: 2026-05-17 04:47:25+00:00
platform_ids:
  github:
    issue_id: '355'
    url: https://github.com/chatterzhao/freely/issues/355
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-16T01:49:51Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## raw-20260516T014923Z39Z

| Field | Value |
|-------|-------|
| local_id | `raw-20260516T014923Z39Z` |
| kind | `raw` |
| status | `open` |
| phase | `none` |
| canonical | `none` |
| created | 2026-05-16T01:49:39Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260516T014923Z39Z`。实现前请用 `wt-create --raw-key 20260516T014939Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P2
status: open
source: chat-inbox
created_at: "2026-05-16T01:49:39Z"
title: "deploy-skills 应支持当前 AI_TOOL 并自动部署，freely start 时触发"

## 背景

`bin/deploy-skills` 当前只支持两个硬编码目标：
- `claude` → `~/.claude/skills/`
- `codex` → `~/.codex/skills/`

但项目配置的 AI tool 可能是任意值（如 `oc-acp-ds-flash-auto`），skill 不会被部署到对应工具的 skill 目录。

## 问题

1. deploy-skills 不识别项目当前配置的 `AI_TOOL`，只从 `FREELY_TOOLS` 或硬编码 `claude` 读取
2. 不支持 opencode、cc、iflow 等工具的 skill 路径
3. `freely start` / `freely daemon start` 没有自动触发 skill 部署
4. 修改 skill 后执行 `freely deploy-skills` 的人为步骤可能被遗漏

## 需求

### 1. deploy-skills 支持动态目标

从项目 config 读取当前 AI_TOOL，自动映射到对应 skill 目录：

| AI_TOOL | 目标路径 |
|---------|---------|
| claude* | ~/.claude/skills/ |
| codex* | ~/.codex/skills/ |
| oc-* / opencode | 项目 .opencode/ 或 ~/.config/opencode/ |
| cc* | (待确认) |
| iflow* | (待确认) |
| kiro-cli* | (待确认) |

对未识别的工具应报错而非静默跳过。

### 2. freely start 时自动触发

`freely start` / `freely daemon start` 在启动流程中调用 `deploy-skills --tools <AI_TOOL>`，确保每次启动时 skill 与源保持同步。

### 3. 强制覆盖选项

当前 deploy-skills 在目标已存在且内容一致时跳过。应默认强制覆盖（source of truth 是项目内的 skill 定义），或提供 `--force` 标志。

## 范围

- `bin/deploy-skills` — 目标映射逻辑
- `docs/system/workspace/scripts/runtime/freely` — start 流程中增加自动部署
