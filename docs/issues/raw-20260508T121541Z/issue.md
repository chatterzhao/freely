---
local_id: raw-20260508T121541Z
kind: raw
status: proposed
phase_state: proposed
platform_ids:
  github:
    issue_id: '257'
    url: https://github.com/chatterzhao/freely/issues/257
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-08T12:15:50Z'
updated_at: '2026-05-08T12:18:04Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## Bug

`platform-adapter.py` `pull_raw_issue` 第 326 行只比较了 `standard_key != raw_key`，**没有先检查标题是否已包含 canonical key**：

```python
standard_key = _created_at_to_key(created_at)
if standard_key and standard_key != raw_key:  # ← 缺了标题检查！
    raw_key = standard_key  # 覆盖
```

## 设计意图

只有当标题里**没有** `raw-{key}` 时，才用 `created_at` 派生 key。标题已有 key 时不应覆盖。

## 本次案例

- 标题: `raw-20260508T111130Z: reference-transaction hook ...` ← 已有 key
- created_at: `2026-05-08T11:11:39Z` ← 晚了 9 秒
- 应跳过标准化，但当前代码仍覆盖 → key 变成 `111139Z`

## 修复

```python
title = info.get("title", "")
if f"raw-{raw_key}" not in title and standard_key and standard_key != raw_key:
    # 只有标题缺失 raw key 时才标准化
    ...
```
- pre_tests_path: docs/epics/platform-adapter-title-key/verification/pre-tests.md
- verification_artifact_dir: docs/epics/platform-adapter-title-key/code-reviews
