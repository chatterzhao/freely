#!/usr/bin/env bash
# lib-content.sh — sourced by bin/issue-sync, never executed directly.
# Platform projection: title, body and labels for an issue document.

# Check if there are unsynced comments since last_synced_comment_at.
# _comment_blocks: parse every "### comment-<ts>" block in the document body.
# Prints "<ts>\t<body-on-one-line>" per block, oldest first.
_comment_blocks() {
  python3 -c "
import re
with open('$1') as f:
    content = f.read()
parts = content.split('---', 2)
body = parts[2] if len(parts) >= 3 else content
pattern = re.compile(r'### (comment-\S+)\n(.*?)(?=\n### comment-|\Z)', re.DOTALL)
for match in pattern.finditer(body):
    ts = match.group(1)[len('comment-'):]
    text = match.group(2)
    lines = text.split('\n')
    # strip the optional metadata prefix: a {json} line or leading '- key:' bullets
    while lines and (not lines[0].strip() or lines[0].startswith('- ') or lines[0].startswith('{')):
        lines.pop(0)
    print(ts + '\t' + '\\n'.join(lines).strip())
" 2>/dev/null || true
}

_last_comment_body() {
  python3 -c "
import re
with open('$1') as f:
    content = f.read()
parts = content.split('---', 2)
body = parts[2] if len(parts) >= 3 else content
pattern = re.compile(r'### (comment-\S+)\n(.*?)(?=\n### comment-|\Z)', re.DOTALL)
blocks = list(pattern.finditer(body))
if not blocks:
    raise SystemExit(0)
text = blocks[-1].group(2)
lines = text.split('\n')
while lines and (not lines[0].strip() or lines[0].startswith('- ') or lines[0].startswith('{')):
    lines.pop(0)
print('\n'.join(lines).strip())
" 2>/dev/null || true
}

_has_unsynced_comments() {
  local file="$1" platform="$2"
  local last_sync
  last_sync=$(python3 -c "
import yaml
yaml.SafeLoader.yaml_implicit_resolvers.pop('tag:yaml.org,2002:timestamp', None)
with open('$file') as f: content = f.read()
parts = content.split('---', 2)
if len(parts) >= 3:
  fm = yaml.safe_load(parts[1]) or {}
  lsca = fm.get('last_synced_comment_at', {}) or {}
  print(lsca.get('$platform', ''))
" 2>/dev/null || true)
  [[ -z "$last_sync" || "$last_sync" == "None" ]] && return 0  # never synced
  # Any comment block newer than the last sync counts, whatever its metadata
  # shape and wherever it sits (system events are not under `## Comments`).
  # Both timestamps are UTC and fixed width, so plain string compare is exact.
  local normalised_sync="${last_sync//-/}"
  normalised_sync="${normalised_sync//:/}"
  normalised_sync="${normalised_sync:0:15}"
  local ts _rest
  while IFS=$'\t' read -r ts _rest; do
    [[ -z "$ts" ]] && continue
    if [[ "${ts:0:15}" > "$normalised_sync" ]]; then
      return 0
    fi
  done < <(_comment_blocks "$file")
  return 1
}
_issue_title() {
  local file="$1" local_id="$2"
  local title
  title=$(_fm_get "$file" "issue_title")
  if [[ -n "$title" && "$title" != "None" ]]; then
    printf '%s\n' "$title"
    return 0
  fi
  # Fallback: first # heading in body, or canonical doc
  title=$(awk '/^---$/ && !skipped{skipped=1; next} /^---$/ && skipped{skipped=0; next} /^# /{print substr($0,3); exit}' "$file")
  if [[ -z "$title" ]]; then
    local canon; canon=$(_fm_get "$file" "canonical_issue_path")
    if [[ -n "$canon" && "$canon" != "None" && -f "$ROOT_DIR/$canon" ]]; then
      title=$(head -5 "$ROOT_DIR/$canon" | sed -n 's/^# //p' | head -1)
    fi
  fi
  printf '%s\n' "${title:-$local_id}"
}

_platform_title() {
  local local_id="$1" file="$2"
  local kind title
  kind=$(_fm_get "$file" "kind")
  title=$(_issue_title "$file" "$local_id")
  # Single source of truth shared with platform-adapter.pull_raw_issue() and
  # `freely feedback edit --title` (see sync/raw_title_contract.py).
  # linked/other kinds keep their historical projection unchanged.
  python3 - "$ROOT_DIR/docs/system/workspace/scripts/sync" "$local_id" "$kind" "$title" <<'PY'
import sys
sys.path.insert(0, sys.argv[1])
from raw_title_contract import platform_title
print(platform_title(sys.argv[2], sys.argv[3], sys.argv[4]))
PY
}

# ── body + label projection ──────────────────────────────
# #4166: the shape of a platform issue lives in exactly one place —
# sync/issue_create_contract.py — shared with `freely feedback` and with
# `issue-sync update`. The previous inline `awk` strip only removed the `---`
# markers, so the YAML keys were published as body text, and the label list was
# a second literal that `feedback` kept in sync by hand.

_ISSUE_CREATE_CONTRACT="$ROOT_DIR/docs/system/workspace/scripts/sync/issue_create_contract.py"

_issue_body() {
  local file="$1" local_id="$2" title
  title="$(_issue_title "$file" "$local_id")"
  python3 "$_ISSUE_CREATE_CONTRACT" body \
    --file "$file" --local-id "$local_id" --title "$title"
}

_labels() {
  local file="$1"
  python3 "$_ISSUE_CREATE_CONTRACT" labels --file "$file"
}
