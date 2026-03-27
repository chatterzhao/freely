# shellcheck shell=bash

normalize_codex_slot_name() {
  printf '%s' "$1" | sed 's/\./-/g'
}

codex_active_slot_file() {
  printf '%s\n' "$HOME/.codex/active-slot"
}

codex_active_auth_file() {
  printf '%s\n' "$HOME/.codex/auth.json"
}

watchdog_run_dir_for_project() {
  local project="$1"
  printf '%s\n' "$project/.freely/run"
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
  ts="$(date '+%Y%m%d-%H%M%S')"
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
  local timeout_secs="${FREELY_ACCOUNT_SWITCH_WAIT_SECS:-60}"
  local interval_secs="${FREELY_ACCOUNT_SWITCH_WAIT_INTERVAL_SECS:-1}"
  local start_ts now owner_pid waiting_logged=0
  [[ "$timeout_secs" =~ ^[0-9]+$ ]] || timeout_secs=60
  [[ "$interval_secs" =~ ^[0-9]+$ ]] || interval_secs=1
  start_ts="$(date +%s)"

  while codex_slot_switch_in_progress; do
    if [[ "$waiting_logged" == "0" ]]; then
      owner_pid="$(codex_slot_switch_lock_owner_pid)"
      log_warn "codex slot switch is already in progress (owner_pid=${owner_pid:-unknown}); waiting before watchdog probe/relaunch" >&2
      waiting_logged=1
    fi
    now="$(date +%s)"
    if (( now - start_ts >= timeout_secs )); then
      log_warn "timed out waiting for codex slot switch to finish before watchdog recovery" >&2
      return 1
    fi
    sleep "$interval_secs"
  done

  return 0
}

codex_slot_switch_probe_lock_acquire() {
  local reason="${1:-watchdog_probe}"
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
      log_warn "timed out waiting to serialize watchdog codex probe behind slot switch activity"
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
  printf '%s\n' "$(run_dir_for_project "$project")/codex-availability-state.env"
}

codex_availability_cache_file() {
  local project="$1"
  printf '%s\n' "$(run_dir_for_project "$project")/codex-availability-cache.tsv"
}

codex_oauth_usage_url() {
  printf '%s\n' "${CODEX_OAUTH_USAGE_URL:-https://chatgpt.com/backend-api/wham/usage}"
}

codex_saved_slot_auth_file() {
  local slot="$1"
  printf '%s\n' "${AUTH_DIR:-$HOME/.ai-auth}/codex-${slot}/auth.json"
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
  local project="$1" phase="$2" blocked_reason="$3" previous_slot="$4" active_slot="$5" inventory_fingerprint="$6" wake_trigger="$7" earliest_slot="$8" earliest_reset="$9"
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

codex_oauth_probe_single_slot() {
  local slot="$1" auth_file="$2" output_file="$3"
  local usage_url token auth_email response_file http_code response_body
  usage_url="$(codex_oauth_usage_url)"
  if [[ ! -f "$auth_file" ]]; then
    printf '%s\tmissing_auth\t\t0\t0\tauth file missing\n' "$slot" >"$output_file"
    return 0
  fi

  read -r token auth_email < <(python3 - <<'PY' "$auth_file"
import base64
import json
import sys

path = sys.argv[1]
token = ""
email = ""
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)
token = data.get("tokens", {}).get("access_token", "") or data.get("access_token", "")
id_token = data.get("tokens", {}).get("id_token", "")
if id_token:
    try:
        payload = id_token.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        email = json.loads(base64.urlsafe_b64decode(payload.encode())).get("email", "")
    except Exception:
        email = ""
print(token, email)
PY
)

  if [[ -z "$token" ]]; then
    printf '%s\tmissing_token\t%s\t0\t0\taccess token missing\n' "$slot" "$auth_email" >"$output_file"
    return 0
  fi

  response_file="$(mktemp)"
  if ! http_code="$(curl -sS -o "$response_file" -w '%{http_code}' -H "Authorization: Bearer $token" "$usage_url" 2>/dev/null)"; then
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

rate_limits = payload.get("rate_limits", {}) if isinstance(payload, dict) else {}
primary = rate_limits.get("primary", {}) if isinstance(rate_limits, dict) else {}
secondary = rate_limits.get("secondary", {}) if isinstance(rate_limits, dict) else {}
primary_used = primary.get("used_percent")
secondary_used = secondary.get("used_percent")
primary_reset = numeric_reset(primary.get("resets_at"))
secondary_reset = numeric_reset(secondary.get("resets_at"))

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
    human = datetime.fromtimestamp(int(reset_at), timezone.utc).strftime("%Y.%m.%d %H:%M:%S")
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
  local candidate auth_file tmp_dir results_file result_file
  local usable_slot="" earliest_slot="" earliest_reset=""
  local saw_result=0 current_identity
  current_identity="$(codex_current_cooldown_identity "$project")"
  tmp_dir="$(mktemp -d)"
  results_file="$tmp_dir/results.tsv"

  while IFS= read -r candidate; do
    [[ -n "$candidate" ]] || continue
    auth_file="$(codex_saved_slot_auth_file "$candidate")"
    result_file="$tmp_dir/${candidate}.tsv"
    codex_oauth_probe_single_slot "$candidate" "$auth_file" "$result_file" &
  done < <(codex_saved_slots "$project")
  wait || true

  cat "$tmp_dir"/*.tsv 2>/dev/null >"$results_file" || true
  if [[ ! -s "$results_file" ]]; then
    rm -rf "$tmp_dir"
    printf 'none\n'
    return 1
  fi

  codex_write_availability_cache_from_sweep_results "$project" "$results_file"
  codex_overwrite_slot_cooldowns_from_sweep_results "$project" "$results_file"

  printf '\n%-30s  %-20s  %s\n' "Slot" "OAuth status" "Details" >&2
  printf '%s\n' "$(printf '%-30s  %-20s  %s' '' '' '' | tr ' ' '-')" >&2
  while IFS=$'\t' read -r candidate status auth_email reset_at http_code detail; do
    [[ -n "$candidate" ]] || continue
    saw_result=1
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
    printf '%-30s  %-20s  %s\n' "$candidate" "$status" "$detail" >&2
  done <"$results_file"
  printf '\n' >&2

  rm -rf "$tmp_dir"
  if [[ -n "$usable_slot" ]]; then
    printf 'usable:%s\n' "$usable_slot"
    return 0
  fi
  if [[ -n "$earliest_slot" && -n "$earliest_reset" ]]; then
    printf 'all_unavailable:%s|%s\n' "$earliest_slot" "$earliest_reset"
    return 0
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
  human_readable="$(date -r "$reset_at" '+%Y.%m.%d %H:%M:%S' 2>/dev/null || date -d "@$reset_at" '+%Y.%m.%d %H:%M:%S' 2>/dev/null || echo '')"
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
  done < <(codex_saved_slots "$project")
  return 1
}

select_next_codex_slot() {
  local project="$1" current_identity="${2:-}"
  local normalized_current candidate
  normalized_current="$(normalize_codex_slot_name "$current_identity")"
  while IFS= read -r candidate; do
    [[ -n "$candidate" ]] || continue
    if [[ -z "$normalized_current" || "$candidate" != "$normalized_current" ]]; then
      if ! codex_slot_is_available_now "$project" "$candidate"; then
        continue
      fi
      printf '%s\n' "$candidate"
      return 0
    fi
  done < <(codex_saved_slots "$project")
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
  done < <(codex_saved_slots "$project")
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
  done < <(codex_saved_slots "$project")
}

watchdog_reset_buffer_seconds() {
  local buffer="${WATCHDOG_RESET_BUFFER_SECS:-60}"
  [[ "$buffer" =~ ^[0-9]+$ ]] || buffer=60
  printf '%s\n' "$buffer"
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
  done < <(codex_saved_slots "$project")
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
#   timeout
#   error:<message>
# Exit code:
#   0 for usable or rate limited
#   1 for other probe failures
codex_probe_current_slot_now() {
  local project="$1" prompt_file output_file rc timeout_secs="${CODEX_PROBE_TIMEOUT:-15}" probe_lock_held=0
  local current_slot artifact_path partial_output
  wait_for_codex_slot_switch_idle "$project" || return 1
  codex_slot_switch_probe_lock_acquire "watchdog_probe_current_slot" || return 1
  probe_lock_held=1
  current_slot="$(codex_current_slot "$project" || true)"
  prompt_file="$(mktemp)"
  output_file="$(mktemp)"
  printf 'hi\n' >"$prompt_file"
  rc=0

  # Run codex exec with proxy and timeout
  (
    cd "$project"
    # Export proxy env for codex
    export ALL_PROXY="${ALL_PROXY:-http://127.0.0.1:7890}"
    export HTTP_PROXY="${HTTP_PROXY:-http://127.0.0.1:7890}"
    export HTTPS_PROXY="${HTTPS_PROXY:-http://127.0.0.1:7890}"

    if [[ -n "${AI_MODEL:-}" ]]; then
      codex exec \
        --skip-git-repo-check \
        -C "$project" \
        -m "$AI_MODEL" \
        -c "model_reasoning_effort=\"${AI_REASONING_EFFORT:-medium}\"" \
        --dangerously-bypass-approvals-and-sandbox \
        - <"$prompt_file"
    else
      codex exec \
        --skip-git-repo-check \
        -C "$project" \
        -c "model_reasoning_effort=\"${AI_REASONING_EFFORT:-medium}\"" \
        --dangerously-bypass-approvals-and-sandbox \
        - <"$prompt_file"
    fi
  ) >"$output_file" 2>&1 &
  local pid=$!

  # Wait with timeout
  local slept=0
  while [[ $slept -lt $timeout_secs ]]; do
    partial_output="$(cat "$output_file" 2>/dev/null || true)"
    if printf '%s\n' "$partial_output" | grep -qi "deactivated_workspace\|402 Payment Required"; then
      kill "$pid" 2>/dev/null || true
      wait "$pid" 2>/dev/null || true
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
    if ! kill -0 "$pid" 2>/dev/null; then
      break
    fi
    sleep 1
    ((slept++))
  done

  # Kill if still running
  if kill -0 "$pid" 2>/dev/null; then
    kill "$pid" 2>/dev/null
    wait "$pid" 2>/dev/null || true
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

  # Strip ANSI escape codes for reliable grep matching
  # Handle various escape sequences: ESC[...m, ESC]...BEL, ESC[?...h/l, etc.
  output="$(printf '%s\n' "$output" | sed -E 's/\x1b\[[0-9;]*[a-zA-Z]//g; s/\x1b\].*\x07//g; s/\x1b\][^\x1b]*\x1b\\//g')"

  # Check for success.
  if [[ "$rc" -eq 0 ]]; then
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

  if printf '%s\n' "$output" | grep -qi "deactivated_workspace\|402 Payment Required"; then
    artifact_path="$(write_codex_probe_artifact "$project" "$current_slot" "deactivated-workspace" "$output")"
    if [[ -n "$artifact_path" ]]; then
      log_warn "codex probe observed deactivated_workspace for slot ${current_slot:-unknown}; details captured at $artifact_path"
    fi
  fi

  # Generic error
  local error_msg
  error_msg="$(printf '%s' "$output" | head -1 | tr '\n' ' ' | cut -c1-50)"
  printf 'error:%s\n' "$error_msg"
  return 0
}

probe_any_usable_codex_slot_now() {
  local project="$1" candidate probe_result reset_at original_slot active_slot original_active_slot auth_backup="" auth_file
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
  done < <(codex_saved_slots "$project")

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
  local project="$1"
  local candidate probe_result reset_at
  local usable_slot=""
  local earliest_slot="" earliest_reset=""
  local -a slot_status=()
  local current_identity original_slot active_slot original_active_slot auth_backup="" auth_file

  current_identity="$(codex_current_cooldown_identity "$project")"
  original_slot="$(codex_current_slot "$project")"
  original_active_slot="$(read_codex_active_slot)"
  auth_file="$(codex_active_auth_file)"
  if [[ -f "$auth_file" ]]; then
    auth_backup="$(mktemp)"
    cp "$auth_file" "$auth_backup"
  fi

  probe_result="$(codex_oauth_sweep_all_slots "$project" || true)"
  case "$probe_result" in
    usable:*)
      usable_slot="${probe_result#usable:}"
      if [[ -n "$usable_slot" ]]; then
        switch_to_codex_slot "$project" "$usable_slot" "oauth_sweep_promote_usable_slot" >/dev/null || true
        [[ -z "$auth_backup" ]] || rm -f "$auth_backup"
        printf 'usable:%s\n' "$usable_slot"
        return 0
      fi
      ;;
    all_unavailable:*)
      restore_codex_probe_origin "$original_slot" "$original_active_slot" "$auth_backup" >/dev/null || true
      [[ -z "$auth_backup" ]] || rm -f "$auth_backup"
      printf '%s\n' "$probe_result"
      return 0
      ;;
  esac

  # Print header
  printf '\n%-30s  %-15s  %s\n' "Slot" "Status" "Details" >&2
  printf '%s\n' "$(printf '%-30s  %-15s  %s' '' '' '' | tr ' ' '-')" >&2

  while IFS= read -r candidate; do
    [[ -n "$candidate" ]] || continue
    switch_to_codex_slot "$project" "$candidate" "probe_all_slots" >/dev/null || continue

    probe_result="$(codex_probe_current_slot_now "$project")" || continue

    local status_line="" status_icon="" status_text="" details=""

    case "$probe_result" in
      usable)
        usable_slot="$candidate"
        status_icon="✅"
        status_text="usable"
        details="ready to use"
        ;;
      rate_limited:*)
        reset_at="${probe_result#rate_limited:}"
        if [[ -z "$earliest_reset" || "$reset_at" -lt "$earliest_reset" ]]; then
          earliest_slot="$candidate"
          earliest_reset="$reset_at"
        fi
        status_icon="⏳"
        status_text="rate_limited"
        local human_time
        human_time="$(date -r "$reset_at" '+%Y.%m.%d %H:%M:%S' 2>/dev/null || date -d "@$reset_at" '+%Y.%m.%d %H:%M:%S' 2>/dev/null || echo "$reset_at")"
        details="resets at $human_time"
        ;;
      subscription_expired)
        status_icon="💳"
        status_text="subscription"
        details="plan expired or quota exceeded"
        ;;
      deactivated_workspace)
        status_icon="🚫"
        status_text="deactivated"
        details="workspace deactivated (402)"
        ;;
      unauthorized)
        status_icon="🔒"
        status_text="unauthorized"
        details="auth token invalid or expired"
        ;;
      timeout)
        status_icon="⏱️"
        status_text="timeout"
        details="probe timed out after ${CODEX_PROBE_TIMEOUT:-15}s"
        ;;
      error:*)
        status_icon="❌"
        status_text="error"
        details="${probe_result#error:}"
        ;;
      *)
        status_icon="❓"
        status_text="unknown"
        details="$probe_result"
        ;;
    esac

    # Mark current slot
    local current_marker=""
    if [[ "$(normalize_codex_slot_name "$candidate")" == "$current_identity" ]]; then
      current_marker=" *"
    fi

    # Print status line
    printf '%s %-28s  %-15s  %s\n' "$status_icon" "$candidate$current_marker" "$status_text" "$details" >&2

    slot_status+=("$candidate:$status_text")
  done < <(codex_saved_slots "$project")

  printf '\n' >&2

  # Return results
  if [[ -n "$usable_slot" ]]; then
    active_slot="$(codex_current_slot "$project")"
    if [[ -n "$active_slot" && "$(normalize_codex_slot_name "$active_slot")" != "$(normalize_codex_slot_name "$usable_slot")" ]]; then
      switch_to_codex_slot "$project" "$usable_slot" "probe_promote_usable_slot" >/dev/null || true
    fi
    [[ -z "$auth_backup" ]] || rm -f "$auth_backup"
    printf 'usable:%s\n' "$usable_slot"
    return 0
  elif [[ -n "$earliest_slot" ]]; then
    restore_codex_probe_origin "$original_slot" "$original_active_slot" "$auth_backup" >/dev/null || true
    [[ -z "$auth_backup" ]] || rm -f "$auth_backup"
    printf 'all_unavailable:%s|%s\n' "$earliest_slot" "$earliest_reset"
    return 0
  else
    restore_codex_probe_origin "$original_slot" "$original_active_slot" "$auth_backup" >/dev/null || true
    [[ -z "$auth_backup" ]] || rm -f "$auth_backup"
    printf 'none\n'
    return 1
  fi
}

switch_to_codex_slot() {
  local project="$1" slot="$2" reason="$3"
  local ai_bin output actual_slot requested_normalized actual_slot_normalized
  wait_for_codex_slot_switch_idle "$project" || return 1
  ai_bin="$(ai_cli_bin_for_project "$project")"
  [[ -x "$ai_bin" && -n "$slot" ]] || return 1
  output="$("$ai_bin" --quiet --format json switch codex "$slot" --yes 2>/dev/null || true)"
  requested_normalized="$(normalize_codex_slot_name "$slot")"
  actual_slot="$(codex_current_slot "$project")"
  actual_slot_normalized="$(normalize_codex_slot_name "$actual_slot")"
  if printf '%s\n' "$output" | grep -qE '"switched": *true' && \
    [[ -n "$actual_slot" && "$actual_slot_normalized" == "$requested_normalized" ]]; then
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
  next_slot="$(select_next_codex_slot "$project" "$current_identity")"
  [[ -n "$next_slot" ]] || return 1
  switch_to_codex_slot "$project" "$next_slot" "$reason"
}

ensure_codex_slot_ready_for_manager() {
  local project="$1"
  local current_slot current_identity current_probe_result probe_result probe_status probe_slot
  local all_unavailable_info earliest_slot earliest_reset
  local current_fingerprint previous_phase="" previous_blocked_reason="" previous_slot="" previous_fingerprint="" wake_reason="" wake_trigger="" recovery_trigger=""

  wait_for_codex_slot_switch_idle "$project" || return 1
  current_slot="$(codex_current_slot "$project")"
  current_identity="$current_slot"
  current_fingerprint="$(codex_saved_slots_fingerprint "$project")"

  if codex_load_availability_state "$project"; then
    previous_phase="${AVAILABILITY_PHASE:-}"
    previous_blocked_reason="${BLOCKED_REASON:-}"
    previous_slot="${PREVIOUS_SLOT:-}"
    previous_fingerprint="${SAVED_SLOTS_FINGERPRINT:-}"
  fi

  codex_write_availability_state "$project" "probing" "${previous_blocked_reason:-probe_pending}" "${previous_slot:-$current_identity}" "$current_identity" "$current_fingerprint" "" "" ""

  if [[ -n "$current_identity" ]]; then
    current_probe_result="$(codex_probe_current_slot_now "$project" || true)"
    case "$current_probe_result" in
      usable)
        if [[ "$previous_phase" == "all_unavailable" || "$previous_phase" == "probing" ]]; then
          recovery_trigger="${previous_blocked_reason:-slot_probe_blocked}"
          wake_reason="watchdog_probed_current_slot_usable"
          if [[ -n "$previous_fingerprint" && "$previous_fingerprint" != "$current_fingerprint" ]]; then
            wake_reason="watchdog_inventory_change_found_usable_slot"
            wake_trigger="inventory_change"
          elif [[ "$previous_phase" == "all_unavailable" || "$previous_blocked_reason" == "all_slots_unavailable" ]]; then
            wake_reason="watchdog_probed_and_found_usable_slot"
            wake_trigger="periodic_reprobe"
          else
            wake_trigger="periodic_reprobe"
          fi
          log_info "watchdog found a usable current codex slot for manager bootstrap (trigger=$recovery_trigger reason=$wake_reason previous_slot=${previous_slot:-$current_identity} active_slot=$current_identity)"
          write_manager_bootstrap_handoff "$project" "$recovery_trigger" "${previous_slot:-$current_identity}" "$current_identity" "$wake_reason" "inspect-fleet-and-recover-workers"
          codex_write_availability_state "$project" "ready" "" "${previous_slot:-$current_identity}" "$current_identity" "$current_fingerprint" "$wake_trigger" "" ""
        else
          codex_clear_availability_state "$project"
        fi
        return 0
        ;;
    esac
  fi

  probe_result="$(probe_all_codex_slots_and_update_cooldown "$project" || true)"
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
          wake_trigger="periodic_reprobe"
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
        log_warn "no codex slot is usable for manager bootstrap; earliest_reset=${earliest_reset} remains a hint only while watchdog keeps probing"
      else
        log_warn "no codex slot is usable for manager bootstrap; watchdog will keep manager down until a later probe succeeds"
      fi
      return 1
      ;;
  esac

  codex_write_availability_state "$project" "all_unavailable" "slot_probe_failed" "${current_identity:-unknown}" "${current_identity:-unknown}" "$current_fingerprint" "" "" ""
  write_manager_bootstrap_handoff "$project" "slot_probe_failed" "${current_identity:-unknown}" "${current_identity:-unknown}" "watchdog_hold_until_slot_is_usable" "keep-manager-down-until-watchdog-finds-usable-slot"
  log_error "no codex slot is currently available for manager bootstrap"
  return 1
}
