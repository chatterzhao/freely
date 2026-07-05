---
local_id: raw-20260705T084915Z15Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260705T084915Z-A
platform_ids:
  github:
    issue_id: '3748'
    url: https://github.com/chatterzhao/freely/issues/3748
    synced_at: ''
  gitee:
    issue_id: IJYUNG
    url: https://gitee.com/zhaoquan/freely/issues/IJYUNG
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-05T08:49:37Z'
updated_at: '2026-07-05T08:49:37Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题
_ensure_acp_bridge_running 中 tool change 检测用全局 AGENT_AI_TOOL（永远=claude），导致 opencode/cline bridge 被误判为 tool changed，反复 kill+restart。

## 修复
_current_base 改为用 bridge 自己的 $base_tool 参数
