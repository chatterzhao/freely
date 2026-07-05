---
local_id: raw-20260507T143546Z
kind: raw
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: '2026-06-17T00:23:18Z'
platform_ids:
  github:
    issue_id: '249'
    url: https://github.com/chatterzhao/freely/issues/249
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-07T14:35:46Z'
intake_id: ''
author: platform
channel: github
session_refs: []
pre_tests_path: docs/epics/platform-pull-standardize/verification/pre-tests.md
verification_artifact_dir: docs/epics/platform-pull-standardize/code-reviews
platform_state: closed
---

- pre_tests_path: docs/epics/platform-pull-standardize/verification/pre-tests.md
- verification_artifact_dir: docs/epics/platform-pull-standardize/code-reviews

## 问题
用户手动创建的 issue 标题 key 可能缺秒，需自动标准化。

## 修复
pull 时用平台 created_at 标准化标题 key。
