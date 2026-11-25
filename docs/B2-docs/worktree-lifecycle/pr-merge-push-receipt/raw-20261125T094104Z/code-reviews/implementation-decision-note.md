---
issue_id: I-20261125T094104Z-A
issue_path: docs/B2-docs/worktree-lifecycle/pr-merge-push-receipt/raw-20261125T094104Z/issues/I-20261125T094104Z-A.md
phase_state: completed
---

- issue_id: I-20261125T094104Z-A
- issue_path: docs/B2-docs/worktree-lifecycle/pr-merge-push-receipt/raw-20261125T094104Z/issues/I-20261125T094104Z-A.md

# Implementation Decision Note: I-20261125T094104Z-A

- decision: 仅改 `_sync_issues_changed_in_merge` 的 push 块，逐 configured remote（跳过 all）push 源分支并汇总结果；失败 → 非零 + failed_remotes + 重试命令，成功 → 逐 remote 回执。不抽公共 helper、不动 develop-push 段。
- why_this: 同文件 develop-push 段（:401-423）已是正确范式，对齐它改动最小、语义一致；抽 helper 会触碰已稳定代码增加回归面，本轮不值。
- alternatives_considered: ① 删 `|| true` 保留 push all——多 pushurl 无法定位失败平台，否决；② 抽公共 helper——触碰 develop-push 段，回归面大，否决；③ 失败回滚 commit——过度设计，否决。
- boundary_non_goals: 不改 develop-push 段、不改 pr-create/pr-review、不改 adapter、不改 wt-close；保留自动 push 必要性。
- residual_risk: 若未来 develop-push 段范式变更，两处需同步；本轮接受，另议 helper 抽取。
