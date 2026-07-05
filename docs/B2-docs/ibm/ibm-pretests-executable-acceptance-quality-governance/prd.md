# PRD: ibm-pretests-executable-acceptance-quality-governance

## Goal

把 Freely 的 IBM `pre-tests.md` 从“integration / acceptance-first”进一步收紧为“默认可执行、可恢复、带真环境与狗粮测试面的 acceptance contract”。

## Why Now

当前真源已经方向正确，但 enforcement 不够强，导致新 issue 仍能在 IBM 阶段写出弱验收。这个缺口已经直接在 `manager-owner-stance-and-source-patrol-governance` 暴露，说明再不收紧，上游能力线会继续在弱验收下推进。

## Product Surface

- `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/prd-quality-bar.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/ibm-completion-gate.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/issue-materialization-checklist.md`

## Non-Goals

- 新测试 runner
- 统一所有 verification review 模板
- 重写所有历史 issue 的 `pre-tests.md`
- 要求每个 issue 都新写自动化脚本

## Non-Negotiables

- 不允许 `pre-tests.md` 仅由 wording review / truth-source reading checks 构成主验收面
- 不允许 `prd.md` 的 `Eval Plan` 脱离环境、证据、失败判据
- 不允许 Freely 自治能力跳过 integration / application-native real-environment / end-to-end dogfood 三类测试面而不说明理由
- 不把 runtime scenario 与 dogfood observation 误降级为“非正式测试”

## Context Pack

- `I-20260322-0135` 已明确 `pre-tests.md` 是 issue-level acceptance 控制面
- 现有真源仍允许弱写法混过去，尤其在治理型 issue 上
- Freely 自治缺口常先在 `freely start`、`freely chat`、manager patrol、worker delegation、status surfaces 中暴露

## Decomposition Tree

1. 收紧 `doc-ibm-execution` 的主规则
2. 收紧 `prd-quality-bar` 的 `Eval Plan` / `pre-tests.md` 派生要求
3. 收紧 `ibm-completion-gate` 的 done-ibm 前提
4. 收紧 `issue-materialization-checklist` 的 materialization 写法

## Prototype Path

最小原型是把上述 IBM 真源改成一致、强约束口径，并用治理检查和样本文档回读验证“无法再自然写出弱验收”。

## Eval Plan

成功：
- IBM 真源明确要求 `pre-tests.md` 先写 executable acceptance contract
- `prd.md` 的 `Eval Plan` 默认先写环境、证据、失败判据、replay expectation
- Freely 自治能力默认需要回答：
  - pre-merge focused regression / smoke
  - post-merge integration acceptance
  - post-merge application-native real-environment acceptance
  - post-merge end-to-end dogfood acceptance
- 若某类不适用，真源要求显式写理由与替代证据

失败：
- 仍能从真源中得出“治理型 issue 主要看 wording review 就够了”
- `pre-tests.md` 仍能不写 environment / evidence / failure signal 而被视为合格
- 真源把 runtime scenario 当成“非正式补充”，而不是 acceptance 的一部分

## Execution Slices

1. `doc-ibm-execution` 主规则
2. `prd-quality-bar`
3. `ibm-completion-gate`
4. `issue-materialization-checklist`
5. lifecycle writeback

## Revisit Triggers

- 当 verification review 模板要被统一结构化
- 当 `pre-tests.md` 需要 machine-readable schema
- 当 protected verification environments 的 evidence collection 需要自动化

## Dev-Loop Handoff

本 issue 的实现就是 IBM 真源改写本身。验证依赖治理检查与样本文档回读，不需要新增 runtime 代码。
