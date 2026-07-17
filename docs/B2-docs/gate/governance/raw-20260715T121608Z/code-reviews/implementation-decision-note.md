---
issue_id: I-20260715T121608Z-A
issue_path: docs/B2-docs/gate/governance/raw-20260715T121608Z/issues/I-20260715T121608Z-A.md
phase_state: completed
---

- issue_id: I-20260715T121608Z-A
- issue_path: docs/B2-docs/gate/governance/raw-20260715T121608Z/issues/I-20260715T121608Z-A.md

## Implementation Decision Note

- decision: GATE 1 两轮实拦证明跨 raw 批量收敛在现行门禁无合规单工位通道——本 lane 转型为取证交付（证据包 A3+B13+C6+D1）+ 能力缺口立案移交；不绕过、不逐 key 空转 16 个仪式 lane
- why_this: 状态真源只能跟证据走；07-15 scanner 计数（15/13）与今日现状的差额已被日常 lane 消化，如实按今日证据收敛
- alternatives_considered: 按 07-15 清单盲改（部分已收敛、部分无证据，否）；等 runtime worker 处理（已实测 worker ACP init 超时且无产出移除工位，否）
- boundary_non_goals: 不动无 merge 证据的 3 个 legacy I-*；不修 worker ACP init 超时缺陷（另案跟进）
- residual_risk: 16 项漂移在 batch-reconcile 能力落地前持续存在（证据包保鲜:全部锚为 immutable commit/平台终态）；能力立案若被判 overkill,fallback=逐 key 工位分批
