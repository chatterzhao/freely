---
local_id: raw-20260511T151342Z
kind: raw
priority: medium
phase_state: completed
phase_state: proposed
source: platform
platform_ids:
  github:
    issue_id: "304"
    owner: chatterzhao
    repo: freely
created_at: "2026-05-11T15:13:42Z"
title: "fix: merge-guarded returns non-zero exit on successful merge"
platform_state: closed
---
## 问题
merge-guarded 在 merge 成功后仍返回 exit 1。原因：用 git merge --continue 返回值判断成功，
而非检查 MERGE_HEAD 是否已被清理。

## 修复
改为用 MERGE_HEAD 状态判断 merge 是否成功。成功但 continue_rc 非零时打 warning 到 stderr。
