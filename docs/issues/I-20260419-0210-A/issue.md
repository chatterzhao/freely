---
local_id: I-20260419-0210-A
kind: linked
phase_state: completed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: "2026-05-19T23:20:00Z"
platform_ids:
  github:
    issue_id: '153'
    url: https://github.com/chatterzhao/freely/issues/153
    synced_at: '2026-04-27T11:28:04Z'
  gitee:
    issue_id: IJFOA5
    url: https://gitee.com/zhaoquan/freely/issues/IJFOA5
    synced_at: '2026-04-27T13:17:31Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/protected-branch-ref-only-entrypoint-enforcement-governance/issues/protected-branch-ref-only-entrypoint-enforcement-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:28:04Z'
hash: ''
created_at: '2026-04-27T11:28:04Z'
updated_at: '2026-05-17T12:24:44Z'
platform_state: closed
---

Freely already declares `freely pr-merge-guarded` as the canonical protected-merge entrypoint, but the current enforcement only covers merge-commit creation and merge completion. A real protected-root replay on `2026-04-19` proved that `git merge --ff-only` can still advance `develop` directly to a feature commit because no merge commit is created and `pre-merge-commit` never runs.

That means the protected-branch entrypoint contract is still incomplete.

canonical: docs/epics/workspace-routing-foundation/protected-branch-ref-only-entrypoint-enforcement-governance/issues/protected-branch-ref-only-entrypoint-enforcement-governance.md
