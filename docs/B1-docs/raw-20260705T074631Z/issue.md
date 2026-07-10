---
local_id: raw-20260705T074631Z31Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260705T074631Z-A
platform_ids:
  github:
    issue_id: '3746'
    url: https://github.com/chatterzhao/freely/issues/3746
    synced_at: ''
  gitee:
    issue_id: IJYUG4
    url: https://gitee.com/zhaoquan/freely/issues/IJYUG4
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-05T07:46:56Z'
updated_at: '2026-07-05T07:46:56Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

\n\n## 问题
_rotate_log 只覆盖 a2a-server.log。db-daemon.log、watchdog-sse.log、lifecycle-trace.log、runtime-events.log 均无 rotation。

## 修复
_rotate_log 扩展到覆盖全部 5 个持续写入日志：启动时 rotate + 主循环定期检查。
