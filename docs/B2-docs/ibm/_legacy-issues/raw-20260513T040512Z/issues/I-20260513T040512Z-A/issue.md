---
local_id: I-20260513T040512Z-A
kind: i_issue
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
promoted_from: raw-20260513T040512Z12Z
source_candidate: docs/B1-docs/raw-20260513T040512Z12Z/candidates.md
milestone: M-20260513T040512Z-A
candidate: C-20260513T040512Z-A
canonical_issue_path: ''
platform_ids:
  github:
    issue_id: '327'
    url: https://github.com/chatterzhao/freely/issues/327
primary_platform: github
last_synced_comment_at: {}
hash: ''
created_at: 2026-05-19 16:29:00+00:00
updated_at: '2026-06-21T15:21:54Z'
intake_id: ''
author: zhaoquan
channel: freely-feat-execution
session_refs: []
pre_tests_path: docs/B2-docs/ibm/_legacy-issues/raw-20260513T040512ZI-20260513T040512Z-A/pre-tests.md
verification_artifact_dir: docs/B2-docs/task-lifecycle-scan-batch/code-reviews/
platform_state: closed
---

# I-20260513T040512Z-A: task-lifecycle-scan 批量化 — 1+3 阶段扫描替代 O(n) API 逐项查询

- source_candidate: `docs/B1-docs/raw-20260513T040512Z12Z/candidates.md`
- milestone: `M-20260513T040512Z-A`
- pre_tests_path: `docs/B2-docs/ibm/_legacy-issues/raw-20260513T040512ZI-20260513T040512Z-A/pre-tests.md`

## 目标

将 `task-lifecycle-scan.py` 从 O(n) API 逐项查询改造为 1+3 阶段批量化扫描，全程仅 1 次 `gh issue list` API 调用，将扫描总耗时从 >2min 降至 <5s。

## 范围

- Phase 0: 用 `gh issue list --state all --limit 1000` 批量抓取替代 `gh issue view N` 逐项查询
- Phase 1: 本地 vs 平台分类（一致/不一致/仅本地）
- Phase 2: 反向发现 platform_only 的 raw-{key} issue
- Phase 3: lifecycle chain trace 零 API 调用，仅用本地缓存结果
- 移除 `SKIP_PLATFORM_CHECK`

## 验收条件

- Phase 0: `gh issue list --state all --limit 1000` 批量抓取替代逐项查询
- Phase 1: 本地 vs 平台分类正确（一致/不一致/仅本地）
- Phase 2: 反向发现 platform_only 的 raw-{key} issue
- Phase 3: lifecycle chain trace 零 API 调用，仅用本地缓存结果
- SKIP_PLATFORM_CHECK 移除
- 扫描总耗时 < 5s（之前 > 2min）
