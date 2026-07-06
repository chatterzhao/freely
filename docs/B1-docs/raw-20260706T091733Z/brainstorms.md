---
b1_id: B1-20260706T091733Z
phase_state: completed
source_raw: raw-20260706T091733Z
produced_candidate: C-20260706T091733Z-A
---
# B1: 门禁硬拦截 — 彻底堵死绕过路径

## Problem
三种绕过方式: git --no-verify, gh pr merge --admin, gh issue close (单平台)

## Fix
1. gh wrapper 扩展: pr merge + issue close 拦截
2. git wrapper: 剥离 --no-verify
3. CI enforce_admins: true
4. SKILL.md 铁律置顶

## Candidate
- candidate_id: C-20260706T091733Z-A
- status: promoted
