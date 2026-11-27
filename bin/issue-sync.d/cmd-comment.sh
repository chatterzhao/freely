#!/usr/bin/env bash
# cmd-comment.sh — sourced by bin/issue-sync, never executed directly.
# `issue-sync comment` — push the newest unsynced comment.

cmd_comment() {
  local local_id="$1" file
  if ! file="$(_issue_file_for "$local_id")"; then
    echo "[ERROR] issue-sync: cannot resolve issue document for $local_id" >&2
    echo "  checked: $ISSUES_DIR/$local_id/issue.md and docs/B2-docs/**/issues/$local_id.md" >&2
    exit 1
  fi

  # Dedup: check if there are unsynced comments
  if [[ -n "${GH_REPO:-}" ]] && ! _has_unsynced_comments "$file" "github"; then
    echo "[issue-sync] skip comment: no unsynced comments for $local_id (GitHub)"
  fi

  # Extract the latest comment block. System events (promote / promote_finalized)
  # write bullet metadata, user comments write a {json} line, so the reader must
  # accept both instead of assuming a `## Comments` section (#4183).
  local last_comment
  last_comment="$(_last_comment_body "$file")"

  if [[ -z "$last_comment" ]]; then
    echo "[issue-sync] no unsynced comments for $local_id"
    return 0
  fi

  local gh_id gitee_id ts gitee_state synced_gh=0 synced_gitee=0
  gh_id=$(_gh_issue_number "$file")
  gitee_id=$(_gitee_resolve_issue_number "$file" "$local_id")
  ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  if [[ -n "${GH_REPO:-}" && -n "$gh_id" ]]; then
    echo "[issue-sync] GitHub: adding comment to #$gh_id"
    _gh_comment "$gh_id" "$last_comment"
    synced_gh=1
  fi

  if [[ -n "${GITEE_REPO:-}" && -n "$gitee_id" ]]; then
    # #4737: Gitee rejects comments on CLOSED issues when the repo's
    # `issue_comment` setting is false (the default). `can_comment` may still
    # be true, so the UI looks normal and the bare HTTP 401 is misleading.
    # Read the state first and report the real cause instead of posting blind.
    gitee_state=$(_gitee_cli get "$gitee_id" 2>/dev/null | python3 -c '
import json, sys
try:
    print((json.load(sys.stdin).get("state") or "unknown").lower())
except Exception:
    print("unknown")
' 2>/dev/null || echo unknown)
    if [[ "$gitee_state" == "closed" ]]; then
      echo "[issue-sync] Gitee: skip comment on $gitee_id — issue is CLOSED and repo setting issue_comment=false rejects closed-issue comments (can_comment may be true). Reopen the issue or enable issue_comment=true via PATCH /repos/{owner}/{repo}." >&2
    else
      echo "[issue-sync] Gitee: adding comment to $gitee_id"
      if _gitee_comment "$gitee_id" "$last_comment" >/dev/null; then
        synced_gitee=1
      else
        echo "[issue-sync] Gitee: comment FAILED" >&2
      fi
    fi
  fi

  # Update last_synced_comment_at
  python3 -c "
import yaml
yaml.SafeLoader.yaml_implicit_resolvers.pop('tag:yaml.org,2002:timestamp', None)
with open('$file') as f: content = f.read()
parts = content.split('---', 2)
fm = yaml.safe_load(parts[1]) if len(parts) >= 3 else {}
fm.setdefault('last_synced_comment_at', {})
if '$synced_gh' == '1': fm['last_synced_comment_at']['github'] = '$ts'
if '$synced_gitee' == '1': fm['last_synced_comment_at']['gitee'] = '$ts'
fm['updated_at'] = '$ts'
new_fm = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False).strip()
body_text = parts[2] if len(parts) >= 3 else ''
with open('$file', 'w') as f: f.write('---\n' + new_fm + '\n---' + body_text)
" 2>/dev/null || true

  echo "[issue-sync] comment complete: $local_id"
}
