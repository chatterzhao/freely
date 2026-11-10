#!/usr/bin/env bash
# cmd-create.sh — sourced by bin/issue-sync, never executed directly.
# `issue-sync create` — idempotent platform creation.

cmd_create() {
  local local_id="$1" file
  if ! file="$(_issue_file_for "$local_id")"; then
    echo "[ERROR] issue-sync: cannot resolve issue document for $local_id" >&2
    echo "  checked: $ISSUES_DIR/$local_id/issue.md and docs/B2-docs/**/issues/$local_id.md" >&2
    exit 1
  fi

  local title body labels
  title=$(_platform_title "$local_id" "$file")
  body=$(_issue_body "$file" "$local_id")
  labels=$(_labels "$file")

  local -a _created=() _failed=()
  [[ -n "${GH_REPO:-}" ]] || true

  # ── #4225: consult platform-side identity before creating on a platform that
  # is missing from the local cache. `platform_ids` can be partial after a
  # degraded pull (R6); a missing local id is NOT proof the platform has no
  # replica. Only engage for raw-* issues and only when some configured
  # platform is actually missing locally — the healthy path (all ids present)
  # does zero extra I/O and behaves byte-identically. ──
  local _guard_on=0 _receipt="" _kind
  _kind="$(_fm_get "$file" "kind")"
  if [[ "$local_id" == raw-* && "$_kind" == "raw" \
        && -f "$_ADAPTER_SCRIPT" && -f "$_GUARD_SCRIPT" ]]; then
    local _missing=0
    if [[ -n "${GH_REPO:-}" ]] && ! _already_on_platform "$file" github; then _missing=1; fi
    if [[ -n "${GITEE_REPO:-}" ]] && ! _already_on_platform "$file" gitee; then _missing=1; fi
    if [[ "$_missing" == "1" ]]; then
      _guard_on=1
      _receipt="$(_replica_receipt "${local_id#raw-}")"
    fi
  fi

  # GitHub
  if [[ -n "${GH_REPO:-}" ]]; then
    if _already_on_platform "$file" "github"; then
      echo "[issue-sync] skip create: $local_id already on GitHub"
      _created+=("github")
    else
      local _st _rid _rurl
      IFS=$'\t' read -r _st _rid _rurl <<<"$(_replica_decide "$_guard_on" "$_receipt" github)"
      case "$_st" in
        present)
          # A canonical replica already exists on the platform. Backfill the
          # cached id instead of creating a duplicate (#4225).
          echo "[issue-sync] GitHub: replica $_rid already exists on platform; backfilling platform_ids (no create)"
          _update_platform_ids "$file" "github" "$_rid" "$_rurl"
          _created+=("github")
          ;;
        indeterminate)
          # Transport blip / ambiguous identity is not a verdict (R7/#4195).
          # Refuse to create: creating now could duplicate an existing replica.
          echo "[issue-sync] GitHub: platform-side identity undetermined; refusing to create (rerun after platform recovers)" >&2
          _failed+=("github")
          ;;
        *)  # absent — platform confirmed no replica; original create path.
          echo "[issue-sync] GitHub: creating issue..."
          local url=""
          url=$(_gh_create "$title" "$body" "$labels") || url=""
          if [[ -n "$url" ]]; then
            local gh_num; gh_num=$(basename "$url")
            echo "[issue-sync] GitHub: $url"
            _update_platform_ids "$file" "github" "$gh_num" "$url"
            _created+=("github")
          else
            echo "[issue-sync] GitHub: FAILED (no issue url returned)" >&2
            _failed+=("github")
          fi
          ;;
      esac
    fi
  fi

  # Gitee. The token lives in gitee-issue.py (freely_user_env); gating here on a
  # shell variable this script never assigns silently skipped the whole channel.
  if [[ -n "${GITEE_REPO:-}" ]]; then
    if _already_on_platform "$file" "gitee"; then
      echo "[issue-sync] skip create: $local_id already on Gitee"
      _created+=("gitee")
    else
      local _gst _grid _grurl
      IFS=$'\t' read -r _gst _grid _grurl <<<"$(_replica_decide "$_guard_on" "$_receipt" gitee)"
      case "$_gst" in
        present)
          echo "[issue-sync] Gitee: replica $_grid already exists on platform; backfilling platform_ids (no create)"
          _update_platform_ids "$file" "gitee" "$_grid" "$_grurl"
          _created+=("gitee")
          ;;
        indeterminate)
          echo "[issue-sync] Gitee: platform-side identity undetermined; refusing to create (rerun after platform recovers)" >&2
          _failed+=("gitee")
          ;;
        *)  # absent — original create path.
          echo "[issue-sync] Gitee: creating issue..."
          local out="" rc=0 num=""
          out=$(_gitee_create "$title" "$body" 2>&1) || rc=$?
          num=$(printf '%s' "$out" | _gitee_issue_number_from_json 2>/dev/null || true)
          if [[ "$rc" -eq 0 && -n "$num" ]]; then
            echo "[issue-sync] Gitee: created $num"
            _update_platform_ids "$file" "gitee" "$num" "https://gitee.com/$GITEE_REPO/issues/$num"
            _created+=("gitee")
          else
            echo "[issue-sync] Gitee: FAILED (rc=$rc) $(printf '%s' "$out" | tail -1)" >&2
            _failed+=("gitee")
          fi
          ;;
      esac
    fi
  fi

  # platform_state is a claim about ALL configured platforms. Writing it while any
  # platform has no id is exactly the self-certification #4149 is about, and the
  # batch scanner then skips the issue forever (#793 uses the same field).
  if [[ ${#_failed[@]} -eq 0 ]]; then
    _scan_state_record_sync "$local_id" "$file"
    # `platform_state` is a raw-issue field; linked I-* documents do not declare
    # it and adding it would silently change their schema.
    if _fm_has_key "$file" "platform_state"; then
      _fm_set_str "$file" "platform_state" "open"
    fi
    echo "[issue-sync] create complete: $local_id"
    return 0
  fi
  if [[ ${#_created[@]} -eq 0 ]]; then
    echo "[issue-sync] create FAILED on every configured platform: ${_failed[*]}" >&2
    exit 1
  fi
  echo "[issue-sync] create PARTIAL: created=${_created[*]} failed=${_failed[*]}" >&2
  echo "[issue-sync] platform_state left unchanged; re-run 'issue-sync create $local_id' to heal" >&2
  exit 3
}
