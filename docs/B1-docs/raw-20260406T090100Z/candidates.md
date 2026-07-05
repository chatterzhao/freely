# Candidates - 20260406-0901--codex-reconnect-probe-fast-fail

## C-20260406T090100Z-A: legacy issue

- candidate_format_version: `v2`
- title: `Codex reconnect probe fast-fail and runtime network classification alignment`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/B2-docs/config/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance/issues/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance.md`
- promoted_issue_id: `I-20260406T090100Z-A`
- source_brainstorm: `docs/B1-docs/raw-20260406T090100Z/brainstorms.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- problem: Codex live-auth probe currently waits for full timeout even after partial output has already shown `ERROR: Reconnecting...` or equivalent connection-failure evidence, causing `ai status` / `switch` / manager bootstrap to hang and misreport the incident as generic timeout.
- why_now:
  - dogfood runs show real `codex exec "hi"` sessions that oscillate between success and reconnect failure
  - operators need Freely to stop hanging on obvious reconnect evidence and to classify it as network-local rather than auth-local
  - the existing runtime network-failure owner already froze bounded recovery semantics, so this follow-on should align probe classification with that contract instead of inventing a second taxonomy
- acceptance_criteria:
  - `codex_probe_current_slot_now` returns `network_failure` as soon as reconnect/connection-failure evidence appears in partial output
  - the probe terminates its child process tree and writes an artifact immediately on that fast-fail path
  - `ai status` and unsaved-live-auth `ai switch codex` surface `probe_status=network_failure`
  - runtime reconnect log lines classify as `execution_network_transient|persistent` rather than generic `ai_exit_rc_*`
- promotion_gate:
  - keep probe status vocabulary narrow: add only `network_failure`, not a family of near-synonyms like `reconnecting`, `transport_error`, `probe_stall`
  - treat reconnect evidence as network-local and temporary; do not rotate slot/account purely because the probe saw it
  - do not widen this slice into a full redesign of manager bootstrap or removal of launch-time probing
- open_questions:
  - should future operator surfaces link the latest `codex-probe-artifacts/*.log` path directly in `ai status` or `live-status`
  - if upstream Codex later exposes a machine-readable connectivity exit code, should Freely prefer that over string matching
- acceptance_reviews:
  - reviewer: `codex-self-review`
    verdict: `supports_promotion`
    note: the reconnect fast-fail slice is narrower than the completed Codex bundle owner and warrants a new follow-on owner because it changes probe status vocabulary, runtime classification, and operator-facing launch behavior after the original contract was already closed.
