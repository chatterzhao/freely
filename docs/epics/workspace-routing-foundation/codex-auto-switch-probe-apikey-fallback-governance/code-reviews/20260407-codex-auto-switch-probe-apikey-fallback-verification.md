# Verification: codex-auto-switch-probe-apikey-fallback-governance

- issue_id: `I-20260407-0023-A`
- issue_path: `docs/epics/workspace-routing-foundation/codex-auto-switch-probe-apikey-fallback-governance/issues/codex-auto-switch-probe-apikey-fallback-governance.md`
- verified_in_branch: `feature/codex-auto-switch-probe-apikey-fallback-20260406-2138`
- verified_in_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260406-2138-feature-codex-auto-switch-probe-apikey-fallback`
- verified_at: `2026-04-07`
- verifier: `codex`
- verdict: `pass_for_verification`

## Scope Verdict

- `PASS`: `freely ai switch codex` auto mode no longer stops on `all_unavailable:*` when saved `apikey-*` slots still exist; it continues into exec-only probing and can select the usable apikey slot.
- `PASS`: the shared watchdog probe path follows the same rule instead of returning early on the account-only sweep result.
- `PASS`: the new regression proves the unavailable account slot stays unavailable while the saved apikey slot is still probed and chosen.
- `PASS`: live manual replay still shows both saved slots in `./bin/ai list`, explicit switch to `apikey-codex-a1007-1` succeeds, and `codex exec "hi"` works afterward with `provider: codex-a1007`.

## Commands

1. `./bin/test-lane feature-local -- bash docs/system/workspace/scripts/tests/test-freely-ai-apikey-switch-all-unavailable-falls-back-to-exec`
2. `./bin/test-lane feature-local -- bash docs/system/workspace/scripts/tests/test-freely-ai-apikey-switch-oauth-unreachable-falls-back-to-exec`
3. `./bin/test-lane feature-local -- bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch-oauth-unreachable`
4. `./bin/test-lane feature-local -- bash docs/system/workspace/scripts/tests/test-ai-cli-codex-apikey-slot-bundle-switch`
5. `git diff --check`
6. `./bin/governance-check`
7. `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260406-2138-feature-codex-auto-switch-probe-apikey-fallback --issue docs/epics/workspace-routing-foundation/codex-auto-switch-probe-apikey-fallback-governance/issues/codex-auto-switch-probe-apikey-fallback-governance.md`
8. `./bin/ai list`
9. `./bin/ai --quiet --format json switch apikey-codex-a1007-1`
10. `codex exec "hi"`

## Findings

- The previous regression only affected the `all_unavailable:*` branch. The stricter `oauth_unreachable` behavior for account-only inventories remains intact and is still covered by the existing focused regression.
- Live account-mode `codex exec` on this machine still shows external TLS/certificate failures after switching to account; this verification did not reopen that environment-specific evidence because the repaired contract is the saved-apikey fallback after an account sweep.

## Residual Risk

- This owner only proves the saved-slot path. Unsaved current-live apikey bootstrap, interactive login UX, and reconnect fast-fail classification remain governed by their own follow-on owners.
- The manual live replay proved the apikey slot path only. Account-slot live execution remains dependent on external environment health.
