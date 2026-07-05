---
b1_id: B1-20260626T161720Z
phase_state: completed
source_raw: raw-20260626T161720Z20Z
source_url: https://github.com/chatterzhao/freely/issues/3567
produced_candidate: C-20260626T161720Z-A
created_at: 2026-06-26
---

# B1_IBM: 废弃 AI_TOOL，agent-table 成为唯一真相源

## Input
- source_raw: raw-20260626T161720Z20Z
- discovered during: Freely daemon start, Manager 降级到 kiro-cli alias 导致无法启动

## Problem
- AI_TOOL 从 config.toml 读取，可能残留旧 alias（kiro-cli）
- AGENT_AI_TOOL 降级到 AI_TOOL 再降级到默认值，掩盖问题
- sync_tooling 写 AGENT_AI_TOOL 到 worker config，绕了一圈
- agent-table 是唯一正确定义 per-agent slot 的地方

## Brainstorm
### Option A: 只修降级链
AGENT_AI_TOOL → AI_TOOL → claude。alias 残留问题仍在，治标不治本。

### Option B: agent-table 成为唯一源
load_config 从 agent-table 解析 AGENT_AI_TOOL，自动派生 AI_TOOL。不写 config，不降级。freely init 生成模板。

## Decision: Option B
- why_this: 彻底消除 AI_TOOL 的 alias 残留问题和 config 写入绕路
- alternatives_considered: A（治标）

## Candidate
- candidate_id: C-20260626T161720Z-A
- status: promoted
- milestone: M-20260626T161720Z-A
