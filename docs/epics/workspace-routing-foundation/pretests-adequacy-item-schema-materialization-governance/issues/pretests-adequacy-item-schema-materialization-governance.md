# Issue: pretests-adequacy-item-schema-materialization-governance

- issue_id: `I-20260411-1415-A`
- title: Pre-tests adequacy item schema materialization governance
- phase_state: `in_ibm`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `pretests-adequacy-item-schema-materialization-governance`
- issue-name: `pretests-adequacy-item-schema-materialization-governance`
- priority: `P0`
- source_candidate: `docs/pre-brainstorms/20260411-1415--pretests-adequacy-item-schema-materialization/candidates.md#c-20260411-1415-a`
- source_brainstorm: `docs/pre-brainstorms/20260411-1415--pretests-adequacy-item-schema-materialization/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/pretests-adequacy-item-schema-materialization-governance/pre-tests.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/pretests-adequacy-item-schema-materialization-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/pre-tests-evidence-binding-and-completion-gate-governance/issues/pre-tests-evidence-binding-and-completion-gate-governance.md`
  - `docs/epics/workspace-routing-foundation/verification-contract-and-premerge-adequacy-governance/issues/verification-contract-and-premerge-adequacy-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

现在真正缺的是 machine-readable adequacy semantics。最小五件套让 gate 能看见“跑过某些测试”，但还不足以判断“是否跑够了当前 lane / promote gate 需要的测试面”。

## Scope

1. 冻结 adequacy item v2 schema
2. 为 gate 增加充分性诊断
3. 定义 phased enforcement
4. 更新 IBM/doc 真源，确保新 owner 不再只写标题式测试项

## Non-Goals

1. 不做 launch hard gate
2. 不做 cleanup / retirement gate
3. 不新增 `tests.md`
4. 不做全仓历史强迁移

## IBM Handoff

- implementation_scope_summary:
  - 先把 v2 schema 与 enforcement phase policy 定住，再局部接到 gate。
  - 兼容性优先，不能因为 schema 升级制造历史大回归。
- required_doc_refs:
  - `docs/epics/workspace-routing-foundation/pretests-adequacy-item-schema-materialization-governance/prd.md`
  - `docs/epics/workspace-routing-foundation/pretests-adequacy-item-schema-materialization-governance/pre-tests.md`
  - `docs/epics/workspace-routing-foundation/pretests-adequacy-item-schema-materialization-governance/tasks.md`
  - `docs/system/workspace/scripts/quality/pretests-gate`
  - `docs/system/workspace/scripts/quality/governance-merge-gate`
  - `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`

## Next

1. next_action: `finish IBM materialization and implement schema v2 plus phased gate enforcement`
2. revisit_trigger: 若 phased enforcement 证明必须把 skill/doc update 与 gate enforcement 拆分成两个 owner。
