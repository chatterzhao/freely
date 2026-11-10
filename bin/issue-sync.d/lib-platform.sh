#!/usr/bin/env bash
# lib-platform.sh — sourced by bin/issue-sync, never executed directly.
# Platform I/O: repo detection, write wrappers, platform_ids bookkeeping.

# ── platform detection ───────────────────────────────────

_gh_repo() {
  gh repo view --json nameWithOwner -q '.nameWithOwner' 2>/dev/null || echo ""
}

# Accept every remote URL shape git can hand us: scp-like (`git@host:owner/repo.git`),
# ssh/https URLs, and host paths. The previous awk kept the `git@host:` prefix and the
# trailing `.git`, producing a value no API accepts (#4149).
_gitee_repo_from_url() {
  local url="${1:-}" path
  [[ -n "$url" ]] || return 0
  path="${url#*://}"
  if [[ "$path" == "$url" ]]; then
    path="${url#*:}"          # scp-like: [user@]host:owner/repo(.git)
  else
    path="${path#*/}"         # drop scheme + host
  fi
  path="${path#/}"
  path="${path%.git}"
  [[ "$path" == */* ]] && printf '%s\n' "$path"
  return 0
}

_gitee_repo() {
  local url
  url=$(git remote get-url origin 2>/dev/null || true)
  if [[ "$url" != *gitee* ]]; then
    url=$(git remote -v 2>/dev/null | awk '/gitee.*\(push\)/ {print $2; exit}')
  fi
  _gitee_repo_from_url "$url"
}

# ── GitHub ops ───────────────────────────────────────────
# #4166: writes go through platform-adapter.py (`issue-write-one`), so this
# script only orchestrates. Direct shell-level platform writes meant every
# entry point had its own label/body/error behaviour.

_platform_adapter_py() {
  printf '%s\n' "$ROOT_DIR/docs/system/workspace/scripts/sync/platform-adapter.py"
}

_gh_write() {
  local action="$1"; shift
  FREELY_PLATFORM_REPO="$GH_REPO" \
    python3 "$(_platform_adapter_py)" issue-write-one github "$action" "$@"
}

_gh_create() {
  local title="$1" body="$2" labels="$3"
  local result url
  result="$(_gh_write create "" "$title" "$body" "$labels" 2>&1 || true)"
  # The adapter answers JSON, so stop at the closing quote instead of taking
  # the rest of the line (`NEW88"}}` used to become the issue id).
  url=$(printf '%s\n' "$result" | grep -o 'https://github.com/[^"]*' | head -1)
  printf '%s\n' "${url:-}"
}

_gh_comment() {
  local issue_number="$1" message="$2"
  if _gh_write comment "$issue_number" "" "$message" >/dev/null 2>&1; then
    echo "ok"
  else
    echo "fail"
  fi
}

_gh_close() {
  local issue_number="$1" reason="${2:-completed}"
  # The adapter closes through the platform handler; `--reason` is not part of
  # the cross-platform contract, so the closed state is what callers can rely on.
  if _gh_write close "$issue_number" >/dev/null 2>&1; then
    echo "ok"; return 0
  fi
  echo "fail"; return 1
}

_gh_update() {
  local issue_number="$1" title="$2" body="$3" labels="$4"
  _gh_write update "$issue_number" "$title" "$body" "$labels" >/dev/null 2>&1 || true
  echo "ok"
}

# ── Gitee ops ────────────────────────────────────────────

# Gitee writes use the SAME CLI contract the adapter uses
# (`gitee-issue.py --repo <repo> <subcommand> [flags]`). The previous helper passed
# a JSON blob as a positional argument, so argparse exited 2 on every call and
# a trailing `|| echo` fallback then turned that into a valid-looking empty
# result, so every write "succeeded" without touching the platform (#4149).
_gitee_cli() {
  local action="$1"; shift
  [[ -n "${GITEE_REPO:-}" ]] || { echo "[issue-sync] gitee repo unknown" >&2; return 2; }
  python3 "$ROOT_DIR/docs/system/workspace/scripts/runtime/gitee-issue.py" \
    --repo "$GITEE_REPO" "$action" "$@"
}

_gitee_create()  { _gitee_cli create --title "${1:-}" --body "${2:-}"; }
_gitee_update()  { _gitee_cli update "${1:-}" --title "${2:-}" --body "${3:-}"; }
_gitee_comment() { _gitee_cli comment "${1:-}" --body "${2:-}"; }

_gitee_close() {
  local num="${1:-}" comment="${2:-}"
  if [[ -n "$comment" ]]; then
    _gitee_cli close "$num" --comment "$comment"
  else
    _gitee_cli close "$num"
  fi
}

# Pull the platform id out of the JSON the CLI prints.
_gitee_issue_number_from_json() {
  python3 -c 'import json, sys
try:
    d = json.load(sys.stdin)
except Exception:
    print("")
else:
    print(d.get("number") or d.get("id") or "")'
}

# ── platform_ids helpers ─────────────────────────────────

_gh_issue_number() {
  local file="$1"
  python3 -c "
import yaml, json
with open('$file') as f: content = f.read()
parts = content.split('---', 2)
if len(parts) >= 3:
  fm = yaml.safe_load(parts[1]) or {}
  ids = fm.get('platform_ids', {}) or {}
  gh = ids.get('github', {}) or {}
  print(gh.get('issue_id', ''))
" 2>/dev/null || true
}

_gitee_issue_id() {
  local file="$1"
  python3 -c "
import yaml
yaml.SafeLoader.yaml_implicit_resolvers.pop('tag:yaml.org,2002:timestamp', None)
with open('$file') as f: content = f.read()
parts = content.split('---', 2)
if len(parts) >= 3:
  fm = yaml.safe_load(parts[1]) or {}
  ids = fm.get('platform_ids', {}) or {}
  gt = ids.get('gitee', {}) or {}
  print(gt.get('issue_id', ''))
" 2>/dev/null || true
}

_update_platform_ids() {
  local file="$1" platform="$2" issue_id="$3" url="$4"
  local ts; ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  python3 -c "
import yaml, re
# Disable timestamp auto-parsing to preserve datetime string format.
yaml.SafeLoader.yaml_implicit_resolvers.pop('tag:yaml.org,2002:timestamp', None)
with open('$file') as f: content = f.read()
parts = content.split('---', 2)
fm = yaml.safe_load(parts[1]) if len(parts) >= 3 else {}
fm.setdefault('platform_ids', {})

# Only update platform_ids if the issue_id actually changed.
existing = fm.get('platform_ids', {}).get('$platform', {}).get('issue_id', '')
platform_changed = (str(existing) != '$issue_id')

fm['platform_ids']['$platform'] = {'issue_id': '$issue_id', 'url': '$url', 'synced_at': '$ts'}

# Only set updated_at when platform data materially changed.
if platform_changed:
    fm['updated_at'] = '$ts'

if not fm.get('primary_platform'): fm['primary_platform'] = '$platform'

# Infer created_at from raw key timestamp when missing.
# raw-20260619T030248Z → 2026-06-19T03:02:48Z
if not fm.get('created_at'):
    local_id = fm.get('local_id', '')
    m = re.match(r'(?:raw-)?(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})Z', local_id or '')
    if m:
        fm['created_at'] = f\"{m[1]}-{m[2]}-{m[3]}T{m[4]}:{m[5]}:{m[6]}Z\"
    else:
        fm['created_at'] = '$ts'  # fallback

new_fm = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False).strip()
body_text = parts[2] if len(parts) >= 3 else ''
with open('$file', 'w') as f: f.write('---\n' + new_fm + '\n---' + body_text)
" 2>/dev/null || true
}

# Fallback: search Gitee for issue by [RAW-{key}] or [I-{key}] title prefix
_gitee_find_by_local_id() {
  local local_id="$1"
  local search_prefix
  if [[ "$local_id" == raw-* ]]; then
    search_prefix="[RAW-${local_id#raw-}]"
  else
    search_prefix="[${local_id}]"
  fi
  local result
  result=$(python3 "$ROOT_DIR/docs/system/workspace/scripts/runtime/gitee-issue.py" \
    --repo "${GITEE_REPO:-}" list --state open --per-page 50 2>/dev/null | \
    python3 -c "
import sys,json
issues=json.load(sys.stdin)
for i in issues:
    if '${search_prefix}' in i.get('title',''):
        print(i.get('number', i.get('id','')))
        break
" 2>/dev/null || true)
  if [[ -n "$result" && "$result" != "null" ]]; then
    echo "$result"
    return 0
  fi
  return 1
}

# Get or find platform issue number, with fallback search by title (both platforms)
_gitee_resolve_issue_number() {
  local file="$1" local_id="$2"
  local num
  num=$(_gitee_issue_id "$file")
  if [[ -z "$num" || "$num" == "None" ]]; then
    num=$(_gitee_find_by_local_id "$local_id" || true)
    if [[ -n "$num" ]]; then
      echo "[issue-sync] found Gitee issue #$num by title search for $local_id" >&2
      _update_platform_ids "$file" "gitee" "$num" "https://gitee.com/${GITEE_REPO:-}/issues/$num"
    fi
  fi
  echo "$num"
}
