# shellcheck shell=bash

normalize_codex_account_name() {
  printf '%s' "$1" | sed 's/\./-/g'
}

codex_account_switch_lock_dir() {
  printf '%s\n' "${AI_CLI_SWITCH_LOCK_DIR:-$HOME/.codex/account-switch.lock}"
}

codex_account_switch_lock_state_file() {
  printf '%s\n' "$(codex_account_switch_lock_dir)/state.env"
}

codex_account_switch_lock_owner_pid() {
  local state_file
  state_file="$(codex_account_switch_lock_state_file)"
  [[ -f "$state_file" ]] || return 0
  sed -n 's/^owner_pid=//p' "$state_file" | tail -n 1
}

codex_account_switch_lock_cleanup_if_stale() {
  local lock_dir owner_pid
  lock_dir="$(codex_account_switch_lock_dir)"
  [[ -d "$lock_dir" ]] || return 0
  owner_pid="$(codex_account_switch_lock_owner_pid)"
  if [[ -z "$owner_pid" ]] || ! kill -0 "$owner_pid" 2>/dev/null; then
    rm -rf "$lock_dir"
  fi
}

codex_account_switch_in_progress() {
  local lock_dir owner_pid inherited_owner_pid
  codex_account_switch_lock_cleanup_if_stale
  lock_dir="$(codex_account_switch_lock_dir)"
  [[ -d "$lock_dir" ]] || return 1
  owner_pid="$(codex_account_switch_lock_owner_pid)"
  inherited_owner_pid="${AI_CLI_SWITCH_LOCK_OWNER_PID:-}"
  [[ -n "$owner_pid" ]] || return 1
  [[ "$owner_pid" != "$$" ]] || return 1
  [[ -z "$inherited_owner_pid" || "$owner_pid" != "$inherited_owner_pid" ]] || return 1
  kill -0 "$owner_pid" 2>/dev/null
}

wait_for_codex_account_switch_idle() {
  local project="$1"
  local timeout_secs="${FREELY_ACCOUNT_SWITCH_WAIT_SECS:-60}"
  local interval_secs="${FREELY_ACCOUNT_SWITCH_WAIT_INTERVAL_SECS:-1}"
  local start_ts now owner_pid waiting_logged=0
  [[ "$timeout_secs" =~ ^[0-9]+$ ]] || timeout_secs=60
  [[ "$interval_secs" =~ ^[0-9]+$ ]] || interval_secs=1
  start_ts="$(date +%s)"

  while codex_account_switch_in_progress; do
    if [[ "$waiting_logged" == "0" ]]; then
      owner_pid="$(codex_account_switch_lock_owner_pid)"
      log_warn "codex account switch is already in progress (owner_pid=${owner_pid:-unknown}); waiting before watchdog probe/relaunch"
      waiting_logged=1
    fi
    now="$(date +%s)"
    if (( now - start_ts >= timeout_secs )); then
      log_warn "timed out waiting for codex account switch to finish before watchdog recovery"
      return 1
    fi
    sleep "$interval_secs"
  done

  return 0
}

codex_account_switch_probe_lock_acquire() {
  local reason="${1:-watchdog_probe}"
  local timeout_secs="${AI_CLI_SWITCH_LOCK_WAIT_SECS:-60}"
  local lock_dir state_file start_ts now owner_pid inherited_owner_pid
  lock_dir="$(codex_account_switch_lock_dir)"
  state_file="$(codex_account_switch_lock_state_file)"
  inherited_owner_pid="${AI_CLI_SWITCH_LOCK_OWNER_PID:-}"
  [[ "$timeout_secs" =~ ^[0-9]+$ ]] || timeout_secs=60
  mkdir -p "$(dirname "$lock_dir")"
  start_ts="$(date +%s)"

  while true; do
    codex_account_switch_lock_cleanup_if_stale
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

    owner_pid="$(codex_account_switch_lock_owner_pid)"
    if [[ -n "$owner_pid" && ( "$owner_pid" == "$$" || ( -n "$inherited_owner_pid" && "$owner_pid" == "$inherited_owner_pid" ) ) ]]; then
      export AI_CLI_SWITCH_LOCK_OWNER_PID="$owner_pid"
      return 0
    fi

    now="$(date +%s)"
    if (( now - start_ts >= timeout_secs )); then
      log_warn "timed out waiting to serialize watchdog codex probe behind account switch activity"
      return 1
    fi
    sleep 1
  done
}

codex_account_switch_probe_lock_release() {
  local lock_dir owner_pid inherited_owner_pid
  lock_dir="$(codex_account_switch_lock_dir)"
  [[ -d "$lock_dir" ]] || return 0
  owner_pid="$(codex_account_switch_lock_owner_pid)"
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
  wait_for_codex_account_switch_idle "$project" || return 1
  ai_bin="$(ai_cli_bin_for_project "$project")"
  [[ -x "$ai_bin" ]] || return 0
  output="$("$ai_bin" --quiet --format json whoami codex 2>/dev/null || true)"
  printf '%s\n' "$output" | sed -n 's/.*"account": *"\([^"]*\)".*/\1/p' | tail -n 1
}

codex_current_slot() {
  local project="$1" ai_bin output
  wait_for_codex_account_switch_idle "$project" || return 1
  ai_bin="$(ai_cli_bin_for_project "$project")"
  [[ -x "$ai_bin" ]] || return 0
  output="$("$ai_bin" --quiet --format json whoami codex 2>/dev/null || true)"
  printf '%s\n' "$output" | sed -n 's/.*"slot": *"\([^"]*\)".*/\1/p' | tail -n 1
}

codex_saved_accounts() {
  local project="$1" ai_bin output
  wait_for_codex_account_switch_idle "$project" || return 1
  ai_bin="$(ai_cli_bin_for_project "$project")"
  [[ -x "$ai_bin" ]] || return 0
  output="$("$ai_bin" --quiet --format json list 2>/dev/null || true)"
  printf '%s\n' "$output" | grep -o '"codex-[^"]*"' | tr -d '"' | sed 's/^codex-//'
}

codex_record_account_cooldown() {
  local project="$1" account="$2" reset_at="$3"
  local file tmp normalized human_readable
  [[ -n "$account" && -n "$reset_at" ]] || return 0
  normalized="$(normalize_codex_account_name "$account")"
  # Convert timestamp to human-readable format
  human_readable="$(date -r "$reset_at" '+%Y.%m.%d %H:%M:%S' 2>/dev/null || date -d "@$reset_at" '+%Y.%m.%d %H:%M:%S' 2>/dev/null || echo '')"
  file="$(codex_account_cooldown_file "$project")"
  mkdir -p "$(dirname "$file")"
  tmp="${file}.tmp"
  {
    if [[ -f "$file" ]]; then
      # Keep existing entries (preserve human-readable column if present)
      awk -F '\t' -v account="$normalized" '$1 != account {print $1 "\t" $2 "\t" $3}' "$file"
    fi
    printf '%s\t%s\t%s\n' "$normalized" "$reset_at" "$human_readable"
  } >"$tmp"
  mv "$tmp" "$file"
}

codex_account_cooldown_reset_at() {
  local project="$1" account="$2"
  local file normalized
  normalized="$(normalize_codex_account_name "$account")"
  file="$(codex_account_cooldown_file "$project")"
  [[ -f "$file" ]] || return 0
  awk -F '\t' -v account="$normalized" '$1 == account {print $2}' "$file" | tail -n 1
}

codex_clear_account_cooldown() {
  local project="$1" account="$2"
  local file tmp normalized
  normalized="$(normalize_codex_account_name "$account")"
  file="$(codex_account_cooldown_file "$project")"
  [[ -f "$file" ]] || return 0
  tmp="${file}.tmp"
  # Preserve all columns except the target account
  awk -F '\t' -v account="$normalized" '$1 != account {print $1 "\t" $2 "\t" $3}' "$file" >"$tmp"
  mv "$tmp" "$file"
}

codex_account_is_available_now() {
  local project="$1" account="$2"
  local reset_at
  reset_at="$(codex_account_cooldown_reset_at "$project" "$account")"
  if [[ -z "$reset_at" ]]; then
    return 0
  fi
  [[ "$(seconds_until_epoch "$reset_at")" == "0" ]]
}

codex_any_saved_account_available_now() {
  local project="$1" candidate
  while IFS= read -r candidate; do
    [[ -n "$candidate" ]] || continue
    if codex_account_is_available_now "$project" "$candidate"; then
      return 0
    fi
  done < <(codex_saved_accounts "$project")
  return 1
}

select_next_codex_account() {
  local project="$1" current_account="$2"
  local normalized_current candidate
  normalized_current="$(normalize_codex_account_name "$current_account")"
  while IFS= read -r candidate; do
    [[ -n "$candidate" ]] || continue
    if [[ -z "$normalized_current" || "$candidate" != "$normalized_current" ]]; then
      if ! codex_account_is_available_now "$project" "$candidate"; then
        continue
      fi
      printf '%s\n' "$candidate"
      return 0
    fi
  done < <(codex_saved_accounts "$project")
}

select_earliest_reset_codex_account() {
  local project="$1" current_account="$2"
  local normalized_current candidate reset_at best_account="" best_reset=""
  normalized_current="$(normalize_codex_account_name "$current_account")"
  while IFS= read -r candidate; do
    [[ -n "$candidate" ]] || continue
    if [[ -n "$normalized_current" && "$candidate" == "$normalized_current" ]]; then
      continue
    fi
    reset_at="$(codex_account_cooldown_reset_at "$project" "$candidate")"
    [[ -n "$reset_at" ]] || continue
    if [[ -z "$best_reset" || "$reset_at" -lt "$best_reset" ]]; then
      best_account="$candidate"
      best_reset="$reset_at"
    fi
  done < <(codex_saved_accounts "$project")
  if [[ -n "$best_account" ]]; then
    printf '%s|%s\n' "$best_account" "$best_reset"
  fi
}

select_any_available_codex_account() {
  local project="$1" candidate
  while IFS= read -r candidate; do
    [[ -n "$candidate" ]] || continue
    if codex_account_is_available_now "$project" "$candidate"; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done < <(codex_saved_accounts "$project")
}

watchdog_reset_buffer_seconds() {
  local buffer="${WATCHDOG_RESET_BUFFER_SECS:-60}"
  [[ "$buffer" =~ ^[0-9]+$ ]] || buffer=60
  printf '%s\n' "$buffer"
}

select_earliest_reset_codex_account_any() {
  local project="$1" candidate reset_at best_account="" best_reset=""
  while IFS= read -r candidate; do
    [[ -n "$candidate" ]] || continue
    reset_at="$(codex_account_cooldown_reset_at "$project" "$candidate")"
    [[ -n "$reset_at" ]] || continue
    if [[ -z "$best_reset" || "$reset_at" -lt "$best_reset" ]]; then
      best_account="$candidate"
      best_reset="$reset_at"
    fi
  done < <(codex_saved_accounts "$project")
  if [[ -n "$best_account" ]]; then
    printf '%s|%s\n' "$best_account" "$best_reset"
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
codex_probe_current_account_now() {
  local project="$1" prompt_file output_file rc timeout_secs="${CODEX_PROBE_TIMEOUT:-15}" probe_lock_held=0
  wait_for_codex_account_switch_idle "$project" || return 1
  codex_account_switch_probe_lock_acquire "watchdog_probe_current_account" || return 1
  probe_lock_held=1
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
    if ! kill -0 "$pid" 2>/dev/null; then
      break
    fi
    sleep 1
    ((slept++))
  done

  # Kill if still running
  if kill -0 "$pid" 2>/dev/null; then
    kill "$pid" 2>/dev/null
    wait "$pid" 2>/dev/null
    rm -f "$prompt_file" "$output_file"
    if [[ "$probe_lock_held" == "1" ]]; then
      codex_account_switch_probe_lock_release
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
    codex_account_switch_probe_lock_release
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

  # Generic error
  local error_msg
  error_msg="$(printf '%s' "$output" | head -1 | tr '\n' ' ' | cut -c1-50)"
  printf 'error:%s\n' "$error_msg"
  return 0
}

probe_any_usable_codex_account_now() {
  local project="$1" candidate probe_result reset_at
  while IFS= read -r candidate; do
    [[ -n "$candidate" ]] || continue
    switch_to_codex_account "$project" "$candidate" "probe_saved_accounts" >/dev/null || continue

    probe_result="$(codex_probe_current_account_now "$project")" || continue
    case "$probe_result" in
      usable)
      codex_clear_account_cooldown "$project" "$candidate"
      printf '%s\n' "$candidate"
      return 0
      ;;
      rate_limited:*)
        reset_at="${probe_result#rate_limited:}"
        codex_record_account_cooldown "$project" "$candidate" "$reset_at"
        ;;
    esac
  done < <(codex_saved_accounts "$project")
}

# Probe ALL saved accounts and update cooldown file
# Output format:
#   usable:<account>           - Found a usable account
#   earliest:<account>|<reset_at>  - All accounts rate limited, this is earliest available
#   none                       - No accounts saved or all failed without rate limit info
probe_all_codex_accounts_and_update_cooldown() {
  local project="$1"
  local candidate probe_result reset_at
  local usable_account=""
  local earliest_account="" earliest_reset=""
  local -a account_status=()
  local current_account

  current_account="$(codex_current_account "$project")"

  # Print header
  printf '\n%-30s  %-15s  %s\n' "Account" "Status" "Details" >&2
  printf '%s\n' "$(printf '%-30s  %-15s  %s' '' '' '' | tr ' ' '-')" >&2

  while IFS= read -r candidate; do
    [[ -n "$candidate" ]] || continue
    switch_to_codex_account "$project" "$candidate" "probe_all_accounts" >/dev/null || continue

    probe_result="$(codex_probe_current_account_now "$project")" || continue

    local status_line="" status_icon="" status_text="" details=""

    case "$probe_result" in
      usable)
        codex_clear_account_cooldown "$project" "$candidate"
        usable_account="$candidate"
        status_icon="✅"
        status_text="usable"
        details="ready to use"
        ;;
      rate_limited:*)
        reset_at="${probe_result#rate_limited:}"
        codex_record_account_cooldown "$project" "$candidate" "$reset_at"
        if [[ -z "$earliest_reset" || "$reset_at" -lt "$earliest_reset" ]]; then
          earliest_account="$candidate"
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

    # Mark current account
    local current_marker=""
    if [[ "$(normalize_codex_account_name "$candidate")" == "$(normalize_codex_account_name "$current_account")" ]]; then
      current_marker=" *"
    fi

    # Print status line
    printf '%s %-28s  %-15s  %s\n' "$status_icon" "$candidate$current_marker" "$status_text" "$details" >&2

    account_status+=("$candidate:$status_text")
  done < <(codex_saved_accounts "$project")

  printf '\n' >&2

  # Return results
  if [[ -n "$usable_account" ]]; then
    printf 'usable:%s\n' "$usable_account"
    return 0
  elif [[ -n "$earliest_account" ]]; then
    printf 'earliest:%s|%s\n' "$earliest_account" "$earliest_reset"
    return 0
  else
    printf 'none\n'
    return 1
  fi
}

switch_to_codex_account() {
  local project="$1" account="$2" reason="$3"
  local ai_bin output actual_account actual_slot requested_normalized actual_slot_normalized actual_account_normalized
  wait_for_codex_account_switch_idle "$project" || return 1
  ai_bin="$(ai_cli_bin_for_project "$project")"
  [[ -x "$ai_bin" && -n "$account" ]] || return 1
  output="$("$ai_bin" --quiet --format json switch codex "$account" --yes 2>/dev/null || true)"
  requested_normalized="$(normalize_codex_account_name "$account")"
  actual_account="$(codex_current_account "$project")"
  actual_slot="$(codex_current_slot "$project")"
  actual_slot_normalized="$(normalize_codex_account_name "$actual_slot")"
  actual_account_normalized="$(normalize_codex_account_name "$actual_account")"
  if printf '%s\n' "$output" | grep -qE '"switched": *true' && \
    { [[ -n "$actual_slot" && "$actual_slot_normalized" == "$requested_normalized" ]] || [[ -n "$actual_account" && "$actual_account_normalized" == "$requested_normalized" ]]; }; then
    # Only log if not a probe operation (probe logs are handled by caller)
    if [[ "$reason" != probe_all_accounts ]]; then
      log_warn "auto-switched codex account to $account (reason=$reason)" >&2
    fi
    printf '%s\n' "$account"
    return 0
  fi
  if [[ -n "$actual_account" ]]; then
    log_warn "codex account switch verification failed (requested=$account actual=$actual_account reason=$reason)" >&2
  fi
  return 1
}

switch_to_next_codex_account() {
  local project="$1" reason="$2"
  local current_account next_account
  current_account="$(codex_current_account "$project")"
  next_account="$(select_next_codex_account "$project" "$current_account")"
  [[ -n "$next_account" ]] || return 1
  switch_to_codex_account "$project" "$next_account" "$reason"
}

ensure_codex_account_ready_for_manager() {
  local project="$1"
  local current_account available_account probed_account earliest_info earliest_account earliest_reset wait_seconds wait_buffer
  local post_wait_probe_result post_wait_status post_wait_account post_wait_reset

  wait_for_codex_account_switch_idle "$project" || return 1
  current_account="$(codex_current_account "$project")"
  if [[ -n "$current_account" ]] && codex_account_is_available_now "$project" "$current_account"; then
    return 0
  fi

  available_account="$(select_any_available_codex_account "$project")"
  if [[ -n "$available_account" ]]; then
    if [[ -z "$current_account" || "$available_account" != "$(normalize_codex_account_name "$current_account")" ]]; then
      switch_to_codex_account "$project" "$available_account" "ensure_manager" >/dev/null
      write_manager_bootstrap_handoff "$project" "account_unavailable" "$current_account" "$available_account" "watchdog_switched_to_available_account" "inspect-fleet-and-recover-workers"
    fi
    return 0
  fi

  probed_account="$(probe_any_usable_codex_account_now "$project" || true)"
  if [[ -n "$probed_account" ]]; then
    write_manager_bootstrap_handoff "$project" "stale_or_missing_cooldown_probe" "$current_account" "$probed_account" "watchdog_probed_and_found_usable_account" "inspect-fleet-and-recover-workers"
    return 0
  fi

  earliest_info="$(select_earliest_reset_codex_account_any "$project")"
  earliest_account="${earliest_info%%|*}"
  earliest_reset="${earliest_info##*|}"
  if [[ -n "$earliest_account" && -n "$earliest_reset" && "$earliest_info" == *"|"* ]]; then
    if [[ -z "$current_account" || "$earliest_account" != "$(normalize_codex_account_name "$current_account")" ]]; then
      switch_to_codex_account "$project" "$earliest_account" "all_accounts_cooling_down" >/dev/null || true
    fi
    write_manager_bootstrap_handoff "$project" "all_accounts_cooling_down" "$current_account" "$earliest_account" "watchdog_waiting_for_earliest_reset" "recheck-account-availability-before-manager-bootstrap"
    wait_seconds="$(seconds_until_epoch "$earliest_reset")"
    wait_buffer="$(watchdog_reset_buffer_seconds)"
    if [[ "${wait_seconds:-0}" =~ ^[0-9]+$ ]]; then
      wait_seconds=$((wait_seconds + wait_buffer))
    fi
    if [[ "${wait_seconds:-0}" =~ ^[0-9]+$ ]] && (( wait_seconds > 0 )); then
      log_warn "all codex accounts cooling down before manager bootstrap; sleeping until reset_at=${earliest_reset} plus buffer=${wait_buffer}s (sleep=${wait_seconds}s)"
      sleep_with_rate_limit_recheck "$project" "$wait_seconds" 1
    fi
    post_wait_probe_result="$(probe_all_codex_accounts_and_update_cooldown "$project" || true)"
    post_wait_status="${post_wait_probe_result%%:*}"
    case "$post_wait_status" in
      usable)
        post_wait_account="${post_wait_probe_result#usable:}"
        if [[ -n "$post_wait_account" ]]; then
          if [[ -z "$current_account" || "$post_wait_account" != "$(normalize_codex_account_name "$current_account")" ]]; then
            switch_to_codex_account "$project" "$post_wait_account" "ensure_manager" >/dev/null || true
          fi
          write_manager_bootstrap_handoff "$project" "cooldown_elapsed" "$earliest_account" "$post_wait_account" "watchdog_resumed_after_wait" "inspect-fleet-and-recover-workers"
          return 0
        fi
        ;;
      earliest)
        post_wait_account="${post_wait_probe_result#earliest:}"
        post_wait_reset="${post_wait_account##*|}"
        post_wait_account="${post_wait_account%%|*}"
        if [[ -n "$post_wait_account" && -n "$post_wait_reset" ]]; then
          if [[ -z "$current_account" || "$post_wait_account" != "$(normalize_codex_account_name "$current_account")" ]]; then
            switch_to_codex_account "$project" "$post_wait_account" "all_accounts_cooling_down" >/dev/null || true
          fi
          write_manager_bootstrap_handoff "$project" "all_accounts_cooling_down" "$earliest_account" "$post_wait_account" "watchdog_still_waiting_after_probe" "recheck-account-availability-before-manager-bootstrap"
        fi
        ;;
    esac
  fi

  log_error "no codex account is currently available for manager bootstrap"
  return 1
}
