---
local_id: raw-20260716T040152Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260716T040152Z-A
platform_ids:
  github:
    issue_id: '3932'
    url: https://github.com/chatterzhao/freely/issues/3932
    synced_at: ''
  gitee:
    issue_id: IK1EIW
    url: https://gitee.com/zhaoquan/freely/issues/IK1EIW
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-16T04:02:15Z'
updated_at: '2026-07-16T04:02:15Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 问题概述

研究 Freely agent 编排全链路后发现多处缺陷。最严重的是 a2a-exit 缺少 --reason 参数，导致 Reviewer 调度链路完全断裂。

## Bug 1 (CRITICAL)
a2a_task.py a2a-exit argparse 没有 --reason 参数。Worker 调 a2a-exit --state input-required --reason needs-review:b1 时，reason 被 parse_known_args() 静默丢弃。SSE event 无 reason → watchdog 路由到 UNKNOWN → Reviewer 永远不会被调度。

## 其他 Bug
- Reviewer 调度双路径竞态 (watchdog_sse.py vs freely-cycle)
- agent_assign(update_only=True) 静默失败
- a2a-exit 不在 PATH (bin/ 下无 wrapper)
- 零端到端集成测试覆盖

详见 docs/B1-docs/raw-20260716T035829Z/issue.md
