---
issue_id: I-20261103T121047Z-A
issue_path: docs/B2-docs/worktree-lifecycle/merge-guard-issue-sync-scope/raw-20261103T121047Z/issues/I-20261103T121047Z-A.md
phase_state: completed
---

- issue_id: I-20261103T121047Z-A
- issue_path: docs/B2-docs/worktree-lifecycle/merge-guard-issue-sync-scope/raw-20261103T121047Z/issues/I-20261103T121047Z-A.md

## Implementation Decision Note

- decision: 把 merge-time 同步范围收敛为分支 raw key；过滤抽纯函数单测。Gitee reopen 复用 close 的 legacy 请求形态。
- why_this: 事故根因是 diff 全量文档被当作生命周期推进；按 key 收敛最小且不改变正常 lane 行为。
- alternatives_considered: 跳过 merge issue-sync（丢失正常收口）；只处理 absorbed 文档（无法区分治理数据）。
- boundary_non_goals: 不新增平台写、不改 scan/gate；不批量补历史 issue。
- residual_risk: 若未来一个 lane 需要收口多个 raw issue，必须显式 issue-sync close，而不是依赖 merge diff；已在 candidate revisit_trigger 记录。
