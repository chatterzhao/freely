# Issue: ibm-pretests-executable-acceptance-quality-governance

- issue_id: `I-20260326-1815`
- title: IBM pre-tests executable acceptance quality governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `ibm-pretests-executable-acceptance-quality-governance`
- issue-name: `ibm-pretests-executable-acceptance-quality-governance`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/ibm-pretests-executable-acceptance-quality-governance/code-reviews`
- priority: P0
- source_candidate: `docs/B1-docs/raw-20260326-1733/candidates.md#c-20260326-1733-a`
- source_brainstorm: `docs/B1-docs/raw-20260326-1733/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/epics/workspace-routing-foundation/integration-acceptance-first-verification-governance/issues/integration-acceptance-first-verification-governance.md`
  - `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`
  - `docs/system/workspace/three-loop-capability-lifecycle.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 已经把 `pre-tests.md` 定义成 issue-level acceptance 控制面，也把 verification 收敛成 integration / acceptance-first。但当前 enforcement 仍然不够强：

- `prd.md` 的 `Eval Plan` 仍可能先收缩成 truth-source wording review
- `pre-tests.md` 仍可能退化成“单独阅读某文档时能否看出语义”
- governance / agent / skill 改造型 issue 尤其容易缺少真实 runtime、application-native real-environment 与 end-to-end dogfood 验收面

对 Freely 这种自治 AI 开发系统来说，这会让最关键的能力线在 IBM 阶段就失去可执行 acceptance contract，后续 verification、replay 与 closeout 只能靠口头解释恢复。

## Scope

1. 强化 `doc-ibm-execution` 与 IBM references：
- `pre-tests.md` 默认必须表达 executable acceptance contract
- 不能只停在 wording review / truth-source reading checklist

2. 冻结 `prd.md -> pre-tests.md` 的更强派生关系：
- `prd.md` 的 `Eval Plan` 必须先写行为验收、环境、证据与失败判据
- 再允许补充 truth-source review

3. 对 Freely 自治能力写清默认测试面：
- pre-merge focused regression / smoke
- post-merge integration acceptance
- post-merge application-native real-environment acceptance
- post-merge end-to-end dogfood acceptance
- 若某项不适用，必须显式写出不适用理由与替代证据面

4. 写清 protected verification environment 的恢复信息：
- target environment
- evidence
- failure signals
- replay expectation / failure handling

5. 本条 issue 只改 IBM 真源与 checklist：
- `docs/system/workspace/skills/doc-ibm-execution/**`
- 不在本条 lifecycle 中统一所有 verification review 模板
- 不重写所有历史 issue 的 `pre-tests.md`

## Acceptance

- `doc-ibm-execution` 真源明确 `pre-tests.md` 默认是 executable acceptance contract，而不是 wording review 清单。
- `prd-quality-bar` 明确 `Eval Plan` 与 `pre-tests.md` 必须覆盖环境、证据、失败判据与 runtime/dogfood 验收面。
- `ibm-completion-gate` 与 `issue-materialization-checklist` 明确：
  - Freely 自治能力默认要回答 integration / application-native real-environment / end-to-end dogfood 三类 post-merge acceptance
  - 若不适用，必须显式记录理由与替代证据
- `pre-tests.md` 的最小结构足够让后续 dev-loop / verification / replay 恢复“该跑什么、在哪跑、通过证据是什么”。
- 新规则不误导为“每个 issue 都必须新写脚本测试”；允许 runtime scenario、dogfood observation 与 focused regression 组合成验收面。

## Completion

- `docs/epics/workspace-routing-foundation/ibm-pretests-executable-acceptance-quality-governance/issues/ibm-pretests-executable-acceptance-quality-governance.md`
- `docs/epics/workspace-routing-foundation/ibm-pretests-executable-acceptance-quality-governance/brainstorms/b-ibm-pretests-executable-acceptance-quality-governance.md`
- `docs/epics/workspace-routing-foundation/ibm-pretests-executable-acceptance-quality-governance/prd.md`
- `docs/epics/workspace-routing-foundation/ibm-pretests-executable-acceptance-quality-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/ibm-pretests-executable-acceptance-quality-governance/tasks.md`
- `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/prd-quality-bar.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/ibm-completion-gate.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/issue-materialization-checklist.md`
- `docs/progress/workspace-routing-foundation/p-ibm-pretests-executable-acceptance-quality-governance.md`
- `docs/epics/workspace-routing-foundation/ibm-pretests-executable-acceptance-quality-governance/code-reviews/20260326-ibm-pretests-executable-acceptance-quality-governance-verification.md`

## Verification

- `./bin/governance-check`
- review the updated IBM truth sources for:
  - explicit executable acceptance wording
  - explicit real-environment / dogfood coverage rules
  - clear non-applicable fallback semantics

## Next

- 当前 lifecycle 已完成 IBM materialization、truth-source 改写与 verification。
- 若后续还要统一 verification review 模板或引入 machine-readable acceptance schema，应通过新的 lifecycle 承接。
