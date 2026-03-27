# Verification: project-scoped-network-proxy-configuration-and-launcher-inheritance-governance

- issue_id: `I-20260327-0651`
- verification_scope: feature-lane verification before merge to `develop`
- verified_in_worktree: `feature/network-proxy-config-capability-restack`

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-init-codex-project-config-force`
2. `bash docs/system/workspace/scripts/tests/test-freely-init-cc-config`
3. `bash docs/system/workspace/scripts/tests/test-freely-network-proxy-resolver`
4. `bash docs/system/workspace/scripts/tests/test-freely-network-proxy-launcher-inheritance`
5. `bash docs/system/workspace/scripts/tests/test-freely-network-proxy-oauth-inheritance`
6. `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch`
7. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager`
8. `./bin/governance-check`

## Result

- `freely init` now writes project-scoped proxy defaults into `.freely/config.env`, so later frontends only need to mutate one config truth source.
- `network-proxy-resolver.sh` now drives both codex launcher inheritance and watchdog OAuth/curl inheritance without falling back to hardcoded localhost defaults.
- OAuth sweep now sends the fuller CodexBar-style request contract, and no-arg `freely ai switch codex` refreshes saved auth inventory before choosing a usable slot.
- Governance remains clean aside from the repository's pre-existing legacy naming warnings.
