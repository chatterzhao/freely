# Issue: integration-acceptance-first-verification-governance

- issue_id: `I-20260322-0135`
- title: Integration-acceptance-first IBM and verification governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `integration-acceptance-first-verification-governance`
- issue-name: `integration-acceptance-first-verification-governance`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/integration-acceptance-first-verification-governance/code-reviews`
- priority: P0
- source_candidate: `docs/B1-docs/raw-20260322-0135/candidates.md#c-20260322-0135-a`
- source_brainstorm: `docs/B1-docs/raw-20260322-0135/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`
  - `docs/system/workspace/three-loop-capability-lifecycle.md`
  - `docs/LAWS.md`

## Why

Freely 在狗粮过程中已经多次证明，真实缺口更常先通过端到端行为暴露，而不是先通过逐行代码审查暴露。现有真源已经要求 IBM 产出 `prd.md`、`pre-tests.md`、`tasks.md`，但还没有把下面这条口径明确写死：

- `pre-tests.md` 是 issue-level acceptance 的主控制面
- verification 默认应优先检查 integration / acceptance evidence
- code review 的默认角色是风险定位与缺口解释，而不是替代行为验收

如果这条规则不明确，后续 AI 容易重新退化成“先读代码，再补测试”，而不是“先跑验收，再定向读代码解释风险”。

## Scope

1. 明确 `pre-tests.md` 在 IBM 中的主导地位：它不是附属清单，而是 issue-level acceptance 控制面。
2. 明确 verification 的默认优先级：
   - integration / acceptance evidence first
   - targeted code review second
3. 在三层 loop 真源中写清：
   - AI-native capability delivery 的验收优先级是行为优先，不默认等同于逐行代码评审
4. 允许存在 `post-merge acceptance`，但必须在 `pre-tests.md` 中显式标识，而不是 merge 后临时想起。

## Acceptance

- `doc-ibm-execution` 真源明确 `pre-tests.md` 是 issue-level acceptance 控制面
- `prd-quality-bar` / `ibm-completion-gate` / issue materialization checklist 明确 `pre-tests.md` 必须以 integration / acceptance 为主，且可区分 `pre-merge` / `post-merge`
- `three-loop-capability-lifecycle` 明确 verification 默认先看 integration / acceptance evidence，再做定向代码评审
- `LAWS.md` 补齐 develop 合并 gate 的优先级语义：集成/验收优先于代码阅读完成度

## Completion

- `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/prd-quality-bar.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/ibm-completion-gate.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/issue-materialization-checklist.md`
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/LAWS.md`
- `docs/progress/workspace-routing-foundation/p-integration-acceptance-first-verification-governance.md`
- `docs/epics/workspace-routing-foundation/integration-acceptance-first-verification-governance/code-reviews/20260322-integration-acceptance-first-verification-governance-verification.md`

## Verification

- `./bin/governance-check`
- review the updated IBM / loop / laws truth sources for consistent wording

## Next

- 当前批次已完成规则收敛。
- 若后续要继续把 verification review 模板结构化成脚手架，应通过新的 lifecycle 承接，不在本 issue 上继续扩 scope。
