---
local_id: raw-20260705T012851Z51Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260705T012851Z-A
platform_ids:
  github:
    issue_id: '3736'
    url: https://github.com/chatterzhao/freely/issues/3736
    synced_at: ''
  gitee:
    issue_id: IJYTNU
    url: https://gitee.com/zhaoquan/freely/issues/IJYTNU
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-05T01:29:12Z'
updated_at: '2026-07-05T01:29:12Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题

启动 freely daemon 时报错:
  freely: line 22179: _unique_tools[*]: unbound variable

agent-table 扫描时 _unique_tools 数组为空，set -u 下 [*] 触发 unbound variable。

## 修复

两处改为 ${_unique_tools[*]:-} 和 ${_cycle_tools[*]:-}。
