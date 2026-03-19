# shellcheck shell=bash

normalize_codex_account_name() {
  printf '%s' "$1" | sed 's/\./-/g'
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
  local file tmp normalized
  [[ -n "$account" && -n "$reset_at" ]] || return 0
  normalized="$(normalize_codex_account_name "$account")"
  file="$(codex_account_cooldown_file "$project")"
  mkdir -p "$(dirname "$file")"
  tmp="${file}.tmp"
  {
    if [[ -f "$file" ]]; then
      awk -F '\t' -v account="$normalized" '$1 != account {print $1 "\t" $2}' "$file"
    fi
    printf '%s\t%s\n' "$normalized" "$reset_at"
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
  awk -F '\t' -v account="$normalized" '$1 != account {print $1 "\t" $2}' "$file" >"$tmp"
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

codex_probe_current_account_now() {
  local project="$1" prompt_file output_file rc
  prompt_file="$(mktemp)"
  output_file="$(mktemp)"
  printf 'Reply with exactly: OK\n' >"$prompt_file"
  rc=0
  (
    cd "$project"
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
  ) >"$output_file" 2>&1 || rc=$?
  rm -f "$prompt_file"
  if [[ "$rc" -eq 0 ]] && rg -q '^OK$' "$output_file"; then
    rm -f "$output_file"
    return 0
  fi
  rm -f "$output_file"
  return 1
}

probe_any_usable_codex_account_now() {
  local project="$1" candidate
  while IFS= read -r candidate; do
    [[ -n "$candidate" ]] || continue
    switch_to_codex_account "$project" "$candidate" "probe_saved_accounts" >/dev/null || continue
    if codex_probe_current_account_now "$project"; then
      codex_clear_account_cooldown "$project" "$candidate"
      printf '%s\n' "$candidate"
      return 0
    fi
  done < <(codex_saved_accounts "$project")
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
