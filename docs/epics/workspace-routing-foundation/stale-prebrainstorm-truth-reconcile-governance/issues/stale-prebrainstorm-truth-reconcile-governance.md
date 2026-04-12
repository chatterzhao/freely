# Issue: stale-prebrainstorm-truth-reconcile-governance

- issue_id: `I-20260411-1417-A`
- title: Stale pre-brainstorm truth reconcile governance
- phase_state: `in_ibm`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `stale-prebrainstorm-truth-reconcile-governance`
- issue-name: `stale-prebrainstorm-truth-reconcile-governance`
- priority: `P1`
- source_candidate: `docs/pre-brainstorms/20260411-1417--stale-prebrainstorm-truth-reconcile/candidates.md#c-20260411-1417-a`
- source_brainstorm: `docs/pre-brainstorms/20260411-1417--stale-prebrainstorm-truth-reconcile/brainstorms.md`
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
  - `docs/pre-brainstorms/20260408-1205--verification-contract-and-premerge-adequacy/brainstorms.md`
  - `docs/pre-brainstorms/20260327-0651--pretests-gate-and-network-proxy-config/brainstorms.md`

## Next

1. next_action: `keep the representative reconcile batch and verification receipt as IBM materialization evidence, then decide whether to open a separate execution owner only for any newly discovered stale pattern that current labels cannot explain`
2. revisit_trigger: 若新的审计仍因为旧 pre-brainstorm 语句把已实现能力误判为缺失，且现有 reconcile labels不足以解释该偏差。

## Current State Note

- `pre-tests.md` 当前的 `pass` 只表示 IBM materialization 与代表样本 reconcile 已被记录，不表示本 owner 已进入 execution loop。
- 在出现需要真正修改 runtime / hook / gate 的新 stale pattern 之前，本 owner 保持 `phase_state: in_ibm` 是刻意边界，而不是 lifecycle 漏写。
