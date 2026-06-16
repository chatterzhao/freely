---
local_id: raw-20260508T004541Z
kind: raw
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: 2026-05-17T04:47:25Z
platform_ids:
  github:
    issue_id: '250'
    url: https://github.com/chatterzhao/freely/issues/250
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-08T00:45:41Z'
intake_id: ''
author: platform
channel: github
session_refs: []
pre_tests_path: docs/epics/skill-ref-cleanup/verification/pre-tests.md
verification_artifact_dir: docs/epics/skill-ref-cleanup/code-reviews
platform_state: closed
---

- pre_tests_path: docs/epics/skill-ref-cleanup/verification/pre-tests.md
- verification_artifact_dir: docs/epics/skill-ref-cleanup/code-reviews

## 背景

项目 skill 已部署到 ~/.claude/skills/，引用 skill 应使用 skill:name 而非路径。

## 改动

将项目文件中路径引用改为 skill 名。deploy-skills 支持多工具部署。
