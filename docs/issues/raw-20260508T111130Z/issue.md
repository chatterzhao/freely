---
local_id: raw-20260508T111130Z
kind: raw
status: proposed
phase_state: proposed
platform_ids:
  github:
    issue_id: '256'
    url: https://github.com/chatterzhao/freely/issues/256
primary_platform: github
---

# raw-20260508T111130Z: reference-transaction hook 误拦截 branch delete

## 问题

`git branch -d` 删除已合并的 `test-pre-merge-*` 分支时被 reference-transaction hook 拦截。

## 根因

Hook 收到 aborted 事务时 `old_oid=000... new_oid=000...`，触发了 creation guard。

## 修复

在 creation guard 前加 aborted/no-op 事务跳过检查。
