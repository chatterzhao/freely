# Code Review: integration-acceptance-first-verification-governance
- issue_id: `I-20260322-0135`

## Scope

- `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/prd-quality-bar.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/ibm-completion-gate.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/issue-materialization-checklist.md`
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/LAWS.md`

## Findings

- IBM 真源现在明确 `pre-tests.md` 是 issue-level acceptance 控制面，而不是附属清单。
- verification 默认顺序被明确成 integration / acceptance evidence first，代码评审退居二级验证面。
- 真源已显式允许某些验收只能在 merge 后完成，但要求在 `pre-tests.md` 中提前标出 `post-merge acceptance`。

## Verification

- `./bin/governance-check`
- review the updated truth sources for wording consistency

## Result

- pass
