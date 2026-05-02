# 候选：pre-test-merge-post-merge-acceptance-stall

- id: `C-20260322-0715-A`
- title: Detect and recover pre-test-merge manager acceptance stalls after delegated continuation
- note: 历史候选名保留 `pre-test-merge`，当前 canonical 语义按 `test-pre-merge-*` 测试批次前缀族解释
- source_brainstorm: `docs/pre-brainstorms/20260322-0715--pre-test-merge-post-merge-acceptance-stall/brainstorms.md`
- status: `needs_research`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `pending://pre-test-merge-acceptance-stall-materialization`
- depends_on:
  - `pending://pre-test-merge-responsibility-usage-and-lifecycle-governance-materialization`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- why_now:
  - `I-20260322-0445` 的真实 post-merge acceptance 已经把 delegated continuation 注入 prompt
  - 但 `pre-test-merge` 主管长时间没有产出新的 continuity / decision
  - 这会让 merge 后验收停在半路，破坏 integration-acceptance-first 规则
  - 2026-03-24 `develop` canonical followthrough 再次复现了“delegated continuation 已进 prompt，但未及时 materialize 新 continuity”的形态，不过现场只到 stall threshold 边缘，尚不足以直接判成 runtime patch bug
- expected_outcome:
  - define a watchdog-visible acceptance-stall contract for pre-test-merge manager continuations
  - distinguish legitimate long-running patrol from stalled delegated acceptance
  - recover or reroute when the manager prompt has consumed the delegated handoff but no new continuity is emitted
  - make the stall contract depend on manager continuity/decision progress, not on worker prompt inventory
- acceptance_hint:
  - real post-merge acceptance no longer remains indefinitely at `current_prompt_has_delegated_continuation=1` with no new manager continuity
  - runtime can surface or recover this stall instead of leaving acceptance hanging
  - a run that has not yet exceeded prompt/cycle stall threshold must not be misclassified as a runtime stall
- decision_reason:
  - boundary-governance for `pre-test-merge` now routes through the dedicated governance issue
  - this candidate remains active because the concrete acceptance-stall detection and recovery contract is still unresolved
- next_action:
  - keep this candidate visible while the governance issue stabilizes `test-pre-merge-*` protected-env lifecycle semantics
  - rerun canonical dogfood long enough to cross the watchdog stall threshold before deciding a runtime patch is needed
  - if the same shape still persists past threshold, materialize a separate runtime/orchestration issue for delegated acceptance stall detection and recovery
- revisit_trigger:
  - after the governance issue freezes `test-pre-merge-*` role/stale semantics
  - or earlier if another post-merge acceptance run reproduces the same delegated-continuation stall
