---
local_id: I-20260405-2358-A
kind: linked
phase_state: completed
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260405-2358/code-reviews
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: "2026-05-19T23:20:00Z"
platform_ids:
  github:
    issue_id: '115'
    url: https://github.com/chatterzhao/freely/issues/115
    synced_at: '2026-04-27T11:25:15Z'
  gitee:
    issue_id: IJFO8W
    url: https://gitee.com/zhaoquan/freely/issues/IJFO8W
    synced_at: '2026-04-27T13:16:35Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/config/packaging/raw-20260402-0403issues/fresh-project-bootstrap-and-baseline-scoping-followthrough-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:25:15Z'
hash: ''
created_at: '2026-04-27T11:25:15Z'
updated_at: '2026-05-17T08:01:49Z'
platform_state: closed
---

Upgraded `memark 0.1.1` replay showed canonical Freely root still missed one narrow bootstrap prerequisite:

1. MemArk now requires `.memark/` and `corpus/` to be ignored before `memark init` can run at the main repository root.
2. Canonical Freely root previously did not ignore those paths, so the new guidance correctly rejected root init there.
3. Linked Freely worktrees were already using MemArk successfully, which means the remaining defect is bootstrap metadata at the protected root, not th

canonical: docs/B2-docs/config/packaging/raw-20260402-0403issues/memark-protected-root-bootstrap-followthrough-governance.md
