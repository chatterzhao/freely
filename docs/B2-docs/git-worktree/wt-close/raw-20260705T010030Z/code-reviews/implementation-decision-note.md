---
issue_id: I-20260705T010030Z-A
issue_path: docs/epics/worktree-close/rawkey-unify/raw-20260705T010030Z/issues/I-20260705T010030Z-A.md
phase_state: done_b2_ibm
---
- issue_id: I-20260705T010030Z-A
- issue_path: docs/epics/worktree-close/rawkey-unify/raw-20260705T010030Z/issues/I-20260705T010030Z-A.md
## Implementation Decision Note
- decision: wt-close 去掉 --branch，改为 --raw-key 唯一入口
- why_this: 消除分支名传入路径，统一为 raw key 驱动
- alternatives_considered: 保留 --branch 作为别名 → 增加维护负担
- boundary_non_goals: 不改变关闭逻辑和 gate 行为
- residual_risk: 无
