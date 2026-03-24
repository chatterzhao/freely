# Candidates

- id: `C-20260324-0415-A`
- title: Application-native observability planes and runtime observation contract
- status: `needs_research`
- adoption_type: n/a
- source_brainstorm: `docs/pre-brainstorms/20260324-0415--application-native-observability-planes/brainstorms.md`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `pending://application-native-observability-planes-materialization`
- depends_on:
  - `docs/pre-brainstorms/20260320-1945--watchdog-live-status-surface-and-manager-supervision/candidates.md#C-20260320-1945-A`
  - `docs/pre-brainstorms/20260322-0115--cli-first-entrypoint-and-observability-surface-unification/candidates.md#C-20260322-0115-A`
  - `docs/pre-brainstorms/20260308-1244--frontend-probe-dogfooding-loop/candidates.md`
  - `docs/pre-brainstorms/20260322-0715--pre-test-merge-post-merge-acceptance-stall/candidates.md#C-20260322-0715-A`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- why_now:
  - Freely 当前已经有 `live-status`、`fleet-status`、`jsonl`、`cycle log`、continuity artifacts 等有效观察面，但它们仍停留在 CLI/runtime 视角，尚未冻结成统一的多平面产品 contract
  - 用户已明确要求：Freely 要把这些状态暴露给 CLI / TUI / GUI / future API，让用户知道“现在是什么样”“可以在哪里插话”
  - 未来 Freely 开发其他应用时，也需要一套泛化的 application-native real-environment observation contract，而不能误把 Freely 自己的日志格式当通用规则
- expected_outcome:
  - define a generic `application-native runtime observation contract`
  - define Freely's own concrete observability planes as the first profile over that contract
  - freeze how CLI / TUI / GUI / future API share one backend observability model
  - freeze how multi-worktree and multi-subagent sessions/logs map back to user-facing surfaces
- acceptance_hint:
  - observation is no longer described only as “check logs / wait threshold”; it is expressed as current-state plane, session plane, stream plane, fleet plane, and artifact plane
  - Freely self-host profile maps these planes to `live-status`, `fleet-status`, `jsonl`, `cycle log`, continuity, prompts, and intake/resolution artifacts
  - the contract stays application-native: other apps can provide different surfaces while still fitting the same progress/stall/evidence model
  - `20260322-0715` and related stall candidates consume this observation contract instead of redefining ad-hoc log rules
- decision_reason:
  - the product direction is clear, but the exact plane model and ownership split across runtime, CLI, frontend probe, and future API are not yet stable enough to materialize into implementation issues
- next_action:
  - continue pre-brainstorm and freeze the minimum plane model
  - explicitly define which layer owns current-state, session mapping, stream tail, fleet overview, and artifact evidence
  - define the observation order contract and how Freely's own profile instantiates it
  - decide whether this line promotes as one issue family or splits into backend contract plus frontend/probe consumers
- revisit_trigger:
  - when the minimum plane set, ownership split, and application-native observation order can be frozen into issue-level contract
  - or when future dogfood again exposes that current CLI surfaces are insufficient to tell users where they can safely interrupt or debug
