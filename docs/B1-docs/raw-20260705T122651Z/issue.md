---
local_id: raw-20260705T122651Z51Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260705T122651Z-A
platform_ids:
  github:
    issue_id: '3753'
    url: https://github.com/chatterzhao/freely/issues/3753
    synced_at: ''
  gitee:
    issue_id: IJYV78
    url: https://gitee.com/zhaoquan/freely/issues/IJYV78
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-05T12:27:12Z'
updated_at: '2026-07-05T12:27:12Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 问题
B2 SKILL.md copy-paste 示例中 docs/epics 路径缺层，共 10 处：
- 缺 story+raw：行170/176/177/457/464（7处）
- 缺 raw：行419（1处）
- 缺 story：行169（1处）
- 缺 story+raw：行241（1处）
- 路径非 epic：pr-review-guarded:184

规范：docs/B2-docs/{epic}/{story}/raw-{key}/...
