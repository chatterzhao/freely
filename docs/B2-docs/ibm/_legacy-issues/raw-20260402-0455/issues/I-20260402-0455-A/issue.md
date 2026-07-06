---
local_id: I-20260402-0455-A
kind: linked
phase_state: absorbed
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260402-0455/code-reviews
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '91'
    url: https://github.com/chatterzhao/freely/issues/91
    synced_at: '2026-04-27T11:22:51Z'
  gitee:
    issue_id: IJFO7Y
    url: https://gitee.com/zhaoquan/freely/issues/IJFO7Y
    synced_at: '2026-04-27T13:15:54Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/git-worktree/worktree-exclusive-ownership-and-promotion-lease-governance/issues/worktree-exclusive-ownership-and-promotion-lease-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:22:51Z'
hash: ''
created_at: '2026-04-27T11:22:51Z'
updated_at: '2026-05-17T12:22:01Z'
platform_state: closed
---

Freely 已经有 manager-first worker scheduling、fleet patrol、hygiene alert、cleanup followthrough、issue-bound merge gate 和 PID/session ownership 校验，但这些真相之间还缺一个长期可消费的 ownership surface：

1. launch-time scheduling truth
   - `dispatch_priority`
   - `parallel_safe`
   - `write_scope`
2. occupancy-ish truth
   - `supervisor.pid`
   - `ai.pid`
   - session/jsonl evidence
3. missing lifecycle ownership truth
   - 谁此刻拥有 `edit`
   - 谁此刻拥有 `cleanup`
   - 谁此刻拥有 `promotion`

没有第 3 层，就仍会出现多 AI 同树双写、重复 cleanup、以及

canonical: docs/B2-docs/git-worktree/worktree-exclusive-ownership-and-promotion-lease-governance/issues/worktree-exclusive-ownership-and-promotion-lease-governance.md
