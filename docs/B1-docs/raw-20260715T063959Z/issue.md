---
local_id: raw-20260715T063959Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260715T063959Z-A
platform_ids:
  github:
    issue_id: '3906'
    url: https://github.com/chatterzhao/freely/issues/3906
    synced_at: ''
  gitee:
    issue_id: IK16N5
    url: https://gitee.com/zhaoquan/freely/issues/IK16N5
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-15T06:40:24Z'
updated_at: '2026-07-15T06:40:24Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 根因
AI_MODE（Claude AI 交互姿态）和 task_mode（daemon 运行模式）是两个不同变量。前者只有 auto/step 两个有效值。aimode-hotfix2 错误地将 ${AI_MODE:-auto} 改为 ${AI_MODE:-wait}，导致 --mode wait 传给 Claude，start-lead-agent.sh 报 unsupported mode，AI 永远 tool_unproductive。

## 修复
6 处 ${AI_MODE:-wait} → ${AI_MODE:-auto}。保留 3 处 ${AI_MODE:-none} 守卫（log 行不需要有效 mode 值）。
task_mode 默认值 wait 不受影响。
