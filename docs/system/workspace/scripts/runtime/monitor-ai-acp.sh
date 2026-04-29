#!/usr/bin/env bash
# monitor-ai-acp.sh: ACP-native AI lifecycle monitor.
#
# Replaces PID-based monitor-ai-cli.sh when AI_TOOL_ADAPTER=acp.
# Delegates to tool-launchers.sh for per-tool ACP syntax.
#
# Architecture:
#   freely → monitor-ai-acp.sh → tool-launchers.sh → run-acp-prompt.py → acp-bridge → claude-agent-acp
#
# Completion: session/prompt stopReason="end_turn" (ACP-native, not PID exit).
# Server persistence: acp-bridge keeps claude-agent-acp alive across cycles.
# Session persistence: session/resume for cache hits across cycles.
#
# Usage: same interface as monitor-ai-cli.sh
#   monitor-ai-acp.sh --project <path> --tool <name> --prompt-file <path>
#     [--tool-adapter acp] [--claude-session-id <uuid>] [--tool-resume-target <uuid>]
#     [--mode auto|step] [--model <id>] [--reasoning-effort <effort>]
#     [--pid-file <path>] [--log-file <path>] [--debug-log-file <path>]
#     [--failure-marker-file <path>] [--network-failure-marker-file <path>]
#     [--launch-kind fresh|resume|fork|fresh_with_handoff]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"

# ── Tool launcher integration ──────────────────────────────────────

_load_tool_launchers() {
  if [[ -f "$SCRIPT_DIR/tool-launchers.sh" ]]; then
    source "$SCRIPT_DIR/tool-launchers.sh"
  elif [[ -f "$SCRIPT_DIR/../tool-launchers.sh" ]]; then
    source "$SCRIPT_DIR/../tool-launchers.sh"
  else
    echo "[ERROR] tool-launchers.sh not found" >&2
    exit 1
  fi
}

# ── Bridge management ──────────────────────────────────────────────

_bridge_pid_file() {
  echo "$1/.freely/run/acp-bridge.pid"
}

_bridge_socket() {
  echo "$1/.freely/run/acp-bridge.sock"
}

_bridge_ensure_running() {
  local project="$1"
  local pid_file socket bridge_script
  pid_file="$(_bridge_pid_file "$project")"
  socket="$(_bridge_socket "$project")"

  # Already running?
  if [[ -f "$pid_file" ]]; then
    local pid
    pid=$(cat "$pid_file" 2>/dev/null || true)
    if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null && [[ -S "$socket" ]]; then
      return 0
    fi
    rm -f "$pid_file" "$socket"
  fi

  bridge_script="$SCRIPT_DIR/acp-bridge.py"
  [[ -f "$bridge_script" ]] || bridge_script="$(dirname "$SCRIPT_DIR")/runtime/acp-bridge.py"
  [[ -f "$bridge_script" ]] || {
    echo "[ERROR] acp-bridge.py not found" >&2
    return 1
  }

  python3 "$bridge_script" start --project "$project" >/dev/null 2>&1 || {
    echo "[ERROR] failed to start ACP bridge" >&2
    return 1
  }

  # Wait for socket
  local waited=0
  while [[ ! -S "$socket" ]] && (( waited < 50 )); do
    sleep 0.1
    waited=$((waited + 1))
  done
  [[ -S "$socket" ]] || { echo "[ERROR] bridge socket did not appear" >&2; return 1; }
}

# ── Error detection ────────────────────────────────────────────────

_detect_acp_failure() {
  local log_file="$1" failure_marker="$2" network_failure_marker="$3"
  [[ -f "$log_file" ]] || return 0

  if grep -qE '(Connection refused|Connection reset|TLS|timeout|ECONNREFUSED|ENOTFOUND|ETIMEDOUT|socket hang up|proxy|DNS)' "$log_file" 2>/dev/null; then
    [[ -n "$network_failure_marker" ]] && echo "network_failure" > "$network_failure_marker"
  fi

  if grep -qE '(401|402|403|429|Unauthorized|Payment Required|insufficient_quota|rate_limit|quota exceeded|InsufficientBalance)' "$log_file" 2>/dev/null; then
    [[ -n "$failure_marker" ]] && echo "auth_or_rate_limit" > "$failure_marker"
  fi
}

# ── Session state ──────────────────────────────────────────────────

_write_acp_session_state() {
  local project="$1" session_id="$2" log_file="$3" launch_kind="$4"
  local state_dir="$project/.freely/run"
  mkdir -p "$state_dir"
  local state_file="$state_dir/session-state.env"

  {
    echo "# ACP session state — $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "SESSION_ID_CURRENT=$session_id"
    echo "SESSION_LAUNCH_KIND=$launch_kind"
    echo "SESSION_ANCHOR_UPDATED_AT=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "AI_TOOL_ADAPTER=acp"
  } > "$state_file"
}

# ── Main ───────────────────────────────────────────────────────────

main() {
  local project="" tool="" tool_adapter="acp" prompt_file=""
  local session_id="" resume_target=""
  local mode="auto" model="" reasoning_effort="" launch_kind="fresh"
  local pid_file="" log_file="" debug_log_file=""
  local failure_marker_file="" network_failure_marker_file=""
  local tool_capabilities="" tool_policy=""
  local codex_capability_model="" codex_capability_sandbox="" codex_capability_approval_policy="" codex_capability_cwd_mode=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --project) project="$2"; shift 2 ;;
      --tool) tool="$2"; shift 2 ;;
      --tool-adapter) tool_adapter="$2"; shift 2 ;;
      --prompt-file) prompt_file="$2"; shift 2 ;;
      --claude-session-id|--session-id) session_id="$2"; shift 2 ;;
      --tool-resume-target|--resume-target) resume_target="$2"; shift 2 ;;
      --mode) mode="$2"; shift 2 ;;
      --model) model="$2"; shift 2 ;;
      --reasoning-effort) reasoning_effort="$2"; shift 2 ;;
      --launch-kind) launch_kind="$2"; shift 2 ;;
      --pid-file) pid_file="$2"; shift 2 ;;
      --log-file) log_file="$2"; shift 2 ;;
      --debug-log-file) debug_log_file="$2"; shift 2 ;;
      --failure-marker-file) failure_marker_file="$2"; shift 2 ;;
      --network-failure-marker-file) network_failure_marker_file="$2"; shift 2 ;;
      --tool-capabilities) tool_capabilities="$2"; shift 2 ;;
      --tool-policy) tool_policy="$2"; shift 2 ;;
      --codex-capability-model) codex_capability_model="$2"; shift 2 ;;
      --codex-capability-sandbox) codex_capability_sandbox="$2"; shift 2 ;;
      --codex-capability-approval-policy) codex_capability_approval_policy="$2"; shift 2 ;;
      --codex-capability-cwd-mode) codex_capability_cwd_mode="$2"; shift 2 ;;
      *) echo "[ERROR] unknown arg: $1" >&2; exit 1 ;;
    esac
  done

  [[ -n "$project" && -n "$tool" && -n "$prompt_file" ]] || {
    echo "[ERROR] missing required args (--project, --tool, --prompt-file)" >&2
    exit 1
  }
  [[ -f "$prompt_file" ]] || { echo "[ERROR] prompt file not found: $prompt_file" >&2; exit 1; }

  # Ensure persistent ACP server is running
  _bridge_ensure_running "$project" || exit 1

  _load_tool_launchers || exit 1

  # Write own PID as initial AI PID (freely uses this for liveness)
  # The bridge PID is the real AI process handle — written below.
  if [[ -n "$pid_file" ]]; then
    echo "$$" > "$pid_file"
  fi

  # Launch ACP via tool abstraction (same pattern as monitor-ai-cli.sh)
  # run-acp-prompt.py connects to bridge, sends prompt, blocks until stopReason, exits.
  # The child PID represents the transport, NOT the AI server (which stays alive).
  (
    cd "$project"
    tool_run_from_prompt_file \
      "$project" "$tool" "$tool_adapter" "$model" "$reasoning_effort" \
      "$mode" "$prompt_file" "$launch_kind" \
      "$tool_capabilities" "$tool_policy" \
      "$codex_capability_model" "$codex_capability_sandbox" \
      "$codex_capability_approval_policy" "$codex_capability_cwd_mode" \
      "$debug_log_file" "$session_id" "$resume_target"
  ) >>"$log_file" 2>&1 &

  local child_pid=$!

  # Write bridge PID as AI PID for liveness checks
  local bridge_pid
  bridge_pid=$(cat "$(_bridge_pid_file "$project")" 2>/dev/null || echo "$child_pid")
  if [[ -n "$pid_file" ]]; then
    echo "$bridge_pid" > "$pid_file"
  fi

  echo "$child_pid"

  # ── Monitor loop (transport monitoring, not AI completion detection) ──
  while kill -0 "$child_pid" 2>/dev/null; do
    # Live failure detection
    if [[ -n "$failure_marker_file" || -n "$network_failure_marker_file" ]]; then
      _detect_acp_failure "$log_file" "$failure_marker_file" "$network_failure_marker_file"
      if [[ -f "$failure_marker_file" || -f "$network_failure_marker_file" ]]; then
        kill "$child_pid" 2>/dev/null || true
        break
      fi
    fi
    sleep 1
  done

  set +e
  wait "$child_pid"
  local child_rc=$?
  set -e

  # ── Completion detection: stopReason from ACP protocol output ──
  local session_id_out stop_reason
  session_id_out=$(sed -n 's/^session id: //p' "$log_file" | head -n 1)
  stop_reason=$(grep -o 'stop_reason=[a-z_]*' "$log_file" | head -n 1 | cut -d= -f2)

  if [[ -z "$stop_reason" ]]; then
    stop_reason="unknown"
  fi

  # Write session state for next cycle's resume
  if [[ -n "$session_id_out" ]]; then
    _write_acp_session_state "$project" "$session_id_out" "$log_file" "$launch_kind"
  fi

  # Post-exit failure detection
  if [[ -n "$failure_marker_file" || -n "$network_failure_marker_file" ]]; then
    _detect_acp_failure "$log_file" "$failure_marker_file" "$network_failure_marker_file"
  fi

  # Completion verdict: stopReason is the authoritative signal
  if [[ "$stop_reason" == "end_turn" ]]; then
    echo "[ACP] cycle complete: session=${session_id_out:-unknown} stopReason=end_turn" >&2
    exit 0
  else
    echo "[WARN] ACP cycle finished with stopReason=$stop_reason (rc=$child_rc)" >&2
    exit 1
  fi
}

main "$@"
