---
local_id: I-20260405-0425-A
kind: linked
phase_state: absorbed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '104'
    url: https://github.com/chatterzhao/freely/issues/104
    synced_at: '2026-04-27T11:24:04Z'
  gitee:
    issue_id: IJFO8I
    url: https://gitee.com/zhaoquan/freely/issues/IJFO8I
    synced_at: '2026-04-27T13:16:18Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/develop-guarded-merge-entrypoint-enforcement-governance/issues/develop-guarded-merge-entrypoint-enforcement-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:24:04Z'
hash: ''
created_at: '2026-04-27T11:24:04Z'
updated_at: '2026-05-17T12:22:41Z'
platform_state: closed
---

Freely 已经有 `freely pr-merge-guarded` 作为 merge 真源，但 `develop` 上的 `pre-merge-commit` 仍允许“没有 canonical guarded handshake 的 merge”继续走后续 gate。结果是：

1. 手工裸 `git merge` 与仓库自有 `freely pr-merge-guarded` 入口并存。
2. 只要 staged merge 内容满足 governance / promotion gate，裸 merge 仍能落地。
3. 这类误用又会在 protected branch 上制造新的治理偏差，并且让人类和 agent 在两个 merge 入口之间来回误用。

canonical: docs/epics/workspace-routing-foundation/develop-guarded-merge-entrypoint-enforcement-governance/issues/develop-guarded-merge-entrypoint-enforcement-governance.md
