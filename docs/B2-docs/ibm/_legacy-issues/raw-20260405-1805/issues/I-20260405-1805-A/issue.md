---
local_id: I-20260405-1805-A
kind: linked
phase_state: absorbed
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260405-1805/code-reviews
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '111'
    url: https://github.com/chatterzhao/freely/issues/111
    synced_at: '2026-04-27T11:24:42Z'
  gitee:
    issue_id: IJFO8R
    url: https://gitee.com/zhaoquan/freely/issues/IJFO8R
    synced_at: '2026-04-27T13:16:29Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/gate/test-pre-merge-family-promotion-gate-enforcement-governance/raw-20260405-1805issues/test-pre-merge-family-promotion-gate-enforcement-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:24:42Z'
hash: ''
created_at: '2026-04-27T11:24:42Z'
updated_at: '2026-06-21T15:21:49Z'
platform_state: closed
---

`I-20260405-1615-A` 已经把新的 promote model 冻结成正式 owner，但当前仓库执行的仍是旧规则：

1. `CONSTITUTION` / `LAWS` / `pre-test-merge-flow.md` 仍允许或默认 `feature/* -> develop`。
2. `pr-merge-guarded` tests 仍阻止 `test-pre-merge-* -> develop`。
3. 如果只改文档不改 gate，或者只改 gate 不改文档，就会在同一时间保留两套互相冲突的合法路径。

因此这条 owner 的职责不是重新研究 promote model，而是把新模型接到治理真源和 protected-branch gate 上，并让 regression tests 一起对齐。

canonical: docs/B2-docs/gate/test-pre-merge-family-promotion-gate-enforcement-governance/raw-20260405-1805issues/test-pre-merge-family-promotion-gate-enforcement-governance.md
