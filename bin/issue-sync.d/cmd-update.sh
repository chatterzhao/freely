#!/usr/bin/env bash
# cmd-update.sh — sourced by bin/issue-sync, never executed directly.
# `issue-sync update` — refresh title/body/labels.

cmd_update() {
  local local_id="$1" file title body labels gh_id gitee_id
  if ! file="$(_issue_file_for "$local_id")"; then
    echo "[ERROR] issue-sync: cannot resolve issue document for $local_id" >&2
    echo "  checked: $ISSUES_DIR/$local_id/issue.md and docs/B2-docs/**/issues/$local_id.md" >&2
    exit 1
  fi

  # Dedup: skip if content hasn't changed since last sync
  if ! _changed_since_last_sync "$local_id" "$file"; then
    echo "[issue-sync] skip update: $local_id unchanged since last sync"
    return 0
  fi

  title=$(_platform_title "$local_id" "$file")
  body=$(_issue_body "$file" "$local_id")
  labels=$(_labels "$file")

  gh_id=$(_gh_issue_number "$file")
  if [[ -n "${GH_REPO:-}" && -n "$gh_id" ]]; then
    echo "[issue-sync] GitHub: updating #$gh_id"
    _gh_update "$gh_id" "$title" "$body" "$labels"
  fi

  gitee_id=$(_gitee_resolve_issue_number "$file" "$local_id")
  if [[ -n "${GITEE_REPO:-}" && -n "$gitee_id" ]]; then
    echo "[issue-sync] Gitee: updating $gitee_id"
    _gitee_update "$gitee_id" "$title" "$body" >/dev/null || echo "[issue-sync] Gitee: update FAILED" >&2
  fi

  echo "[issue-sync] update complete: $local_id"
}
