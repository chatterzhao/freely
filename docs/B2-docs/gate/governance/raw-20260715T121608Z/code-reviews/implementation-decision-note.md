---
issue_id: I-20260715T121608Z-A
issue_path: docs/B2-docs/gate/governance/raw-20260715T121608Z/issues/I-20260715T121608Z-A.md
phase_state: completed
---

- issue_id: I-20260715T121608Z-A
- issue_path: docs/B2-docs/gate/governance/raw-20260715T121608Z/issues/I-20260715T121608Z-A.md

## Implementation Decision Note

- decision: 按证据收敛 16 处历史状态（3 I-* completed 附 merge 实证 + 13 legacy raw absorbed 附平台实测）；6 个显式留档不动（3 无 merge 证据 + 3 有实证但 RED-GREEN/tasks 历史欠账未清、被 pretests-gate 实拦）
- why_this: 状态真源只能跟证据走；07-15 scanner 计数（15/13）与今日现状的差额已被日常 lane 消化，如实按今日证据收敛
- alternatives_considered: 按 07-15 清单盲改（部分已收敛、部分无证据，否）；等 runtime worker 处理（已实测 worker ACP init 超时且无产出移除工位，否）
- boundary_non_goals: 不动无 merge 证据的 3 个 legacy I-*；不修 worker ACP init 超时缺陷（另案跟进）
- residual_risk: absorbed 无 I-* 锚的 13 个 raw 若未来 gate 收紧需 archive 线补锚；3 个欠账 I-* 的历史 RED-GREEN 补章属欠账治理线 scope，本 lane 不代偿
