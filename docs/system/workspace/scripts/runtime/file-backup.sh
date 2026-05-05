#!/usr/bin/env bash

backup_file_with_timestamp() {
  local target_path="$1"
  local timestamp backup_path suffix
  [[ -f "$target_path" && -s "$target_path" ]] || return 0
  timestamp="$(date -u '+%Y%m%dT%H%M%SZ')"
  backup_path="${target_path}.backup-${timestamp}"
  suffix=1
  while [[ -e "$backup_path" ]]; do
    backup_path="${target_path}.backup-${timestamp}-${suffix}"
    suffix=$((suffix + 1))
  done
  cp -p "$target_path" "$backup_path" 2>/dev/null || cp "$target_path" "$backup_path"
}
