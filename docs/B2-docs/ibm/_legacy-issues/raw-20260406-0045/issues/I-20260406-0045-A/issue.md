---
local_id: I-20260406-0045-A
kind: linked
phase_state: completed
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260406-0045/code-reviews
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: "2026-05-19T23:20:00Z"
platform_ids:
  github:
    issue_id: '118'
    url: https://github.com/chatterzhao/freely/issues/118
    synced_at: '2026-04-27T11:25:33Z'
  gitee:
    issue_id: IJFO90
    url: https://gitee.com/zhaoquan/freely/issues/IJFO90
    synced_at: '2026-04-27T13:16:39Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/gate/governance-check-protected-merge-history-source-policy-governance/raw-20260406-0045issues/governance-check-protected-merge-history-source-policy-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:25:33Z'
hash: ''
created_at: '2026-04-27T11:25:33Z'
updated_at: '2026-05-17T12:23:14Z'
platform_state: closed
---

一次真实的 `feature/* -> test-pre-merge-* -> develop` promote 后，`./bin/governance-check` 在 canonical `develop` 上误报：

1. 它把 `test-pre-merge-*` 批次内部的 merge commit 也当成了 `develop` 的 protected merge 历史。
2. 因此 `Freely-Source-Branch: feature/*` 在 batch 内是合法的，却被拿到 `develop` 的规则下重新校验。
3. 结果是有效的 guarded merge 刚完成，post-merge followthrough 反而立即失败。

canonical: docs/B2-docs/gate/governance-check-protected-merge-history-source-policy-governance/raw-20260406-0045issues/governance-check-protected-merge-history-source-policy-governance.md
