#!/usr/bin/env bash
# cmd-promote.sh — sourced by bin/issue-sync, never executed directly.
# `issue-sync promote` — create the I-* child, keep raw open.

cmd_promote() {
  local raw_id="$1" i_id="$2"
  local raw_file i_file
  raw_file="$ISSUES_DIR/$raw_id/issue.md"
  [[ -f "$raw_file" ]] || { echo "[ERROR] $raw_file not found" >&2; exit 1; }
  if ! i_file="$(_issue_file_for "$i_id")"; then
    echo "[ERROR] issue-sync promote: cannot resolve the B2 document for $i_id" >&2
    echo "  looked for docs/B2-docs/**/issues/$i_id.md" >&2
    exit 1
  fi

  echo "[issue-sync] promote: $raw_id → $i_id"

  # 1. Create I-* on platforms (with kind/linked label)
  cmd_create "$i_id"

  # 2. Record promotion without changing the raw phase.
  local promoted_at; promoted_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  if [[ "$(_fm_get "$raw_file" "schema_version")" == "1" ]]; then
    _raw_transition_if_strict "$raw_file" "promotion_started" "$i_id" "" "" "$promoted_at"
  else
    local promoted_json
    promoted_json=$(_fm_get "$raw_file" "promoted_children")
    if [[ -z "$promoted_json" || "$promoted_json" == "None" ]]; then
      _fm_set "$raw_file" "promoted_children" "[\"$i_id\"]"
    else
      local new_list
      new_list=$(python3 -c "import json; lst = json.loads('$promoted_json'); '$i_id' not in lst and lst.append('$i_id'); print(json.dumps(lst))" 2>/dev/null || echo "[\"$i_id\"]")
      _fm_set "$raw_file" "promoted_children" "$new_list"
    fi
  fi

  # 3. Update I-* with cross-reference back to raw
  cat >> "$i_file" <<CROSSREF

### comment-$(date -u +"%Y%m%dT%H%M%SZ")
- source: system
- event: promoted_from
- source_id: $raw_id

Promoted from $raw_id
CROSSREF

  echo "[issue-sync] promote complete: $raw_id → $i_id (raw stays open until all children promoted)"
}
