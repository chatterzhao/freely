# Verification: codex-current-live-apikey-bootstrap-without-saved-slot-governance

- issue_id: `I-20260406-1829-A`
- issue_path: `docs/B2-docs/config/codex-current-live-apikey-bootstrap-without-saved-slot-governance/issues/codex-current-live-apikey-bootstrap-without-saved-slot-governance.md`
- verified_in_branch: `feature/codex-current-live-apikey-bootstrap-dev-20260406-1904`
- verified_in_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260406-1904-feature-codex-current-live-apikey-bootstrap-dev`
- verified_at: `2026-04-06`
- verifier: `codex`
- verdict: `pass_for_verification`

## Scope Verdict

- `PASS`: `ai switch codex` accepts a usable current live API-key auth even when the saved-slot inventory is empty, and keeps `slot=null` instead of inventing a fake saved slot.
- `PASS`: manager bootstrap can recover from `all_unavailable` using the same bounded `current-live` identity when a current live Codex API key becomes usable.
- `PASS`: the owner package is governance-clean after absorbing the bounded residual slice from the old residual lane.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-ai-cli-switch-current-live-apikey-without-saved-slot`
2. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-current-live-apikey-without-saved-slot`
3. `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260406-1904-feature-codex-current-live-apikey-bootstrap-dev --issue docs/B2-docs/config/codex-current-live-apikey-bootstrap-without-saved-slot-governance/issues/codex-current-live-apikey-bootstrap-without-saved-slot-governance.md`
4. `./bin/governance-check`
5. `git diff --check`

## Findings

- The watchdog-side residual did not need a synthetic saved slot; bounded `current-live` identity is sufficient for recovery handoff when the prior phase was `all_unavailable`.
- The pre-existing `ai-cli` current-live switch path in this execution lane already covered the user-visible `usable_current_auth` contract, so this owner only needed to lock it with issue-bound regression coverage instead of reintroducing the older residual diff verbatim.
- Old residual-tree disposition is now explicit:
  - `docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh`
  - `docs/system/workspace/scripts/tests/test-ai-cli-switch-current-live-apikey-without-saved-slot`
  - `docs/system/workspace/scripts/tests/test-freely-ensure-manager-current-live-apikey-without-saved-slot`
  were absorbed by this owner.
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/system/workspace/scripts/tests/test-freely-runtime-auth-failure-signal-filter`
  belong to `I-20260406-0901-A`.
  - The old residual `docs/system/workspace/scripts/runtime/ai-cli` diff should not be transplanted verbatim; this lane already had a stronger current-live switch path in base, so the old tree is now evidence-only and should remain `retire-only`.

## Residual Risk

- Current-live bootstrap remains Codex-specific. If another provider needs equivalent no-saved-slot bootstrap semantics, that should be handled as a separate follow-on instead of widening this owner.
- This session cannot write `.git/worktrees/...`, so the verified lane is not yet checkpointed or promoted. The remaining work is execution-boundary followthrough, not additional scope in this owner.
