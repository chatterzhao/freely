# Candidates - 20260410-1430--preferred-auth-method-account-switch-fix

## Context
- Source brainstorm: `docs/B1-docs/raw-20260410T143000Z/brainstorms.md`
- Status: promoted
- Reopens: I-20260405T002700Z-A (narrow follow-on bug fix)

## Candidates

### C-20260410T143000Z-A: legacy issue
- candidate_format_version: `v2`
- title: Fix preferred_auth_method lost when switching to account slot
- problem: When switching from an apikey slot to an account slot, `preferred_auth_method` is deleted from live config but not restored, because account slots have empty `config-auth.toml` fragments.
- why_now: Discovered during code review. The field should be set to `"chatgpt"` for account slots and `"apikey"` for apikey slots.
- acceptance_criteria:
  - Switching to account slot sets `preferred_auth_method = "chatgpt"` in live config
  - Switching to apikey slot sets `preferred_auth_method = "apikey"` in live config
  - Existing test `test-ai-cli-codex-apikey-slot-bundle-switch` continues to pass
  - New assertion added to verify account switch behavior
- fix_approach: Add fallback logic in `codex_apply_saved_slot_config_fragment` to set `preferred_auth_method` based on `slot_kind` when the fragment doesn't provide it.
- priority: P1
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_id: `I-20260410T143000Z-A`
- promoted_issue_path: `docs/B2-docs/config/codex-apikey-slot-bundle-and-provider-aware-probe-governance/issues/preferred-auth-method-account-switch-fix.md`
- source_brainstorm: `docs/B1-docs/raw-20260410T143000Z/brainstorms.md`
- session_refs: []
- next_action: Merge this narrow fix to `develop` as a follow-on to `I-20260405T002700Z-A`.