#!/usr/bin/env bash
set -euo pipefail

SCRIPT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
# shellcheck disable=SC1091
source "$SCRIPT_ROOT/runtime/tool-launchers.sh"

usage() {
  cat <<'EOF'
Usage:
  monitor-ai-cli.sh \
    --project <abs_path> \
    --tool <tool> \
    --tool-adapter <adapter> \
    --model <model_or_empty> \
    --reasoning-effort <effort_or_empty> \
    --tool-capabilities <csv_or_empty> \
    --tool-policy <policy_or_empty> \
    --codex-capability-model <model_or_empty> \
    --codex-capability-sandbox <sandbox_or_empty> \
    --codex-capability-approval-policy <approval_or_empty> \
    --codex-capability-cwd-mode <cwd_mode_or_empty> \
    --debug-log-file <abs_file_or_empty> \
    --claude-session-id <uuid_or_empty> \
    --tool-resume-target <tool_specific_resume_target_or_empty> \
    --mode <auto|step> \
    --prompt-file <abs_file> \
    --pid-file <abs_file> \
    --log-file <abs_file> \
    --failure-marker-file <abs_file_or_empty> \
    --launch-kind <fresh|resume|fresh_with_handoff>
EOF
}

preflight_error() {
  local message="$1"
  [[ -n "$log_file" ]] && printf '%s\n' "$message" >>"$log_file"
  printf '%s\n' "$message" >&2
  exit 1
}

abs_path_or_fail() {
  local p="$1"
  [[ "$p" == /* ]] || {
    echo "[ERROR] path must be absolute: $p" >&2
    exit 1
  }
  echo "$p"
}

workcell_state_file_for_project() {
  local current_project="$1"
  printf '%s\n' "$current_project/.freely/run/workcell-state.env"
}

session_state_file_for_project() {
  local current_project="$1"
  printf '%s\n' "$current_project/.freely/run/session-state.env"
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

extract_tool_session_id_from_log_if_present() {
  local current_tool="$1" current_log_file="$2"
  [[ -f "$current_log_file" ]] || return 0
  case "$current_tool" in
    codex)
      sed -n 's/^session id: //p' "$current_log_file" | head -n 1
      ;;
    test-session)
      sed -n 's/^session id: //p' "$current_log_file" | head -n 1
      ;;
    opencode)
      sed -n 's/.*service=session id=\(ses_[A-Za-z0-9_]*\).*/\1/p' "$current_log_file" | head -n 1
      ;;
    cc|cc-use-codex-cli|claude|codex|opencode)
      # Delegate to session-cache module; fall back to inline extraction.
      if declare -f session_extract_id_from_log >/dev/null 2>&1; then
        session_extract_id_from_log "$current_tool" "$current_log_file"
      else
        local claude_debug_log="${current_log_file%.log}.debug.log"
        local session_id
        session_id="$(sed -n 's/.*session[._]id[=:]\s*\([a-f0-9]\{8\}-[a-f0-9]\{4\}-[a-f0-9]\{4\}-[a-f0-9]\{4\}-[a-f0-9]\{12\}\).*/\1/p' "$claude_debug_log" 2>/dev/null | head -n 1)"
        [[ -z "$session_id" ]] && session_id="$(sed -n 's/.*session[._]id[=:]\s*\([a-f0-9]\{8\}-[a-f0-9]\{4\}-[a-f0-9]\{4\}-[a-f0-9]\{4\}-[a-f0-9]\{12\}\).*/\1/p' "$current_log_file" 2>/dev/null | head -n 1)"
        printf '%s\n' "$session_id"
      fi
      ;;
    *)
      ;;
  esac
}

find_codex_jsonl_path_for_session_if_present() {
  local session_id="$1"
  local sessions_root
  [[ -n "$session_id" ]] || return 0
  sessions_root="${CODEX_HOME:-$HOME/.codex}/sessions"
  [[ -d "$sessions_root" ]] || return 0
  find "$sessions_root" -type f -name "*${session_id}.jsonl" | sort | tail -n 1
}

write_live_session_state_if_possible() {
  local current_project="$1" current_tool="$2" current_log_file="$3" current_prompt_file="$4" current_launch_kind="$5"
  local session_state_file tmp_file tool_session_id tool_resume_target tool_jsonl_path
  local last_launch_kind last_rotation_reason last_cycle_log last_prompt_file
  local last_context_compacted last_context_ratio last_primary_rate_limit_used_percent last_primary_rate_limit_resets_at
  local last_secondary_rate_limit_used_percent last_secondary_rate_limit_resets_at last_route_only_handoff
  local current_tool_slot last_active_slot last_slot_switch_reason last_slot_switch_at last_cycle_debug_log
  local last_claude_jsonl_path last_codex_mcp_used last_codex_mcp_thread_id last_codex_mcp_jsonl_path
  local claude_session_id_current_state claude_session_id_previous_state last_project_dirty_entries
  local last_worktree_summary_total last_worktree_summary_dirty last_delegated_pending_ids
  local last_delegated_pending_count last_delegated_consumed_ids last_delegated_consumed_at
  local last_restart_storm_window_secs last_restart_storm_count last_process_churn_peak
  local last_restart_storm_signal_at last_restart_storm_signal_reason last_restart_storm_escalated_at
  local last_restart_storm_escalation_target auto_recovery_attempted_tools_csv auto_recovery_origin_tool
  local checkpoint_drift_streak route_only_streak resume_streak

  session_state_file="$(session_state_file_for_project "$current_project")"
  mkdir -p "$(dirname "$session_state_file")"

  tool_session_id=""
  tool_resume_target=""
  tool_jsonl_path=""
  last_launch_kind=""
  last_rotation_reason=""
  last_cycle_log=""
  last_prompt_file=""
  last_context_compacted="0"
  last_context_ratio=""
  last_primary_rate_limit_used_percent=""
  last_primary_rate_limit_resets_at=""
  last_secondary_rate_limit_used_percent=""
  last_secondary_rate_limit_resets_at=""
  last_route_only_handoff="0"
  current_tool_slot=""
  last_active_slot=""
  last_slot_switch_reason=""
  last_slot_switch_at=""
  last_cycle_debug_log=""
  last_claude_jsonl_path=""
  last_codex_mcp_used="0"
  last_codex_mcp_thread_id=""
  last_codex_mcp_jsonl_path=""
  claude_session_id_current_state=""
  claude_session_id_previous_state=""
  last_project_dirty_entries="0"
  last_worktree_summary_total="0"
  last_worktree_summary_dirty="0"
  last_delegated_pending_ids=""
  last_delegated_pending_count="0"
  last_delegated_consumed_ids=""
  last_delegated_consumed_at=""
  last_restart_storm_window_secs="0"
  last_restart_storm_count="0"
  last_process_churn_peak="0"
  last_restart_storm_signal_at=""
  last_restart_storm_signal_reason=""
  last_restart_storm_escalated_at=""
  last_restart_storm_escalation_target=""
  auto_recovery_attempted_tools_csv=""
  auto_recovery_origin_tool=""
  checkpoint_drift_streak="0"
  route_only_streak="0"
  resume_streak="0"

  if [[ -f "$session_state_file" ]]; then
    unset LAST_TOOL_SESSION_ID LAST_TOOL_RESUME_TARGET LAST_TOOL_JSONL_PATH LAST_LAUNCH_KIND LAST_ROTATION_REASON LAST_CYCLE_LOG LAST_PROMPT_FILE LAST_CONTEXT_COMPACTED LAST_CONTEXT_RATIO LAST_PRIMARY_RATE_LIMIT_USED_PERCENT LAST_PRIMARY_RATE_LIMIT_RESETS_AT LAST_SECONDARY_RATE_LIMIT_USED_PERCENT LAST_SECONDARY_RATE_LIMIT_RESETS_AT LAST_ROUTE_ONLY_HANDOFF CURRENT_TOOL_SLOT LAST_ACTIVE_SLOT LAST_SLOT_SWITCH_REASON LAST_SLOT_SWITCH_AT LAST_CYCLE_DEBUG_LOG LAST_CLAUDE_JSONL_PATH LAST_CODEX_MCP_USED LAST_CODEX_MCP_THREAD_ID LAST_CODEX_MCP_JSONL_PATH TOOL_SESSION_ID_CURRENT TOOL_SESSION_ID_PREVIOUS SESSION_PARENT_ID LAST_PROJECT_DIRTY_ENTRIES LAST_WORKTREE_SUMMARY_TOTAL LAST_WORKTREE_SUMMARY_DIRTY LAST_DELEGATED_CONTINUATION_PENDING_IDS LAST_DELEGATED_CONTINUATION_PENDING_COUNT LAST_DELEGATED_CONTINUATION_CONSUMED_IDS LAST_DELEGATED_CONTINUATION_CONSUMED_AT LAST_RESTART_STORM_WINDOW_SECS LAST_RESTART_STORM_COUNT LAST_PROCESS_CHURN_PEAK LAST_RESTART_STORM_SIGNAL_AT LAST_RESTART_STORM_SIGNAL_REASON LAST_RESTART_STORM_ESCALATED_AT LAST_RESTART_STORM_ESCALATION_TARGET AUTO_RECOVERY_ATTEMPTED_TOOLS_CSV AUTO_RECOVERY_ORIGIN_TOOL CHECKPOINT_DRIFT_STREAK_CURRENT ROUTE_ONLY_STREAK_CURRENT RESUME_STREAK_CURRENT
    # shellcheck disable=SC1090
    source "$session_state_file"
    tool_session_id="${LAST_TOOL_SESSION_ID:-}"
    tool_resume_target="${LAST_TOOL_RESUME_TARGET:-}"
    tool_jsonl_path="${LAST_TOOL_JSONL_PATH:-}"
    last_launch_kind="${LAST_LAUNCH_KIND:-}"
    last_rotation_reason="${LAST_ROTATION_REASON:-}"
    last_cycle_log="${LAST_CYCLE_LOG:-}"
    last_prompt_file="${LAST_PROMPT_FILE:-}"
    last_context_compacted="${LAST_CONTEXT_COMPACTED:-0}"
    last_context_ratio="${LAST_CONTEXT_RATIO:-}"
    last_primary_rate_limit_used_percent="${LAST_PRIMARY_RATE_LIMIT_USED_PERCENT:-}"
    last_primary_rate_limit_resets_at="${LAST_PRIMARY_RATE_LIMIT_RESETS_AT:-}"
    last_secondary_rate_limit_used_percent="${LAST_SECONDARY_RATE_LIMIT_USED_PERCENT:-}"
    last_secondary_rate_limit_resets_at="${LAST_SECONDARY_RATE_LIMIT_RESETS_AT:-}"
    last_route_only_handoff="${LAST_ROUTE_ONLY_HANDOFF:-0}"
    current_tool_slot="${CURRENT_TOOL_SLOT:-}"
    last_active_slot="${LAST_ACTIVE_SLOT:-}"
    last_slot_switch_reason="${LAST_SLOT_SWITCH_REASON:-}"
    last_slot_switch_at="${LAST_SLOT_SWITCH_AT:-}"
    last_cycle_debug_log="${LAST_CYCLE_DEBUG_LOG:-}"
    last_claude_jsonl_path="${LAST_CLAUDE_JSONL_PATH:-}"
    last_codex_mcp_used="${LAST_CODEX_MCP_USED:-0}"
    last_codex_mcp_thread_id="${LAST_CODEX_MCP_THREAD_ID:-}"
    last_codex_mcp_jsonl_path="${LAST_CODEX_MCP_JSONL_PATH:-}"
    claude_session_id_current_state="${TOOL_SESSION_ID_CURRENT:-}"
    claude_session_id_previous_state="${TOOL_SESSION_ID_PREVIOUS:-}"
    last_project_dirty_entries="${LAST_PROJECT_DIRTY_ENTRIES:-0}"
    last_worktree_summary_total="${LAST_WORKTREE_SUMMARY_TOTAL:-0}"
    last_worktree_summary_dirty="${LAST_WORKTREE_SUMMARY_DIRTY:-0}"
    last_delegated_pending_ids="${LAST_DELEGATED_CONTINUATION_PENDING_IDS:-}"
    last_delegated_pending_count="${LAST_DELEGATED_CONTINUATION_PENDING_COUNT:-0}"
    last_delegated_consumed_ids="${LAST_DELEGATED_CONTINUATION_CONSUMED_IDS:-}"
    last_delegated_consumed_at="${LAST_DELEGATED_CONTINUATION_CONSUMED_AT:-}"
    last_restart_storm_window_secs="${LAST_RESTART_STORM_WINDOW_SECS:-0}"
    last_restart_storm_count="${LAST_RESTART_STORM_COUNT:-0}"
    last_process_churn_peak="${LAST_PROCESS_CHURN_PEAK:-0}"
    last_restart_storm_signal_at="${LAST_RESTART_STORM_SIGNAL_AT:-}"
    last_restart_storm_signal_reason="${LAST_RESTART_STORM_SIGNAL_REASON:-}"
    last_restart_storm_escalated_at="${LAST_RESTART_STORM_ESCALATED_AT:-}"
    last_restart_storm_escalation_target="${LAST_RESTART_STORM_ESCALATION_TARGET:-}"
    auto_recovery_attempted_tools_csv="${AUTO_RECOVERY_ATTEMPTED_TOOLS_CSV:-}"
    auto_recovery_origin_tool="${AUTO_RECOVERY_ORIGIN_TOOL:-}"
    checkpoint_drift_streak="${CHECKPOINT_DRIFT_STREAK_CURRENT:-0}"
    route_only_streak="${ROUTE_ONLY_STREAK_CURRENT:-0}"
    resume_streak="${RESUME_STREAK_CURRENT:-0}"
  fi

  if [[ -z "$tool_session_id" ]]; then
    tool_session_id="$(extract_tool_session_id_from_log_if_present "$current_tool" "$current_log_file")"
  fi
  if [[ "$current_tool" == "codex" && -n "$tool_session_id" && -z "$tool_jsonl_path" ]]; then
    tool_jsonl_path="$(find_codex_jsonl_path_for_session_if_present "$tool_session_id")"
  fi
  if [[ -z "$tool_resume_target" && -n "$tool_session_id" ]]; then
    tool_resume_target="$tool_session_id"
  fi
  # Fallback: TOOL_SESSION_ID_CURRENT from _persist_session_anchor_early
  if [[ -z "$tool_resume_target" && -n "${TOOL_SESSION_ID_CURRENT:-}" ]]; then
    tool_resume_target="${TOOL_SESSION_ID_CURRENT:-}"
  fi

  [[ -n "$tool_session_id" || -n "$tool_resume_target" || -n "$tool_jsonl_path" ]] || return 0

  tmp_file="$(mktemp "${session_state_file}.tmp.XXXXXX")"
  cat >"$tmp_file" <<EOF
LAST_TOOL_SESSION_ID="$tool_session_id"
LAST_TOOL_RESUME_TARGET="$tool_resume_target"
LAST_TOOL_JSONL_PATH="$tool_jsonl_path"
LAST_LAUNCH_KIND="${last_launch_kind:-$current_launch_kind}"
LAST_ROTATION_REASON="$last_rotation_reason"
LAST_CYCLE_LOG="${last_cycle_log:-$current_log_file}"
LAST_PROMPT_FILE="${last_prompt_file:-$current_prompt_file}"
LAST_CONTEXT_COMPACTED="$last_context_compacted"
LAST_CONTEXT_RATIO="$last_context_ratio"
LAST_PRIMARY_RATE_LIMIT_USED_PERCENT="$last_primary_rate_limit_used_percent"
LAST_PRIMARY_RATE_LIMIT_RESETS_AT="$last_primary_rate_limit_resets_at"
LAST_SECONDARY_RATE_LIMIT_USED_PERCENT="$last_secondary_rate_limit_used_percent"
LAST_SECONDARY_RATE_LIMIT_RESETS_AT="$last_secondary_rate_limit_resets_at"
LAST_ROUTE_ONLY_HANDOFF="$last_route_only_handoff"
CURRENT_TOOL_SLOT="$current_tool_slot"
LAST_ACTIVE_SLOT="$last_active_slot"
LAST_SLOT_SWITCH_REASON="$last_slot_switch_reason"
LAST_SLOT_SWITCH_AT="$last_slot_switch_at"
LAST_CYCLE_DEBUG_LOG="$last_cycle_debug_log"
LAST_CLAUDE_JSONL_PATH="$last_claude_jsonl_path"
LAST_CODEX_MCP_USED="$last_codex_mcp_used"
LAST_CODEX_MCP_THREAD_ID="$last_codex_mcp_thread_id"
LAST_CODEX_MCP_JSONL_PATH="$last_codex_mcp_jsonl_path"
# Protect: never overwrite valid UUID with empty.
# _persist_session_anchor_early writes this before launch.
if [[ -n "${claude_session_id_current_state:-}" ]]; then
  TOOL_SESSION_ID_CURRENT="$claude_session_id_current_state"
fi
TOOL_SESSION_ID_PREVIOUS="$claude_session_id_previous_state"
SESSION_PARENT_ID="${SESSION_PARENT_ID:-${TOOL_SESSION_ID_CURRENT:-}}"
LAST_PROJECT_DIRTY_ENTRIES="$last_project_dirty_entries"
LAST_WORKTREE_SUMMARY_TOTAL="$last_worktree_summary_total"
LAST_WORKTREE_SUMMARY_DIRTY="$last_worktree_summary_dirty"
LAST_DELEGATED_CONTINUATION_PENDING_IDS="$last_delegated_pending_ids"
LAST_DELEGATED_CONTINUATION_PENDING_COUNT="$last_delegated_pending_count"
LAST_DELEGATED_CONTINUATION_CONSUMED_IDS="$last_delegated_consumed_ids"
LAST_DELEGATED_CONTINUATION_CONSUMED_AT="$last_delegated_consumed_at"
LAST_RESTART_STORM_WINDOW_SECS="$last_restart_storm_window_secs"
LAST_RESTART_STORM_COUNT="$last_restart_storm_count"
LAST_PROCESS_CHURN_PEAK="$last_process_churn_peak"
LAST_RESTART_STORM_SIGNAL_AT="$last_restart_storm_signal_at"
LAST_RESTART_STORM_SIGNAL_REASON="$last_restart_storm_signal_reason"
LAST_RESTART_STORM_ESCALATED_AT="$last_restart_storm_escalated_at"
LAST_RESTART_STORM_ESCALATION_TARGET="$last_restart_storm_escalation_target"
AUTO_RECOVERY_ATTEMPTED_TOOLS_CSV="$auto_recovery_attempted_tools_csv"
AUTO_RECOVERY_ORIGIN_TOOL="$auto_recovery_origin_tool"
CHECKPOINT_DRIFT_STREAK_CURRENT="$checkpoint_drift_streak"
ROUTE_ONLY_STREAK_CURRENT="$route_only_streak"
RESUME_STREAK_CURRENT="$resume_streak"
EOF
  mv "$tmp_file" "$session_state_file"
}

write_workcell_launch_state_if_possible() {
  # workcell-state.env: daemon runtime fields only (7 fields).
  # Closeout context removed — read directly from worker-verification-contract.env.
  state_file="$(workcell_state_file_for_project "$current_project")"
  mkdir -p "$(dirname "$state_file")"

  desired_state="running"
  supervisor_state="up"
  exit_reason="starting"
  role_hint="worker"
  entrypoint_mode="foreground"

  if [[ -f "$state_file" ]]; then
    desired_state="$(meta_env_value "$state_file" "DESIRED_RUNTIME_STATE")"
    desired_state="${desired_state:-running}"
    supervisor_state="$(meta_env_value "$state_file" "LAST_SUPERVISOR_STATE")"
    supervisor_state="${supervisor_state:-up}"
    entrypoint_mode="$(meta_env_value "$state_file" "LAST_ENTRYPOINT_MODE")"
    entrypoint_mode="${entrypoint_mode:-foreground}"
    role_hint="$(meta_env_value "$state_file" "LAST_ROLE_HINT")"
    role_hint="${role_hint:-worker}"
  fi

  updated_at="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  tmp_file="$(mktemp "${state_file}.tmp.XXXXXX")"
  cat >"$tmp_file" <<ENDOFSTATE
DESIRED_RUNTIME_STATE="${desired_state:-running}"
LAST_SUPERVISOR_STATE="${supervisor_state:-up}"
LAST_AI_STATE="up"
LAST_EXIT_REASON="ai_launch_in_flight"
LAST_ENTRYPOINT_MODE="${entrypoint_mode:-foreground}"
LAST_ROLE_HINT="${role_hint:-worker}"
LAST_STATE_UPDATED_AT="$updated_at"
ENDOFSTATE
  mv "$tmp_file" "$state_file"
}

project=""
tool=""
tool_adapter=""
model=""
reasoning_effort=""
mode=""
prompt_file=""
pid_file=""
log_file=""
launch_kind=""
tool_capabilities=""
tool_policy=""
codex_capability_model=""
codex_capability_sandbox=""
codex_capability_approval_policy=""
codex_capability_cwd_mode=""
debug_log_file=""
claude_session_id=""
tool_resume_target=""
network_failure_marker_file=""
failure_marker_file=""

runtime_error_signal_excerpt() {
  local current_log_file="$1" current_debug_log_file="${2:-}" current_prompt_file="${3:-}"
  local -a existing_files=()
  [[ -f "$current_log_file" ]] && existing_files+=("$current_log_file")
  [[ -f "$current_debug_log_file" ]] && existing_files+=("$current_debug_log_file")
  [[ ${#existing_files[@]} -gt 0 ]] || return 1
  awk -v prompt_file="$current_prompt_file" '
    BEGIN {
      prompt_line_count = 0
      if (prompt_file != "" && (getline line < prompt_file) > 0) {
        prompt[++prompt_line_count] = line
        while ((getline line < prompt_file) > 0) {
          prompt[++prompt_line_count] = line
        }
        close(prompt_file)
      }
      skipping_prompt = 0
      prompt_index = 0
      current_file = ""
    }
    function emit_if_match(line) {
      if (line ~ /^[0-9]{4}-[0-9]{2}-[0-9]{2}T.* (ERROR|WARN) /) { print line; return }
      if (line ~ /^[0-9]{4}-[0-9]{2}-[0-9]{2}T.* \[(ERROR|WARN)\]/) { print line; return }
      if (line ~ /^(ERROR|WARN)(:| |$)/) { print line; return }
      if (line ~ /^Error:/) { print line; return }
      if (line ~ /^\[(ERROR|WARN)\]/) { print line; return }
      if (line ~ /^(Please log in|Login required|Unauthorized|deactivated_workspace|workspace deactivated)/) { print line; return }
      if (line ~ /^OAuth inventory refresh failed/) { print line; return }
      if (line ~ /^FREELY_NETWORK_PROXY_MODE=explicit but no proxy values are set/) { print line; return }
      if (line ~ /^curl: \([0-9]+\)/) { print line; return }
      if (line ~ /^Attempt [0-9]+ failed\./) { print line; return }
      if (line ~ /(Failed to create session:|cannot access session files|thread\/start failed|permission denied)/) { print line; return }
    }
    {
      line = $0
      if (FILENAME != current_file) {
        current_file = FILENAME
        skipping_prompt = 0
        prompt_index = 0
      }
      if (prompt_line_count > 0) {
        if (!skipping_prompt && line == "user") {
          skipping_prompt = 1
          prompt_index = 1
          next
        }
        if (skipping_prompt) {
          if (prompt_index <= prompt_line_count && line == prompt[prompt_index]) {
            prompt_index++
            if (prompt_index > prompt_line_count) {
              skipping_prompt = 0
            }
            next
          }
          skipping_prompt = 0
        }
      }
      emit_if_match(line)
    }
  ' "${existing_files[@]}" 2>/dev/null
}

filter_known_benign_runtime_error_noise() {
  local current_tool="$1"
  if [[ "$current_tool" == "codex" ]]; then
    if [[ "$(codex_live_auth_kind)" == "apikey" ]]; then
      sed \
        -e '/failed to refresh available models: timeout waiting for child process to exit/d' \
        -e '/codex_login::auth::manager: Failed to refresh token: 401 Unauthorized/d'
      return 0
    fi
    sed '/failed to refresh available models: timeout waiting for child process to exit/d'
    return 0
  fi
  cat
}

log_has_runtime_network_failure() {
  local current_tool="$1" current_log_file="$2" current_debug_log_file="${3:-}"
  local excerpt=""
  excerpt="$(runtime_error_signal_excerpt "$current_log_file" "$current_debug_log_file" "$prompt_file" || true)"
  excerpt="$(printf '%s\n' "$excerpt" | filter_known_benign_runtime_error_noise "$current_tool")"
  [[ -n "$excerpt" ]] || return 1

  # Let tools finish their own reconnect/backoff loop without a monitor-level
  # kill. Post-exit runtime recovery classifies reconnect logs and applies the
  # bounded execution-network backoff policy; hard network failures still trip
  # immediately here.
  if printf '%s\n' "$excerpt" | rg -qi \
    'worker quit with fatal: Transport channel closed|invalid peer certificate|certificate was not trusted|certificate expired|received fatal alert|websocket: failed to connect|connection closed via error|curl: \((7|28|35|52|56)\)|timed out|timeout|connection reset|connection refused|connection aborted|network is unreachable|temporary failure in name resolution|eai_again|enotfound|tls handshake|proxyconnect tcp|proxy error|bad gateway|service unavailable|gateway timeout|upstream connect error|Failed to refresh token: error sending request for url \("https://auth\.openai\.com/oauth/token"\)'; then
    return 0
  fi
  return 1
}

log_has_runtime_tool_failure() {
  local current_tool="$1" current_log_file="$2" current_debug_log_file="${3:-}"
  local excerpt=""
  excerpt="$(runtime_error_signal_excerpt "$current_log_file" "$current_debug_log_file" "$prompt_file" | filter_known_benign_runtime_error_noise "$current_tool")"
  case "$current_tool" in
    codex)
      printf '%s\n' "$excerpt" | rg -qi \
        '401|402 payment required|403 forbidden|429 too many requests|exceeded retry limit|auth error: 402|unauthorized|invalid.?token|token.?expired|authentication.?failed|deactivated_workspace|workspace deactivated|请先登录|subscription.?expired|login required|usage limit|try again|预扣费额度失败|剩余额度不足|余额不足|insufficient balance|insufficient credit|pre.?charge.*failed|billing hard limit|quota exceeded|cannot access session files|permission denied|thread/start failed'
      ;;
    cc|cc-use-codex-cli|kiro-cli)
      printf '%s\n' "$excerpt" | rg -qi \
        'API error \(attempt [0-9]+/[0-9]+\): (401|402|403|429)|provider_response_error|insufficient_quota|quota exceeded|insufficient balance|insufficient credit|payment required|authentication.?failed|auth error:\s*no api key available|no api key available|api key required|missing api key|unauthorized|invalid.?token|token.?expired|subscription.?expired|login required|deactivated_workspace|workspace deactivated|monthly request limit reached|unable to verify subscription status:\s*service error'
      ;;
    iflow)
      printf '%s\n' "$excerpt" | rg -qi \
        'auth error:\s*no api key available|no api key available|api key required|missing api key|unauthorized|invalid.?token|token.?expired|subscription.?expired|login required|deactivated_workspace|workspace deactivated|insufficient_quota|quota exceeded|insufficient balance|insufficient credit|payment required|平台并发限制|请控制单并发使用|并发限制|concurrency limit|concurrent limit|too many concurrent'
      ;;
    *)
      return 1
      ;;
  esac
}

log_has_iflow_local_state_failure() {
  local current_log_file="$1" current_debug_log_file="${2:-}"
  local -a existing_files=()
  [[ -f "$current_log_file" ]] && existing_files+=("$current_log_file")
  [[ -f "$current_debug_log_file" ]] && existing_files+=("$current_debug_log_file")
  [[ ${#existing_files[@]} -gt 0 ]] || return 1
  rg -qi \
    'HistoryError: Failed to update project metadata: Error: (EPERM|EACCES): .*\/\.iflow\/(config|history)\/|An unexpected critical error occurred:|Error: (EPERM|EACCES): .*\/\.iflow\/(config|history)\/' \
    "${existing_files[@]}"
}

live_runtime_network_failure_detected() {
  local current_tool="$1" current_log_file="$2" current_debug_log_file="${3:-}"
  if log_has_runtime_network_failure "$current_tool" "$current_log_file" "$current_debug_log_file"; then
    return 0
  fi
  return 1
}

live_runtime_failure_reason() {
  local current_tool="$1" current_log_file="$2" current_debug_log_file="${3:-}"
  if live_runtime_network_failure_detected "$current_tool" "$current_log_file" "$current_debug_log_file"; then
    printf 'network_failure\n'
    return 0
  fi
  if [[ "$current_tool" == "iflow" ]] && log_has_iflow_local_state_failure "$current_log_file" "$current_debug_log_file"; then
    printf 'tool_runtime_failure\n'
    return 0
  fi
  if log_has_runtime_tool_failure "$current_tool" "$current_log_file" "$current_debug_log_file"; then
    printf 'tool_runtime_failure\n'
    return 0
  fi
  return 1
}

child_pids_for_parent() {
  local parent_pid="$1"
  [[ -n "$parent_pid" ]] || return 0
  ps -Ao pid=,ppid= 2>/dev/null | awk -v parent_pid="$parent_pid" '$2 == parent_pid { print $1 }'
}

collect_descendant_pids() {
  local parent_pid="$1" child_pid nested_pid
  [[ -n "$parent_pid" ]] || return 0
  while IFS= read -r child_pid; do
    [[ -n "$child_pid" ]] || continue
    printf '%s\n' "$child_pid"
    while IFS= read -r nested_pid; do
      [[ -n "$nested_pid" ]] || continue
      printf '%s\n' "$nested_pid"
    done < <(collect_descendant_pids "$child_pid")
  done < <(child_pids_for_parent "$parent_pid")
}

terminate_pid_tree() {
  local root_pid="$1" signal="${2:-TERM}" descendant_pid
  [[ -n "$root_pid" ]] || return 0
  while IFS= read -r descendant_pid; do
    [[ -n "$descendant_pid" ]] || continue
    kill "-$signal" "$descendant_pid" 2>/dev/null || true
  done < <(collect_descendant_pids "$root_pid" | awk '!seen[$0]++')
  kill "-$signal" "$root_pid" 2>/dev/null || true
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project) project="$(abs_path_or_fail "${2:-}")"; shift 2 ;;
    --tool) tool="${2:-}"; shift 2 ;;
    --tool-adapter) tool_adapter="${2:-}"; shift 2 ;;
    --model) model="${2:-}"; shift 2 ;;
    --reasoning-effort) reasoning_effort="${2:-}"; shift 2 ;;
    --mode) mode="${2:-}"; shift 2 ;;
    --prompt-file) prompt_file="$(abs_path_or_fail "${2:-}")"; shift 2 ;;
    --pid-file) pid_file="$(abs_path_or_fail "${2:-}")"; shift 2 ;;
    --log-file) log_file="$(abs_path_or_fail "${2:-}")"; shift 2 ;;
    --launch-kind) launch_kind="${2:-}"; shift 2 ;;
    --tool-capabilities) tool_capabilities="${2:-}"; shift 2 ;;
    --tool-policy) tool_policy="${2:-}"; shift 2 ;;
    --codex-capability-model) codex_capability_model="${2:-}"; shift 2 ;;
    --codex-capability-sandbox) codex_capability_sandbox="${2:-}"; shift 2 ;;
    --codex-capability-approval-policy) codex_capability_approval_policy="${2:-}"; shift 2 ;;
    --codex-capability-cwd-mode) codex_capability_cwd_mode="${2:-}"; shift 2 ;;
    --debug-log-file) debug_log_file="$(abs_path_or_fail "${2:-}")"; shift 2 ;;
    --claude-session-id) claude_session_id="${2:-}"; shift 2 ;;
    --tool-resume-target) tool_resume_target="${2:-}"; shift 2 ;;
    --network-failure-marker-file) network_failure_marker_file="$(abs_path_or_fail "${2:-}")"; shift 2 ;;
    --failure-marker-file) failure_marker_file="$(abs_path_or_fail "${2:-}")"; shift 2 ;;
    *) usage; exit 1 ;;
  esac
done

[[ -n "$project" && -n "$tool" && -n "$mode" && -n "$prompt_file" && -n "$pid_file" && -n "$log_file" && -n "$launch_kind" ]] || {
  usage
  exit 1
}

mkdir -p "$(dirname "$pid_file")" "$(dirname "$log_file")"
[[ -d "$project" ]] || preflight_error "[ERROR] project not found: $project"
[[ -f "$prompt_file" ]] || preflight_error "[ERROR] prompt file not found: $prompt_file"
[[ -n "$tool_adapter" ]] || tool_adapter="$(tool_default_adapter "$tool")"
if [[ -n "$network_failure_marker_file" ]]; then
  mkdir -p "$(dirname "$network_failure_marker_file")"
  rm -f "$network_failure_marker_file"
fi
if [[ -n "$failure_marker_file" ]]; then
  mkdir -p "$(dirname "$failure_marker_file")"
  rm -f "$failure_marker_file"
fi
if ! tool_adapter_supports_launch_kind "$tool" "$tool_adapter" "$launch_kind"; then
  preflight_error "[ERROR] launch kind '$launch_kind' is not supported for tool '$tool' with adapter '$tool_adapter' (supported: $(tool_supported_launch_kinds_for_adapter "$tool" "$tool_adapter" | tr '\n' ',' | sed 's/,$//'))"
fi
if [[ "$launch_kind" == "resume" ]] && tool_requires_explicit_resume_target "$tool" && [[ -z "$tool_resume_target" ]]; then
  preflight_error "[ERROR] $tool resume requires --tool-resume-target"
fi

(
  cd "$project"
  tool_run_from_prompt_file "$project" "$tool" "$tool_adapter" "$model" "$reasoning_effort" "$mode" "$prompt_file" "$launch_kind" "$tool_capabilities" "$tool_policy" "$codex_capability_model" "$codex_capability_sandbox" "$codex_capability_approval_policy" "$codex_capability_cwd_mode" "$debug_log_file" "$claude_session_id" "$tool_resume_target"
) >>"$log_file" 2>&1 &

child_pid=$!
echo "$child_pid" >"$pid_file"
write_workcell_launch_state_if_possible "$project"
write_live_session_state_if_possible "$project" "$tool" "$log_file" "$prompt_file" "$launch_kind"
echo "$child_pid"

while kill -0 "$child_pid" 2>/dev/null; do
  write_live_session_state_if_possible "$project" "$tool" "$log_file" "$prompt_file" "$launch_kind"
  if [[ -n "$network_failure_marker_file" || -n "$failure_marker_file" ]]; then
    live_failure_reason=""
    live_failure_reason="$(live_runtime_failure_reason "$tool" "$log_file" "$debug_log_file" || true)"
    if [[ -n "$live_failure_reason" ]]; then
      if [[ "$live_failure_reason" == "network_failure" && -n "$network_failure_marker_file" ]]; then
        printf 'network_failure\n' >"$network_failure_marker_file"
      fi
      if [[ "$live_failure_reason" != "network_failure" && -n "$failure_marker_file" ]]; then
        printf '%s\n' "$live_failure_reason" >"$failure_marker_file"
      fi
      terminate_pid_tree "$child_pid" TERM
      break
    fi
  fi
  sleep 1
done

set +e
wait "$child_pid"
child_rc=$?
set -e

if [[ "$child_rc" -ne 0 ]]; then
  terminate_pid_tree "$child_pid" KILL
fi

if [[ -n "$network_failure_marker_file" || -n "$failure_marker_file" ]]; then
  write_live_session_state_if_possible "$project" "$tool" "$log_file" "$prompt_file" "$launch_kind"
  live_failure_reason=""
  live_failure_reason="$(live_runtime_failure_reason "$tool" "$log_file" "$debug_log_file" || true)"
  if [[ -n "$live_failure_reason" ]]; then
    if [[ "$live_failure_reason" == "network_failure" && -n "$network_failure_marker_file" ]]; then
      printf 'network_failure\n' >"$network_failure_marker_file"
    fi
    if [[ "$live_failure_reason" != "network_failure" && -n "$failure_marker_file" ]]; then
      printf '%s\n' "$live_failure_reason" >"$failure_marker_file"
    fi
  fi
fi

exit "$child_rc"
