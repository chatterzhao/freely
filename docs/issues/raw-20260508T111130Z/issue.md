---
local_id: raw-20260508T111130Z
kind: raw
phase_state: completed
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: 2026-05-17T04:47:25Z
platform_ids:
  github:
    issue_id: '256'
    url: https://github.com/chatterzhao/freely/issues/256
primary_platform: github
pre_tests_path: docs/epics/reference-transaction-delete-fix/verification/pre-tests.md
verification_artifact_dir: docs/epics/reference-transaction-delete-fix/code-reviews
platform_state: closed
---

# raw-20260508T111130Z: reference-transaction hook 误拦截 branch delete

- pre_tests_path: docs/epics/reference-transaction-delete-fix/verification/pre-tests.md
- verification_artifact_dir: docs/epics/reference-transaction-delete-fix/code-reviews

## 问题

`git branch -d` 删除已合并的 `test-pre-merge-*` 分支时被 reference-transaction hook 拦截。

## 根因

Hook 收到 aborted 事务时 `old_oid=000... new_oid=000...`，触发了 creation guard。

## 修复

在 creation guard 前加 aborted/no-op 事务跳过检查。
