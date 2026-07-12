---
local_id: raw-20260712T105347Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260712T105347Z-A
platform_ids:
  github:
    issue_id: '3887'
    url: https://github.com/chatterzhao/freely/issues/3887
    synced_at: ''
  gitee:
    issue_id: IK0G7W
    url: https://gitee.com/zhaoquan/freely/issues/IK0G7W
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-12T10:54:09Z'
updated_at: '2026-07-12T10:54:09Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 问题
FREELY_SKIP_IBM_GATE 可跳过路径硬编码在 governance-merge-gate 中，
用户无法添加项目特定的治理目录。

## 修复
1. .freely/config.toml 增加 [skip_ibm_gate] allowed_paths 白名单
2. templates/config.toml.example 同步更新
3. governance-merge-gate 读取 config.toml 路径

## 验收
- freely init 新项目默认生成 [skip_ibm_gate] 段
- allowed_paths 中路径可通过 FREELY_SKIP_IBM_GATE
