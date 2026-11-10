#!/usr/bin/env bash
# cmd-promote-finalize.sh — sourced by bin/issue-sync, never executed directly.
# `issue-sync promote-finalize` — absorb the raw and close it everywhere.

# cmd_promote_finalize: close raw after all children promoted.
# Adds closing comment listing all I-* children, then closes raw on platforms.
cmd_promote_finalize() {
  local raw_id="$1"
  local raw_file
  raw_file="$ISSUES_DIR/$raw_id/issue.md"
  [[ -f "$raw_file" ]] || { echo "[ERROR] $raw_file not found" >&2; exit 1; }

  local promoted_json children_text
  promoted_json=$(_fm_get "$raw_file" "promoted_children")
  if [[ -z "$promoted_json" || "$promoted_json" == "None" ]]; then
    echo "[issue-sync] promote-finalize: no children to finalize for $raw_id"
    return 1
  fi

  # Build closing comment listing all children
  children_text=$(python3 -c "
import json
children = json.loads('$promoted_json')
lines = ['拆解为以下任务:']
for i, cid in enumerate(children, 1):
    lines.append(f'{i}. [{cid}](will-be-updated)')
print('\n'.join(lines))
" 2>/dev/null || echo "Promoted to: $promoted_json")

  # Strict metadata derives the first verifiable canonical relation from registered children.
  local finalized_at; finalized_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  if [[ "$(_fm_get "$raw_file" "schema_version")" == "1" ]]; then
    _raw_effect finalize "$raw_file" "$ROOT_DIR" "$finalized_at"
  else
    _fm_set_str "$raw_file" "phase_state" "absorbed"
  fi

  # Add one retry-safe closing comment to raw.
  if ! grep -q '^- event: promote_finalized$' "$raw_file"; then
    cat >> "$raw_file" <<COMMENT

### comment-$(date -u +"%Y%m%dT%H%M%SZ")
- source: system
- event: promote_finalized
- children: $promoted_json

$children_text
COMMENT
  fi

  # Platform synchronization follows the local terminal transition. A failed close
  # leaves absorbed/open state for an idempotent batch retry.
  cmd_comment "$raw_id"
  cmd_close "$raw_id" "completed"

  echo "[issue-sync] promote-finalize complete: $raw_id closed with $promoted_json"
}
