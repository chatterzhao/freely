---
local_id: raw-20260720T012820Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260720T012820Z-A
platform_ids:
  github:
    issue_id: '4034'
    url: https://github.com/chatterzhao/freely/issues/4034
    synced_at: ''
  gitee:
    issue_id: IK2693
    url: https://gitee.com/zhaoquan/freely/issues/IK2693
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-20T01:28:43Z'
updated_at: '2026-07-20T01:28:43Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 根因
run-acp-prompt.py --launch-kind仅接受fresh/resume/fork/prompt。跨tool时传new→argparse报错→worker立即崩溃→日志全空。

## 修复
freely L13345: new→fresh。fresh做session/new,正是跨tool需要的行为。
