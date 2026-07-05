# Issue: stale-prebrainstorm-truth-reconcile-governance

- issue_id: `I-20260411-1417-A`
- title: Stale pre-brainstorm truth reconcile governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `stale-prebrainstorm-truth-reconcile-governance`
- issue-name: `stale-prebrainstorm-truth-reconcile-governance`
- priority: `P1`
- source_candidate: `docs/B1-docs/raw-20260411/candidates.md#c-20260411-1417-a`
- source_brainstorm: `docs/B1-docs/raw-20260411/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/stale-prebrainstorm-truth-reconcile-governance/pre-tests.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/stale-prebrainstorm-truth-reconcile-governance/code-reviews`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

当前预研审计经常被 stale truth 带偏，浪费时间去重复验证已经落地的 gate / hook / owner，也容易把 deferred gap 误判成 regression。

## Scope

1. 冻结 reconcile policy
2. 选一个 representative batch
3. 用 pointer-based 最小编辑修正 stale truth
4. 保持 `pre-tests.md` 命名与 owner 边界不漂移

## Non-Goals

1. 不做全仓大清洗
2. 不改 runtime / gate 逻辑
3. 不做共享索引批量重写；按 owner materialization 规范所需的最小注册 append 不算超 scope
4. 不把 reconcile owner 和执行层 hardening 混做

## IBM Handoff

- implementation_scope_summary:
  - 本 owner 是文档真相纠偏，不是能力实现 owner。
  - 每个 reconcile 变更都必须带 canonical truth pointer。
- required_doc_refs:
  - `docs/epics/workspace-routing-foundation/stale-prebrainstorm-truth-reconcile-governance/prd.md`
  - `docs/epics/workspace-routing-foundation/stale-prebrainstorm-truth-reconcile-governance/pre-tests.md`
  - `docs/epics/workspace-routing-foundation/stale-prebrainstorm-truth-reconcile-governance/tasks.md`
  - `docs/B1-docs/raw-20260408/brainstorms.md`
  - `docs/B1-docs/raw-20260327/brainstorms.md`

## Next

1. next_action: `completed on canonical develop; the representative reconcile batch and verification receipt are now canonical delivered truth.`
2. revisit_trigger: Re-open only if a future stale pattern cannot be explained by the current reconcile labels and needs a new bounded follow-on owner.

## Current State Note

- `pre-tests.md` 的 pass 已对应 canonical delivered truth，且本 owner 现已完成闭环。
- 未来若出现新的 stale pattern，应另开更窄的 follow-on owner，而不是回写本 owner。
