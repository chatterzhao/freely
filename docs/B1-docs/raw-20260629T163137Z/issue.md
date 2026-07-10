---
local_id: raw-20260629T163137Z37Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260629T163137Z-A
platform_ids:
  github:
    issue_id: '3631'
    url: https://github.com/chatterzhao/freely/issues/3631
    synced_at: ''
  gitee:
    issue_id: IJXOMS
    url: https://gitee.com/zhaoquan/freely/issues/IJXOMS
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-29T16:31:58Z'
updated_at: '2026-06-29T16:31:58Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 背景

pr-review-guarded 是 PR 的 6 维 review 入口，当前存在以下问题。

## 问题列表

### 1. review 文件输出路径不正确
- 从 fix worktree 跑：能找到 I-* issue，路径正确（落在 issue 的 verification_artifact_dir）
- 从 develop 工位跑（Manager 也可以跑 reviewer agent）：找不到 I-* issue → fallback 到 
- 需要：无论从哪里跑，都正确解析到 issue 的  路径

### 2. ACP 静默失败
-  通过 ACP 调 reviewer agent，ACP 不可用时静默失败
- pr-review-guarded 报错 Review
