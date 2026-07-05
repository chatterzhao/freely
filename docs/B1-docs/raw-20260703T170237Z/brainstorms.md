---
b1_id: B1-20260703T170237Z
phase_state: completed
source_raw: raw-20260703T170237Z37Z
produced_candidate: C-20260703T170237Z-A
---

# B1: AI crash evidence丢失

## Problem
AI exit rc!=0 时，cycle debug log 含 stderr crash 信息。但 daemon 重启后
旧 cycle log 被清理，根因无法排查。14:42 opencode crash 就丢了证据。

## Fix
rc!=0 时复制 cycle_debug_log → .freely/logs/crash-{tool}-{timestamp}.log
用 $AI_TOOL（registry-derived），不硬编码，适用所有工具。

## Candidate
- candidate_id: C-20260703T170237Z-A
- status: promoted
- milestone: M-20260703T170237Z-A
