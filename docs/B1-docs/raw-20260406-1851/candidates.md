# Candidates - 20260406-1851--codex-interactive-login-and-apikey-input-flow

## C-20260406-1851-A

- candidate_format_version: `v2`
- title: `Codex interactive login and API-key input flow`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/codex-interactive-login-and-apikey-input-flow-governance/issues/codex-interactive-login-and-apikey-input-flow-governance.md`
- promoted_issue_id: `I-20260406-1851-A`
- source_brainstorm: `docs/B1-docs/raw-20260406-1851/brainstorms.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- problem: `Freely currently lacks a governed first-hop interactive Codex login flow for auth-mode selection and API-key provider/base-url/key collection, so the existing dirty implementation sits outside owner truth and risks drifting from the completed bundle contract.`
- why_now:
  - `feature/codex-apikey-login-interactive` already contains a bounded UX patch plus four targeted tests, but no canonical owner
  - the completed bundle/probe owner closed without freezing interactive login UX as a separate follow-on
  - continuing implementation without a candidate/issue would violate the current pre-brainstorm-first governance loop
- acceptance_criteria:
  - `freely ai login codex` supports bounded interactive auth-mode selection between `account` and `apikey`
  - `freely ai login codex apikey` supports interactive provider/base-url/api-key collection plus `--name/--url/--key` direct-arg parity
  - empty required input fails without mutating live auth/config or saved-slot state
  - successful login preserves saved-slot and JSON output continuity for Codex API-key mode
- promotion_gate:
  - keep this owner narrower than the completed bundle/probe owner; do not reopen provider residue cleanup, probe routing, or generic cross-tool parity
  - do not widen the slice into current-live bootstrap without saved-slot inventory
  - do not widen the slice into standalone `ai-switch-cli` extraction or product-level init/set-tool UX redesign
- open_questions:
  - should prompt defaults remain hard-coded for Codex (`custom`, `https://api.openai.com/v1`) or be sourced from an existing provider registry when that becomes stable
  - should successful interactive apikey login always save a slot immediately, or should future UX allow `live-only` auth without slot persistence
- acceptance_reviews:
  - reviewer: `codex-self-review`
    verdict: `supports_follow_on_owner`
    note: the dirty interactive login patch is a narrow Codex-first UX follow-on with explicit tests and does not fit the reconnect-fast-fail or current-live bootstrap owners.
