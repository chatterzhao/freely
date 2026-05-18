---
local_id: I-20260321-1835-A
kind: linked
phase_state: absorbed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '40'
    url: https://github.com/chatterzhao/freely/issues/40
    synced_at: '2026-04-27T11:15:56Z'
  gitee:
    issue_id: IJFO64
    url: https://gitee.com/zhaoquan/freely/issues/IJFO64
    synced_at: '2026-04-27T13:14:37Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/develop-merge-issue-binding-and-cmi-governance/issues/develop-merge-issue-binding-and-cmi-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:15:56Z'
hash: ''
created_at: '2026-04-27T11:15:56Z'
updated_at: '2026-05-17T12:20:47Z'
platform_state: closed
---

当前 develop merge gate 已经修掉了 hook 时序缺口，但还存在第二层漏洞：

- merge diff 里只要带一个 `status: absorbed` 的候选
- 且它的 `promoted_issue_path` 指向仓库里某个存在的 owner issue
- gate 就可能把它当成 develop merge 的充分治理证据

这不够。develop-bound implementation merge 必须先绑定到一个具体 issue，再验证这一条 issue 的 `C/M/I` 链是否完整、candidate 状态是否属于允许放行的少数状态。否则可以拿不相干的 owner issue 借道过门禁。

本轮又确认了第三层缺口：即便 merge diff 已经绑定到一个真实 owner issue，gate 仍可能放过两类不完整 execution merge：

- capability / implementation 变更由 `in_ibm` / `done_ibm` / `completed` issue 挂名
- capability / i

canonical: docs/epics/workspace-routing-foundation/develop-merge-issue-binding-and-cmi-governance/issues/develop-merge-issue-binding-and-cmi-governance.md
