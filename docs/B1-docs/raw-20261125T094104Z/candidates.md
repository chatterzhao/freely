---
candidate_id: C-20261125T094104Z-A
status: promoted
source_raw: raw-20261125T094104Z
created_at: 2026-11-25
milestone: M-20261125T094104Z-A
---

# Candidates

## C-20261125T094104Z-A: pr-merge issue-sync push 回执 fail-closed

- candidate_format_version: v2
- title: 逐 remote push 源分支并汇总失败，消除虚假成功回执
- status: promoted
- promoted_issue_path: docs/B2-docs/worktree-lifecycle/pr-merge-push-receipt/raw-20261125T094104Z/issues/I-20261125T094104Z-A.md
- milestone: M-20261125T094104Z-A
- decision_reason: 同文件 develop-push 段已有逐 remote 校验范式，issue-sync 段用 push all + || true + 无条件回执，是实现偏差；#4699 合并现场实证 github 源分支落后一个 commit 而回执未报失败
- next_action: 修改 pr-merge-guarded 的 _sync_issues_changed_in_merge push 块 → B2 → RED → dev → GREEN → PR
- revisit_trigger: 若 develop-push 段范式变更需同步
- acceptance_criteria:
  - 逐 configured platform（跳过 all）push 源分支
  - 汇总每个 remote 结果，失败 remote 列入 failed_remotes
  - 任一失败 → 非零退出 + 可操作重试命令，不打印无条件 "pushed"
  - 成功回执区分各 remote 状态
- promotion_gate: B1 brainstorms 含 B0 四行 + 四问 + 方案评估，判定为实现偏差
- open_questions: []
