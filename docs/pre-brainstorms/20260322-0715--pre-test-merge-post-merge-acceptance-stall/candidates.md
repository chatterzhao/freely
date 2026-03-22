# 候选：pre-test-merge-post-merge-acceptance-stall

- id: `C-20260322-0715-A`
- title: Detect and recover pre-test-merge manager acceptance stalls after delegated continuation
- source_brainstorm: `docs/pre-brainstorms/20260322-0715--pre-test-merge-post-merge-acceptance-stall/brainstorms.md`
- status: `proposed`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `pending://pre-test-merge-acceptance-stall-materialization`
- session_refs: []
- why_now:
  - `I-20260322-0445` 的真实 post-merge acceptance 已经把 delegated continuation 注入 prompt
  - 但 `pre-test-merge` 主管长时间没有产出新的 continuity / decision
  - 这会让 merge 后验收停在半路，破坏 integration-acceptance-first 规则
- expected_outcome:
  - define a watchdog-visible acceptance-stall contract for pre-test-merge manager continuations
  - distinguish legitimate long-running patrol from stalled delegated acceptance
  - recover or reroute when the manager prompt has consumed the delegated handoff but no new continuity is emitted
- acceptance_hint:
  - real post-merge acceptance no longer remains indefinitely at `current_prompt_has_delegated_continuation=1` with no new manager continuity
  - runtime can surface or recover this stall instead of leaving acceptance hanging
