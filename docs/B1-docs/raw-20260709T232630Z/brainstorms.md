---
b1_id: B1-20260709T232630Z
phase_state: completed
source_raw: raw-20260709T232630Z
produced_candidate: C-20260709T232630Z-A
---

# B1_IBM: acp-bridge.log 按 base_tool 分离

## Input
raw #3848: 三个 bridge 共用 acp-bridge.log，互相 truncate 覆盖

## Problem
- claude/opencode/cline 三个 bridge 写同一个 `acp-bridge.log`
- 每个 bridge 启动时 `_truncate_log()` 清空日志，后续启动的 bridge 覆盖前面的
- 日志行无法区分来源 bridge

## Discovery
价值判断：值得修。直接影响可观测性和故障诊断能力。

## Brainstorm
### Option A: 按 base_tool 分离日志（推荐）
`acp-bridge.log` → `acp-bridge-{base_tool}.log`
每个 bridge 独立日志，truncate 只影响自己。

### Option B: 单一日志 + base_tool 前缀
不改文件名，每行加 `[base_tool]` 前缀。不改 truncate 行为。
缺点：仍然互相覆盖。

## Decision: Option A
3 文件 ~15 处改动。每个 bridge 独立文件，truncate 安全。

## Candidate
- candidate_id: C-20260709T232630Z-A
- status: promoted
- milestone: M-20260709T232630Z-A
