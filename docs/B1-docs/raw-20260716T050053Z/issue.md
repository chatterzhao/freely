---
local_id: raw-20260716T050053Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3936'
    url: https://github.com/chatterzhao/freely/issues/3936
    synced_at: ''
  gitee:
    issue_id: IK1EQO
    url: https://gitee.com/zhaoquan/freely/issues/IK1EQO
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-16T05:01:24Z'
updated_at: '2026-07-16T05:01:24Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## Bug A (CRITICAL): 内联 Python NameError: name 're' is not defined

每次 AI launch 前触发。Traceback 在 <stdin> line 170。daemon-launch.log 中 20+ 次出现。
出现在 session anchor persisted early 和 launching via acp 之间。

## Bug B (FIXED): a2a_task.py 缺少 import re
line 157/161 使用 re.sub/re.match 但文件顶部无 import re。已修复。

## Bug C: ACP bridge session 结束通知不可靠
AI session 正常结束但 supervisor 收不到 ai_cycle_finished → 90s stall timeout 误判 → recovery kill bridge → restart loop

## Bug D: 重启循环无退避
manager_launch_requested decision=none 每 11s 无限重试
