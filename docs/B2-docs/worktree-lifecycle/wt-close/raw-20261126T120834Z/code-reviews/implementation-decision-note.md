---
issue_id: I-20261126T120834Z-A
issue_path: docs/B2-docs/worktree-lifecycle/wt-close/raw-20261126T120834Z/issues/I-20261126T120834Z-A.md
phase_state: done_b2_ibm
---

# Implementation Decision Note

- issue_id: I-20261126T120834Z-A
- issue_path: docs/B2-docs/worktree-lifecycle/wt-close/raw-20261126T120834Z/issues/I-20261126T120834Z-A.md
- decision: 退役门禁删除自造 HEAD 相等判据，以 `test-evidence.py validate --json` 的 `ok` 为唯一新鲜度判据。
- why_this: #4703 已定义 current/equivalent/stale 三态，退役门禁是遗漏的消费者；两套判据对同一份证据给出相反结论。
- alternatives_considered: 在退役门禁复制 equivalent 判据（第二真源，否）；强制所有提交重跑（吞吐损失，否）。
- boundary_non_goals: 不改 `test-evidence.py`，不改敏感路径与 HARD_EXCLUDED，不改其他门禁。
- residual_risk: 旧工作树若已在 gate 文件中写入 EQUIVALENCE_CHAIN，行为立即变化；这是修复的目标语义。
