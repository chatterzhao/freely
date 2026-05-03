# Verification: scan-pr-platform-config

- issue_id: `I-20260501-0000-A`
- issue_path: `docs/epics/workspace-routing-foundation/scan-pr-platform-config/issues/I-20260501-0000-A.md`
- date: `2026-05-01`
- type: `governance-merge-gate`
- decision: `pass`
- why_this: `Hotfix adds PR scan surface with FREELY_REPO_PLATFORMS config. Minimal code change in the freely runtime script.`
- alternatives_considered:
  - `Extend task-lifecycle-scan.py instead of bash inline — rejected: lifecycle scan delegates to python; PR data injected after`
  - `Add PR scan as separate binary — rejected: complexity disproportionate for a config-driven scan`
- boundary_non_goals:
  - `Platform auth management (tokens, credentials) — out of scope`
  - `PR auto-sync or write-back to platforms — not included`
- residual_risk: `Low. PR scan depends on platform CLIs (gh, gitee) being installed and authenticated. Runtime handles missing CLIs gracefully by skipping.`

## Verification Items

1. **PR scan function**: `scan_repo_platform_prs()` present in `freely` script
2. **Config**: `FREELY_REPO_PLATFORMS` declared in config template (empty = no PR scanning)
3. **Surface**: `open_pull_requests` surface with advisory trust level in scan JSON
4. **Platforms**: github (gh) and gitee (gitee) supported with correct CLI mapping
5. **Backward compat**: Empty FREELY_REPO_PLATFORMS → no PR data; existing scans unaffected
6. **Governance**: `./bin/governance-check` — no regressions from this branch

## Result

PASS
