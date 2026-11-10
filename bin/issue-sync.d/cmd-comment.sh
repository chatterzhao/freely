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

  local gh_id gitee_id ts
  gh_id=$(_gh_issue_number "$file")
  gitee_id=$(_gitee_resolve_issue_number "$file" "$local_id")
  ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  if [[ -n "${GH_REPO:-}" && -n "$gh_id" ]]; then
    echo "[issue-sync] GitHub: adding comment to #$gh_id"
    _gh_comment "$gh_id" "$last_comment"
  fi

  if [[ -n "${GITEE_REPO:-}" && -n "$gitee_id" ]]; then
    echo "[issue-sync] Gitee: adding comment to $gitee_id"
    _gitee_comment "$gitee_id" "$last_comment" >/dev/null || echo "[issue-sync] Gitee: comment FAILED" >&2
  fi

  # Update last_synced_comment_at
  python3 -c "
import yaml
yaml.SafeLoader.yaml_implicit_resolvers.pop('tag:yaml.org,2002:timestamp', None)
with open('$file') as f: content = f.read()
parts = content.split('---', 2)
fm = yaml.safe_load(parts[1]) if len(parts) >= 3 else {}
fm.setdefault('last_synced_comment_at', {})
fm['last_synced_comment_at']['github'] = '$ts'
fm['last_synced_comment_at']['gitee'] = '$ts'
fm['updated_at'] = '$ts'
new_fm = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False).strip()
body_text = parts[2] if len(parts) >= 3 else ''
with open('$file', 'w') as f: f.write('---\n' + new_fm + '\n---' + body_text)
" 2>/dev/null || true

  echo "[issue-sync] comment complete: $local_id"
}
