---
local_id: raw-20260506T1230Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260506T1230Z-A
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
platform_ids:
  github:
    issue_id: '280'
    url: https://github.com/chatterzhao/freely/issues/280
    synced_at: '2026-05-10T09:29:50Z'
primary_platform: github
source_candidate: docs/pre-brainstorms/20260506-wt-create-dual/candidates.md
created_at: 2026-05-06 12:30:00+00:00
updated_at: '2026-06-02T17:03:11Z'
author: zhaoquan
channel: github
session_refs: []
pre_tests_path: docs/epics/wt-create-dual/verification/pre-tests.md
verification_artifact_dir: docs/epics/wt-create-dual/code-reviews
platform_state: closed
---

## 问题
wt-create 每次只创建一个工位，fix/feat 和 test-pre-merge 都基于 develop。

## 方案
一次性创建两个工位：test-pre-merge 基于 develop，fix/feat 基于 test-pre-merge。
fix→test-pre-merge 变为 fast-forward。

- pre_tests_path: `docs/epics/wt-create-dual/verification/pre-tests.md`
- verification_artifact_dir: `docs/epics/wt-create-dual/code-reviews`
