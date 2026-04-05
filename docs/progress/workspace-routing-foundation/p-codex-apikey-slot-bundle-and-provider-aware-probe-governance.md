# Progress: codex-apikey-slot-bundle-and-provider-aware-probe-governance

- issue_id: `I-20260405-0027-A`
- issue_path: `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/issues/codex-apikey-slot-bundle-and-provider-aware-probe-governance.md`
- title: `Codex API-key slot bundle and provider-aware probe governance`
- phase_state: `completed`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/tool-authorization-bootstrap-research-20260405-0335`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260405-0335-feature-tool-authorization-bootstrap-research`
- updated_at: `2026-04-05`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Current Slice

- add a minimal Codex slot manifest so each saved slot records `slot_kind`, legacy/account compatibility, and provider metadata without widening other tools
- teach `freely ai login/save/switch/whoami/status` to treat Codex live auth as `auth.json + config-auth.toml`, with cross-kind `account <-> apikey` config clearing and restoration
- branch watchdog probe routing by slot kind so `account-*` keeps OAuth inventory plus exec confirmation, while `apikey-*` uses exec-only truth and is never gated by OAuth sweep reachability
- harden the embedded TOML materializer so preserved config tables such as `[projects."/tmp/demo"]` survive account/apikey cross-kind switches without invalid serialization
- keep `freely ai switch codex --format json` machine-readable in auto mode by emitting one JSON envelope while `apikey -> apikey` switches clear previous provider residue when the target provider changes
- route home-level config rewrites through a shared runtime backup helper so untracked live config files get timestamped rollback copies before mutation

## Evidence

- `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/prd.md`
- `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/tasks.md`
- `docs/system/workspace/scripts/runtime/ai-cli`
- `docs/system/workspace/scripts/runtime/file-backup.sh`
- `docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh`
- `docs/system/workspace/scripts/tests/test-ai-cli-login-creates-incremented-slot`
- `docs/system/workspace/scripts/tests/test-ai-cli-codex-apikey-slot-bundle-switch`
- `docs/system/workspace/scripts/tests/test-freely-ai-account-switch`
- `docs/system/workspace/scripts/tests/test-freely-ai-account-switch-oauth-unreachable`
- `docs/system/workspace/scripts/tests/test-freely-ai-apikey-switch-oauth-unreachable-falls-back-to-exec`
- `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/code-reviews/20260405-codex-apikey-slot-bundle-and-provider-aware-probe-implementation-decision.md`
- `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/code-reviews/20260405-codex-apikey-slot-bundle-and-provider-aware-probe-verification.md`

## Verification Notes

- Passed `bash docs/system/workspace/scripts/tests/test-ai-cli-login-creates-incremented-slot`
- Passed `bash docs/system/workspace/scripts/tests/test-ai-cli-codex-apikey-slot-bundle-switch`
- Passed `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch`
- Passed `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch-oauth-unreachable`
- Passed `bash docs/system/workspace/scripts/tests/test-freely-ai-apikey-switch-oauth-unreachable-falls-back-to-exec`
- Passed `bash -n docs/system/workspace/scripts/runtime/ai-cli`
- Passed `bash -n docs/system/workspace/scripts/runtime/file-backup.sh`
- Passed `bash -n docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh`
- Passed `git diff --check`
- Wrote issue-bound implementation decision and verification artifacts under `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/code-reviews/`
- `./bin/governance-check` still reports only the two known historical protected-merge receipt gaps on `develop` (`6969be7e02ea0c380a9e9fc892b5184168d261fb`, `9fa8ec35bb9532235bd8cb51b6e20c6730836d7c`); no new lane-local regression was introduced

## Next Action

- treat this owner as closed. Any future multi-tool parity, standalone `ai-switch-cli` extraction, or stronger syntax-preserving config mutation must route through dedicated follow-on owners instead of reopening this Codex-first closeout.
