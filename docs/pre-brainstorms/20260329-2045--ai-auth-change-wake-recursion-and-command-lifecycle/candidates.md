# Candidates - 20260329-2045--ai-auth-change-wake-recursion-and-command-lifecycle

## Context
- Source brainstorm: ./brainstorms.md
- Status: active

## Candidates

### C-20260329-2045-A
- candidate_format_version: v2
- title: Decouple ai auth success-path commands from recursive auth-change wake
- problem: `bin/ai switch codex` can print a successful switch result and still not exit because it synchronously enters `auth-change-wake`, which process-tree evidence shows as the immediate child of the still-alive `ai-cli`. The wider `watchdog-driven slot switching -> ai switch -> notify` loop is the strongest current hypothesis, not yet a fully captured closed loop. `bin/ai login codex` is a likely same-family path, but the clean hard reproduction for this candidate remains `switch`.
- why_now: This was reproduced locally with live process inspection, including a no-op `switch codex <current-slot>` run that still printed success and remained alive behind a synchronous `auth-change-wake` child. That makes the issue narrower and stronger than “login sometimes hangs”: even without real OAuth or a cross-slot change, the success-path lifecycle is wrong.
- acceptance_criteria:
  - `ai switch codex` exits promptly after a successful switch result
  - a no-op `ai switch codex <current-slot>` exits promptly after printing success
  - `auth-change-wake` cannot recurse back into the same success-path notification loop
  - operator interruption does not leave residual recursive wake helpers alive beyond the bounded cleanup window defined by the issue
  - any preserved wake behavior remains compatible with manager/watchdog auth recovery
- promotion_gate:
  - prove the recursion chain with process-tree evidence, not just user perception of a hanging terminal
  - keep the first issue scoped to command lifecycle and wake recursion, not general account governance
  - decide explicitly whether the repair should be async wake, re-entrancy guard, notify suppression, or a combination, only after IBM freezes the contract
- open_questions:
  - should `ai login codex` eventually adopt the same exit contract once its post-success path is verified without relying on real login replay
  - should successful `ai switch/login` fire-and-forget the wake, or should they wait only for a bounded acknowledgement
  - should watchdog-initiated `ai switch` suppress `notify_freely_auth_change` by default to avoid self-triggered wake loops
  - if no-op `switch` is already the current slot, should it skip `notify_freely_auth_change` entirely
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The strongest field fact is a concrete command-lifecycle failure: even no-op ai switch success can remain alive behind auth-change-wake. The issue should stay focused on success-path wake semantics and exit guarantees.`
    verdict: `ready_for_ibm`
- priority: P1
- status: promoted
- decision_reason: The bug is real and reproduced on `switch`, and the first safe step is now an IBM-scoped issue that freezes exit semantics, wake re-entrancy boundaries, and non-regression coverage before any runtime patch is attempted. `login` remains a same-family follow-on concern unless cleaner evidence upgrades it inside the issue.
- promoted_issue_path: `docs/epics/workspace-routing-foundation/ai-auth-change-wake-command-lifecycle-governance/issues/ai-auth-change-wake-command-lifecycle-governance.md`
- milestone: `docs/milestones.md#M-20260306-workspace-routing-foundation`
- next_action: Enter IBM on a narrow owner issue around auth-change-wake recursion and command exit semantics, then decide the minimal safe repair.
- revisit_trigger: Reopen or widen this line if later evidence shows the same recursion on non-codex auth commands or proves that the residual helpers survive beyond operator interruption in a durable way.
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
