---
local_id: raw-20260506T140000Z
kind: raw
phase_state: dropped
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
source_candidate: docs/B1-docs/raw-20260506/candidates.md
platform_ids:
  github:
    issue_id: '273'
    url: https://github.com/chatterzhao/freely/issues/273
    synced_at: '2026-05-10T09:28:57Z'
primary_platform: github
created_at: 2026-05-06 14:00:00+00:00
author: zhaoquan
channel: github
session_refs: []
pre_tests_path: docs/B2-docs/merge-guarded-fix-whitelist/verification/pre-tests.md
verification_artifact_dir: docs/B2-docs/merge-guarded-fix-whitelist/code-reviews
updated_at: '2026-06-21T20:12:47Z'
platform_state: closed
---

## 问题
pr-merge-guarded 只接受 feature/* 和 hotfix/* → test-pre-merge-*，fix/* 不在白名单。

## 修复
validate_merge_direction + pre-flight gate 增加 fix/* 支持。

- pre_tests_path: `docs/B2-docs/merge-guarded-fix-whitelist/verification/pre-tests.md`
- verification_artifact_dir: `docs/B2-docs/merge-guarded-fix-whitelist/code-reviews`
