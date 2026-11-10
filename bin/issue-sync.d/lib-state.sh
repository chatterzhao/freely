#!/usr/bin/env bash
# lib-state.sh — sourced by bin/issue-sync, never executed directly.
# Scan-state bookkeeping and change detection (`_changed_since_last_sync`).

SCAN_STATE="$ISSUES_DIR/.scan-state"
_scan_state_get() {
  local key="$1"
  [[ -f "$SCAN_STATE" ]] || return 0
  python3 -c "import json; d=json.load(open('$SCAN_STATE')); print(d.get('$key',''))" 2>/dev/null || true
}

_scan_state_set() {
  local key="$1" value="$2"
  local tmp
  tmp=$(python3 -c "
import json, os
state = {}
if os.path.exists('$SCAN_STATE'):
  with open('$SCAN_STATE') as f: state = json.load(f)
state['$key'] = $value
print(json.dumps(state, indent=2, default=str))
" 2>/dev/null || true)
  printf '%s\n' "$tmp" > "$SCAN_STATE"
}

_scan_state_record_sync() {
  local local_id="$1" file="$2"
  local ts mtime
  ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  mtime=$(stat -f %m "$file" 2>/dev/null || echo 0)
  python3 -c "
import json, os
state = {}
if os.path.exists('$SCAN_STATE'):
  with open('$SCAN_STATE') as f: state = json.load(f)
state['last_sync_at'] = '$ts'
state.setdefault('synced_issues', {})
state['synced_issues']['$local_id'] = {'mtime': $mtime, 'synced_at': '$ts'}
with open('$SCAN_STATE', 'w') as f: json.dump(state, f, indent=2, default=str)
" 2>/dev/null || true
}

# Check if platform_ids already has a live issue for a platform.
# Returns 0 (already exists) if found, 1 (needs create) otherwise.
_already_on_platform() {
  local file="$1" platform="$2"
  local pid
  pid=$(python3 -c "
import yaml
yaml.SafeLoader.yaml_implicit_resolvers.pop('tag:yaml.org,2002:timestamp', None)
with open('$file') as f: content = f.read()
parts = content.split('---', 2)
if len(parts) >= 3:
  fm = yaml.safe_load(parts[1]) or {}
  ids = fm.get('platform_ids', {}) or {}
  p = ids.get('$platform', {}) or {}
  val = p.get('issue_id', '')
  print(val)
" 2>/dev/null || true)
  [[ -n "$pid" && "$pid" != "None" ]]
}
# Content hash for change detection.
_content_hash() {
  local file="$1"
  python3 -c "
import hashlib
with open('$file') as f: content = f.read()
print(hashlib.sha256(content.encode()).hexdigest()[:16])
" 2>/dev/null || true
}

# Check if content changed since last sync.
# Returns 1 (unchanged) on first run (no stored hash = nothing to compare).
_changed_since_last_sync() {
  local local_id="$1" file="$2"
  local last_hash current_hash
  last_hash=$(python3 -c "
import json, os
if os.path.exists('$SCAN_STATE'):
  with open('$SCAN_STATE') as f: state = json.load(f)
  synced = state.get('synced_issues', {}).get('$local_id', {})
  print(synced.get('hash', ''))
" 2>/dev/null || true)
  # No previous hash = first sync of this issue. Consider it unchanged
  # to avoid spamming updates on initial batch run.
  [[ -z "$last_hash" || "$last_hash" == "None" ]] && return 1
  current_hash=$(_content_hash "$file")
  [[ "$last_hash" != "$current_hash" ]]
}
