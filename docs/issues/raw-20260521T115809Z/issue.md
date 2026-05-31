---
local_id: raw-20260521T115809Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260521T115809Z-A
platform_ids:
  github:
    issue_id: '1820'
    url: https://github.com/chatterzhao/freely/issues/1820
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/issues/I-20260521T115809Z-A/issue.md
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-21T11:58:21Z'
updated_at: '2026-05-31T00:29:09Z'
intake_id: ''
author: platform
channel: github
session_refs: []
force_closed_at: '2026-05-21T15:26:36Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
platform_state: closed
---

## 问题

执行 `./bin/pr-merge-guarded develop fix/raw-20260521T095313Z-type-based-alias-resolution` 后，合并提交信息为：

```
Merge branch forbidden into develop
Freely-Bypass-Mode: forbidden
Freely-Source-Branch: forbidden
```

`Freely-Source-Branch` 应该是 `fix/raw-20260521T095313Z-type-based-alias-resolution`，但实际值为 `forbidden`。

## 根因分析

`render_merge_message()` 函数中 `source_branch` 参数被错误传入了 `Freely-Bypass-Mode` 值（`forbidden`）而非真实分支名。

## 影响

- 合并历史中无法追溯到真实源分支
- `Freely-Source-Branch` 元数据不可信
- 影响 audit trail 完整性

## 修复方向

在 `docs/system/workspace/scripts/worktree/pr-merge-guarded` 中定位 `render_merge_message` 调用，确保传入正确的 source branch 名称。
