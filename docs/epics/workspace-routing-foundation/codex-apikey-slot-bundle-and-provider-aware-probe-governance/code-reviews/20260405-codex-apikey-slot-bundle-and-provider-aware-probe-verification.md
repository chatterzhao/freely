# Verification: codex-apikey-slot-bundle-and-provider-aware-probe-governance

- issue_id: `I-20260405-0027-A`
- issue_path: `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/issues/codex-apikey-slot-bundle-and-provider-aware-probe-governance.md`
- branch: `feature/tool-authorization-bootstrap-research-20260405-0335`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260405-0335-feature-tool-authorization-bootstrap-research`
- verification_date: `2026-04-05`
- verifier: `codex`
- verdict: `pass_for_verification`

## Scope Verdict

- `PASS`: Codex saved slots now preserve bundle truth across `auth.json`, `config-auth.toml`, and `manifest.json`, and `whoami/status` surface `slot_kind` plus `provider_id`.
- `PASS`: cross-kind materialization clears stale provider residue when switching `apikey -> account` and when switching `apikey -> apikey` to a different provider, while preserving unrelated config tables such as `[projects."/tmp/demo"]`.
- `PASS`: home-level config rewrites now use a shared runtime backup helper that leaves timestamped sibling backups before mutation, so the protection surface is reusable for future tools instead of staying embedded in Codex-only code.
- `PASS`: when OAuth inventory is unreachable but saved API-key slots exist, auto switch and watchdog recovery fall back to exec-based usability truth instead of blocking on curl/OAuth inventory.
- `PASS`: `freely ai switch codex --format json` auto mode now emits one machine-readable JSON envelope instead of mixing duplicate JSON objects on stdout.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-ai-cli-login-creates-incremented-slot`
2. `bash docs/system/workspace/scripts/tests/test-ai-cli-codex-apikey-slot-bundle-switch`
3. `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch`
4. `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch-oauth-unreachable`
5. `bash docs/system/workspace/scripts/tests/test-freely-ai-apikey-switch-oauth-unreachable-falls-back-to-exec`
6. `./bin/governance-check`
7. `bash -n docs/system/workspace/scripts/runtime/ai-cli`
8. `bash -n docs/system/workspace/scripts/runtime/file-backup.sh`

## Findings

- Historical governance debt remains outside this lane: `./bin/governance-check` still reports the two known protected-merge receipt gaps on `develop` (`6969be7e02ea0c380a9e9fc892b5184168d261fb`, `9fa8ec35bb9532235bd8cb51b6e20c6730836d7c`).
- No new lane-local regression was observed after fixing the TOML serializer, provider residue clearing, and JSON envelope behavior.

## Residual Risk

- Verification is still Codex-only. Other tools remain at weaker capability tiers until they get their own saved-truth and probe evidence.
- The current shell/Python writer preserves semantic correctness but not original TOML comments or ordering; a future extracted backend may want a more syntax-preserving config mutator.
