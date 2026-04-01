# 候选：multi-tool-group-auto-switch-governance

- id: `C-20260331-1840-A`
- candidate_format_version: `v2`
- title: Introduce multi-tool auto-switch v1 with codex slot recovery and kiro-to-codex fallback
- source_brainstorm: `docs/pre-brainstorms/20260331-1840--multi-tool-group-auto-switch-governance/brainstorms.md`
- problem: Freely's current runtime config and watchdog recovery model remain effectively single-tool even though workspace truth already exposes multiple tools with different continuity and availability contracts. As a result, failures such as tool-specific limits or auth exhaustion can only be handled with ad hoc per-tool logic instead of a canonical recovery order of same-tool slot sweep, controlled cross-tool fallback, and explicit all-tools-unavailable surfacing.
- why_now:
  - 当前 runtime 配置面仍只有单个 `AI_TOOL`，但能力真源已经承认多个外部工具与工具优先级并存。
  - 真实现场已出现 `kiro-cli` 限额/订阅校验失败，而既有 watchdog 恢复 contract 主要仍围绕 codex slot family。
  - 如果不先冻结多工具组恢复合同，后续只会继续为单个工具追加特判，导致 watchdog、runtime、manager 各自维护不同的可用性真相。
- acceptance_criteria:
  - freeze a runtime-owned config contract for `AUTO_SWITCH_SLOT`, `AUTO_SWITCH_TOOL`, and `AI_FALLBACK_TOOLS` without reusing `tools.md` priorities as fallback truth
  - keep same-tool automatic slot recovery limited to tool families with canonical watchdog truth in v1, namely `codex`
  - classify `kiro_monthly_request_limit` and `kiro_subscription_status_service_error` as tool-local failures eligible for cross-tool fallback when enabled
  - require cross-tool fallback to degrade to `fresh_with_handoff` instead of preserving resume semantics
  - make `ensure-manager` switch a protected manager project from `kiro-cli` to `codex` before relaunch when the project desires running, no manager is alive, and Codex readiness succeeds
  - preserve explicit `all_unavailable` / no-launch behavior for Codex readiness rather than silently forcing an unsafe relaunch
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
    summary: `The broad multi-tool direction still needs follow-on work, but the v1 slice is now safe to materialize: keep Codex as the only automatic fallback target, force fresh_with_handoff across tools, and leave generic tool groups out of scope.`
    verdict: `promote`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/multi-tool-auto-switch-v1-codex-fallback-governance/issues/multi-tool-auto-switch-v1-codex-fallback-governance.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- expected_outcome:
  - define a runtime-owned fallback order separate from `tools.md`
  - keep `AI_TOOL` as the single active tool pointer in v1 while adding `AUTO_SWITCH_SLOT`, `AUTO_SWITCH_TOOL`, and `AI_FALLBACK_TOOLS`
  - preserve Codex slot-sweep / no-launch invariants as the same-tool recovery truth
  - let `ensure-manager` absorb `kiro-cli -> codex` fallback for tool-local failures without local blind relaunch
  - force cross-tool fallback to `fresh_with_handoff`
- likely_truth_sources:
  - `.freely/config.env`
  - `docs/system/workspace/tools.md`
  - `docs/system/workspace/scripts/runtime/ai-cli`
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
  - `docs/pre-brainstorms/20260318-1818--ai-cli-availability-manager/brainstorms.md`
- decision_reason:
  - 现有真源已经足够支撑一个窄 v1：Codex 保持 same-tool slot sweep truth，Kiro 只提供 tool-local failure 分类，再由 `ensure-manager` 做 `kiro-cli -> codex` fallback。
  - `tools.md` 仍然只负责任务路由，不直接充当 runtime fallback 顺序真源；因此 v1 需要单独冻结 `AI_FALLBACK_TOOLS`。
  - continuity truth 目前不支持跨工具保留 resume 语义，所以 v1 必须把 cross-tool fallback 明确降级为 `fresh_with_handoff`。
- next_action:
  - materialize the v1 owner for runtime-owned fallback config, Codex-only same-tool recovery, and `kiro-cli -> codex` control-plane fallback
  - keep generic multi-tool groups, `cc`, `cc-use-codex-cli`, `iflow`, and host/network-global failures out of the first implementation slice
- revisit_trigger:
  - 当 v1 证明 `kiro-cli -> codex` fallback 与 Codex no-launch truth稳定后，再决定是否扩成更泛化的多工具组 contract
