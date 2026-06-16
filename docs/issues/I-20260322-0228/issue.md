---
local_id: I-20260322-0228
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '46'
    url: https://github.com/chatterzhao/freely/issues/46
    synced_at: '2026-04-27T11:16:31Z'
  gitee:
    issue_id: IJFO6C
    url: https://gitee.com/zhaoquan/freely/issues/IJFO6C
    synced_at: '2026-04-27T13:14:44Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/manager-delegation-after-sufficient-patrol-evidence-governance/issues/manager-delegation-after-sufficient-patrol-evidence-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:16:31Z'
hash: ''
created_at: '2026-04-27T11:16:31Z'
updated_at: '2026-04-27T11:16:31Z'
platform_state: closed
---

真实 Freely dogfood 已经证明主管能够：

- 接住 `freely chat` 的项目级监督请求
- patrol 全部剩余 worktree
- 正确判断 disposition，如 `retire-only` / `retire-now` / `continue-dev`
- 并行调用 subagent 收集证据
- 写出新的 manager continuity

但这次也暴露出新的 gap：

- 当证据已经足够支持下一步执行时，主管仍继续做更多只读核查
- 没有及时切换到具体 worker handoff / cleanup execution

因此这条 issue 的目标不是增强 patrol，而是为主管补上：

- `sufficient patrol evidence`
- `delegation threshold`
- `stop patrolling and delegate`

的硬性治理语义。

canonical: docs/epics/workspace-routing-foundation/manager-delegation-after-sufficient-patrol-evidence-governance/issues/manager-delegation-after-sufficient-patrol-evidence-governance.md
