---
local_id: raw-20260510T133900Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260510T133900Z-A
platform_ids:
  github:
    issue_id: '290'
    url: https://github.com/chatterzhao/freely/issues/290
primary_platform: github
platform_state: closed
updated_at: '2026-06-21T20:13:17Z'
---
## 问题
wt-create 先创建 test-pre-merge 再基于它创建 fix，导致 test 成为 fix 的父。删除 test 后 fix 失去基。
## 修复
顺序反转：fix ← develop，test-pre-merge ← fix。
