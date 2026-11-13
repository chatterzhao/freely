#!/usr/bin/env bash
# cmd-close.sh — sourced by bin/issue-sync, never executed directly.
# `issue-sync close` — close every configured platform replica.

cmd_close() {
  local local_id="$1" reason="${2:-completed}" file gh_id gitee_id
  if ! file="$(_issue_file_for "$local_id")"; then
    echo "[ERROR] issue-sync: cannot resolve issue document for $local_id" >&2
    echo "  checked: $ISSUES_DIR/$local_id/issue.md and docs/B2-docs/**/issues/$local_id.md" >&2
    exit 1
  fi

  # Strict raw closure is delegated to the configured-platform effect. Only a
  # complete all-platform close may commit platform_state=closed locally.
  # The effect validates the local phase BEFORE touching any platform, so a
  # non-terminal raw aborts with zero platform writes. Its exit code is
  # propagated: 0 complete, 3 partial (retryable), 1 nothing closed.
  if [[ "$(_fm_get "$file" "schema_version")" == "1" ]]; then
    # #4225: heal a partial platform_ids cache from platform-side discovery
    # first, so close-platforms closes every real replica. No-op on healthy
    # (all-ids-present) docs; never fabricates an id from a degraded read.
    _backfill_close_replicas "$file" "$local_id"
    # kind=linked carries its own field set, so the strict RAW validator inside
    # close-platforms rejects it ("raw metadata fields are missing, extra, or
    # reordered") - every I-* close failed and linked replicas stayed OPEN.
    local _effect_kind _effect_cmd
    _effect_kind="$(_fm_get "$file" "kind")"
    if [[ "$_effect_kind" == "linked" ]]; then
      _effect_cmd="close-linked"
    else
      _effect_cmd="close-platforms"
    fi
    local _effect_rc=0
    _raw_effect "$_effect_cmd" "$file" "$ROOT_DIR" || _effect_rc=$?
    if [[ "$_effect_rc" -eq 0 ]]; then
      echo "[issue-sync] close complete: $local_id"
      return 0
    fi
    if [[ "$_effect_rc" -eq 3 ]]; then
      echo "[ERROR] issue-sync close: partial close for $local_id — at least one platform is still open; rerun to finish" >&2
      return 3
    fi
    echo "[ERROR] issue-sync close: configured platform close failed for $local_id" >&2
    return 1
  fi

  gh_id=$(_gh_issue_number "$file")
  gitee_id=$(_gitee_resolve_issue_number "$file" "$local_id")

  # Fallback: if I-* has no platform_ids, trace up to raw-* parent.
  # Supports both promoted_from (legacy) and parent_raw (post-2026-06-20).
  local kind="$(_fm_get "$file" "kind")"
  if [[ -z "$gh_id" && -z "$gitee_id" && "$kind" == "linked" ]]; then
    local parent_id="$(_fm_get "$file" "parent_raw")"
    [[ -z "$parent_id" ]] && parent_id="$(_fm_get "$file" "promoted_from")"
    if [[ -n "$parent_id" ]]; then
      local parent_file="$ISSUES_DIR/$parent_id/issue.md"
      if [[ -f "$parent_file" ]]; then
        gh_id=$(_gh_issue_number "$parent_file")
        gitee_id=$(_gitee_resolve_issue_number "$parent_file" "$parent_id")
        echo "[issue-sync] close fallback: using parent $parent_id platform_ids (gh=$gh_id, gitee=$gitee_id)"
      fi
    fi
  fi

  # Fallback 2: search GitHub by raw-key in title (raw-key is universal identifier).
  # All artefacts carry raw-key — worktree, branch, raw issue, I-* issue.
  if [[ -z "$gh_id" && -n "${GH_REPO:-}" ]]; then
    local _search_key="${local_id#raw-}"
    [[ "$_search_key" == "$local_id" ]] && _search_key="${local_id#I-}"
    local _found
    _found=$(gh issue list -R "$GH_REPO" --search "raw-${_search_key} in:title" --state open --json number --jq '.[0].number' 2>/dev/null || true)
    if [[ -z "$_found" ]]; then
      _found=$(gh issue list -R "$GH_REPO" --search "${local_id} in:title" --state open --json number --jq '.[0].number' 2>/dev/null || true)
    fi
    if [[ -n "$_found" ]]; then
      gh_id="$_found"
      echo "[issue-sync] close fallback: found GitHub #$gh_id by raw-key search"
    fi
  fi

  # If all fallbacks exhausted, error instead of silently skipping.
  if [[ -z "$gh_id" && -z "$gitee_id" ]]; then
    echo "[ERROR] issue-sync close: cannot find platform issue for $local_id" >&2
    echo "  platform_ids empty, parent raw has no platform_ids, GitHub search found nothing." >&2
    echo "  Please verify the issue was created on a platform, or close it manually." >&2
    exit 1
  fi

  # Legacy path: per-platform accounting. `platform_state=closed` is an assertion
  # about EVERY configured platform, so it may only be written after all of them
  # accepted the close (#4184). Partial success is retryable and must stay visible
  # to the batch scanner as unsynced.
  local closed_count=0 failed_count=0 status_line=""
  if [[ -n "${GH_REPO:-}" && -n "$gh_id" ]]; then
    echo "[issue-sync] GitHub: closing #$gh_id"
    if _gh_close "$gh_id" "$reason" >/dev/null; then
      closed_count=$((closed_count + 1)); status_line+="github: closed; "
    else
      failed_count=$((failed_count + 1)); status_line+="github: error; "
      echo "[issue-sync] GitHub: close FAILED" >&2
    fi
  fi

  if [[ -n "${GITEE_REPO:-}" && -n "$gitee_id" ]]; then
    echo "[issue-sync] Gitee: closing $gitee_id"
    if _gitee_close "$gitee_id" >/dev/null; then
      closed_count=$((closed_count + 1)); status_line+="gitee: closed; "
    else
      failed_count=$((failed_count + 1)); status_line+="gitee: error; "
      echo "[issue-sync] Gitee: close FAILED" >&2
    fi
  fi

  echo "[issue-sync] close status: ${status_line%; }"
  if [[ "$failed_count" -gt 0 ]]; then
    if [[ "$closed_count" -gt 0 ]]; then
      echo "[ERROR] issue-sync close: partial close for $local_id — at least one platform is still open; rerun to finish" >&2
      return 3
    fi
    echo "[ERROR] issue-sync close: no platform accepted the close for $local_id" >&2
    return 1
  fi

  _fm_set_str "$file" "platform_state" "closed"
  echo "[issue-sync] close complete: $local_id"
}
