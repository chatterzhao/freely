# shellcheck shell=bash

normalize_codex_account_name() {
  printf '%s' "$1" | sed 's/\./-/g'
}

# Parse "Mar 23rd, 2026 3:51 PM" format to Unix timestamp
parse_try_again_time() {
  local date_str="$1"
  [[ -n "$date_str" ]] || return 1
  python3 -c "
import re
from datetime import datetime
import sys

date_str = sys.argv[1]
# Remove ordinal suffixes (st, nd, rd, th)
cleaned = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)
try:
    dt = datetime.strptime(cleaned, '%b %d, %Y %I:%M %p')
    print(int(dt.timestamp()))
except Exception:
    sys.exit(1)
" "$date_str" 2>/dev/null
}

# Extract "try again at ..." time from codex output
# Returns Unix timestamp, or empty if not found
extract_try_again_time_from_output() {
  local output="$1"
  local try_again_str
  # Match: try again at Mar 23rd, 2026 3:51 PM.
  try_again_str="$(printf '%s\n' "$output" | grep -oiE 'try again at [^.]+\.' | sed 's/try again at //i' | sed 's/\.$//' | head -1)"
  [[ -n "$try_again_str" ]] || return 1
  parse_try_again_time "$try_again_str"
}

codex_current_account() {
  local project="$1" ai_bin output
  ai_bin="$(ai_cli_bin_for_project "$project")"
  [[ -x "$ai_bin" ]] || return 0
  output="$("$ai_bin" --quiet --format json whoami codex 2>/dev/null || true)"
  printf '%s\n' "$output" | sed -n 's/.*"account": *"\([^"]*\)".*/\1/p' | tail -n 1
}

codex_saved_accounts() {
  local project="$1" ai_bin output
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

# Probe current codex account with proxy support and timeout
# Returns:
#   0 + stdout empty: success, account is usable
#   0 + stdout non-empty: rate limited, stdout contains reset_at timestamp
#   1: other error (timeout, network, etc.)
codex_probe_current_account_now() {
  local project="$1" prompt_file output_file rc timeout_secs="${CODEX_PROBE_TIMEOUT:-15}"
  prompt_file="$(mktemp)"
  output_file="$(mktemp)"
  printf 'Reply with exactly: OK\n' >"$prompt_file"
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
    return 1  # Timeout
  fi

  wait "$pid" 2>/dev/null || rc=$?
  rm -f "$prompt_file"

  local output
  output="$(cat "$output_file")"
  rm -f "$output_file"

  # Check for success
  if [[ "$rc" -eq 0 ]] && printf '%s\n' "$output" | rg -q '^OK$'; then
    return 0
  fi

  # Check for rate limit
  if printf '%s\n' "$output" | grep -qi "usage limit\|try again"; then
    local reset_at
    reset_at="$(extract_try_again_time_from_output "$output")"
    if [[ -n "$reset_at" ]]; then
      printf '%s\n' "$reset_at"
    fi
    return 0  # Return 0 to signal we have rate limit info
  fi

  return 1  # Other error
}

probe_any_usable_codex_account_now() {
  local project="$1" candidate reset_at
  while IFS= read -r candidate; do
    [[ -n "$candidate" ]] || continue
    switch_to_codex_account "$project" "$candidate" "probe_saved_accounts" >/dev/null || continue

    reset_at="$(codex_probe_current_account_now "$project")"
    local probe_rc=$?

    if [[ $probe_rc -eq 0 && -z "$reset_at" ]]; then
      # Success: account is usable
      codex_clear_account_cooldown "$project" "$candidate"
      printf '%s\n' "$candidate"
      return 0
    elif [[ -n "$reset_at" ]]; then
      # Rate limited: record cooldown
      codex_record_account_cooldown "$project" "$candidate" "$reset_at"
    fi
  done < <(codex_saved_accounts "$project")
}

# Probe ALL saved accounts and update cooldown file
# Output format:
#   usable:<account>           - Found a usable account
#   earliest:<account>|<reset_at>  - All accounts rate limited, this is earliest available
#   none                       - No accounts saved or all failed without rate limit info
probe_all_codex_accounts_and_update_cooldown() {
  local project="$1"
  local candidate reset_at probe_rc
  local usable_account=""
  local earliest_account="" earliest_reset=""

  while IFS= read -r candidate; do
    [[ -n "$candidate" ]] || continue
    switch_to_codex_account "$project" "$candidate" "probe_all_accounts" >/dev/null || continue

    reset_at="$(codex_probe_current_account_now "$project")"
    probe_rc=$?

    if [[ $probe_rc -eq 0 && -z "$reset_at" ]]; then
      # Success: account is usable
      codex_clear_account_cooldown "$project" "$candidate"
      usable_account="$candidate"
      # Don't return immediately - continue probing to update all cooldowns
    elif [[ -n "$reset_at" ]]; then
      # Rate limited: record cooldown
      codex_record_account_cooldown "$project" "$candidate" "$reset_at"
      # Track earliest available
      if [[ -z "$earliest_reset" || "$reset_at" -lt "$earliest_reset" ]]; then
        earliest_account="$candidate"
        earliest_reset="$reset_at"
      fi
    fi
  done < <(codex_saved_accounts "$project")

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
  local ai_bin output actual_account requested_normalized actual_normalized
  ai_bin="$(ai_cli_bin_for_project "$project")"
  [[ -x "$ai_bin" && -n "$account" ]] || return 1
  output="$("$ai_bin" --quiet --format json switch codex "$account" --yes 2>/dev/null || true)"
  requested_normalized="$(normalize_codex_account_name "$account")"
  actual_account="$(codex_current_account "$project")"
  actual_normalized="$(normalize_codex_account_name "$actual_account")"
  if printf '%s\n' "$output" | rg -q '"switched": *true' && [[ -n "$actual_account" && "$actual_normalized" == "$requested_normalized" ]]; then
    log_warn "auto-switched codex account to $account (reason=$reason)" >&2
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
  local current_account available_account probed_account earliest_info earliest_account earliest_reset wait_seconds

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
    if [[ "${wait_seconds:-0}" =~ ^[0-9]+$ ]] && (( wait_seconds > 0 )); then
      log_warn "all codex accounts cooling down before manager bootstrap; sleeping until reset_at=${earliest_reset} (sleep=${wait_seconds}s)"
      sleep_with_rate_limit_recheck "$project" "$wait_seconds"
    fi
    available_account="$(select_any_available_codex_account "$project")"
    if [[ -n "$available_account" ]]; then
      if [[ -z "$current_account" || "$available_account" != "$(normalize_codex_account_name "$current_account")" ]]; then
        switch_to_codex_account "$project" "$available_account" "ensure_manager" >/dev/null || true
      fi
      write_manager_bootstrap_handoff "$project" "cooldown_elapsed" "$earliest_account" "$available_account" "watchdog_resumed_after_wait" "inspect-fleet-and-recover-workers"
      return 0
    fi
  fi

  log_error "no codex account is currently available for manager bootstrap"
  return 1
}
