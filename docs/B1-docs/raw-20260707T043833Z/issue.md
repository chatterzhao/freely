---
local_id: raw-20260707T043833Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3795'
    url: https://github.com/chatterzhao/freely/issues/3795
    synced_at: ''
  gitee:
    issue_id: IJZBPS
    url: https://gitee.com/zhaoquan/freely/issues/IJZBPS
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-07T04:38:54Z'
updated_at: '2026-07-07T04:38:54Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题

之前重构过"只允许 platform 模式"，但遗漏了很多路径。本地 raw issue（chat-inbox / freely.db new-issue）仍然可以绕过平台创建，导致：
1. 创建的 raw issue 没有 GitHub/Gitee ID
2. 后续门禁检查时失败（找不到 platform issue）
3. develop 保护工位被污染

## 需要清理

1. freely_db_manager.py: 移除 new-issue chat_type 的创建逻辑
2. governance-merge-gate: 移除 chat-inbox catch-all (GATE 2a)
3. freely-db-cli: 移除 --type new-issue
4. task-lifecycle-scan.py: 移除本地 issue 扫描
5. 任何其他 fallback/兼容路径

## 设计原则

- 不留任何 fallback——要么 platform，要么拒绝
- 所有 issue 必须通过 freely feedback 创建（双平台同步）
- 如果 platform API 不可用，直接报错，不降级到本地模式
