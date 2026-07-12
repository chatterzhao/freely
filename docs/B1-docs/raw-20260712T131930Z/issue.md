---
local_id: raw-20260712T131930Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260712T131930Z-A
platform_ids:
  github:
    issue_id: '3896'
    url: https://github.com/chatterzhao/freely/issues/3896
    synced_at: ''
  gitee:
    issue_id: IK0GPM
    url: https://gitee.com/zhaoquan/freely/issues/IK0GPM
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-12T13:19:54Z'
updated_at: '2026-07-12T13:19:54Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题
templates/config.toml.example 中 [skip_ibm_gate] 的 allowed_paths 包含多行注释:
  allowed_paths = [
    # "docs/my-custom-governance-dir/",
  ]
freely init 将此 TOML 写入 config.toml 时变成字符串 "[]" 而非数组 []，
导致 governance-merge-gate 的 tomllib 解析失败。

## 修复
allowed_paths = []（单行空数组，注释移到上方）
