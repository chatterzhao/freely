---
local_id: raw-20260708T222454Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260708T222454Z-A
platform_ids:
  github:
    issue_id: '3836'
    url: https://github.com/chatterzhao/freely/issues/3836
    synced_at: ''
  gitee:
    issue_id: IJZS1I
    url: https://gitee.com/zhaoquan/freely/issues/IJZS1I
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-08T22:25:19Z'
updated_at: '2026-07-08T22:25:19Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题

1. 不扫纯平台 issue（无本地 issue.md）→ 测试证实检测不到跨平台不一致
2. get_all_platform_issue_states 只查 GitHub，不查 Gitee
3. extract_github_id 只取 GitHub ID，issue.md 有 platform_ids dict 不用
4. _sync_platform_direct 先 close 不先 update content
5. dropped 和 closed 应同样对待（都是 terminal 同步）
6. N=0 平台不阻塞报错

## 修复
1. scan 扫所有平台 OPEN issues → 比对本地
2. 逐平台查状态，遍历 configured_platforms
3. terminal: update_issue(body=phase_state) → close_issue
4. 跨平台不一致 API 直修，不生成 worktree item
5. N=0 → sys.exit 报错

## 验收
创建双平台测试 issue → 制造 GitHub=CLOSED/Gitee=OPEN → scan 检测到 → API 同步
