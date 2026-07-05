# Issue: Fix preferred_auth_method lost when switching to account slot

- issue_id: `I-20260410-1430-A`
- title: `Fix preferred_auth_method lost when switching to account slot`
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `codex-apikey-slot-bundle-and-provider-aware-probe-governance`
- issue-name: `preferred-auth-method-account-switch-fix`
- priority: `P1`
- source_candidate: `docs/B1-docs/raw-20260410-1430/candidates.md#c-20260410-1430-a`
- source_brainstorm: `docs/B1-docs/raw-20260410-1430/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-preferred-auth-method-account-switch-fix.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/code-reviews`
- follow_on_to: `I-20260405-0027-A`
- created_at: `2026-04-10`
- session_refs: []

## Problem

When switching from an apikey slot to an account slot, the `preferred_auth_method` field is deleted from live `~/.codex/config.toml` but not restored. This happens because account slots have empty `config-auth.toml` fragments.

## Root Cause

In `codex_apply_saved_slot_config_fragment`:
1. L793: `data.pop("preferred_auth_method", None)` - removes the field from live config
2. L802: tries to restore from fragment, but account fragment is empty
3. Result: field is permanently lost after switch

## Fix

Added fallback logic to set `preferred_auth_method` based on `slot_kind` when the fragment doesn't provide it:
- account slot -> `"chatgpt"`
- apikey slot -> `"apikey"`

## Files Changed

- `docs/system/workspace/scripts/runtime/ai-cli`: Added fallback logic
- `docs/system/workspace/scripts/tests/test-ai-cli-codex-apikey-slot-bundle-switch`: Added verification

## Acceptance Evidence

- `test-ai-cli-codex-apikey-slot-bundle-switch` passes
- New assertion verifies account switch sets `preferred_auth_method = "chatgpt"`

## Completion Note

Narrow bug fix merged as follow-on to `I-20260405-0027-A`. No new architecture or scope change.
