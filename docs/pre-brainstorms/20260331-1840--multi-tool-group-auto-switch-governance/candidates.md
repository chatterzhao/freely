# 候选：multi-tool-group-auto-switch-governance

- id: `C-20260331-1840-A`
- candidate_format_version: `v2`
- title: Introduce tool-group availability governance with same-tool slot recovery before cross-tool fallback
- source_brainstorm: `docs/pre-brainstorms/20260331-1840--multi-tool-group-auto-switch-governance/brainstorms.md`
- problem: Freely's current runtime config and watchdog recovery model remain effectively single-tool even though workspace truth already exposes multiple tools with different continuity and availability contracts. As a result, failures such as tool-specific limits or auth exhaustion can only be handled with ad hoc per-tool logic instead of a canonical recovery order of same-tool slot sweep, controlled cross-tool fallback, and explicit all-tools-unavailable surfacing.
- why_now:
  - 当前 runtime 配置面仍只有单个 `AI_TOOL`，但能力真源已经承认多个外部工具与工具优先级并存。
  - 真实现场已出现 `kiro-cli` 限额/订阅校验失败，而既有 watchdog 恢复 contract 主要仍围绕 codex slot family。
  - 如果不先冻结多工具组恢复合同，后续只会继续为单个工具追加特判，导致 watchdog、runtime、manager 各自维护不同的可用性真相。
- acceptance_criteria:
  - freeze a canonical configuration boundary for project-local tool-group selection versus global AI profile storage
  - define the semantics of `auto_switch_slot` and `auto_switch_tool`, including manual CLI/UI/file edits sharing one persisted truth
  - define a failure allow/deny matrix that distinguishes `slot-local`, `tool-local`, and `host/network-global` failures
  - define a canonical recovery order of same-tool slot sweep before cross-tool fallback
  - define continuity rules for cross-tool fallback, including when `fresh_with_handoff` is mandatory and what evidence must be preserved
  - define multi-tool control-plane invariants equivalent to current watchdog safety rules: probe-first truth, no-launch during sweep, serialized switching, and structured handoff before relaunch
- promotion_gate:
  - keep the first materialized issue focused on control-plane contract and minimum viable implementation slice, not a full redesign of every tool integration
  - do not blur task-routing tool preference in `tools.md` with runtime-owned availability fallback truth unless ownership is made explicit
  - freeze project config versus global profile config precedence before implementation begins
  - prove which tool families can participate in v1 without regressing continuity guarantees or fake-health behavior
  - keep host/proxy/network-global failures out of cross-tool fallback unless explicit evidence proves a tool-local boundary
- open_questions:
  - should project config stay env-based or move to a structured file once tool groups and active pointers are introduced
  - should the runtime fallback order reuse `tools.md` priorities or define a separate runtime-owned ordering truth
  - should `cc` / `cc-use-codex-cli` participate in v1 tool fallback, or should v1 stay limited to tools with stronger availability and continuity evidence
  - should cross-tool fallback ever preserve resume semantics across continuity classes, or always degrade to `fresh_with_handoff`
  - where should the canonical tool-switch lock and no-launch gate state live
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The feature direction is valid, but it is not yet safe to implement until continuity downgrade rules, control-plane invariants, and config precedence are frozen.`
    verdict: `needs_research`
- status: `needs_research`
- milestone: `unassigned`
- promoted_issue_path: `pending://issue-materialization`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- expected_outcome:
  - define a canonical config contract for multiple tools and per-tool slot families
  - freeze the semantics of `auto_switch_slot` and `auto_switch_tool`
  - define a recovery order of same-tool slot sweep before cross-tool fallback
  - keep the feature CLI-first while allowing future UI and manual file edits to operate on the same persisted truth
  - freeze continuity downgrade rules and multi-tool no-launch invariants before implementation
  - surface a canonical all-tools-unavailable state instead of looped `rc=0` or fake-health outcomes
- likely_truth_sources:
  - `.freely/config.env`
  - `docs/system/workspace/tools.md`
  - `docs/system/workspace/scripts/runtime/ai-cli`
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
  - `docs/pre-brainstorms/20260318-1818--ai-cli-availability-manager/brainstorms.md`
- decision_reason:
  - 这不是单一工具 bugfix，而是新的控制面 contract：配置、恢复状态机、失败分类、tool-vs-slot 边界都要一起冻结。
  - 现有 codex-slot watchdog family 可以提供输入，但还不足以直接承载“多工具组 + 跨工具 fallback”这条更宽的能力面。
  - 因此当前最稳的是保持 `needs_research` candidate，继续做预研和 contract 收敛，而不是匆忙 materialize 或直接实现。
- next_action:
  - compare existing codex-slot watchdog truths with tool-agnostic recovery needs
  - freeze whether the config should stay env-based or move to a structured file
  - define how CLI commands, future UI, and direct file edits share one canonical configuration source
  - draft a tool-level failure taxonomy covering slot-local, tool-local, and host/network-global failures
  - freeze continuity downgrade rules and a minimum allow/deny matrix for cross-tool fallback
  - decide the minimum set of tools that can participate in v1 automatic fallback without fake-health regressions
- revisit_trigger:
  - 当配置真源、tool/slot 责任边界与最小 failure taxonomy 冻结后，重新判断是否 materialize 成新的 milestone-owned issue
