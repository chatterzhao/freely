---
b1_id: B1-20260710T000650Z
phase_state: completed
source_raw: raw-20260710T000650Z
produced_candidate: C-20260710T000650Z-A
---

# B1_IBM: pre-scan-fix + scan raw_key fallback

## Problem
Scan 输出 685 items，636 个是 terminal phase + 无 platform_ids 的本地文档残留。无法自动同步，也不该进入 Manager AI cycle。

## Decision
1. 新增 pre-scan-fix.sh — 脚本批量修复本地文档，走完整 workflow + --skip-ibm
2. scan 新增 raw_key_pid_index — platform_ids 为空时用 raw_key 从平台 issue 标题匹配

## Candidate
- candidate_id: C-20260710T000650Z-A
- status: promoted
- milestone: M-20260710T000650Z-A
