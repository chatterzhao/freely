#!/usr/bin/env bash

_tool_launchers_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"

freely_tool_launchers_repo_root() {
  local script_dir="$1" root
  root="$(git -C "$script_dir" rev-parse --show-toplevel 2>/dev/null || true)"
  if [[ -n "$root" ]]; then
    printf '%s\n' "$root"
    return 0
  fi
  case "$script_dir" in
    */docs/system/workspace/scripts/runtime)
      printf '%s\n' "${script_dir%/docs/system/workspace/scripts/runtime}"
      ;;
    *)
      printf '%s\n' "$script_dir"
      ;;
  esac
}

SELF_ROOT="$(freely_tool_launchers_repo_root "$_tool_launchers_dir")"

NETWORK_PROXY_RESOLVER_LIB="$SELF_ROOT/docs/system/workspace/scripts/runtime/network-proxy-resolver.sh"
[[ -f "$NETWORK_PROXY_RESOLVER_LIB" ]] || {
  echo "[ERROR] missing network proxy resolver module: $NETWORK_PROXY_RESOLVER_LIB" >&2
  return 1
}
# shellcheck disable=SC1090
source "$NETWORK_PROXY_RESOLVER_LIB"

codex_slot_switch_lock_dir_for_launch() {
  printf '%s\n' "${AI_CLI_SWITCH_LOCK_DIR:-$HOME/.codex/slot-switch.lock}"
}

codex_slot_switch_lock_state_file_for_launch() {
  printf '%s\n' "$(codex_slot_switch_lock_dir_for_launch)/state.env"
}

codex_slot_switch_lock_owner_pid_for_launch() {
  local state_file
  state_file="$(codex_slot_switch_lock_state_file_for_launch)"
  [[ -f "$state_file" ]] || return 0
  sed -n 's/^owner_pid=//p' "$state_file" | tail -n 1
}

codex_slot_switch_lock_cleanup_if_stale_for_launch() {
  local lock_dir owner_pid
  lock_dir="$(codex_slot_switch_lock_dir_for_launch)"
  [[ -d "$lock_dir" ]] || return 0
  owner_pid="$(codex_slot_switch_lock_owner_pid_for_launch)"
  if [[ -z "$owner_pid" ]] || ! kill -0 "$owner_pid" 2>/dev/null; then
    rm -rf "$lock_dir"
  fi
}

codex_slot_switch_in_progress_for_launch() {
  local lock_dir owner_pid inherited_owner_pid
  codex_slot_switch_lock_cleanup_if_stale_for_launch
  lock_dir="$(codex_slot_switch_lock_dir_for_launch)"
  [[ -d "$lock_dir" ]] || return 1
  owner_pid="$(codex_slot_switch_lock_owner_pid_for_launch)"
  inherited_owner_pid="${AI_CLI_SWITCH_LOCK_OWNER_PID:-}"
  [[ -n "$owner_pid" ]] || return 1
  [[ "$owner_pid" != "$$" ]] || return 1
  [[ -z "$inherited_owner_pid" || "$owner_pid" != "$inherited_owner_pid" ]] || return 1
  kill -0 "$owner_pid" 2>/dev/null
}

wait_for_codex_slot_switch_idle_before_launch() {
  local timeout_secs="${FREELY_ACCOUNT_SWITCH_WAIT_SECS:-60}"
  local interval_secs="${FREELY_ACCOUNT_SWITCH_WAIT_INTERVAL_SECS:-1}"
  local start_ts now owner_pid waiting_logged=0
  [[ "$timeout_secs" =~ ^[0-9]+$ ]] || timeout_secs=60
  [[ "$interval_secs" =~ ^[0-9]+$ ]] || interval_secs=1
  start_ts="$(date +%s)"

  while codex_slot_switch_in_progress_for_launch; do
    if [[ "$waiting_logged" == "0" ]]; then
      owner_pid="$(codex_slot_switch_lock_owner_pid_for_launch)"
      echo "[WARN] codex slot switch is already in progress (owner_pid=${owner_pid:-unknown}); waiting before codex launch" >&2
      waiting_logged=1
    fi
    now="$(date +%s)"
    if (( now - start_ts >= timeout_secs )); then
      echo "[ERROR] timed out waiting for codex slot switch to finish before codex launch" >&2
      return 1
    fi
    sleep "$interval_secs"
  done
}

tool_default_capabilities() {
  local tool="$1"
  case "$tool" in
    cc-use-codex-cli) printf 'codex-cli\n' ;;
    *) printf '\n' ;;
  esac
}

tool_default_policy() {
  local tool="$1"
  case "$tool" in
    cc-use-codex-cli) printf 'prefer-codex-for-repo-work\n' ;;
    *) printf '\n' ;;
  esac
}

tool_has_capability() {
  local capabilities="$1" capability="$2"
  [[ -n "$capability" ]] || return 1
  printf '%s\n' "$capabilities" | tr ',' '\n' | sed 's/^ *//; s/ *$//' | grep -Fxq "$capability"
}

tool_accepts_explicit_resume_target() {
  local tool="$1"
  case "$tool" in
    codex|iflow) return 0 ;;
    *) return 1 ;;
  esac
}

tool_requires_explicit_resume_target() {
  local tool="$1"
  case "$tool" in
    codex) return 0 ;;
    *) return 1 ;;
  esac
}

cc_codex_policy_prompt() {
  local policy="${1:-}"
  local project_root="${2:-}"
  local codex_model="${3:-gpt-5.4}"
  local codex_sandbox="${4:-workspace-write}"
  local codex_approval_policy="${5:-never}"
  local codex_cwd_mode="${6:-project-root}"
  cat <<EOF
Freely runtime policy:
- You are running as Claude Code inside Freely.
- If the codex-cli MCP tool is available, prefer using it for repository implementation, bug fixing, code review, and verification work.
- For new repository work, start a Codex MCP session instead of keeping the entire implementation inside Claude.
- For continuation of the same repository task, prefer continuing the existing Codex MCP thread when prior context already points to one.
- When calling the Codex MCP tool for a new session, pass these parameters unless the task explicitly requires something stricter:
  - model=${codex_model}
  - sandbox=${codex_sandbox}
  - approval-policy=${codex_approval_policy}
  - cwd=${project_root} (cwd policy: ${codex_cwd_mode})
- When continuing an existing Codex MCP thread, preserve the same repository-root cwd and the same non-interactive approval policy unless the task explicitly requires a stricter mode.
- The current runtime is non-interactive when permission mode is bypassPermissions; do not ask the user for confirmations that the runtime has already pre-approved.
- Current cc policy: ${policy:-default}
EOF
}

tool_run_from_prompt_file() {
  local project="$1"
  local tool="$2"
  local model="${3:-}"
  local reasoning_effort="${4:-}"
  local mode="$5"
  local prompt_file="$6"
  local launch_kind="$7"
  local tool_capabilities="${8:-}"
  local tool_policy="${9:-}"
  local codex_capability_model="${10:-gpt-5.4}"
  local codex_capability_sandbox="${11:-workspace-write}"
  local codex_capability_approval_policy="${12:-never}"
  local codex_capability_cwd_mode="${13:-project-root}"
  local debug_log_file="${14:-}"
  local claude_session_id="${15:-}"
  local tool_resume_target="${16:-}"

  case "$tool" in
    codex)
      wait_for_codex_slot_switch_idle_before_launch || return 1
      freely_apply_project_network_proxy_env "$project"
      local -a args=(exec --skip-git-repo-check -C "$project")
      if [[ "$launch_kind" == "resume" ]]; then
        [[ -n "$tool_resume_target" ]] || {
          echo "[ERROR] codex resume requires an explicit session target" >&2
          return 1
        }
        args=(exec resume "$tool_resume_target" --skip-git-repo-check)
      fi
      [[ -n "$model" ]] && args+=(-m "$model")
      [[ -n "$reasoning_effort" ]] && args+=(-c "model_reasoning_effort=\"$reasoning_effort\"")
      [[ "$mode" == "auto" ]] && args+=(--dangerously-bypass-approvals-and-sandbox)
      exec codex "${args[@]}" - <"$prompt_file"
      ;;
    iflow)
      local -a args=()
      [[ -n "$model" ]] && args+=(-m "$model")
      if [[ "$launch_kind" == "resume" ]]; then
        if [[ -n "$tool_resume_target" ]]; then
          args+=(-r "$tool_resume_target")
        else
          args+=(-c)
        fi
      fi
      if [[ "$mode" == "auto" ]]; then
        exec iflow "${args[@]}" -p "$(cat "$prompt_file")" -y --max-turns 100
      else
        exec iflow "${args[@]}" -p "$(cat "$prompt_file")" --default --max-turns 100
      fi
      ;;
    kiro-cli)
      local selected_model="${model:-auto}"
      if [[ "$launch_kind" == "resume" ]]; then
        if [[ "$mode" == "auto" ]]; then
          exec kiro-cli chat --resume --no-interactive --trust-all-tools --model "$selected_model" "继续上次未完成工作，按项目意图和宪法持续推进。"
        else
          exec kiro-cli chat --resume --model "$selected_model" "继续上次未完成工作，按项目意图和宪法持续推进。"
        fi
      fi

      if [[ "$mode" == "auto" ]]; then
        exec kiro-cli chat --no-interactive --trust-all-tools --model "$selected_model" <"$prompt_file"
      else
        exec kiro-cli chat --model "$selected_model" <"$prompt_file"
      fi
      ;;
    cc|cc-use-codex-cli)
      local prompt_text system_prompt
      local -a args=(-p)
      prompt_text="$(cat "$prompt_file")"
      if [[ "$mode" == "auto" ]]; then
        args+=(--permission-mode bypassPermissions)
      fi
      [[ -n "$debug_log_file" ]] && args+=(--debug-file "$debug_log_file")
      [[ -n "$claude_session_id" ]] && args+=(--session-id "$claude_session_id")
      [[ -n "$model" && "$model" != "default" ]] && args+=(--model "$model")
      [[ -n "$reasoning_effort" ]] && args+=(--effort "$reasoning_effort")
      if tool_has_capability "$tool_capabilities" "codex-cli"; then
        system_prompt="$(cc_codex_policy_prompt "$tool_policy" "$project" "$codex_capability_model" "$codex_capability_sandbox" "$codex_capability_approval_policy" "$codex_capability_cwd_mode")"
        args+=(--append-system-prompt "$system_prompt")
      fi
      exec claude "${args[@]}" "$prompt_text"
      ;;
    test-sleep)
      exec bash -lc 'echo "[TEST] mock AI CLI started"; sleep 5'
      ;;
    test-compact)
      exec bash -lc 'echo "[TEST] mock AI CLI started"; echo "context compacted"; sleep 1'
      ;;
    test-once)
      exec bash -lc 'echo "[TEST] mock AI CLI started"; sleep 1'
      ;;
    test-session)
      exec bash -lc 'echo "session id: test-session"; echo "[TEST] mock AI CLI started"; sleep 1'
      ;;
    test-route-only)
      exec bash -lc "cat <<'EOF'
[TEST] mock AI CLI started
selected_tool = test-route-only
target_skill_or_loop = workspace/skills/doc-ibm-execution/SKILL.md
\`next_prompt\`：
```text
你现在承接第二跳，直接进入 workspace/skills/doc-ibm-execution/SKILL.md 并修改真实文档产物。
```
EOF
sleep 1"
      ;;
    *)
      echo "[ERROR] unsupported tool: $tool" >&2
      return 1
      ;;
  esac
}
