---
local_id: I-20260322-0245
kind: linked
phase_state: dropped
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260322-0245/code-reviews
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '47'
    url: https://github.com/chatterzhao/freely/issues/47
    synced_at: '2026-04-27T11:16:38Z'
  gitee:
    issue_id: IJFO6E
    url: https://gitee.com/zhaoquan/freely/issues/IJFO6E
    synced_at: '2026-04-27T13:14:47Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/runtime/runtime-worker-launch-linkage-and-stall-recovery-governance/issues/runtime-worker-launch-linkage-and-stall-recovery-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:16:38Z'
hash: ''
created_at: '2026-04-27T11:16:38Z'
updated_at: '2026-04-27T11:16:38Z'
platform_state: closed
---

Freely 最新 dogfood 证明：

- manager 已能 patrol 并稳定产出 `retire-only / continue-dev`
- manager 已能写出 worker launch order 与 worker prompt artifact

但 runtime 还缺少两条关键能力：

1. 没有把这些 manager-generated worker handoff 转成目标 worker worktree 的实际执行
2. 长时间无输出且有待处理 intake 的 AI 进程不会被 runtime 识别成 stall 并恢复

因此 current gap 已经不在 manager prompt 语义，而在 runtime control plane。

canonical: docs/B2-docs/runtime/runtime-worker-launch-linkage-and-stall-recovery-governance/issues/runtime-worker-launch-linkage-and-stall-recovery-governance.md
