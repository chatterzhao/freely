#!/usr/bin/env bash
# lib-frontmatter.sh — sourced by bin/issue-sync, never executed directly.
# Frontmatter, issue-document resolution and raw lifecycle effects.
# Single owner of every `_fm_*` call: the lifecycle CLI, never inline YAML.

_fm_get() {
  python3 "$_FM_CLI" get --file "$1" --key "$2" 2>/dev/null || true
}

_fm_set() {
  python3 "$_FM_CLI" set --file "$1" --key "$2" --value "$3" 2>/dev/null || true
}

_fm_set_str() {
  local file="$1" key="$2" value="$3"
  _fm_set "$file" "$key" "'$value'"
}

# _issue_file_for: resolve an issue document by local id across both layouts.
#   B1: docs/B1-docs/<id>/issue.md
#   B2: docs/B2-docs/**/issues/<id>.md
# `promote` used to hand a B2 I-* id to cmd_create, which only knew the B1 layout,
# so platform creation for promoted issues could never succeed (#4183).
_issue_file_for() {
  local local_id="$1" direct
  direct="$ISSUES_DIR/$local_id/issue.md"
  if [[ -f "$direct" ]]; then
    printf '%s\n' "$direct"
    return 0
  fi
  local -a matches=()
  local found
  while IFS= read -r found; do
    [[ -n "$found" ]] && matches+=("$found")
  done < <(find "$ROOT_DIR/docs/B2-docs" -type f -path "*/issues/${local_id}.md" 2>/dev/null || true)
  if [[ ${#matches[@]} -eq 0 ]]; then
    # Legacy fallback: some historical B2 trees carry a filename prefix variant.
    while IFS= read -r found; do
      [[ -n "$found" ]] && matches+=("$found")
    done < <(find "$ROOT_DIR/docs/B2-docs" -type f -path "*/issues/${local_id}-*.md" 2>/dev/null || true)
  fi
  if [[ ${#matches[@]} -eq 0 ]]; then
    return 1
  fi
  if [[ ${#matches[@]} -gt 1 ]]; then
    printf '[issue-sync] ambiguous issue document for %s:\n' "$local_id" >&2
    printf '  %s\n' "${matches[@]}" >&2
    return 2
  fi
  printf '%s\n' "${matches[0]}"
}

_fm_has_key() {
  python3 "$_FM_CLI" has-key --file "$1" --key "$2" 2>/dev/null
}

_raw_effect() {
  local contract_root="${RAW_METADATA_CONTRACT_ROOT:-$ROOT_DIR}"
  PYTHONPATH="$contract_root/docs/system/workspace/scripts/lifecycle" python3 \
    "$contract_root/docs/system/workspace/scripts/lifecycle/raw_lifecycle_effects.py" "$@"
}

_raw_transition_if_strict() {
  local file="$1" event="$2" issue_id="${3:-}" issue_path="${4:-}"
  local source_candidate="${5:-}" at="${6:-}" note="${7:-}"
  [[ "$(_fm_get "$file" "schema_version")" == "1" ]] || return 1
  _raw_effect transition "$file" "$event" "$ROOT_DIR" "$issue_id" "$issue_path" \
    "$source_candidate" "$at" "$note"
}
