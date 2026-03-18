# Candidates - 20260317-1101--frontend-runtime-baseline-for-probe

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260317-1101
- title: Frontend Runtime Baseline for Probe
- problem: `Frontend Probe v0` 已有最小 shell 与 adapter 骨架，但仓库缺少真实 frontend build/runtime baseline，导致实现继续推进时只能增加样板而无法进入可运行状态。
- why_now: 不先补这层 baseline，Probe v0 会长期停在 mock/runtime-stub 阶段，无法形成真正的产品狗粮闭环。
- acceptance_hint: 明确 frontend 宿主入口、React renderer 挂载、Tauri runtime 注入、最小 build/test 方式，以及与 `Frontend Probe v0` 的依赖边界。
- priority: P0
- status: promoted
- decision_reason: 这条问题边界已经足够稳定，应直接提升为独立 issue-bound IBM，而不是继续停留在 pre-brainstorm。
- promoted_issue_path: docs/epics/frontend-probe-dogfooding-loop/frontend-runtime-baseline-for-probe/issues/frontend-runtime-baseline-for-probe.md
- milestone: M-20260308-frontend-probe-dogfooding-loop
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "doc-ibm"}]
