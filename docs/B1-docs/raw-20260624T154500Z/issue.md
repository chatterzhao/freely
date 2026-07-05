---
local_id: raw-20260624T154500Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3444'
    url: https://github.com/chatterzhao/freely/issues/3444
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-24T15:42:17Z'
updated_at: '2026-06-24T15:45:00Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260624T154500Z-A
source_candidate: docs/B1-docs/20260624T154500Z--runtime-py-chmod/candidates.md#C-20260624T154500Z-A
---

## 根因

Git 中存储的文件模式为 100644（无执行位），每次 checkout/merge 恢复。需提交模式变更 100644 → 100755。

## 修复

```
find docs/system/workspace/scripts/runtime -name "*.py" -exec chmod +x {} +
git add docs/system/workspace/scripts/runtime/
git commit
```
