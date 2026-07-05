# Candidates - 20260413-0208--foreground-background-runtime-entrypoint-semantics

## Context

- Source brainstorm: `docs/B1-docs/raw-20260413-0208/brainstorms.md`
- Status: promoted

## Candidates

### C-20260413-0208-A: legacy issue
- candidate_format_version: `v2`
- title: Foreground/background runtime entrypoint semantics governance
- problem: 近期 dogfooding 已确认 `freely start` 是前台附着 supervisor，会随调用会话结束而停机；但 Freely 的产品心智与未来 UI/TUI 默认需要一个显式后台自治 runtime。现有实现与测试又已经把 `start/restart/stop/status` 锁成前台/控制面 contract，因此不能直接把 `start` 偷改成后台模式。当前需要先把 foreground、daemon、UI 关闭默认、shared status truth 与回归保护面冻结成 canonical owner，再进入 dev-loop 实现。
- why_now: 如果在没有冻结入口 contract 的情况下直接修 `start`，极易同时打破 event-log / PID / wait / ownership tests、watchdog/recovery 边界，以及未来 UI 启停心智。这已经是产品入口治理问题，不应继续停留在悬空 pre-brainstorm。
- acceptance_criteria:
  - `Freely truth explicitly preserves foreground attached mode and background daemon mode as separate first-class runtime entrypoints.`
  - `start/restart/stop/status remain the canonical foreground or control-plane contract and are not silently redefined into daemon behavior.`
  - `Only explicit daemon start/stop/status/logs command surfaces represent background runtime control.`
  - `UI and TUI default lifecycle semantics point at daemon mode, and closing the frontend does not implicitly stop the background runtime.`
  - `Foreground regressions stay valid while daemon receives a separate persistence or explicit-stop coverage family.`
  - `Daemon mode proves parent-shell exit no longer tears down the runtime or misclassifies the stop as a foreground operator stop.`
  - `Foreground and daemon continue to share a single runtime status truth instead of creating parallel state surfaces.`
- fix_approach: Materialize a bounded owner that freezes runtime entrypoint semantics first, then implements explicit daemon control-plane commands and detach semantics without changing the current foreground contract.
- priority: `P0`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_id: `I-20260413-0208-A`
- promoted_issue_path: `docs/B2-docs/ibm/foreground-background-runtime-entrypoint-semantics-governance/issues/foreground-background-runtime-entrypoint-semantics-governance.md`
- source_brainstorm: `docs/B1-docs/raw-20260413-0208/brainstorms.md`
- session_refs:
  - tool: codex
    session_id: current-thread
    jsonl_path: unavailable://codex-thread-only
    role: author
- next_action: Candidate mirror only. `I-20260413-0208-A` is now the canonical owner for freezing foreground versus daemon runtime semantics and the first bounded daemon control-plane implementation path.
- revisit_trigger: Re-open only if implementation discovery proves daemon cannot share the current runtime truth surfaces, or if preserving foreground command semantics requires splitting CLI contract policy from daemon detach mechanics.
- promotion_gate:
  - `Foreground command semantics must remain explicitly preserved and protected by existing regressions.`
  - `Daemon remains the only explicit background mode marker; do not silently redefine start into background behavior.`
  - `The first owner must keep shared runtime truth singular across foreground, daemon, live-status, and fleet-status.`
  - `Entry-point semantics work must stay separated from unrelated recovery follow-ons such as rate-limit restart gaps.`
- open_questions:
  - `Whether daemon restart belongs in the first owner or should remain a follow-on after start or stop or status or logs stabilize.`
  - `Whether logs follow and attach semantics should share one daemon subcommand or stay distinct.`
  - `Whether top-level short aliases are worth adding after the explicit daemon surface is proven.`
- acceptance_reviews:
  - reviewer: `codex`
    verdict: `pass`
    rationale: `The pre-brainstorm now has stable contract evidence, clear non-goals, and a low-regression implementation direction, so leaving it unbound would violate the milestone visibility rules.`
