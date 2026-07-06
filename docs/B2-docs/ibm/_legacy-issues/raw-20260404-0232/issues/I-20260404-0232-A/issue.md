---
local_id: I-20260404-0232-A
kind: linked
phase_state: absorbed
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260404-0232/code-reviews
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '98'
    url: https://github.com/chatterzhao/freely/issues/98
    synced_at: '2026-04-27T11:23:32Z'
  gitee:
    issue_id: IJFO8B
    url: https://gitee.com/zhaoquan/freely/issues/IJFO8B
    synced_at: '2026-04-27T13:16:08Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/gate/governance-merge-gate-review-aware-regression-alignment-governance/issues/governance-merge-gate-review-aware-regression-alignment-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:23:32Z'
hash: ''
created_at: '2026-04-27T11:23:32Z'
updated_at: '2026-06-21T15:21:44Z'
platform_state: closed
---

`test-governance-merge-gate` still carries a mixed unresolved-candidate implementation case from before staged owner review artifacts became mandatory. Once `I-20260401-2354-A` landed, that fixture started failing earlier on missing review evidence.

Reproducing the current path shows the canonical contract is different from the old expectation: unresolved `needs_research` candidate metadata repairs are allowed to travel inside the same governance owner line when the merge already carries same-l

canonical: docs/B2-docs/gate/governance-merge-gate-review-aware-regression-alignment-governance/issues/governance-merge-gate-review-aware-regression-alignment-governance.md
