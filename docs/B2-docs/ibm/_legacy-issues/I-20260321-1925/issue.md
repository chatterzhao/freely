---
local_id: I-20260321-1925
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '41'
    url: https://github.com/chatterzhao/freely/issues/41
    synced_at: '2026-04-27T11:16:01Z'
  gitee:
    issue_id: IJFO65
    url: https://gitee.com/zhaoquan/freely/issues/IJFO65
    synced_at: '2026-04-27T13:14:38Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/manager-chat-reentry-and-cleanup-misrouting-governance/issues/manager-chat-reentry-and-cleanup-misrouting-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:16:01Z'
hash: ''
created_at: '2026-04-27T11:16:01Z'
updated_at: '2026-04-27T11:16:01Z'
platform_state: closed
---

Freely 当前已经有：

- `chat -> intake -> interruption dispatcher`
- cleanup followthrough worker
- 主管巡检与 restart-point routing 的方法论真源

但真实集成测试显示：
- 当用户通过 chat 发起广义主管巡检任务时
- interruption manager triage 仍可能把它错误解释为 cleanup followthrough
- 结果是新的 supervisor-level signal 没回到 manager continuation，而是直接吸收到旧 cleanup continuity

canonical: docs/B2-docs/ibm/manager-chat-reentry-and-cleanup-misrouting-governance/issues/manager-chat-reentry-and-cleanup-misrouting-governance.md
