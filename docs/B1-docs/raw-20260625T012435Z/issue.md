---
local_id: raw-20260625T012435Z35Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3458'
    url: https://github.com/chatterzhao/freely/issues/3458
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-25T01:24:35Z'
updated_at: '2026-06-25T02:21:11Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260625T012435Z-A
source_candidate: docs/B1-docs/raw-20260625T012435Z35Z/candidates.md#C-20260625T012435Z-A

platform_state: closed---

## 问题

test-pre-merge-* 分支当前与 main/develop 同等级保护：禁止一切直接写入、禁止 fast-forward merge。但 test-pre-merge 的职责是**丢弃式测试沙箱**——它的存在意义就是接收 fix/feature 分支的合并来执行测试。

## 当前行为（错误）

```
fix branch → git merge → test-pre-merge → [HOOK] blocked ❌
```

导致 test skill 无法执行——合并被挡，测试跑不了。

## 正确行为

| 操作 | 允许 | 理由 |
|------|:--:|------|
| fix/feature → merge → test-pre-merge | ✅ | 它的用途 |
| test-pre-merge 上 git commit | ✅ | 丢弃式沙箱 |
| test-pre-merge → merge → develop | ❌ | 只通过 pr-merge-guarded |
| test-pre-merge → push | ❌ | 不上远程 |

## 改动位置

`.githooks/ 中的 ref-update hook，将 test-pre-merge-* 从保护列表中移除
