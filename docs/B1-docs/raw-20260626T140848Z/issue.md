---
local_id: raw-20260626T140848Z48Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3559'
    url: https://github.com/chatterzhao/freely/issues/3559
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-26T14:09:08Z'
updated_at: '2026-06-26T14:09:08Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260626T140848Z-A
source_candidate: docs/B1-docs/raw-20260626T140848Z48Z/candidates.md#C-20260626T140848Z-A

platform_state: closed---

## 问题

line 21 定义 `_RUNTIME_DIR`，但 8 处引用写成了 `RUNTIME_DIR`（少了下划线），导致 Gitee 所有操作抛出 `NameError: name 'RUNTIME_DIR' is not defined`。

## 修复

`str(RUNTIME_DIR / "gitee-issue.py")` → `str(_RUNTIME_DIR / "gitee-issue.py")`，共 8 处（lines 35, 160, 206, 230, 252, 277, 332, 388）。
