# Candidates - 20260414-0255--freely-start-after-failure-recovery-handoff-race

## Context

- Source brainstorm: `docs/B1-docs/20260414-0255--freely-start-after-failure-recovery-handoff-race/brainstorms.md`
- Status: `reviewed`

## Candidates

### C-20260414-0255-A

- candidate_format_version: `v2`
- title: `Freely start codex after-failure recovery must honor saved-slot order`
- source_brainstorm: `docs/B1-docs/20260414-0255--freely-start-after-failure-recovery-handoff-race/brainstorms.md`
- follow_on_to: `I-20260410-1835-B`
- problem: `After a real codex runtime failure, manager recovery still reused the cache-filtered ready-slot selector, so saved codex slots like 1012 and a1018-1 could be skipped before they were actually executed. This broke the intended same-tool inner loop, made root-cause analysis drift toward failure-type labels, and could delay or derail the outer cross-tool recovery loop.`
- why_now:
  - `real freely start replays from bad slots reproduced the skip directly`
  - `the current branch already carries bounded runtime/watchdog fixes, but the canonical owner truth was still describing an older handoff-race theory instead of the observed slot-order bug`
  - `develop-bound guarded promote must carry one precise root cause plus artifact-backed adequacy evidence, not a stale brainstorm narrative`
- acceptance_criteria:
  - `codex after-failure same-tool recovery switches to the next saved slot in strict forward order`
  - `after-failure recovery no longer consults availability cache before executing the next saved slot`
  - `saved-slot selection does not wrap from the tail back to earlier failed slots`
  - `when no later codex slot remains, runtime falls through to the existing cross-tool outer loop without inventing a second switch mechanism`
  - `focused feature-local and premerge-integration regressions pass`
  - `real freely start replay proves a bad codex slot can recover onto a usable slot and continue doing work`
- promotion_gate:
  - `keep one unified switch method; widen only the failure triggers`
  - `do not reintroduce failure-type-specific slot switching`
  - `do not change the outer cross-tool ordering contract`
- open_questions:
  - `none; the remaining work is promote/retirement followthrough rather than more root-cause splitting`
- acceptance_reviews:
  - reviewer: `codex`
    verdict: `accepted`
    note: `The real defect is saved-slot selection semantics after failure, not a taxonomy of limit/network/auth error labels.`
- decision_reason:
  - `the after-failure path must be aligned with the intended inner-loop/outer-loop design: execute the next saved slot first, and only after a real failure continue the traversal`
  - `splitting cached-ready probing from after-failure traversal is the smallest fix that matches observed runtime behavior and avoids new regressions in normal readiness checks`
- priority: `P1`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_id: `I-20260414-0255-A`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/freely-start-auto-recovery-rootcause-governance/issues/freely-start-auto-recovery-rootcause-governance.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - `keep the owner issue in the same bounded lane`
  - `promote the corrected issue/pre-tests/review truth together with the saved-slot-order fix`
  - `after guarded develop promotion, finish post-merge dogfood and retire the temporary worktrees`
- revisit_trigger:
  - `reopen only if later evidence shows the outer cross-tool loop or per-tool slot inventory contract is itself wrong, rather than this after-failure traversal step`
