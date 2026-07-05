# IBM Brainstorm - pretests-adequacy-item-schema-materialization-governance

## Core framing

这条 owner 解决的是“如何 machine-readably 判断跑够了”，不是“再提醒一次测试很重要”。

## Candidate implementation shape

### A. Schema

- 保留五个最小必填字段
- 新增 `surface_kind`、`target_lane`、`promotion_gate`、`task_refs`、`case_design`

### B. Enforcement

- 先 warning
- 再对新 owner hard-gate
- 最后只对 develop-bound promotion 核心字段 selective harden

## Risks

- 不能一刀切打爆历史 owner
- 不能让 richer schema 漂成模板化废话
- 不能把 launch gate 或 retirement gate scope 混进来
