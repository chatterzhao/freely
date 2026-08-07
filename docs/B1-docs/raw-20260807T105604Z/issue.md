---
schema_version: '1'
local_id: raw-20260807T105604Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260807T105604Z-A
platform_ids:
  github:
    issue_id: '4105'
    url: https://github.com/chatterzhao/freely/issues/4105
    synced_at: ''
  gitee:
    issue_id: IK7802
    url: https://gitee.com/zhaoquan/freely/issues/IK7802
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-08-07T10:56:05Z'
updated_at: '2026-08-07T10:56:32Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-08-07T10:58:00Z'
closeout_note: ''
---

workflow_kind: fix

# chore: 解除 .codex/config.toml 跟踪

## 现象
.gitignore 已声明 .codex/ 忽略，但 .codex/config.toml 在规则加入前被跟踪；用户修改（model/sandbox_mode/approval_policy 等个人字段）导致 develop working tree dirty，daemon start 被 clean-tree 检查拒绝。

## 修复方案
git rm --cached .codex/config.toml（解除跟踪，本地保留）（cleanup 类，LAWS §304 豁免路径）。
