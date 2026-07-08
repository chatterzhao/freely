---
b1_id: B1-20260708T222454Z
phase_state: completed
source_raw: raw-20260708T222454Z
---
# B1: scan per-platform state + platform-only detection + direct sync

## Problem
1. scan 不检测纯平台 issue（无本地 issue.md）
2. _sync_platform_direct 只 close 不先 update content
3. 只查 GitHub 状态，不逐平台比对
4. dropped 和 closed 应同样 terminal 同步

## Test Evidence
创建 test issue (GitHub #3835, Gitee IJZS1H), GitHub=CLOSED/Gitee=OPEN → scan 检测不到

## Decision
1. _sync_platform_direct: update_issue(content) → check per-platform → close OPEN
2. 添加 platform-only 检测: 遍历平台 OPEN issues → 比对本地
3. 逐平台状态: 用 fetch_issue_state 逐平台查
4. dropped/absorbed/completed 统一处理
