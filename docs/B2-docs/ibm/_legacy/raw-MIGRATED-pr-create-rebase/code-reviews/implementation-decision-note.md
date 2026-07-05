---
issue_id: I-20260625T131154Z-A
issue_path: docs/issues/I-20260625T131154Z-A/issue.md
phase_state: done_b2_ibm
---

- issue_id: I-20260625T131154Z-A
- issue_path: docs/issues/I-20260625T131154Z-A/issue.md

## Implementation Decision Note

- decision: pr-create-guarded Step 3 从 git merge 改为 git rebase，push 加 --force-with-lease
- why_this: rebase 逐 commit 重放不会产生跨 scope 大 commit，避免 checkpoint-guard 拦截
- alternatives_considered: 修改 checkpoint-guard 豁免 merge commit → 治标不治本，rebase 更干净
- boundary_non_goals: 不改 pr-merge-guarded 的 merge 逻辑
- residual_risk: 首次 rebase 后 push 需 --force-with-lease，已包含在改动中
