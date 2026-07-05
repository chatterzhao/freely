---
local_id: I-20260326-1915
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '59'
    url: https://github.com/chatterzhao/freely/issues/59
    synced_at: '2026-04-27T11:17:45Z'
  gitee:
    issue_id: IJFO6U
    url: https://gitee.com/zhaoquan/freely/issues/IJFO6U
    synced_at: '2026-04-27T13:15:04Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/deep-refactor-fleet-sequencing-governance/issues/deep-refactor-fleet-sequencing-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:17:45Z'
hash: ''
created_at: '2026-04-27T11:17:45Z'
updated_at: '2026-04-27T11:17:45Z'
platform_state: closed
---

Freely 在准备 broad/deep refactor 时，真实 fleet 一度同时存在：

- canonical `develop` runtime 标成 `desired=running`，但实际 `stalled_without_runtime`
- develop-facing merge-prep 工位仍是 `dirty + desired=running`
- 多棵 clean/stopped 上游治理树已经形成新 contract，却还没有先后顺序

如果不先冻结“大重构前先做 fleet sequencing audit”的开发治理规则，就会把 closeout、runtime 健康判断、upstream merge、以及新的重构实现混在一起，导致 owner、依赖和 cleanup judgement 继续失真。

canonical: docs/epics/workspace-routing-foundation/deep-refactor-fleet-sequencing-governance/issues/deep-refactor-fleet-sequencing-governance.md
