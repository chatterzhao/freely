# Candidates - 20260317-1101--frontend-runtime-baseline-for-probe

## Context
- Source brainstorm: ./brainstorms.md
- Status: completed

## Candidates

### C-20260317-1101
- title: Frontend Runtime Baseline for Probe
- problem: `Frontend Probe v0` 已有最小 shell 与 adapter 骨架，但仓库缺少真实 frontend build/runtime baseline，导致实现继续推进时只能增加样板而无法进入可运行状态。
- why_now: 不先补这层 baseline，Probe v0 会长期停在 mock/runtime-stub 阶段，无法形成真正的产品狗粮闭环。
- acceptance_hint: 明确 frontend 宿主入口、React renderer 挂载、Tauri runtime 注入、最小 build/test 方式，以及与 `Frontend Probe v0` 的依赖边界。
- priority: P0
- status: completed
- decision_reason: 这条问题边界已经 materialize 为独立 issue-bound IBM，并已被 `I-20260317-1004` 的 absorption closeout 写回 completed。当前 candidate 仅保留为来源 provenance，不再代表活跃待办。
- promoted_issue_path: docs/B2-docs/human/tui/issues/frontend-runtime-baseline-for-probe.md
- legacy_id_mapping: I-20260317-1004  # 历史遗留的 issue id
- milestone: M-20260308-frontend-probe-dogfooding-loop
- next_action: 保留为历史来源记录。若后续 frontend host/runtime baseline 再暴露新的缺口，应从当前 canonical truth 新开 candidate/issue，而不是恢复这条 candidate。
- completion_note: `frontend-probe-v0` 与 `rust-tauri-probe-bridge-v1` 已吸收该 baseline，`I-20260317-1004` 也已完成 canonical closeout；此 candidate 不再构成活跃 owner。
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "doc-ibm"}]
