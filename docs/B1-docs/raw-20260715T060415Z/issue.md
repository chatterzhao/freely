---
local_id: raw-20260715T060415Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260715T060415Z-A
platform_ids:
  github:
    issue_id: '3904'
    url: https://github.com/chatterzhao/freely/issues/3904
    synced_at: ''
  gitee:
    issue_id: IK162S
    url: https://gitee.com/zhaoquan/freely/issues/IK162S
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-15T06:04:45Z'
updated_at: '2026-07-15T06:04:45Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 根因
task-lifecycle-scan.py 生成 summary.total，但 append_task_source_patrol_seed_if_needed 的 Python 注入代码读 summary.total_incomplete。字段名不匹配导致 total=0 → 跳过 scan 注入。

## 修复
total_incomplete → total（向后兼容：优先 total，fallback total_incomplete）
