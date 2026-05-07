---
local_id: raw-20260506T1400Z
kind: raw
status: proposed
phase_state: proposed
source_candidate: docs/pre-brainstorms/20260506-merge-guarded-fix/candidates.md
platform_ids:
  github: "236"
primary_platform: github
created_at: 2026-05-06T14:00:00Z
author: zhaoquan
channel: github
session_refs: []
pre_tests_path: docs/epics/merge-guarded-fix-whitelist/verification/pre-tests.md
verification_artifact_dir: docs/epics/merge-guarded-fix-whitelist/code-reviews
pre_tests_path: docs/epics/merge-guarded-fix-whitelist/verification/pre-tests.md
verification_artifact_dir: docs/epics/merge-guarded-fix-whitelist/code-reviews
---

## 问题
merge-guarded 只接受 feature/* 和 hotfix/* → test-pre-merge-*，fix/* 不在白名单。

## 修复
validate_merge_direction + pre-flight gate 增加 fix/* 支持。

- pre_tests_path: `docs/epics/merge-guarded-fix-whitelist/verification/pre-tests.md`
- verification_artifact_dir: `docs/epics/merge-guarded-fix-whitelist/code-reviews`
