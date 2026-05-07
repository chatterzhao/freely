---
local_id: raw-20260506T1230Z
kind: raw
status: proposed
phase_state: proposed
platform_ids:
  github: "240"
primary_platform: github
source_candidate: docs/pre-brainstorms/20260506-wt-create-dual/candidates.md
created_at: 2026-05-06T12:30:00Z
updated_at: 2026-05-06T12:30:00Z
author: zhaoquan
channel: github
session_refs: []
pre_tests_path: docs/epics/wt-create-dual/verification/pre-tests.md
verification_artifact_dir: docs/epics/wt-create-dual/code-reviews
---

## 问题
wt-create 每次只创建一个工位，fix/feat 和 test-pre-merge 都基于 develop。

## 方案
一次性创建两个工位：test-pre-merge 基于 develop，fix/feat 基于 test-pre-merge。
fix→test-pre-merge 变为 fast-forward。

- pre_tests_path: `docs/epics/wt-create-dual/verification/pre-tests.md`
- verification_artifact_dir: `docs/epics/wt-create-dual/code-reviews`
