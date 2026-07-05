# 候选：multi-tool-group-auto-switch-governance

- id: `C-20260331T184000Z-A`
- candidate_format_version: `v2`
- title: Materialize generic multi-tool availability manager with same-tool-first recovery
- source_brainstorm: `docs/B1-docs/raw-20260331T184000Z/brainstorms.md`
- problem: Freely's current runtime config and watchdog recovery model remain effectively single-tool even though workspace truth already exposes multiple tools with different continuity and availability contracts. As a result, failures such as tool-specific limits or auth exhaustion can only be handled with ad hoc per-tool logic instead of a canonical recovery order of same-tool slot sweep, controlled cross-tool fallback, and explicit all-tools-unavailable surfacing.
- why_now:
  - 当前 runtime 配置面仍只有单个 `AI_TOOL`，但能力真源已经承认多个外部工具与工具优先级并存。
  - 真实现场已出现 `kiro-cli` 限额/订阅校验失败，而既有 watchdog 恢复 contract 主要仍围绕 codex slot family。
  - 如果不先冻结多工具组恢复合同，后续只会继续为单个工具追加特判，导致 watchdog、runtime、manager 各自维护不同的可用性真相。
- acceptance_criteria:
  - freeze a runtime-owned availability contract for `AUTO_SWITCH_SLOT`, `AUTO_SWITCH_TOOL`, and ordered `AI_FALLBACK_TOOLS`
  - keep same-tool recovery ahead of cross-tool fallback: tools with canonical slot/watchdog truth must exhaust same-tool recovery before trying the next tool
  - preserve Codex watchdog invariants: probe-first truth, shared switch lock, no-launch during sweep/reprobe, and explicit `all_unavailable` handling
  - classify tool failures by recovery scope (`slot_local`, `tool_local`, `host_global`) so cross-tool fallback only happens for tool-local/same-tool exhaustion cases
  - let `ensure-manager` walk the configured fallback list instead of hard-coding `kiro-cli -> codex`, selecting the first tool that proves or declares readiness
  - when every configured tool is unavailable, keep manager launch blocked and pin the earliest-known reset target instead of silently looping or pretending health
- promotion_gate:
  - keep the first materialized issue focused on control-plane contract and minimum viable implementation slice, not a full redesign of every tool integration
  - do not blur task-routing tool preference in `tools.md` with runtime-owned availability fallback truth unless ownership is made explicit
  - freeze project config versus global profile config precedence before implementation begins
  - prove which tool families can participate in v1 without regressing continuity guarantees or fake-health behavior
  - keep host/proxy/network-global failures out of cross-tool fallback unless explicit evidence proves a tool-local boundary
- open_questions:
  - should project config stay env-based or move to a structured file once tool groups and active pointers are introduced
  - should `cc` / `cc-use-codex-cli` participate in v1 tool fallback, or should v1 stay limited to tools with stronger availability and continuity evidence
  - where should the canonical tool-switch lock and no-launch gate state live
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The earlier v1 narrowing solved a real Kiro/Codex bridge, but it contracted below the original brainstorm. This owner now needs to restore the generic availability-manager state machine while preserving Codex watchdog invariants.`
    verdict: `promote`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/B2-docs/ibm/multi-tool-auto-switch-v1-codex-fallback-governance/issues/multi-tool-auto-switch-v1-codex-fallback-governance.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- expected_outcome:
  - define a runtime-owned availability order separate from `tools.md`
  - keep `AI_TOOL` as the active tool pointer while making `AI_FALLBACK_TOOLS` a real ordered recovery list
  - preserve Codex slot-sweep / no-launch invariants as the first same-tool recovery truth and reusable pattern for future tool families
  - let `ensure-manager` consume tool-local failures by walking the configured ordered fallback list instead of a single hard-coded target
  - force cross-tool fallback to `fresh_with_handoff` and keep all-tools-unavailable explicit
- likely_truth_sources:
  - `.freely/config.env`
  - `docs/system/workspace/tools.md`
  - `docs/system/workspace/scripts/runtime/ai-cli`
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/B2-docs/ibm/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
  - `docs/B1-docs/raw-20260318T181800Z/brainstorms.md`
- decision_reason:
  - 原始 brainstorm 与更早的 availability-manager 研究都要求“同工具先恢复，再按工具顺序 fallback”；窄 v1 只是中间桥接，不应覆盖更大的 contract。
  - `tools.md` 仍然只负责任务路由，不直接充当 runtime fallback 顺序真源；因此 recovery order 继续由 project config 的 `AI_FALLBACK_TOOLS` 承接。
  - continuity truth 目前仍不支持跨工具保留 resume 语义，所以 cross-tool fallback 继续明确降级为 `fresh_with_handoff`。
- next_action:
  - widen the active owner from narrow `kiro-cli -> codex` bridge logic into a generic manager availability state machine
  - keep unsupported tool families explicit via capability gaps, but do not keep hard-coded single-target fallback in the runtime
- revisit_trigger:
  - 当 v1 证明 `kiro-cli -> codex` fallback 与 Codex no-launch truth稳定后，再决定是否扩成更泛化的多工具组 contract
