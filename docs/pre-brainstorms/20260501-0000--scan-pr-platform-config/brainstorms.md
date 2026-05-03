# Brainstorms — Scan Open PRs + Repo Platform Config

## Context

Freely's task-source-scan currently has 5 surfaces (human_chat_intake, delegated_continuation,
active_milestone_queue, active_pre_brainstorm_queue, active_progress_queue) but does NOT
scan for open Pull Requests. 

AI discovered PR #163 by reading files (milestone docs, continuity, git log), not through
the scan. PR scanning would enable proactive detection and automated handling (merge, close,
delegate worker for review).

## Design

### 1. Config: FREELY_REPO_PLATFORMS

```env
# .freely/config.env
FREELY_REPO_PLATFORMS="github,gitee"
```

- Comma-separated list of repo platforms
- Each platform has a CLI: `gh` for github, `gitee` for gitee
- Empty/absent = no PR scanning

### 2. PR Scan Function

```bash
scan_repo_platform_prs() {
  local project="$1" platforms_csv="${FREELY_REPO_PLATFORMS:-}"
  [[ -n "$platforms_csv" ]] || return 0
  
  local IFS=","
  for platform in $platforms_csv; do
    case "$platform" in
      github)
        gh pr list --json number,title,state,headRefName,baseRefName,url,createdAt \
          --jq '.[] | "\(.number)|\(.title)|\(.state)|\(.headRefName)|\(.url)"' 2>/dev/null
        ;;
      gitee)
        # gitee CLI or API
        ;;
    esac
  done
}
```

### 3. New Surface in Scan JSON

```json
{
    "surface": "open_pull_requests",
    "source_class": "discovery", 
    "active_count": <N>,
    "trust_level": "advisory_platform_snapshot",
    "needs_reconcile": false,
    "summary_lines": ["<number>|<title>|<state>|<headRefName>|<url>", ...]
}
```

### 4. Integration Points

| File | Change |
|---|---|
| `.freely/config.env` | Add FREELY_REPO_PLATFORMS |
| `freely` ~line 14074 | Add PR snapshot to scan assembly |
| `freely` new function | scan_repo_platform_prs |
| `freely` line 16475 | Add FREELY_REPO_PLATFORMS to config template |

## Success Criteria

1. Config `FREELY_REPO_PLATFORMS="github"` enables PR scanning
2. `task-source-scan` includes `open_pull_requests` surface when platforms configured
3. AI sees open PRs in scan JSON and can delegate workers
4. Empty config = no PR surface (backward compatible)
5. Multiple platforms supported (github + gitee)
