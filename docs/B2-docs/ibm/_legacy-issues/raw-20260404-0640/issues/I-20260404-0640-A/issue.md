---
local_id: I-20260404-0640-A
kind: linked
phase_state: absorbed
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260404-0640/code-reviews
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '99'
    url: https://github.com/chatterzhao/freely/issues/99
    synced_at: '2026-04-27T11:23:39Z'
  gitee:
    issue_id: IJFO8C
    url: https://gitee.com/zhaoquan/freely/issues/IJFO8C
    synced_at: '2026-04-27T13:16:10Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/protected-branch-merge-receipt-gap-followthrough/issues/protected-branch-merge-receipt-gap-followthrough.md
last_synced_comment_at:
  github: '2026-04-27T11:23:39Z'
hash: ''
created_at: '2026-04-27T11:23:39Z'
updated_at: '2026-06-21T15:21:46Z'
platform_state: closed
---

Freely 已经要求 protected-branch merge 写 canonical receipt trailer，也已经对 break-glass merge 建好了 ledger parity audit。但 `develop` ancestry 里仍然出现了一个普通 guarded merge `908a6ad` 没有任何 canonical trailer。当前 `governance-check` 没有对应 ancestry audit，也没有普通 merge 的 backfill 真源，因此这类 gap 只能靠人工 review 暴露。

canonical: docs/B2-docs/ibm/protected-branch-merge-receipt-gap-followthrough/issues/protected-branch-merge-receipt-gap-followthrough.md
