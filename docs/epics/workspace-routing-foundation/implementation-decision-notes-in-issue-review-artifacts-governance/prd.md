# PRD: implementation-decision-notes-in-issue-review-artifacts-governance

## Goal

把 dev-loop 中的关键实现取舍固定到 issue-bound review artifact 中，并让 develop-bound merge gate 在缺失该 decision note 时直接拒绝，从而把 Freely 的 `proof of thoughtfulness` 延伸到实现 closeout。

## Why Now

- candidate / PRD thoughtfulness 已经在 Freely 中冻结，但 implementation closeout 还缺一层 owner-bound explanation surface
- 当前 `governance-merge-gate` 已能解析 candidate / issue / progress / review 关系，继续补这条 gate 的成本最小
- 用户已经明确要求这层能力不能只靠 laws / skill 自觉，而要能被 gate 发现偏航

## Product Surface

- issue-bound `code-reviews/` / verification artifacts
- `docs/LAWS.md`
- `skill:dev-loop-execution`
- `doc-ibm-execution` issue materialization checklist
- `docs/system/workspace/scripts/quality/governance-merge-gate`

## Non-Goals

- 不新增独立 decision-summary 目录
- 不去评判 prose 的优雅程度或思考深度
- 不要求 research-only / IBM-only / milestone-only 变更也写 implementation decision note
- 不把 `prd.md` 重新变成实现日志

## Non-Negotiables

1. canonical landing surface 必须只有一个：issue-bound review artifact
2. gate 必须通过 owner issue 关联 review artifact，而不是做全仓自由扫描
3. decision note 必须表达 implementer 的选择、取舍、边界和残余风险，而不是简单复述“改了什么”
4. 这层 contract 必须复用现有生命周期真源，不新增平行 truth system

## Context Pack

### Current truth

- candidate v2 已要求 `acceptance_criteria`、`promotion_gate`、`open_questions`、`acceptance_reviews`
- issue / PRD / pre-tests 已能冻结 issue-level acceptance
- `governance-merge-gate` 已能把 staged review artifact 解析回 owner issue
- 但 review artifact 目前只要求 `issue_id` 可解析，不要求 implementation decision note

### Gap

- future reviewer / worker 可以看到 code diff，却不一定能从 canonical artifacts 恢复 implementation choice 的原因与放弃项
- 当 implementation drift 发生时，系统无法区分“有 review artifact”与“有 thoughtfulness-bearing review artifact”

## Decomposition Tree

### D1. Contract freeze

- 明确 canonical landing surface
- 明确最小字段
- 明确何时强制

### D2. Authoring truth

- laws 写明 must
- skill / checklist 写明 how

### D3. Enforcement

- merge gate 识别 implementation-bearing diff
- merge gate 通过 owner issue 找到正确 review artifact
- merge gate 校验 note 结构

### D4. Regression proof

- 为缺 review artifact、缺 note、完整 note 三类情况各加回归

## Prototype Path

先以 `governance-merge-gate` 为唯一 enforcement 面：

1. 在测试仓中 staged 一个 `src/` 变更和 owner issue
2. 不提供 review artifact，确认 fail
3. 提供 review artifact 但不写完整 decision note，确认 fail
4. 补齐 decision note 五个字段，确认 pass

## Eval Plan

### Success

- implementer 只需在 owner issue 的 review artifact 中写一份短 decision note
- future reviewer 可以直接从 verification artifact 恢复关键设计取舍
- gate 能发现“有实现变更但没写 decision note”的偏航

### Failure

- gate 仍允许 implementation-bearing diff 在没有 decision note 时通过
- note 结构过于模糊，导致字段缺失却无法机器发现
- 规则要求在多个地方重复写 decision summary，形成新形式主义

### Regression risk

- implementation-bearing path detection 过宽，导致纯文档 / governance prose 也被误拦
- detection 过窄，导致实际 capability 改动逃过 gate
- author 只写占位语句，未来还需要补更强质量 heuristics

## Execution Slices

1. 写入 pre-brainstorm / candidate / issue truth
2. 更新 laws / dev-loop skill / IBM checklist
3. 实现 merge-gate owner-bound note enforcement
4. 为 merge gate 添加 focused regression coverage

## Revisit Triggers

- 如果 field usage 显示 capability path detection 误报频繁
- 如果 review artifact 的五字段仍不足以恢复关键取舍
- 如果未来需要区分“实现 decision note”与“verification conclusion”两个不同 reviewer role

## Dev-Loop Handoff

- implementer 在 develop-bound materialization 时优先打开当前 issue 的 `verification_artifact_dir`
- 在 staged review artifact 中写 `## Implementation Decision Note`
- 保持上游 candidate / PRD / pre-tests 不重复，只在 `why_this` / `boundary_non_goals` 中引用上游边界
