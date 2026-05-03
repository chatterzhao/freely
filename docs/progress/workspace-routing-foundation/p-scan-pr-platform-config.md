# Progress: scan-pr-platform-config

- issue_id: `I-20260501-0000-A`
- issue_path: `docs/issues/I-20260501-0000-A/issue.md`
- title: `PR scan surface + FREELY_REPO_PLATFORMS config`
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `hotfix/I-20260501-0000-A-scan-pr-platform-config`
- updated_at: `2026-05-01`
- session_refs:
  - {tool: ccds, session_id: "20260501-scan-pr-platform", jsonl_path: "unavailable://manual", role: "author"}

## Summary

- Added scan_repo_platform_prs() function to query configured platforms for open PRs
- Added "open_pull_requests" surface in task-source-scan JSON output
- Added FREELY_REPO_PLATFORMS config template (comma-separated platforms)
- Supports github (gh CLI) and gitee (gitee CLI) out of box
- Empty config = no PR scanning (backward compatible)

## Verification

- `./bin/governance-check` (pre-existing failures only, no regressions)
- Rebase onto latest develop with conflict resolution
