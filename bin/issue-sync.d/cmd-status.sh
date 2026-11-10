#!/usr/bin/env bash
# cmd-status.sh — sourced by bin/issue-sync, never executed directly.
# `issue-sync status` — read-only projection of one document.

cmd_status() {
  local local_id="$1" file
  if ! file="$(_issue_file_for "$local_id")"; then
    echo "[ERROR] issue-sync: cannot resolve issue document for $local_id" >&2
    echo "  checked: $ISSUES_DIR/$local_id/issue.md and docs/B2-docs/**/issues/$local_id.md" >&2
    exit 1
  fi

  echo "local_id:        $local_id"
  echo "kind:            $(_fm_get "$file" "kind")"
  echo "phase_state:     $(_fm_get "$file" "phase_state")"
  echo "issue_title:     $(_issue_title "$file" "$local_id")"
  echo "primary_platform: $(_fm_get "$file" "primary_platform")"
  echo "platform_ids:"
  python3 -c "
import yaml
yaml.SafeLoader.yaml_implicit_resolvers.pop('tag:yaml.org,2002:timestamp', None)
with open('$file') as f: content = f.read()
parts = content.split('---', 2)
if len(parts) >= 3:
  fm = yaml.safe_load(parts[1]) or {}
  ids = fm.get('platform_ids', {}) or {}
  for plat, info in ids.items():
    if isinstance(info, dict):
      print(f'  {plat}: #{info.get(\"issue_id\",\"?\")}  {info.get(\"url\",\"\")}  synced={info.get(\"synced_at\",\"?\")}')
" 2>/dev/null || true
  echo "platform_title:  $(_platform_title "$local_id" "$file")"
}
