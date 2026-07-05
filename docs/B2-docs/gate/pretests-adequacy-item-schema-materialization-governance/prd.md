# PRD: pretests-adequacy-item-schema-materialization-governance

## Goal

把 `pre-tests.md` 的 acceptance item 从“最小结构可过门”升级到“可判定是否跑够”，并通过渐进 enforcement materialize richer adequacy schema。

## Why Now

当前 gate 主要只消费最小五件套，能判断“跑没跑”和“有没有证据”，但还不能稳定判断“是否为当前 lane / promote gate 跑够了测试”。

## Product Surface

- `docs/system/workspace/scripts/quality/pretests-gate`
- `docs/system/workspace/scripts/quality/governance-merge-gate`
- `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/prd-quality-bar.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/ibm-completion-gate.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/issue-materialization-checklist.md`
- `docs/system/workspace/scripts/tests/test-pretests-gate`
- `docs/system/workspace/scripts/tests/test-governance-merge-gate`

## Non-Goals

- 不做 runtime launch hard gate
- 不做 cleanup / retirement enforcement
- 不要求一次迁移所有历史 `pre-tests.md`
- 不新增 `tests.md`

## Non-Negotiables

- `pre-tests.md` 继续是唯一 canonical test truth
- v2 schema 必须兼容最小五件套
- enforcement 必须分 phase 上线，先 warning 再 selective hard-gate
- 不允许通过 schema 升级制造历史大面积功能回退

## Prototype Path

1. 冻结 v2 字段：`surface_kind`、`target_lane`、`promotion_gate`、`task_refs`、`case_design`
2. `pretests-gate` 能产出 `not-run` / `run-but-insufficient` / `sufficient-with-evidence` 诊断
3. 新 owner 先吃更强字段，历史 owner 保持兼容
4. `develop` promote 只对选定字段逐步硬化

## Eval Plan

成功：

- richer adequacy 语义有明确 schema 和 phase policy
- gate 能区分“跑了”和“跑够了”
- 旧 owner 不因 schema 上线立刻大面积失败

失败：

- 仍然只能报笼统的 `testing inadequate`
- schema 扩展和 launch / retirement scope 混在一起
- 团队因 schema 不够用又想新增 `tests.md`
