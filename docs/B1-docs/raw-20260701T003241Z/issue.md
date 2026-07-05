---
local_id: raw-20260701T003241Z41Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260701T003241Z-A
platform_ids:
  github:
    issue_id: '3672'
    url: https://github.com/chatterzhao/freely/issues/3672
    synced_at: ''
  gitee:
    issue_id: IJXYF4
    url: https://gitee.com/zhaoquan/freely/issues/IJXYF4
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-01T00:33:03Z'
updated_at: '2026-07-01T00:33:03Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题
已有 config.toml 时 init 会继续修改配置（ACP字段等），与用户预期不符。

## 修复
init 检测到 config.toml 存在且未传 --reset 时阻止执行，提示用户使用 --reset 或 --reset --auto
