#!/usr/bin/env bash
# cmd-comment-delete.sh — sourced by bin/issue-sync, never executed directly.
# `issue-sync comment-delete <local_id> <platform> <comment_id>` (#4740).

cmd_comment_delete() {
  local local_id="$1" platform="${2:-}" comment_id="${3:-}" adapter
  if [[ -z "$local_id" || -z "$platform" || -z "$comment_id" ]]; then
    echo "[ERROR] usage: freely issue-sync comment-delete <local_id> <github|gitee> <comment_id>" >&2
    return 2
  fi
  case "$platform" in
    github|gitee) ;;
    *) echo "[ERROR] comment-delete: platform must be github or gitee" >&2; return 2 ;;
  esac
  adapter="$ROOT_DIR/docs/system/workspace/scripts/sync/platform-adapter.py"
  echo "[issue-sync] deleting comment $comment_id from $platform issue for $local_id"
  python3 "$adapter" delete-comment "$local_id" "$platform" "$comment_id"
  local rc=$?
  if [[ "$rc" -ne 0 ]]; then
    echo "[ERROR] comment-delete failed for $local_id on $platform (comment $comment_id)" >&2
    echo "  retry: freely issue-sync comment-delete $local_id $platform $comment_id" >&2
  fi
  return "$rc"
}
