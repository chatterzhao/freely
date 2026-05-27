# shellcheck shell=bash

_watchdog_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
SELF_ROOT="$(cd "$_watchdog_dir/../../../../../.." && pwd -P)"

NETWORK_PROXY_RESOLVER_LIB="$SELF_ROOT/docs/system/workspace/scripts/runtime/network-proxy-resolver.sh"
[[ -f "$NETWORK_PROXY_RESOLVER_LIB" ]] || {
  echo "[ERROR] missing network proxy resolver module: $NETWORK_PROXY_RESOLVER_LIB" >&2
  return 1
}
# shellcheck disable=SC1090
source "$NETWORK_PROXY_RESOLVER_LIB"

normalize_codex_slot_name() {
  printf '%s' "$1" | sed 's/\./-/g'
}

codex_auto_slot_switch_enabled() {
  local value="${AUTO_SWITCH_SLOT:-true}"
  value="$(printf '%s' "$value" | tr '[:upper:]' '[:lower:]')"
  case "$value" in
    1|true|yes|on) return 0 ;;
    *) return 1 ;;
  esac
}

codex_slot_matches_identity() {
  local slot="$1" identity="$2"
  [[ -n "$slot" && -n "$identity" ]] || return 1
  [[ "$(normalize_codex_slot_name "$slot")" == "$(normalize_codex_slot_name "$identity")" ]]
}

format_epoch_local() {
  local epoch="$1"
  [[ -n "$epoch" ]] || return 1
  date -r "$epoch" '+%Y.%m.%d %H:%M:%S %Z' 2>/dev/null || date -d "@$epoch" '+%Y.%m.%d %H:%M:%S %Z' 2>/dev/null || printf '%s\n' "$epoch"
}

codex_active_slot_file() {
  printf '%s\n' "$HOME/.codex/active-slot"
}

codex_active_auth_file() {
  printf '%s\n' "$HOME/.codex/auth.json"
}

codex_live_auth_kind() {
  local auth_file
  auth_file="$(codex_active_auth_file)"
  python3 - <<'PY' "$auth_file" 2>/dev/null || true
import json
import os
import sys

path = sys.argv[1]
if not os.path.exists(path):
    print("")
    raise SystemExit(0)
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)
if isinstance(data.get("OPENAI_API_KEY"), str) and data.get("OPENAI_API_KEY"):
    print("apikey")
elif isinstance(data.get("tokens"), dict) or isinstance(data.get("access_token"), str):
    print("account")
else:
    print("legacy")
PY
}

watchdog_run_dir_for_project() {
  local project="$1"
  printf '%s\n' "$project/.freely/run"
}

freely_apply_network_proxy_env_for_project() {
  freely_apply_project_network_proxy_env "$1"
}

codex_probe_artifacts_dir_for_project() {
  local project="$1"
  printf '%s\n' "$(watchdog_run_dir_for_project "$project")/codex-probe-artifacts"
}

read_codex_active_slot() {
  local file
  file="$(codex_active_slot_file)"
  [[ -f "$file" ]] || return 0
  tr -d '\n' <"$file"
}

restore_codex_probe_origin() {
  local original_slot="$1" original_active_slot="$2" auth_backup="$3"
  local auth_file
  auth_file="$(codex_active_auth_file)"

  if [[ -n "$auth_backup" && -f "$auth_backup" ]]; then
    mkdir -p "$(dirname "$auth_file")"
    cp "$auth_backup" "$auth_file"
  elif [[ -f "$auth_file" ]]; then
    rm -f "$auth_file"
  fi

  if [[ -n "$original_active_slot" ]]; then
    mkdir -p "$(dirname "$(codex_active_slot_file)")"
    printf '%s\n' "$original_active_slot" >"$(codex_active_slot_file)"
  else
    rm -f "$(codex_active_slot_file)"
  fi

  if [[ -n "$original_slot" ]]; then
    printf '%s\n' "$original_slot"
  fi
}

codex_current_cooldown_identity() {
  local project="$1" current_slot active_slot
  current_slot="$(codex_current_slot "$project")"
  if [[ -n "$current_slot" ]]; then
    printf '%s\n' "$(normalize_codex_slot_name "$current_slot")"
    return 0
  fi
  active_slot="$(read_codex_active_slot)"
  [[ -n "$active_slot" ]] || return 0
  printf '%s\n' "$(normalize_codex_slot_name "$active_slot")"
}

write_codex_probe_artifact() {
  local project="$1" slot="$2" status="$3" output="$4"
  local artifacts_dir ts normalized_slot artifact
  artifacts_dir="$(codex_probe_artifacts_dir_for_project "$project")"
  ts="$(date -u '+%Y%m%dT%H%M%SZ')"
  normalized_slot="$(normalize_codex_slot_name "${slot:-unknown-slot}")"
  mkdir -p "$artifacts_dir"
  artifact="$artifacts_dir/codex-probe-${ts}-${normalized_slot}-${status}.log"
  {
    printf 'timestamp=%s\n' "$(date '+%Y-%m-%dT%H:%M:%S%z')"
    printf 'slot=%s\n' "${slot:-unknown}"
    printf 'status=%s\n' "$status"
    printf '\n'
    printf '%s\n' "$output"
  } >"$artifact"
  printf '%s\n' "$artifact"
}

strip_probe_output_for_matching() {
  printf '%s\n' "${1:-}" | sed -E 's/\x1b\[[0-9;]*[a-zA-Z]//g; s/\x1b\].*\x07//g; s/\x1b\][^\x1b]*\x1b\\//g'
}

codex_probe_output_is_expected_success() {
  local output
  output="$(strip_probe_output_for_matching "${1:-}")"
  if printf '%s\n' "$output" | grep -Eqi \
    'ERROR|WARN|forbidden|unauthorized|authentication|invalid.*token|login required|usage limit|try again|payment required|quota|余额不足|预扣费|subscription|deactivated_workspace|workspace deactivated|reconnecting\.\.\.|timed out|timeout|connection reset|connection refused|connection aborted|network is unreachable|temporary failure in name resolution|eai_again|enotfound|tls handshake|proxyconnect tcp|proxy error|bad gateway|service unavailable|gateway timeout|upstream connect error'
  then
    return 1
  fi
  printf '%s\n' "$output" | awk '
    NF == 0 { next }
    state == 0 && $0 == "user" { state = 1; next }
    state == 1 {
      if ($0 != "hi") exit 1
      state = 2
      next
    }
    state == 2 {
      if ($0 != "codex") exit 1
      state = 3
      next
    }
    state == 3 {
      if ($0 == "tokens used") exit 1
      saw_response = 1
      state = 4
      next
    }
    state >= 4 && $0 == "tokens used" {
      saw_tokens = 1
      state = 5
      next
    }
    END { exit (saw_response && saw_tokens) ? 0 : 1 }
  '
}

codex_probe_is_expected_success() {
  local rc="$1" output="${2:-}"
  [[ "$rc" -eq 0 ]] || return 1
  codex_probe_output_is_expected_success "$output"
}

codex_probe_output_has_deactivated_workspace() {
  local output
  output="$(strip_probe_output_for_matching "${1:-}")"
  printf '%s\n' "$output" | grep -qi "deactivated_workspace\|402 Payment Required"
}

codex_probe_output_has_network_failure() {
  local output
  output="$(strip_probe_output_for_matching "${1:-}")"
  printf '%s\n' "$output" | grep -Eqi \
    'ERROR: Reconnecting|reconnecting\.\.\.|operation timed out|timed out|connection reset|connection refused|connection aborted|network is unreachable|temporary failure in name resolution|eai_again|enotfound|tls handshake|proxyconnect tcp|proxy error|bad gateway|service unavailable|gateway timeout|upstream connect error'
}

terminate_codex_probe_process() {
  local pid="${1:-}" waited=0
  [[ -n "$pid" ]] || return 0
  if kill -0 "$pid" 2>/dev/null; then
    kill "$pid" 2>/dev/null || true
    while kill -0 "$pid" 2>/dev/null && [[ "$waited" -lt 20 ]]; do
      sleep 0.1
      waited=$((waited + 1))
    done
  fi
  if kill -0 "$pid" 2>/dev/null; then
    kill -KILL "$pid" 2>/dev/null || true
  fi
  wait "$pid" 2>/dev/null || true
}

codex_slot_switch_lock_dir() {
  printf '%s\n' "${AI_CLI_SWITCH_LOCK_DIR:-$HOME/.codex/slot-switch.lock}"
}

codex_slot_switch_lock_state_file() {
  printf '%s\n' "$(codex_slot_switch_lock_dir)/state.env"
}

codex_slot_switch_lock_owner_pid() {
  local state_file
  state_file="$(codex_slot_switch_lock_state_file)"
  [[ -f "$state_file" ]] || return 0
  sed -n 's/^owner_pid=//p' "$state_file" 2>/dev/null | tail -n 1
}

codex_slot_switch_lock_cleanup_if_stale() {
  local lock_dir owner_pid
  lock_dir="$(codex_slot_switch_lock_dir)"
  [[ -d "$lock_dir" ]] || return 0
  owner_pid="$(codex_slot_switch_lock_owner_pid)"
  if [[ -z "$owner_pid" ]] || ! kill -0 "$owner_pid" 2>/dev/null; then
    rm -rf "$lock_dir"
  fi
}

codex_slot_switch_in_progress() {
  local lock_dir owner_pid inherited_owner_pid
  codex_slot_switch_lock_cleanup_if_stale
  lock_dir="$(codex_slot_switch_lock_dir)"
  [[ -d "$lock_dir" ]] || return 1
  owner_pid="$(codex_slot_switch_lock_owner_pid)"
  inherited_owner_pid="${AI_CLI_SWITCH_LOCK_OWNER_PID:-}"
  [[ -n "$owner_pid" ]] || return 1
  [[ "$owner_pid" != "$$" ]] || return 1
  [[ -z "$inherited_owner_pid" || "$owner_pid" != "$inherited_owner_pid" ]] || return 1
  kill -0 "$owner_pid" 2>/dev/null
}

wait_for_codex_slot_switch_idle() {
  local project="$1"
  local activity_label="${2:-probe/relaunch}"
  local timeout_secs="${FREELY_ACCOUNT_SWITCH_WAIT_SECS:-60}"
  local interval_secs="${FREELY_ACCOUNT_SWITCH_WAIT_INTERVAL_SECS:-1}"
  local start_ts now owner_pid waiting_logged=0
  [[ "$timeout_secs" =~ ^[0-9]+$ ]] || timeout_secs=60
  [[ "$interval_secs" =~ ^[0-9]+$ ]] || interval_secs=1
  start_ts="$(date +%s)"

  while codex_slot_switch_in_progress; do
    if [[ "$waiting_logged" == "0" ]]; then
      owner_pid="$(codex_slot_switch_lock_owner_pid)"
      log_warn "codex slot switch is already in progress (owner_pid=${owner_pid:-unknown}); waiting before ${activity_label}" >&2
      waiting_logged=1
    fi
    now="$(date +%s)"
    if (( now - start_ts >= timeout_secs )); then
      log_warn "timed out waiting for codex slot switch to finish before ${activity_label}" >&2
      return 1
    fi
    sleep "$interval_secs"
  done

  return 0
}

codex_slot_switch_probe_lock_acquire() {
  local reason="${1:-codex_exec_probe}"
  local activity_label="${2:-codex exec probe}"
  local timeout_secs="${AI_CLI_SWITCH_LOCK_WAIT_SECS:-60}"
  local lock_dir state_file start_ts now owner_pid inherited_owner_pid
  lock_dir="$(codex_slot_switch_lock_dir)"
  state_file="$(codex_slot_switch_lock_state_file)"
  inherited_owner_pid="${AI_CLI_SWITCH_LOCK_OWNER_PID:-}"
  [[ "$timeout_secs" =~ ^[0-9]+$ ]] || timeout_secs=60
  mkdir -p "$(dirname "$lock_dir")"
  start_ts="$(date +%s)"

  while true; do
    codex_slot_switch_lock_cleanup_if_stale
    if mkdir "$lock_dir" 2>/dev/null; then
      cat >"$state_file" <<EOF
owner_pid=$$
started_at=$(date +%s)
reason=$reason
command=probe
target=codex-exec
EOF
      export AI_CLI_SWITCH_LOCK_OWNER_PID="$$"
      return 0
    fi

    owner_pid="$(codex_slot_switch_lock_owner_pid)"
    if [[ -n "$owner_pid" && ( "$owner_pid" == "$$" || ( -n "$inherited_owner_pid" && "$owner_pid" == "$inherited_owner_pid" ) ) ]]; then
      export AI_CLI_SWITCH_LOCK_OWNER_PID="$owner_pid"
      return 0
    fi

    now="$(date +%s)"
    if (( now - start_ts >= timeout_secs )); then
      log_warn "timed out waiting to serialize ${activity_label} behind slot switch activity"
      return 1
    fi
    sleep 1
  done
}

codex_slot_switch_probe_lock_release() {
  local lock_dir owner_pid inherited_owner_pid
  lock_dir="$(codex_slot_switch_lock_dir)"
  [[ -d "$lock_dir" ]] || return 0
  owner_pid="$(codex_slot_switch_lock_owner_pid)"
  inherited_owner_pid="${AI_CLI_SWITCH_LOCK_OWNER_PID:-}"
  if [[ -z "$owner_pid" || "$owner_pid" == "$$" ]]; then
    rm -rf "$lock_dir"
  elif [[ -n "$inherited_owner_pid" && "$owner_pid" == "$inherited_owner_pid" && "$$" == "$inherited_owner_pid" ]]; then
    rm -rf "$lock_dir"
  fi
}

# Parse various time formats from codex output
# Supported formats:
#   - "Mar 23rd, 2026 3:51 PM" (full date)
#   - "1:42 AM" (time only, assumes today or tomorrow)
parse_try_again_time() {
  local date_str="$1"
  [[ -n "$date_str" ]] || return 1
  python3 -c "
import re
from datetime import datetime, timedelta
import sys

date_str = sys.argv[1]
# Remove ordinal suffixes (st, nd, rd, th)
cleaned = re.sub(r\"(\d+)(st|nd|rd|th)\", r\"\1\", date_str).strip()

try:
    # Try full date format: \"Mar 23, 2026 3:51 PM\"
    dt = datetime.strptime(cleaned, \"%b %d, %Y %I:%M %p\")
    print(int(dt.timestamp()))
    sys.exit(0)
except ValueError:
    pass

try:
    # Try time-only format: \"1:42 AM\"
    # Assume it is today, but if the time has already passed, assume tomorrow
    time_only = datetime.strptime(cleaned, \"%I:%M %p\")
    now = datetime.now()
    dt = now.replace(hour=time_only.hour, minute=time_only.minute, second=0, microsecond=0)
    if dt <= now:
        dt += timedelta(days=1)
    print(int(dt.timestamp()))
    sys.exit(0)
except ValueError:
    pass

sys.exit(1)
" "$date_str" 2>/dev/null
}

# Extract "try again at ..." time from codex output
# Returns Unix timestamp, or empty if not found
extract_try_again_time_from_output() {
  local output="$1"
  local try_again_str
  # Match: try again at Mar 23rd, 2026 3:51 PM.
  # Also match: try again at 1:42 AM.
  try_again_str="$(printf '%s\n' "$output" | grep -oiE 'try again at [^.]+\.' | sed 's/try again at //i' | sed 's/\.$//' | head -1)"
  if [[ -z "$try_again_str" ]]; then
    # Try alternative patterns without trailing dot
    try_again_str="$(printf '%s\n' "$output" | grep -oiE 'try again at [A-Za-z0-9, :]+[AP]M' | sed 's/try again at //i' | head -1)"
  fi
  [[ -n "$try_again_str" ]] || return 1
  parse_try_again_time "$try_again_str"
}

codex_current_account() {
  local project="$1" ai_bin output
  wait_for_codex_slot_switch_idle "$project" || return 1
  ai_bin="$(ai_cli_bin_for_project "$project")"
  [[ -x "$ai_bin" ]] || return 0
  output="$("$ai_bin" --quiet --format json whoami codex 2>/dev/null || true)"
  printf '%s\n' "$output" | sed -n 's/.*"auth_email": *"\([^"]*\)".*/\1/p' | tail -n 1
}

codex_current_slot() {
  local project="$1" ai_bin output
  wait_for_codex_slot_switch_idle "$project" || return 1
  ai_bin="$(ai_cli_bin_for_project "$project")"
  [[ -x "$ai_bin" ]] || return 0
  output="$("$ai_bin" --quiet --format json whoami codex 2>/dev/null || true)"
  printf '%s\n' "$output" | sed -n 's/.*"slot": *"\([^"]*\)".*/\1/p' | tail -n 1
}

codex_current_slot_kind() {
  local project="$1" ai_bin output
  wait_for_codex_slot_switch_idle "$project" || return 1
  ai_bin="$(ai_cli_bin_for_project "$project")"
  [[ -x "$ai_bin" ]] || return 0
  output="$("$ai_bin" --quiet --format json whoami codex 2>/dev/null || true)"
  printf '%s\n' "$output" | sed -n 's/.*"slot_kind": *"\([^"]*\)".*/\1/p' | tail -n 1
}

codex_current_identity_hint() {
  local project="$1" current_slot current_slot_kind
  current_slot="$(codex_current_slot "$project")"
  if [[ -n "$current_slot" ]]; then
    printf '%s\n' "$current_slot"
    return 0
  fi
  current_slot_kind="$(codex_current_slot_kind "$project")"
  case "$current_slot_kind" in
    apikey)
      printf 'live-apikey-current\n'
      ;;
  esac
}

codex_saved_slots() {
  local project="$1" ai_bin output
  wait_for_codex_slot_switch_idle "$project" || return 1
  ai_bin="$(ai_cli_bin_for_project "$project")"
  [[ -x "$ai_bin" ]] || return 0
  output="$("$ai_bin" --quiet --format json list 2>/dev/null || true)"
  printf '%s\n' "$output" | grep -o '"codex-[^"]*"' | tr -d '"' | sed 's/^codex-//'
}

codex_availability_state_file() {
  local project="$1"
  printf '%s\n' "$(watchdog_run_dir_for_project "$project")/codex-availability-state.env"
}

codex_availability_cache_file() {
  local project="$1"
  printf '%s\n' "$(watchdog_run_dir_for_project "$project")/codex-availability-cache.tsv"
}

codex_oauth_usage_url() {
  printf '%s\n' "${CODEX_OAUTH_USAGE_URL:-https://chatgpt.com/backend-api/wham/usage}"
}

codex_saved_slot_auth_file() {
  local slot="$1"
  printf '%s\n' "${AUTH_DIR:-$HOME/.ai-auth}/codex-${slot}/auth.json"
}

codex_saved_slot_manifest_file() {
  local slot="$1"
  printf '%s\n' "${AUTH_DIR:-$HOME/.ai-auth}/codex-${slot}/manifest.json"
}

codex_saved_slot_kind() {
  local slot="$1" manifest_file auth_file kind=""
  manifest_file="$(codex_saved_slot_manifest_file "$slot")"
  if [[ -f "$manifest_file" ]]; then
    kind="$(python3 - <<'PY' "$manifest_file" 2>/dev/null || true
import json
import sys
with open(sys.argv[1], "r", encoding="utf-8") as f:
    data = json.load(f)
value = data.get("slot_kind", "")
print(value if isinstance(value, str) else "")
PY
)"
  fi
  if [[ -n "$kind" ]]; then
    printf '%s\n' "$kind"
    return 0
  fi
  case "$slot" in
    account-*) printf 'account\n'; return 0 ;;
    apikey-*) printf 'apikey\n'; return 0 ;;
  esac
  auth_file="$(codex_saved_slot_auth_file "$slot")"
  python3 - <<'PY' "$auth_file" 2>/dev/null || true
import json
import os
import sys

path = sys.argv[1]
if not os.path.exists(path):
    print("legacy")
    raise SystemExit(0)
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)
if isinstance(data.get("OPENAI_API_KEY"), str) and data.get("OPENAI_API_KEY"):
    print("apikey")
elif isinstance(data.get("tokens"), dict) or isinstance(data.get("access_token"), str):
    print("account")
else:
    print("legacy")
PY
}

codex_saved_slots_include_kind() {
  local project="$1" expected_kind="$2" candidate kind slots
  slots="$(codex_saved_slots "$project")"
  while IFS= read -r candidate; do
    [[ -n "$candidate" ]] || continue
    kind="$(codex_saved_slot_kind "$candidate")"
    [[ "$kind" == "$expected_kind" ]] || continue
    return 0
  done <<EOF
$slots
EOF
  return 1
}

codex_saved_slots_fingerprint() {
  local project="$1"
  local slots
  slots="$(codex_saved_slots "$project" | sed '/^$/d')"
  if [[ -z "$slots" ]]; then
    printf 'none\n'
    return 0
  fi
  printf '%s\n' "$slots" | shasum -a 256 | awk '{print $1}'
}

codex_load_availability_state() {
  local project="$1" state_file
  state_file="$(codex_availability_state_file "$project")"
  [[ -f "$state_file" ]] || return 1
  # shellcheck disable=SC1090
  source "$state_file"
}

codex_write_availability_state() {
  local project="$1" phase="$2" blocked_reason="$3" previous_slot="$4" active_slot="$5" inventory_fingerprint="$6" wake_trigger="$7" earliest_slot="$8" earliest_reset="$9" reprobe_next_at="${10:-}" reprobe_attempts="${11:-}" reprobe_max_attempts="${12:-}"
  local state_file
  state_file="$(codex_availability_state_file "$project")"
  mkdir -p "$(dirname "$state_file")"
  cat >"$state_file" <<EOF
AVAILABILITY_PHASE="${phase:-unknown}"
BLOCKED_REASON="${blocked_reason:-}"
PREVIOUS_SLOT="${previous_slot:-}"
ACTIVE_SLOT="${active_slot:-}"
SAVED_SLOTS_FINGERPRINT="${inventory_fingerprint:-}"
WAKE_TRIGGER="${wake_trigger:-}"
EARLIEST_SLOT_HINT="${earliest_slot:-}"
EARLIEST_RESET_HINT="${earliest_reset:-}"
EARLIEST_REPROBE_NEXT_AT="${reprobe_next_at:-}"
EARLIEST_REPROBE_ATTEMPTS="${reprobe_attempts:-}"
EARLIEST_REPROBE_MAX_ATTEMPTS="${reprobe_max_attempts:-}"
LAST_PROBE_AT="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
EOF
}

codex_clear_availability_state() {
  local project="$1"
  rm -f "$(codex_availability_state_file "$project")"
}

codex_overwrite_slot_cooldowns_from_sweep_results() {
  local project="$1" results_file="$2"
  local file tmp
  file="$(codex_slot_cooldown_file "$project")"
  mkdir -p "$(dirname "$file")"
  tmp="${file}.tmp"
  awk -F '\t' '
    $2 == "rate_limited" && $4 ~ /^[0-9]+$/ && $4 > 0 {
      print $1 "\t" $4 "\t" $6
    }
  ' "$results_file" >"$tmp"
  mv "$tmp" "$file"
}

codex_write_availability_cache_from_sweep_results() {
  local project="$1" results_file="$2"
  local file tmp refreshed_at
  file="$(codex_availability_cache_file "$project")"
  mkdir -p "$(dirname "$file")"
  tmp="${file}.tmp"
  refreshed_at="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  {
    printf 'slot\tstatus\tauth_email\treset_at\thttp_code\tdetail\trefreshed_at\n'
    awk -F '\t' -v refreshed_at="$refreshed_at" '
      NF >= 6 {
        print $1 "\t" $2 "\t" $3 "\t" $4 "\t" $5 "\t" $6 "\t" refreshed_at
      }
    ' "$results_file"
  } >"$tmp"
  mv "$tmp" "$file"
}

codex_availability_cache_ttl_seconds() {
  local ttl="${CODEX_AVAILABILITY_CACHE_TTL_SECS:-1800}"
  [[ "$ttl" =~ ^[0-9]+$ ]] || ttl=1800
  printf '%s\n' "$ttl"
}

codex_availability_cache_refreshed_at() {
  local project="$1" file
  file="$(codex_availability_cache_file "$project")"
  [[ -f "$file" ]] || return 1
  awk -F '\t' 'NR==2 {print $7}' "$file"
}

codex_timestamp_to_epoch() {
  local timestamp="$1"
  [[ -n "$timestamp" ]] || return 1
  python3 - <<'PY' "$timestamp" 2>/dev/null
from datetime import datetime
import sys

timestamp = sys.argv[1]
if timestamp.endswith("Z"):
    timestamp = timestamp[:-1] + "+00:00"
try:
    print(int(datetime.fromisoformat(timestamp).timestamp()))
except Exception:
    raise SystemExit(1)
PY
}

codex_availability_cache_is_fresh() {
  local project="$1" refreshed_at refreshed_epoch ttl now
  refreshed_at="$(codex_availability_cache_refreshed_at "$project" || true)"
  [[ -n "$refreshed_at" ]] || return 1
  refreshed_epoch="$(codex_timestamp_to_epoch "$refreshed_at" || true)"
  [[ -n "$refreshed_epoch" && "$refreshed_epoch" =~ ^[0-9]+$ ]] || return 1
  ttl="$(codex_availability_cache_ttl_seconds)"
  now="$(date +%s)"
  (( now - refreshed_epoch <= ttl ))
}

codex_cached_slot_status() {
  local project="$1" slot="$2" file normalized
  file="$(codex_availability_cache_file "$project")"
  normalized="$(normalize_codex_slot_name "$slot")"
  [[ -f "$file" && -n "$normalized" ]] || return 1
  awk -F '\t' -v slot="$normalized" 'NR>1 && $1 == slot {print $2; exit}' "$file"
}

codex_cached_inventory_truth() {
  local project="$1" file
  local usable_slot="" earliest_slot="" earliest_reset=""
  file="$(codex_availability_cache_file "$project")"
  [[ -f "$file" ]] || { printf 'none\n'; return 1; }

  # Read CSV skipping header line; avoid process substitution for portability
  local _first=1
  while IFS=$'\t' read -r slot status auth_email reset_at http_code detail refreshed_at; do
    [[ -n "$_first" ]] && { _first=; continue; }
    [[ -n "$slot" ]] || continue
    if [[ "$status" == "usable" && -z "$usable_slot" ]]; then
      usable_slot="$slot"
    fi
    if [[ "$status" == "rate_limited" && "$reset_at" =~ ^[0-9]+$ && "$reset_at" -gt 0 ]]; then
      if [[ -z "$earliest_reset" || "$reset_at" -lt "$earliest_reset" ]]; then
        earliest_slot="$slot"
        earliest_reset="$reset_at"
      fi
    fi
  done < "$file"

  if [[ -n "$usable_slot" ]]; then
    printf 'usable:%s\n' "$usable_slot"
    return 0
  fi
  if [[ -n "$earliest_slot" && -n "$earliest_reset" ]]; then
    printf 'all_unavailable:%s|%s\n' "$earliest_slot" "$earliest_reset"
    return 0
  fi
  printf 'none\n'
  return 1
}

codex_inventory_truth() {
  local project="$1" refresh_mode="${2:-stale_ok}"
  if [[ "$refresh_mode" != "refresh" ]] && codex_availability_cache_is_fresh "$project"; then
    codex_cached_inventory_truth "$project"
    return $?
  fi

  if codex_availability_cache_is_fresh "$project"; then
    codex_cached_inventory_truth "$project"
    return $?
  fi

  printf 'none\n'
  return 1
}

# Runtime truth for switch/start/status/watchdog must come from real codex exec
# probes. The OAuth/cache helpers above remain advisory only.
codex_exec_saved_slot_truth() {
  local project="$1" excluded_identity="${2:-}" switch_reason="${3:-probe_recovery_slots}" probe_lock_reason="${4:-codex_exec_recovery_probe}" probe_activity_label="${5:-codex exec recovery probe}"
  local candidate probe_result reset_at
  local earliest_slot="" earliest_reset=""
  local original_slot active_slot original_active_slot auth_backup="" auth_file
  local tmp_dir results_file status_text="" details="" auth_email="" detail=""

  original_slot="$(codex_current_slot "$project")"
  original_active_slot="$(read_codex_active_slot)"
  auth_file="$(codex_active_auth_file)"
  if [[ -f "$auth_file" ]]; then
    auth_backup="$(mktemp)"
    cp "$auth_file" "$auth_backup"
  fi
  tmp_dir="$(mktemp -d)"
  results_file="$tmp_dir/exec-results.tsv"

  while IFS= read -r candidate; do
    [[ -n "$candidate" ]] || continue
    if codex_slot_matches_identity "$candidate" "$excluded_identity"; then
      continue
    fi
    switch_to_codex_slot "$project" "$candidate" "$switch_reason" >/dev/null || continue

    probe_result="$(codex_probe_current_slot_now "$project" "$probe_lock_reason" "$probe_activity_label" || true)"
    status_text=""
    details=""
    auth_email=""
    detail=""
    reset_at="0"
    case "$probe_result" in
      usable)
        status_text="usable"
        details="ready to use"
        detail="$details"
        printf '%s\t%s\t%s\t%s\t0\t%s\n' "$candidate" "$status_text" "$auth_email" "$reset_at" "$detail" >>"$results_file"
        [[ -z "$auth_backup" ]] || rm -f "$auth_backup"
        rm -rf "$tmp_dir"
        printf 'usable:%s\n' "$candidate"
        return 0
        ;;
      rate_limited:*)
        reset_at="${probe_result#rate_limited:}"
        status_text="rate_limited"
        details="$reset_at"
        detail="$details"
        if [[ -n "$reset_at" && "$reset_at" =~ ^[0-9]+$ && "$reset_at" -gt 0 ]]; then
          codex_record_slot_cooldown "$project" "$candidate" "$reset_at"
          if [[ -z "$earliest_reset" || "$reset_at" -lt "$earliest_reset" ]]; then
            earliest_slot="$candidate"
            earliest_reset="$reset_at"
          fi
        fi
        ;;
      subscription_expired|deactivated_workspace|unauthorized|network_failure|timeout)
        status_text="$probe_result"
        details="$probe_result"
        detail="$details"
        ;;
      error:*)
        status_text="error"
        details="${probe_result#error:}"
        detail="$details"
        ;;
      *)
        status_text="unknown"
        details="${probe_result:-unknown}"
        detail="$details"
        ;;
    esac
    printf '%s\t%s\t%s\t%s\t0\t%s\n' "$candidate" "$status_text" "$auth_email" "${reset_at:-0}" "$detail" >>"$results_file"
  done <<<"$(codex_saved_slots "$project")"

  restore_codex_probe_origin "$original_slot" "$original_active_slot" "$auth_backup" >/dev/null || true
  [[ -z "$auth_backup" ]] || rm -f "$auth_backup"
  rm -rf "$tmp_dir"
  if [[ -n "$earliest_slot" && -n "$earliest_reset" ]]; then
    printf 'all_unavailable:%s|%s\n' "$earliest_slot" "$earliest_reset"
    return 0
  fi
  printf 'none\n'
  return 1
}

codex_confirm_launch_candidate_slot() {
  local project="$1" candidate="$2" reason="$3" excluded_identity="${4:-}"
  local original_slot original_active_slot auth_backup="" auth_file probe_result reset_at

  [[ -n "$candidate" ]] || { printf 'none\n'; return 1; }
  if codex_slot_matches_identity "$candidate" "$excluded_identity"; then
    printf 'excluded_current_slot\n'
    return 1
  fi
  original_slot="$(codex_current_slot "$project")"
  original_active_slot="$(read_codex_active_slot)"
  auth_file="$(codex_active_auth_file)"
  if [[ -f "$auth_file" ]]; then
    auth_backup="$(mktemp)"
    cp "$auth_file" "$auth_backup"
  fi

  if ! switch_to_codex_slot "$project" "$candidate" "$reason" >/dev/null; then
    restore_codex_probe_origin "$original_slot" "$original_active_slot" "$auth_backup" >/dev/null || true
    [[ -z "$auth_backup" ]] || rm -f "$auth_backup"
    printf 'switch_failed\n'
    return 1
  fi

  probe_result="$(codex_probe_current_slot_now "$project" || true)"
  case "$probe_result" in
    usable)
      [[ -z "$auth_backup" ]] || rm -f "$auth_backup"
      printf 'usable:%s\n' "$candidate"
      return 0
      ;;
    rate_limited:*)
      reset_at="${probe_result#rate_limited:}"
      if [[ -n "$reset_at" && "$reset_at" =~ ^[0-9]+$ && "$reset_at" -gt 0 ]]; then
        codex_record_slot_cooldown "$project" "$candidate" "$reset_at"
      fi
      ;;
  esac

  restore_codex_probe_origin "$original_slot" "$original_active_slot" "$auth_backup" >/dev/null || true
  [[ -z "$auth_backup" ]] || rm -f "$auth_backup"
  printf '%s\n' "${probe_result:-none}"
  return 1
}

codex_oauth_probe_single_slot() {
  local project="$1" slot="$2" auth_file="$3" output_file="$4"
  local usage_url token auth_email account_id response_file http_code response_body
  usage_url="$(codex_oauth_usage_url)"
  if [[ ! -f "$auth_file" ]]; then
    printf '%s\tmissing_auth\t\t0\t0\tauth file missing\n' "$slot" >"$output_file"
    return 0
  fi

  local _auth_data
  _auth_data="$(python3 - "$auth_file" <<'PY'
import base64
import json
import sys

path = sys.argv[1]
token = ""
email = ""
account_id = ""
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)
tokens = data.get("tokens", {}) if isinstance(data.get("tokens", {}), dict) else {}
token = tokens.get("access_token", "") or data.get("access_token", "")
account_id = tokens.get("account_id", "") or data.get("account_id", "")
id_token = data.get("tokens", {}).get("id_token", "")
if id_token:
    try:
        payload = id_token.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        email = json.loads(base64.urlsafe_b64decode(payload.encode())).get("email", "")
    except Exception:
        email = ""
print(token, email, account_id)
PY
  )"
  IFS=' ' read -r token auth_email account_id <<<"$_auth_data"

  if [[ -z "$token" ]]; then
    printf '%s\tmissing_token\t%s\t0\t0\taccess token missing\n' "$slot" "$auth_email" >"$output_file"
    return 0
  fi

  response_file="$(mktemp)"
  if ! http_code="$(
    (
      freely_apply_project_network_proxy_env "$project"
      if [[ -n "$account_id" ]]; then
        curl --connect-timeout 10 --max-time 30 -sS \
          -o "$response_file" \
          -w '%{http_code}' \
          -H "Authorization: Bearer $token" \
          -H "ChatGPT-Account-Id: $account_id" \
          -H "User-Agent: codex-cli" \
          -H "Accept: application/json" \
          "$usage_url"
      else
        curl --connect-timeout 10 --max-time 30 -sS \
          -o "$response_file" \
          -w '%{http_code}' \
          -H "Authorization: Bearer $token" \
          -H "User-Agent: codex-cli" \
          -H "Accept: application/json" \
          "$usage_url"
      fi
    ) 2>/dev/null
  )"; then
    rm -f "$response_file"
    printf '%s\tcurl_error\t%s\t0\t0\toauth query failed\n' "$slot" "$auth_email" >"$output_file"
    return 0
  fi
  response_body="$(cat "$response_file" 2>/dev/null || true)"
  rm -f "$response_file"

  python3 - <<'PY' "$slot" "$auth_email" "$http_code" "$response_body" >"$output_file"
import json
import sys

slot, auth_email, http_code, response_body = sys.argv[1:5]
status = "unknown"
reset_at = "0"
detail = ""

def numeric_reset(value):
    if isinstance(value, (int, float)):
        return str(int(value))
    if isinstance(value, str) and value.isdigit():
        return value
    return "0"

try:
    payload = json.loads(response_body) if response_body else {}
except Exception:
    payload = {}

detail_code = ""
detail_obj = payload.get("detail")
if isinstance(detail_obj, dict):
    detail_code = detail_obj.get("code", "") or ""
elif isinstance(detail_obj, str):
    detail_code = detail_obj

rate_limits = {}
if isinstance(payload, dict):
    if isinstance(payload.get("rate_limits"), dict):
        rate_limits = payload.get("rate_limits", {})
    elif isinstance(payload.get("rate_limit"), dict):
        legacy = payload.get("rate_limit", {})
        rate_limits = {
            "primary": legacy.get("primary"),
            "secondary": legacy.get("secondary"),
            "primary_window": legacy.get("primary_window"),
            "secondary_window": legacy.get("secondary_window"),
        }

primary = {}
secondary = {}
if isinstance(rate_limits, dict):
    primary = rate_limits.get("primary", {}) if isinstance(rate_limits.get("primary"), dict) else {}
    secondary = rate_limits.get("secondary", {}) if isinstance(rate_limits.get("secondary"), dict) else {}
    if not primary:
        primary = rate_limits.get("primary_window", {}) if isinstance(rate_limits.get("primary_window"), dict) else {}
    if not secondary:
        secondary = rate_limits.get("secondary_window", {}) if isinstance(rate_limits.get("secondary_window"), dict) else {}
primary_used = primary.get("used_percent")
secondary_used = secondary.get("used_percent")
primary_reset = numeric_reset(primary.get("resets_at") if "resets_at" in primary else primary.get("reset_at"))
secondary_reset = numeric_reset(secondary.get("resets_at") if "resets_at" in secondary else secondary.get("reset_at"))

if detail_code == "deactivated_workspace":
    status = "deactivated_workspace"
    detail = "workspace deactivated"
elif http_code in {"401", "403"}:
    status = "unauthorized"
    detail = "auth rejected"
elif http_code == "429" or primary_used == 100.0 or secondary_used == 100.0 or primary_used == 100 or secondary_used == 100:
    status = "rate_limited"
    reset_candidates = [x for x in (primary_reset, secondary_reset) if x.isdigit() and int(x) > 0]
    reset_at = min(reset_candidates, key=lambda x: int(x)) if reset_candidates else "0"
    detail = "oauth usage limit reached"
elif http_code.startswith("2"):
    status = "usable"
    detail = "oauth inventory usable"
else:
    status = "unknown"
    detail = detail_code or f"http {http_code}"

human = ""
if reset_at.isdigit() and int(reset_at) > 0:
    from datetime import datetime, timezone
    human = datetime.fromtimestamp(int(reset_at), timezone.utc).astimezone().strftime("%Y.%m.%d %H:%M:%S %Z")
else:
    human = detail

print("\t".join([
    slot,
    status,
    auth_email,
    reset_at,
    http_code,
    human,
]))
PY
}

codex_oauth_sweep_all_slots() {
  local project="$1"
  local candidate auth_file tmp_dir results_file result_file slot_kind swept_candidates=0
  local usable_slot="" earliest_slot="" earliest_reset=""
  local saw_result=0 current_identity curl_error_count=0
  current_identity="$(codex_current_cooldown_identity "$project")"
  tmp_dir="$(mktemp -d)"
  results_file="$tmp_dir/results.tsv"

  while IFS= read -r candidate; do
    [[ -n "$candidate" ]] || continue
    slot_kind="$(codex_saved_slot_kind "$candidate")"
    if [[ "$slot_kind" == "apikey" ]]; then
      continue
    fi
    auth_file="$(codex_saved_slot_auth_file "$candidate")"
    result_file="$tmp_dir/${candidate}.tsv"
    swept_candidates=$((swept_candidates + 1))
    codex_oauth_probe_single_slot "$project" "$candidate" "$auth_file" "$result_file" &
  done <<<"$(codex_saved_slots "$project")"
  wait || true

  cat "$tmp_dir"/*.tsv 2>/dev/null >"$results_file" || true
  if [[ ! -s "$results_file" || "$swept_candidates" -eq 0 ]]; then
    rm -rf "$tmp_dir"
    printf 'none\n'
    return 1
  fi

  codex_write_availability_cache_from_sweep_results "$project" "$results_file"
  codex_overwrite_slot_cooldowns_from_sweep_results "$project" "$results_file"

  printf '\n%-30s  %-20s  %s\n' "Slot" "OAuth status" "Details" >&2
  printf '%s\n' "$(printf '%-30s  %-20s  %s' '' '' '' | tr ' ' '-')" >&2
  while IFS=$'\t' read -r candidate status auth_email reset_at http_code detail; do
    local status_icon="❓"
    [[ -n "$candidate" ]] || continue
    saw_result=1
    if [[ "$status" == "curl_error" ]]; then
      curl_error_count=$((curl_error_count + 1))
    fi
    if [[ "$status" == "usable" && -z "$usable_slot" ]]; then
      usable_slot="$candidate"
    fi
    if [[ "$status" == "rate_limited" && "$reset_at" =~ ^[0-9]+$ && "$reset_at" -gt 0 ]]; then
      if [[ -z "$earliest_reset" || "$reset_at" -lt "$earliest_reset" ]]; then
        earliest_slot="$candidate"
        earliest_reset="$reset_at"
      fi
    fi
    if [[ "$(normalize_codex_slot_name "$candidate")" == "$current_identity" ]]; then
      candidate="${candidate} *"
    fi
    case "$status" in
      usable)
        status_icon="✅"
        ;;
      rate_limited)
        status_icon="⏳"
        ;;
      subscription_expired)
        status_icon="💳"
        ;;
      deactivated_workspace)
        status_icon="🚫"
        ;;
      unauthorized|missing_token)
        status_icon="🔒"
        ;;
      timeout)
        status_icon="⏱️"
        ;;
      curl_error|missing_auth|error)
        status_icon="❌"
        ;;
    esac
    printf '%s %-28s  %-20s  %s\n' "$status_icon" "$candidate" "$status" "$detail" >&2
  done <"$results_file"
  printf '\n' >&2

  local total_results=0
  total_results="$(wc -l <"$results_file" | tr -d ' ')"
  rm -rf "$tmp_dir"
  if [[ -n "$usable_slot" ]]; then
    printf 'usable:%s\n' "$usable_slot"
    return 0
  fi
  if [[ -n "$earliest_slot" && -n "$earliest_reset" ]]; then
    printf 'all_unavailable:%s|%s\n' "$earliest_slot" "$earliest_reset"
    return 0
  fi
  if [[ "$saw_result" == "1" && "$curl_error_count" -gt 0 && "$curl_error_count" -eq "$total_results" ]]; then
    printf 'oauth_unreachable\n'
    return 2
  fi
  [[ "$saw_result" == "1" ]] || return 1
  printf 'none\n'
  return 1
}

codex_prune_stale_slot_cooldowns() {
  local project="$1"
  local file tmp
  file="$(codex_slot_cooldown_file "$project")"
  [[ -f "$file" ]] || return 0
  tmp="${file}.tmp"
  awk -F '\t' '
    NR==FNR {
      if ($0 != "") {
        saved[$0]=1
      }
      next
    }
    NF >= 2 && ($1 in saved) {
      print $0
    }
  ' <(codex_saved_slots "$project") "$file" >"$tmp"
  mv "$tmp" "$file"
}

codex_record_slot_cooldown() {
  local project="$1" slot="$2" reset_at="$3"
  local file tmp normalized human_readable
  [[ -n "$slot" && -n "$reset_at" ]] || return 0
  normalized="$(normalize_codex_slot_name "$slot")"
  # Convert timestamp to human-readable format
  human_readable="$(format_epoch_local "$reset_at")"
  file="$(codex_slot_cooldown_file "$project")"
  mkdir -p "$(dirname "$file")"
  codex_prune_stale_slot_cooldowns "$project"
  tmp="${file}.tmp"
  {
    if [[ -f "$file" ]]; then
      # Keep existing entries (preserve human-readable column if present)
      awk -F '\t' -v slot="$normalized" '$1 != slot {print $1 "\t" $2 "\t" $3}' "$file"
    fi
    printf '%s\t%s\t%s\n' "$normalized" "$reset_at" "$human_readable"
  } >"$tmp"
  mv "$tmp" "$file"
}

codex_slot_cooldown_reset_at() {
  local project="$1" slot="$2"
  local file normalized
  normalized="$(normalize_codex_slot_name "$slot")"
  file="$(codex_slot_cooldown_file "$project")"
  codex_prune_stale_slot_cooldowns "$project"
  [[ -f "$file" ]] || return 0
  awk -F '\t' -v slot="$normalized" '$1 == slot {print $2}' "$file" | tail -n 1
}

codex_clear_slot_cooldown() {
  local project="$1" slot="$2"
  local file tmp normalized
  normalized="$(normalize_codex_slot_name "$slot")"
  file="$(codex_slot_cooldown_file "$project")"
  codex_prune_stale_slot_cooldowns "$project"
  [[ -f "$file" ]] || return 0
  tmp="${file}.tmp"
  # Preserve all columns except the target account
  awk -F '\t' -v slot="$normalized" '$1 != slot {print $1 "\t" $2 "\t" $3}' "$file" >"$tmp"
  mv "$tmp" "$file"
}

codex_slot_is_available_now() {
  local project="$1" slot="$2"
  local reset_at
  reset_at="$(codex_slot_cooldown_reset_at "$project" "$slot")"
  if [[ -z "$reset_at" ]]; then
    return 0
  fi
  [[ "$(seconds_until_epoch "$reset_at")" == "0" ]]
}

codex_any_saved_slot_available_now() {
  local project="$1" candidate
  while IFS= read -r candidate; do
    [[ -n "$candidate" ]] || continue
    if codex_slot_is_available_now "$project" "$candidate"; then
      return 0
    fi
  done <<<"$(codex_saved_slots "$project")"
  return 1
}

select_next_codex_slot() {
  local project="$1" current_identity="${2:-}"
  local normalized_current candidate seen_current=0
  normalized_current="$(normalize_codex_slot_name "$current_identity")"
  while IFS= read -r candidate; do
    [[ -n "$candidate" ]] || continue
    if [[ -z "$normalized_current" ]]; then
      codex_slot_is_available_now "$project" "$candidate" || continue
      printf '%s\n' "$candidate"
      return 0
    fi
    if [[ "$seen_current" == "1" ]]; then
      codex_slot_is_available_now "$project" "$candidate" || continue
      printf '%s\n' "$candidate"
      return 0
    fi
    [[ "$candidate" == "$normalized_current" ]] && seen_current=1
  done <<<"$(codex_saved_slots "$project")"
  return 1
}

select_next_codex_saved_slot() {
  local project="$1" current_identity="${2:-}"
  local normalized_current candidate seen_current=0
  normalized_current="$(normalize_codex_slot_name "$current_identity")"
  while IFS= read -r candidate; do
    [[ -n "$candidate" ]] || continue
    if [[ -z "$normalized_current" ]]; then
      printf '%s\n' "$candidate"
      return 0
    fi
    if [[ "$seen_current" == "1" ]]; then
      printf '%s\n' "$candidate"
      return 0
    fi
    [[ "$candidate" == "$normalized_current" ]] && seen_current=1
  done <<<"$(codex_saved_slots "$project")"
  return 1
}

select_earliest_reset_codex_slot() {
  local project="$1" current_identity="${2:-}"
  local normalized_current candidate reset_at best_slot="" best_reset=""
  normalized_current="$(normalize_codex_slot_name "$current_identity")"
  while IFS= read -r candidate; do
    [[ -n "$candidate" ]] || continue
    if [[ -n "$normalized_current" && "$candidate" == "$normalized_current" ]]; then
      continue
    fi
    reset_at="$(codex_slot_cooldown_reset_at "$project" "$candidate")"
    [[ -n "$reset_at" ]] || continue
    if [[ -z "$best_reset" || "$reset_at" -lt "$best_reset" ]]; then
      best_slot="$candidate"
      best_reset="$reset_at"
    fi
  done <<<"$(codex_saved_slots "$project")"
  if [[ -n "$best_slot" ]]; then
    printf '%s|%s\n' "$best_slot" "$best_reset"
  fi
}

select_any_available_codex_slot() {
  local project="$1" current_identity="${2:-}" candidate normalized_current
  normalized_current="$(normalize_codex_slot_name "$current_identity")"
  while IFS= read -r candidate; do
    [[ -n "$candidate" ]] || continue
    if [[ -n "$normalized_current" && "$candidate" == "$normalized_current" ]]; then
      continue
    fi
    if codex_slot_is_available_now "$project" "$candidate"; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done <<<"$(codex_saved_slots "$project")"
}

watchdog_reset_buffer_seconds() {
  local buffer="${WATCHDOG_RESET_BUFFER_SECS:-30}"
  [[ "$buffer" =~ ^[0-9]+$ ]] || buffer=30
  printf '%s\n' "$buffer"
}

watchdog_reset_reprobe_interval_seconds() {
  local interval="${WATCHDOG_REPROBE_INTERVAL_SECS:-30}"
  [[ "$interval" =~ ^[0-9]+$ ]] || interval=30
  (( interval > 0 )) || interval=30
  printf '%s\n' "$interval"
}

watchdog_reset_reprobe_max_attempts() {
  local max_attempts="${WATCHDOG_REPROBE_MAX_ATTEMPTS:-5}"
  [[ "$max_attempts" =~ ^[0-9]+$ ]] || max_attempts=5
  (( max_attempts > 0 )) || max_attempts=5
  printf '%s\n' "$max_attempts"
}

watchdog_force_reprobe_requested() {
  [[ "${FREELY_FORCE_WATCHDOG_REPROBE:-0}" == "1" ]]
}

compute_all_unavailable_reprobe_schedule() {
  local earliest_reset="$1" previous_earliest_reset="${2:-}" previous_next_at="${3:-}" previous_attempts="${4:-}"
  local now buffer due_at interval max_attempts next_at attempts schedule_from

  [[ "$earliest_reset" =~ ^[0-9]+$ ]] || return 1
  now="$(date +%s)"
  buffer="$(watchdog_reset_buffer_seconds)"
  interval="$(watchdog_reset_reprobe_interval_seconds)"
  max_attempts="$(watchdog_reset_reprobe_max_attempts)"
  due_at=$((earliest_reset + buffer))
  next_at="$due_at"
  attempts="0"

  if [[ "$previous_earliest_reset" =~ ^[0-9]+$ && "$previous_earliest_reset" == "$earliest_reset" ]]; then
    if [[ "$previous_attempts" =~ ^[0-9]+$ ]]; then
      attempts="$previous_attempts"
    fi
    if [[ "$previous_next_at" =~ ^[0-9]+$ && "$previous_next_at" -gt "$next_at" ]]; then
      next_at="$previous_next_at"
    fi
    schedule_from="$next_at"
    if (( now >= schedule_from )); then
      attempts=$((attempts + 1))
      next_at=$((now + interval))
    fi
  fi

  printf '%s|%s|%s|%s\n' "$due_at" "$next_at" "$attempts" "$max_attempts"
}

should_defer_all_unavailable_reprobe() {
  local previous_phase="$1" previous_blocked_reason="$2" previous_fingerprint="$3" current_fingerprint="$4" previous_earliest_reset="$5" previous_next_at="${6:-}"
  local due_at next_at now

  watchdog_force_reprobe_requested && return 1
  [[ "$previous_phase" == "all_unavailable" && "$previous_blocked_reason" == "all_slots_unavailable" ]] || return 1
  [[ -n "$previous_fingerprint" && "$previous_fingerprint" == "$current_fingerprint" ]] || return 1
  [[ "$previous_earliest_reset" =~ ^[0-9]+$ ]] || return 1

  due_at=$((previous_earliest_reset + $(watchdog_reset_buffer_seconds)))
  next_at="$due_at"
  if [[ "$previous_next_at" =~ ^[0-9]+$ && "$previous_next_at" -gt "$next_at" ]]; then
    next_at="$previous_next_at"
  fi
  now="$(date +%s)"
  (( now < next_at ))
}

select_earliest_reset_codex_slot_any() {
  local project="$1" candidate reset_at best_slot="" best_reset=""
  while IFS= read -r candidate; do
    [[ -n "$candidate" ]] || continue
    reset_at="$(codex_slot_cooldown_reset_at "$project" "$candidate")"
    [[ -n "$reset_at" ]] || continue
    if [[ -z "$best_reset" || "$reset_at" -lt "$best_reset" ]]; then
      best_slot="$candidate"
      best_reset="$reset_at"
    fi
  done <<<"$(codex_saved_slots "$project")"
  if [[ -n "$best_slot" ]]; then
    printf '%s|%s\n' "$best_slot" "$best_reset"
  fi
}

# Probe current codex account with proxy support and timeout.
# Output format:
#   usable
#   rate_limited:<reset_at>
#   subscription_expired
#   unauthorized
#   network_failure
#   timeout
#   error:<message>
# Exit code:
#   0 for usable or rate limited
#   1 for other probe failures
# ── Generic slot probe (all tools) ──────────────────────────
# Runs "hi" via tool's non-interactive mode, checks output for success.
# Returns: usable | rate_limited:N | deactivated_workspace | network_failure | unknown_error
slot_probe() {
  local project="$1" tool="$2" slot_dir="$3" timeout_secs="${4:-15}"
  local prompt_file output_file rc pid slept partial_output
  prompt_file="$(mktemp)"
  output_file="$(mktemp)"
  printf 'say hi\n' >"$prompt_file"
  rc=0

  (
    cd "$project"
    freely_apply_project_network_proxy_env "$project"
    case "$tool" in
      claude|cc|cc-use-codex-cli)
        claude -p --settings "$slot_dir/settings.json" <"$prompt_file" &
        ;;
      opencode)
        OPENCODE_CONFIG="$slot_dir/settings.json" opencode run "$(cat "$prompt_file")" &
        ;;
      codex)
        codex exec --skip-git-repo-check -C "$project" --dangerously-bypass-approvals-and-sandbox - <"$prompt_file" &
        ;;
      *)
        rm -f "$prompt_file" "$output_file"
        printf 'unsupported_tool\n'
        return 1
        ;;
    esac
    pid=$!
    wait "$pid" 2>/dev/null || true
  ) >"$output_file" 2>&1 &
  pid=$!

  slept=0
  while [[ $slept -lt $timeout_secs ]]; do
    partial_output="$(cat "$output_file" 2>/dev/null || true)"
    if _slot_probe_output_is_success "$partial_output"; then
      kill "$pid" 2>/dev/null; wait "$pid" 2>/dev/null
      rm -f "$prompt_file" "$output_file"
      printf 'usable\n'; return 0
    fi
    if _slot_probe_output_has_error "$partial_output" "deactivated\|workspace deactivated"; then
      kill "$pid" 2>/dev/null; wait "$pid" 2>/dev/null
      rm -f "$prompt_file" "$output_file"
      printf 'deactivated_workspace\n'; return 0
    fi
    if _slot_probe_output_has_error "$partial_output" "rate.limit\|429\|too many requests"; then
      kill "$pid" 2>/dev/null; wait "$pid" 2>/dev/null
      rm -f "$prompt_file" "$output_file"
      printf 'rate_limited:0\n'; return 0
    fi
    if _slot_probe_output_has_error "$partial_output" "401\|402\|403\|unauthorized\|payment required\|insufficient"; then
      kill "$pid" 2>/dev/null; wait "$pid" 2>/dev/null
      rm -f "$prompt_file" "$output_file"
      printf 'auth_failure\n'; return 0
    fi
    if _slot_probe_output_has_error "$partial_output" "timeout\|connection refused\|network\|DNS\|resolve"; then
      kill "$pid" 2>/dev/null; wait "$pid" 2>/dev/null
      rm -f "$prompt_file" "$output_file"
      printf 'network_failure\n'; return 0
    fi
    sleep 1; slept=$((slept + 1))
  done
  kill "$pid" 2>/dev/null; wait "$pid" 2>/dev/null
  rm -f "$prompt_file" "$output_file"
  printf 'unknown_error\n'
}

_slot_probe_output_is_success() {
  local out="$1"
  [[ -n "$out" ]] || return 1
  # Any non-empty, non-error output after "hi" is success
  ! _slot_probe_output_has_error "$out" "error\|Error\|failed\|Failed"
}

_slot_probe_output_has_error() {
  local out="$1" pattern="$2"
  [[ -n "$out" ]] && echo "$out" | grep -qi "$pattern"
}

codex_probe_current_slot_now() {
  local project="$1" probe_lock_reason="${2:-codex_exec_probe}" probe_activity_label="${3:-codex exec probe}" prompt_file output_file rc timeout_secs="${CODEX_PROBE_TIMEOUT:-15}" probe_lock_held=0
  local current_slot artifact_path partial_output
  wait_for_codex_slot_switch_idle "$project" "$probe_activity_label" || return 1
  codex_slot_switch_probe_lock_acquire "$probe_lock_reason" "$probe_activity_label" || return 1
  probe_lock_held=1
  current_slot="$(codex_current_slot "$project" || true)"
  prompt_file="$(mktemp)"
  output_file="$(mktemp)"
  printf 'say hi\n' >"$prompt_file"
  rc=0

  # Run codex exec with project-scoped proxy resolution and timeout.
  (
    cd "$project"
    freely_apply_project_network_proxy_env "$project"

    local codex_pid=""
    _probe_cleanup_child() {
      if [[ -n "$codex_pid" ]]; then
        kill "$codex_pid" 2>/dev/null || true
        wait "$codex_pid" 2>/dev/null || true
      fi
    }
    trap '_probe_cleanup_child; exit 143' TERM INT

    if [[ -n "${AI_MODEL:-}" ]]; then
      codex exec \
        --skip-git-repo-check \
        -C "$project" \
        -m "$AI_MODEL" \
        -c "model_reasoning_effort=\"${AI_REASONING_EFFORT:-medium}\"" \
        --dangerously-bypass-approvals-and-sandbox \
        - <"$prompt_file" &
    else
      codex exec \
        --skip-git-repo-check \
        -C "$project" \
        -c "model_reasoning_effort=\"${AI_REASONING_EFFORT:-medium}\"" \
        --dangerously-bypass-approvals-and-sandbox \
        - <"$prompt_file" &
    fi
    codex_pid=$!
    wait "$codex_pid"
  ) >"$output_file" 2>&1 &
  local pid=$!

  # Wait with timeout
  local slept=0
  while [[ $slept -lt $timeout_secs ]]; do
    partial_output="$(cat "$output_file" 2>/dev/null || true)"
    if codex_probe_output_is_expected_success "$partial_output"; then
      terminate_codex_probe_process "$pid"
      rm -f "$prompt_file" "$output_file"
      if [[ "$probe_lock_held" == "1" ]]; then
        codex_slot_switch_probe_lock_release
      fi
      printf 'usable\n'
      return 0
    fi
    if codex_probe_output_has_deactivated_workspace "$partial_output"; then
      terminate_codex_probe_process "$pid"
      artifact_path="$(write_codex_probe_artifact "$project" "$current_slot" "deactivated-workspace" "$partial_output")"
      rm -f "$prompt_file" "$output_file"
      if [[ "$probe_lock_held" == "1" ]]; then
        codex_slot_switch_probe_lock_release
      fi
      if [[ -n "$artifact_path" ]]; then
        log_warn "codex probe observed deactivated_workspace for slot ${current_slot:-unknown}; details captured at $artifact_path"
      fi
      printf 'deactivated_workspace\n'
      return 0
    fi
    if codex_probe_output_has_network_failure "$partial_output"; then
      terminate_codex_probe_process "$pid"
      artifact_path="$(write_codex_probe_artifact "$project" "$current_slot" "network-failure" "$partial_output")"
      rm -f "$prompt_file" "$output_file"
      if [[ "$probe_lock_held" == "1" ]]; then
        codex_slot_switch_probe_lock_release
      fi
      if [[ -n "$artifact_path" ]]; then
        log_warn "codex probe observed network failure for slot ${current_slot:-unknown}; details captured at $artifact_path"
      fi
      printf 'network_failure\n'
      return 0
    fi
    if ! kill -0 "$pid" 2>/dev/null; then
      break
    fi
    sleep 1
    ((slept++))
  done

  # Kill if still running
  if kill -0 "$pid" 2>/dev/null; then
    terminate_codex_probe_process "$pid"
    artifact_path="$(write_codex_probe_artifact "$project" "$current_slot" "timeout" "$(cat "$output_file" 2>/dev/null || true)")"
    rm -f "$prompt_file" "$output_file"
    if [[ "$probe_lock_held" == "1" ]]; then
      codex_slot_switch_probe_lock_release
    fi
    if [[ -n "$artifact_path" ]]; then
      log_warn "codex probe timed out for slot ${current_slot:-unknown}; captured partial output at $artifact_path"
    fi
    printf 'timeout\n'
    return 0
  fi

  wait "$pid" 2>/dev/null || rc=$?
  rm -f "$prompt_file"

  local output
  output="$(cat "$output_file")"
  rm -f "$output_file"
  if [[ "$probe_lock_held" == "1" ]]; then
    codex_slot_switch_probe_lock_release
  fi

  output="$(strip_probe_output_for_matching "$output")"

  # Only a fixed successful "hi" transcript is treated as success.
  if codex_probe_is_expected_success "$rc" "$output"; then
    printf 'usable\n'
    return 0
  fi

  # Check for subscription/payment issues
  if printf '%s\n' "$output" | grep -qi "subscription\|billing\|payment\|quota\|plan\|upgrade"; then
    printf 'subscription_expired\n'
    return 0
  fi

  # Check for unauthorized/auth issues
  if printf '%s\n' "$output" | grep -qi "unauthorized\|authentication\|invalid.*token\|login required\|401\|403"; then
    printf 'unauthorized\n'
    return 0
  fi

  # Check for rate limit.
  if printf '%s\n' "$output" | grep -qi "usage limit\|try again"; then
    local reset_at
    reset_at="$(extract_try_again_time_from_output "$output")"
    if [[ -n "$reset_at" ]]; then
      printf 'rate_limited:%s\n' "$reset_at"
      return 0
    fi
    # Fallback: rate limited but no time found, still report it
    printf 'rate_limited:0\n'
    return 0
  fi

  if codex_probe_output_has_deactivated_workspace "$output"; then
    artifact_path="$(write_codex_probe_artifact "$project" "$current_slot" "deactivated-workspace" "$output")"
    if [[ -n "$artifact_path" ]]; then
      log_warn "codex probe observed deactivated_workspace for slot ${current_slot:-unknown}; details captured at $artifact_path"
    fi
    printf 'deactivated_workspace\n'
    return 0
  fi

  if codex_probe_output_has_network_failure "$output"; then
    artifact_path="$(write_codex_probe_artifact "$project" "$current_slot" "network-failure" "$output")"
    if [[ -n "$artifact_path" ]]; then
      log_warn "codex probe observed network failure for slot ${current_slot:-unknown}; details captured at $artifact_path"
    fi
    printf 'network_failure\n'
    return 0
  fi

  # Generic error
  local error_msg
  error_msg="$(printf '%s' "$output" | head -1 | tr '\n' ' ' | cut -c1-50)"
  printf 'error:%s\n' "$error_msg"
  return 0
}

probe_any_usable_codex_slot_now() {
  local project="$1" candidate probe_result reset_at original_slot active_slot original_active_slot auth_backup="" auth_file
  codex_auto_slot_switch_enabled || return 1
  original_slot="$(codex_current_slot "$project")"
  original_active_slot="$(read_codex_active_slot)"
  auth_file="$(codex_active_auth_file)"
  if [[ -f "$auth_file" ]]; then
    auth_backup="$(mktemp)"
    cp "$auth_file" "$auth_backup"
  fi
  while IFS= read -r candidate; do
    [[ -n "$candidate" ]] || continue
    switch_to_codex_slot "$project" "$candidate" "probe_saved_slots" >/dev/null || continue

    probe_result="$(codex_probe_current_slot_now "$project")" || continue
    case "$probe_result" in
      usable)
      [[ -z "$auth_backup" ]] || rm -f "$auth_backup"
      printf '%s\n' "$candidate"
      return 0
      ;;
    esac
  done <<<"$(codex_saved_slots "$project")"

  active_slot="$(codex_current_slot "$project")"
  if [[ -n "$original_slot" && -n "$active_slot" && "$(normalize_codex_slot_name "$original_slot")" != "$(normalize_codex_slot_name "$active_slot")" ]]; then
    switch_to_codex_slot "$project" "$original_slot" "probe_restore_original_slot" >/dev/null || true
  else
    restore_codex_probe_origin "$original_slot" "$original_active_slot" "$auth_backup" >/dev/null || true
  fi
  [[ -z "$auth_backup" ]] || rm -f "$auth_backup"
}

# Probe ALL saved slots and report the first usable slot.
# Output format:
#   usable:<slot>           - Found a usable slot
#   all_unavailable:<slot>|<reset_at>  - No usable slot right now; earliest reset is debug-only hint
#   none                    - No slots saved or all failed without rate limit info
probe_all_codex_slots_and_update_cooldown() {
  local project="$1" excluded_identity="${2:-}" promotion_mode="${3:-promote}"
  local candidate probe_result reset_at
  local usable_slot=""
  local earliest_slot="" earliest_reset=""
  local current_identity original_slot active_slot original_active_slot auth_backup="" auth_file
  local tmp_dir results_file current_marker status_icon="" status_text="" details="" auth_email="" detail=""

  codex_auto_slot_switch_enabled || {
    printf 'none\n'
    return 1
  }

  current_identity="$(codex_current_cooldown_identity "$project")"
  original_slot="$(codex_current_slot "$project")"
  original_active_slot="$(read_codex_active_slot)"
  auth_file="$(codex_active_auth_file)"
  if [[ -f "$auth_file" ]]; then
    auth_backup="$(mktemp)"
    cp "$auth_file" "$auth_backup"
  fi
  tmp_dir="$(mktemp -d)"
  results_file="$tmp_dir/exec-results.tsv"

  # Print header
  printf '\n%-30s  %-15s  %s\n' "Slot" "Status" "Details" >&2
  printf '%s\n' "$(printf '%-30s  %-15s  %s' '' '' '' | tr ' ' '-')" >&2

  while IFS= read -r candidate; do
    [[ -n "$candidate" ]] || continue
    if codex_slot_matches_identity "$candidate" "$excluded_identity"; then
      continue
    fi
    switch_to_codex_slot "$project" "$candidate" "probe_all_slots" >/dev/null || continue

    probe_result="$(codex_probe_current_slot_now "$project")" || continue
    current_marker=""
    status_icon=""
    status_text=""
    details=""
    auth_email=""
    detail=""

    case "$probe_result" in
      usable)
        if [[ -z "$usable_slot" ]]; then
          usable_slot="$candidate"
        fi
        status_icon="✅"
        status_text="usable"
        details="ready to use"
        detail="$details"
        ;;
      rate_limited:*)
        reset_at="${probe_result#rate_limited:}"
        if [[ -n "$reset_at" && "$reset_at" =~ ^[0-9]+$ && "$reset_at" -gt 0 && ( -z "$earliest_reset" || "$reset_at" -lt "$earliest_reset" ) ]]; then
          earliest_slot="$candidate"
          earliest_reset="$reset_at"
        fi
        status_icon="⏳"
        status_text="rate_limited"
        local human_time
        human_time="$(format_epoch_local "$reset_at")"
        details="resets at $human_time"
        detail="$human_time"
        ;;
      subscription_expired)
        status_icon="💳"
        status_text="subscription_expired"
        details="plan expired or quota exceeded"
        detail="$details"
        ;;
      deactivated_workspace)
        status_icon="🚫"
        status_text="deactivated_workspace"
        details="workspace deactivated (402)"
        detail="$details"
        ;;
      unauthorized)
        status_icon="🔒"
        status_text="unauthorized"
        details="auth token invalid or expired"
        detail="$details"
        ;;
      network_failure)
        status_icon="🌐"
        status_text="network_failure"
        details="connection failed before probe completed"
        detail="$details"
        ;;
      timeout)
        status_icon="⏱️"
        status_text="timeout"
        details="probe timed out after ${CODEX_PROBE_TIMEOUT:-15}s"
        detail="$details"
        ;;
      error:*)
        status_icon="❌"
        status_text="error"
        details="${probe_result#error:}"
        detail="$details"
        ;;
      *)
        status_icon="❓"
        status_text="unknown"
        details="$probe_result"
        detail="$details"
        ;;
    esac

    # Mark current slot
    if [[ "$(normalize_codex_slot_name "$candidate")" == "$current_identity" ]]; then
      current_marker=" *"
    fi

    if [[ "$candidate" == account-* ]]; then
      auth_email="${candidate#account-}"
    fi
    printf '%s\t%s\t%s\t%s\t0\t%s\n' \
      "$candidate" \
      "$status_text" \
      "$auth_email" \
      "${reset_at:-0}" \
      "${detail:-$details}" >>"$results_file"

    # Print status line
    printf '%s %-28s  %-15s  %s\n' "$status_icon" "$candidate$current_marker" "$status_text" "$details" >&2
  done <<<"$(codex_saved_slots "$project")"

  if [[ -s "$results_file" ]]; then
    codex_write_availability_cache_from_sweep_results "$project" "$results_file"
    codex_overwrite_slot_cooldowns_from_sweep_results "$project" "$results_file"
  fi
  printf '\n' >&2

  # Return results
  if [[ -n "$usable_slot" ]]; then
    if [[ "$promotion_mode" == "promote" ]]; then
      active_slot="$(codex_current_slot "$project")"
      if [[ -n "$active_slot" && "$(normalize_codex_slot_name "$active_slot")" != "$(normalize_codex_slot_name "$usable_slot")" ]]; then
        switch_to_codex_slot "$project" "$usable_slot" "probe_promote_usable_slot" >/dev/null || true
      fi
    else
      restore_codex_probe_origin "$original_slot" "$original_active_slot" "$auth_backup" >/dev/null || true
    fi
    rm -rf "$tmp_dir"
    [[ -z "$auth_backup" ]] || rm -f "$auth_backup"
    printf 'usable:%s\n' "$usable_slot"
    return 0
  elif [[ -n "$earliest_slot" ]]; then
    restore_codex_probe_origin "$original_slot" "$original_active_slot" "$auth_backup" >/dev/null || true
    rm -rf "$tmp_dir"
    [[ -z "$auth_backup" ]] || rm -f "$auth_backup"
    printf 'all_unavailable:%s|%s\n' "$earliest_slot" "$earliest_reset"
    return 0
  else
    restore_codex_probe_origin "$original_slot" "$original_active_slot" "$auth_backup" >/dev/null || true
    rm -rf "$tmp_dir"
    [[ -z "$auth_backup" ]] || rm -f "$auth_backup"
    printf 'none\n'
    return 1
  fi
}

switch_to_codex_slot() {
  local project="$1" slot="$2" reason="$3"
  local ai_bin output actual_slot requested_normalized actual_slot_normalized switch_output_confirmed="0"
  codex_auto_slot_switch_enabled || return 1
  wait_for_codex_slot_switch_idle "$project" || return 1
  ai_bin="$(ai_cli_bin_for_project "$project")"
  [[ -x "$ai_bin" && -n "$slot" ]] || return 1
  output="$(AI_CLI_SUPPRESS_AUTH_CHANGE_WAKE=1 "$ai_bin" --quiet --format json switch codex "$slot" --yes 2>/dev/null || true)"
  requested_normalized="$(normalize_codex_slot_name "$slot")"
  actual_slot="$(codex_current_slot "$project")"
  actual_slot_normalized="$(normalize_codex_slot_name "$actual_slot")"
  if printf '%s\n' "$output" | grep -qE '"switched": *true'; then
    switch_output_confirmed="1"
  fi
  if [[ -n "$actual_slot" && "$actual_slot_normalized" == "$requested_normalized" ]]; then
    if [[ "$switch_output_confirmed" != "1" && -n "$output" ]]; then
      log_warn "codex slot switch JSON confirmation missing; accepting actual active slot change instead (requested=$slot actual_slot=$actual_slot reason=$reason)" >&2
    fi
    if [[ "$reason" != probe_all_slots ]]; then
      log_warn "auto-switched codex slot to $slot (reason=$reason)" >&2
    fi
    printf '%s\n' "$slot"
    return 0
  fi
  if [[ -n "$actual_slot" ]]; then
    log_warn "codex slot switch verification failed (requested=$slot actual_slot=$actual_slot reason=$reason)" >&2
  fi
  return 1
}

switch_to_next_codex_slot() {
  local project="$1" reason="$2"
  local current_identity next_slot
  current_identity="$(codex_current_cooldown_identity "$project")"
  next_slot="$(select_next_codex_saved_slot "$project" "$current_identity")"
  [[ -n "$next_slot" ]] || return 1
  switch_to_codex_slot "$project" "$next_slot" "$reason"
}

ensure_codex_slot_ready_for_manager() {
  local project="$1" recovery_mode="${2:-entry}"
  local current_slot current_slot_kind current_identity current_probe_identity current_live_kind current_probe_result probe_result probe_status probe_slot cached_current_status
  local failed_current_identity=""
  local all_unavailable_info earliest_slot earliest_reset
  local current_fingerprint previous_phase="" previous_blocked_reason="" previous_slot="" previous_fingerprint="" wake_reason="" wake_trigger="" recovery_trigger=""

  codex_auto_slot_switch_enabled || return 1
  wait_for_codex_slot_switch_idle "$project" || return 1
  current_slot="$(codex_current_slot "$project")"
  current_slot_kind="$(codex_current_slot_kind "$project")"
  current_identity="$(codex_current_identity_hint "$project")"
  if [[ -z "$current_identity" && -n "$current_slot_kind" ]]; then
    current_identity="live-$current_slot_kind"
  fi
  current_probe_identity="${current_identity:-current-live}"
  current_live_kind="$(codex_live_auth_kind)"
  current_fingerprint="$(codex_saved_slots_fingerprint "$project")"
  if [[ "$recovery_mode" == "after_failure" ]]; then
    failed_current_identity="$current_probe_identity"
  fi

  if codex_load_availability_state "$project"; then
    previous_phase="${AVAILABILITY_PHASE:-}"
    previous_blocked_reason="${BLOCKED_REASON:-}"
    previous_slot="${PREVIOUS_SLOT:-}"
    previous_fingerprint="${SAVED_SLOTS_FINGERPRINT:-}"
  fi

  if [[ "$recovery_mode" != "after_failure" && "${previous_phase:-}" == "all_unavailable" && "${previous_blocked_reason:-}" == "all_slots_unavailable" && -n "${previous_fingerprint:-}" && "$previous_fingerprint" == "$current_fingerprint" ]]; then
    log_info "watchdog leaves codex in all_unavailable state until a fresh failure or manual switch requests another real probe"
    return 1
  fi

  codex_write_availability_state "$project" "probing" "${previous_blocked_reason:-probe_pending}" "${previous_slot:-$current_identity}" "$current_identity" "$current_fingerprint" "" "" ""

  cached_current_status="$(codex_cached_slot_status "$project" "$current_identity" || true)"

  if [[ -z "$failed_current_identity" ]]; then
    if [[ -f "$(codex_active_auth_file)" && -n "$current_probe_identity" ]]; then
      codex_clear_availability_state "$project"
      return 0
    fi
    probe_slot="$(select_any_available_codex_slot "$project" || true)"
    if [[ -n "$probe_slot" ]] && switch_to_codex_slot "$project" "$probe_slot" "entry_select_saved_slot" >/dev/null; then
      codex_clear_availability_state "$project"
      return 0
    fi
    codex_write_availability_state "$project" "all_unavailable" "no_ready_saved_slot_without_failure" "${current_identity:-unknown}" "${current_identity:-unknown}" "$current_fingerprint" "" "" ""
    log_warn "no cached ready codex slot is available for manager entry; runtime will wait for manual switch or a later real failure instead of probing in the background"
    return 1
  fi

  probe_result="$(codex_exec_saved_slot_truth "$project" "$failed_current_identity" "after_failure_exec_recovery_slot_probe" "after_failure_exec_recovery_probe" "after-failure codex exec recovery probe" || true)"
  probe_status="${probe_result%%:*}"
  case "$probe_status" in
    usable)
      probe_slot="${probe_result#usable:}"
      if [[ -n "$probe_slot" ]]; then
        recovery_trigger="${previous_blocked_reason:-slot_probe_blocked}"
        wake_reason="watchdog_probed_and_found_usable_slot"
        if [[ -n "$previous_fingerprint" && "$previous_fingerprint" != "$current_fingerprint" ]]; then
          wake_reason="watchdog_inventory_change_found_usable_slot"
          wake_trigger="inventory_change"
        else
          wake_trigger="after_failure_exec_recovery"
        fi
        log_info "watchdog found a usable saved codex slot for manager bootstrap (trigger=$recovery_trigger reason=$wake_reason previous_slot=${current_identity:-${previous_slot:-unknown}} active_slot=$probe_slot)"
        write_manager_bootstrap_handoff "$project" "$recovery_trigger" "${current_identity:-${previous_slot:-unknown}}" "$probe_slot" "$wake_reason" "inspect-fleet-and-recover-workers"
        codex_write_availability_state "$project" "ready" "" "${current_identity:-${previous_slot:-unknown}}" "$probe_slot" "$current_fingerprint" "$wake_trigger" "" ""
        return 0
      fi
      ;;
    all_unavailable)
      all_unavailable_info="${probe_result#all_unavailable:}"
      earliest_slot="${all_unavailable_info%%|*}"
      earliest_reset="${all_unavailable_info##*|}"
      codex_write_availability_state "$project" "all_unavailable" "all_slots_unavailable" "${current_identity:-unknown}" "${current_identity:-unknown}" "$current_fingerprint" "" "$earliest_slot" "$earliest_reset"
      write_manager_bootstrap_handoff "$project" "all_slots_unavailable" "${current_identity:-unknown}" "${current_identity:-unknown}" "watchdog_hold_until_slot_is_usable" "keep-manager-down-until-watchdog-finds-usable-slot"
      if [[ -n "$earliest_slot" && -n "$earliest_reset" && "$all_unavailable_info" == *"|"* ]]; then
        log_warn "no codex slot is usable for manager bootstrap; earliest_reset=${earliest_reset} and runtime will now wait for manual intervention or a later explicit recovery attempt"
      else
        log_warn "no codex slot is usable for manager bootstrap; runtime will wait for manual intervention or a later explicit recovery attempt"
      fi
      return 1
      ;;
  esac

  codex_write_availability_state "$project" "all_unavailable" "slot_probe_failed" "${current_identity:-unknown}" "${current_identity:-unknown}" "$current_fingerprint" "" "" ""
  write_manager_bootstrap_handoff "$project" "slot_probe_failed" "${current_identity:-unknown}" "${current_identity:-unknown}" "watchdog_hold_until_slot_is_usable" "keep-manager-down-until-watchdog-finds-usable-slot"
  log_error "no codex slot is currently available for manager bootstrap"
  return 1
}
