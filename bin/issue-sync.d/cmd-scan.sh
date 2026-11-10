#!/usr/bin/env bash
# cmd-scan.sh — sourced by bin/issue-sync, never executed directly.
# `issue-sync scan` — report what would change, no writes.

cmd_scan() {
  local last_scan
  last_scan=$(_scan_state_get "last_sync_at")
  echo "last_sync_at: ${last_scan:-never}"
  echo ""
  echo "Changed issues since last sync:"
  local found=0
  local _scan_tmp
  _scan_tmp=$(mktemp /tmp/issue-sync-scan.XXXXXX)
  { find "$ISSUES_DIR" -name "issue.md" -print0 2>/dev/null; find "$ROOT_DIR/docs/B2-docs" -name "I-*.md" -print0 2>/dev/null; } > "$_scan_tmp"
  # Collect before printing so the report can be ordered P0 -> P1 -> P2 (#4187).
  # The rank prefix is stripped after a stable sort; ties keep discovery order.
  local -a _scan_rows=()
  while IFS= read -r -d '' issue_file; do
    [[ -n "$issue_file" ]] || continue
    local dir local_id
    dir=$(dirname "$issue_file")
    local_id=$(basename "$dir")
    [[ "$local_id" == raw-* || "$local_id" == I-* ]] || continue

    local kind phase severity _rank
    kind=$(_fm_get "$issue_file" "kind")
    phase=$(_fm_get "$issue_file" "phase_state")
    severity=$(_fm_get "$issue_file" "severity")
    case "$severity" in
      P0) _rank=0 ;;
      P1) _rank=1 ;;
      *) severity="P2"; _rank=2 ;;
    esac

    if [[ "$kind" == "linked" ]] && _changed_since_last_sync "$local_id" "$issue_file"; then
      _scan_rows+=("$_rank|  UPDATE $local_id  kind=$kind phase=$phase sev=$severity  $(_issue_title "$issue_file" "$local_id")")
      found=1
    elif [[ "$kind" == "raw" ]] && ! _already_on_platform "$issue_file" "github" 2>/dev/null; then
      _scan_rows+=("$_rank|  CREATE $local_id  kind=$kind phase=$phase sev=$severity  $(_issue_title "$issue_file" "$local_id")")
      found=1
    fi
  done < "$_scan_tmp"
  rm -f "$_scan_tmp"

  if [[ ${#_scan_rows[@]} -gt 0 ]]; then
    printf '%s\n' "${_scan_rows[@]}" | sort -t'|' -k1,1 -s | cut -d'|' -f2-
  fi
  [[ "$found" -eq 0 ]] && echo "  (none)"
}
