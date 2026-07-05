---
local_id: I-20260321-1745
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '39'
    url: https://github.com/chatterzhao/freely/issues/39
    synced_at: '2026-04-27T11:15:49Z'
  gitee:
    issue_id: IJFO62
    url: https://gitee.com/zhaoquan/freely/issues/IJFO62
    synced_at: '2026-04-27T13:14:35Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/active-lifecycle-boundary-and-dogfooding-capability-discovery/issues/active-lifecycle-boundary-and-dogfooding-capability-discovery.md
last_synced_comment_at:
  github: '2026-04-27T11:15:49Z'
hash: ''
created_at: '2026-04-27T11:15:49Z'
updated_at: '2026-04-27T11:15:49Z'
platform_state: closed
---

Freely 当前仍缺少一条稳定的生命周期边界语义，导致团队会反复争论：

- 什么算“历史”？
- 什么算“当前仍可修改的真源”？
- Freely 在狗粮中暴露出来的问题，应视为一次性项目经验，还是优先判断为 Freely 产品能力缺口？

如果这层边界不固定，后续会不断出现两类错误：

- 把仍在活跃生命周期里的 issue/worktree 错当历史，过早冻结真源
- 把已完成且已收口的历史产物继续当当前承接面回写，破坏追溯性

同时，Freely 开发 Freely 时暴露出的共性问题也会继续停留在聊天或 continuity 里，而不是 materialize 成用户也能复用的能力。

canonical: docs/B2-docs/ibm/active-lifecycle-boundary-and-dogfooding-capability-discovery/issues/active-lifecycle-boundary-and-dogfooding-capability-discovery.md
