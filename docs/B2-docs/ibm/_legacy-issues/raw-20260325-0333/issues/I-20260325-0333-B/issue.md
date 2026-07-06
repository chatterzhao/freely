---
local_id: I-20260325-0333-B
kind: linked
phase_state: dropped
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260325-0333/code-reviews
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '54'
    url: https://github.com/chatterzhao/freely/issues/54
    synced_at: '2026-04-27T11:17:16Z'
  gitee:
    issue_id: IJFO6M
    url: https://gitee.com/zhaoquan/freely/issues/IJFO6M
    synced_at: '2026-04-27T13:14:56Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/story-level-pre-tests-quality-gate-governance/issues/story-level-pre-tests-quality-gate-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:17:16Z'
hash: ''
created_at: '2026-04-27T11:17:16Z'
updated_at: '2026-04-27T11:17:16Z'
platform_state: closed
---

Freely 已经明确 `pre-tests.md` 是 issue-level acceptance 控制面，但还没有冻结 story-level 质量门禁。结果就是：

- `pre-tests.md` 可以“形式存在”，却仍然无法恢复 acceptance contract
- 后续 integration / end-to-end / real-environment 测试即使跑了，也可能建立在不稳定目标上
- completion verification 与 worktree retirement 仍然容易退化成“命令跑过一些、文档也有一份”，而不是“验收定义先站稳”

在更大的 testing evidence ladder 能力完成前，最先必须硬化的是 story-level `pre-tests.md` 质量 gate。

canonical: docs/B2-docs/ibm/story-level-pre-tests-quality-gate-governance/issues/story-level-pre-tests-quality-gate-governance.md
