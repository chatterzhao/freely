# Verification: scan-pr-platform-config

- issue: `I-20260501-0000-A`
- date: `2026-05-01`
- type: `governance-merge-gate`

## Verification Items

1. **PR scan function**: `scan_repo_platform_prs()` present in `freely` script
2. **Config**: `FREELY_REPO_PLATFORMS` declared in config template (empty = no PR scanning)
3. **Surface**: `open_pull_requests` surface with advisory trust level in scan JSON
4. **Platforms**: github (gh) and gitee (gitee) supported with correct CLI mapping
5. **Backward compat**: Empty FREELY_REPO_PLATFORMS → no PR data; existing scans unaffected
6. **Governance**: `./bin/governance-check` — no regressions from this branch

## Result

PASS
