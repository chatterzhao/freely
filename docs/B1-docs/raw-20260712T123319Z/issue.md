---
local_id: raw-20260712T123319Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3891'
    url: https://github.com/chatterzhao/freely/issues/3891
    synced_at: ''
  gitee:
    issue_id: IK0GJX
    url: https://gitee.com/zhaoquan/freely/issues/IK0GJX
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-12T12:33:41Z'
updated_at: '2026-07-12T12:33:41Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题
PR #3888 遗漏了 freely 主脚本第 46 行的 TOOL_REGISTRY 变量路径更新。

## 修复
TOOL_REGISTRY: scripts/runtime/ → tools/
