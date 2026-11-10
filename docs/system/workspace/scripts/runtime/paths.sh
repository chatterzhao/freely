#!/usr/bin/env bash
# paths.sh — single owner for runtime resource paths (#4154).
#
# Every consumer must call these helpers instead of re-deriving a relative
# path. A wrong copy does not fail: `bin/deploy-skills` fell back to
# tools="claude" and ACP tool setup logged one warning and skipped itself.
#
# Usage:
#   source runtime/paths.sh
#   registry="$(freely_tool_registry_path "$ROOT")"

freely_tool_registry_path() {
  local root="${1:-}"
  [[ -n "$root" ]] || return 2
  printf '%s\n' "$root/docs/system/workspace/tools/tool-registry.toml"
}

freely_tool_registry_query_path() {
  local root="${1:-}"
  [[ -n "$root" ]] || return 2
  printf '%s\n' "$root/docs/system/workspace/scripts/runtime/tool-registry-query.py"
}
