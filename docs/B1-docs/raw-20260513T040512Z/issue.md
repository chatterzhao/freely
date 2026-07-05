---
local_id: raw-20260513T040512Z12Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '327'
    url: https://github.com/chatterzhao/freely/issues/327
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-13T04:05:22Z'
updated_at: '2026-06-17T00:25:08Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
force_closed_at: '2026-05-19T19:21:36Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
---

## 现状问题

当前 `task-lifecycle-scan.py` 对每个 lifecycle item 调用 `_is_github_closed()` → `gh issue view N`，O(n) API 导致扫描需要数分钟甚至超时。

## 目标

改为 1 + 3 阶段扫描，全程 1 次 API 调用：

```
Phase 0 — Batch 全量抓
  gh issue list --state all --limit 1000 --json number,title,state,body
  → platform_all: dict[number → state]

Phase 1 — 本地 vs 平台分类
  对 docs/issues/ 每个 issue:
    pid ∈ platform_all? → 一致 / 不一致 / 仅本地

Phase 2 — 反向发现
  platform 上有 raw-{key} 但本地没有 → 需 materialize

Phase 3 — Lifecycle chain trace
  只用前两阶段结果做本地检查，零 API
```

## 关键变更

1. `_is_github_closed()` 改为查预加载的 `platform_all` dict，不再调 `gh issue view`
2. `scan_platform_issues()` 增加 `--state all` 抓全量
3. 新增分类输出：local_only / platform_closed / state_mismatch / platform_only
4. `SKIP_PLATFORM_CHECK` 不再需要

## 验证标准

- 扫描总耗时 < 5s（之前 > 2min）
- 分类结果：本地有平台没有、本地没有平台有、状态不一致三类都能正确识别

<!-- raw-20260513T040512Z12Z -->
