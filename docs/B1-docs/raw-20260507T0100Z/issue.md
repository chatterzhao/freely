---
local_id: raw-20260507T0100Z
kind: raw
phase_state: dropped
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
platform_ids:
  github:
    issue_id: '278'
    url: https://github.com/chatterzhao/freely/issues/278
    synced_at: '2026-05-10T09:29:40Z'
primary_platform: github
created_at: 2026-05-07 01:00:00+00:00
author: zhaoquan
channel: github
session_refs: []
pre_tests_path: docs/B2-docs/fix-branch-naming/verification/pre-tests.md
verification_artifact_dir: docs/epics/fix-branch-naming/code-reviews
source_candidate: docs/B1-docs/raw-20260507/candidates.md
updated_at: 2026-05-17T04:47:25Z
platform_state: closed
---

## 问题
fix-execution SKILL.md 分支规范表中普通 fix 的分支前缀是 feature/ 不是 fix/。

## 修复
7 处 feature/ → fix/，使用 raw-{raw-key}-{slug} 格式。

- pre_tests_path: `docs/B2-docs/fix-branch-naming/verification/pre-tests.md`
- verification_artifact_dir: `docs/epics/fix-branch-naming/code-reviews`
