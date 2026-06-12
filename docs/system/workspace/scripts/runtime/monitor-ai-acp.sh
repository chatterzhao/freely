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

_bridge_short_hash() {
  local project="$1"
  printf '%s' "$project" | shasum -a 256 | cut -c1-16
}

_bridge_pid_file() {
  echo "/tmp/freely-acp-$(_bridge_short_hash "$1").pid"
}

_bridge_socket() {
  echo "/tmp/freely-acp-$(_bridge_short_hash "$1").sock"
}

_bridge_log_file() {
  echo "$1/.freely/run/acp-bridge.log"
}

_bridge_ensure_running() {
  local project="$1" tool="${2:-}"
  local pid_file socket bridge_script tool_file last_tool
  pid_file="$(_bridge_pid_file "$project")"
  socket="$(_bridge_socket "$project")"
  tool_file="$(_bridge_pid_file "$project").tool"

  # Already running?
  if [[ -f "$pid_file" ]]; then
    local pid
    pid=$(cat "$pid_file" 2>/dev/null || true)
    if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null && [[ -S "$socket" ]]; then
      # Same tool/slot? Keep bridge alive.
      last_tool=$(cat "$tool_file" 2>/dev/null || true)
      if [[ -z "$tool" || "$last_tool" == "$tool" ]]; then
        return 0
      fi
      # Tool/slot changed — kill old bridge, restart with new env.
      echo "[bridge] tool changed ($last_tool → $tool), restarting bridge"
      kill "$pid" 2>/dev/null || true
      sleep 1
    fi
    rm -f "$pid_file" "$socket" "$tool_file"
  fi

  bridge_script="$SCRIPT_DIR/acp-bridge.py"
  [[ -f "$bridge_script" ]] || bridge_script="$(dirname "$SCRIPT_DIR")/runtime/acp-bridge.py"
  [[ -f "$bridge_script" ]] || {
    echo "[ERROR] acp-bridge.py not found" >&2
    return 1
  }

  # Export permission mode from slot config for claude-agent-acp.
  # _apply_tool_alias_settings returns early for registered tools, so
  # CLAUDE_CODE_PERMISSION_MODE may not be set. Read it from the slot
  # config here. Only claude uses session/set_mode; codex/opencode
  # handle permissions internally via their own config mechanisms.
  if [[ -n "$tool" && -z "${CLAUDE_CODE_PERMISSION_MODE:-}" ]]; then
    local _slot_dir _settings_file _base_tool
    _base_tool="${tool%%-*}"  # claude-apikey-ds-flash-auto → claude
    _slot_dir=$(ls -d "$HOME/.ai-auth/${tool}" 2>/dev/null | head -1 || true)
    if [[ -z "$_slot_dir" ]]; then
      _slot_dir=$(ls -d "$HOME/.ai-auth/${tool}-"* 2>/dev/null | head -1 || true)
    fi
    if [[ -n "$_slot_dir" && -d "$_slot_dir" ]]; then
      case "$_base_tool" in
        claude)
          _settings_file="$_slot_dir/settings.json"
          if [[ -f "$_settings_file" ]]; then
            export CLAUDE_CODE_PERMISSION_MODE="$(python3 -c "
import json
with open('$_settings_file') as f:
    d = json.load(f)
pm = d.get('permissionMode', '') or d.get('permissions', {}).get('defaultMode', '')
if pm: print(pm)
" 2>/dev/null || echo 'bypassPermissions')"
          fi
          ;;
        codex)
          # codex uses config.toml with approval_policy; bridge doesn't call
          # session/set_mode for codex, but export env for completeness.
          _settings_file="$_slot_dir/config.toml"
          if [[ -f "$_settings_file" ]]; then
            local _approval
            _approval=$(python3 -c "
try:
    import tomllib
except ImportError:
    import tomli as tomllib
with open('$_settings_file','rb') as f:
    d = tomllib.load(f)
print(d.get('approval_policy',''))
" 2>/dev/null)
            if [[ -n "$_approval" ]]; then
              export CLAUDE_CODE_PERMISSION_MODE="$_approval"
            fi
          fi
          ;;
        opencode)
          # opencode uses settings.json with 'permission' field.
          # Permission is already handled by OPENCODE_CONFIG env var.
          ;;
      esac
    fi
  fi

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

  # Persist the tool/slot that started this bridge so we can detect
  # changes on the next call (same base tool, different slot → restart).
  if [[ -n "$tool" ]]; then
    printf '%s\n' "$tool" > "$tool_file"
  fi
}

# ── Helpers ─────────────────────────────────────────────────────────

_file_mtime_epoch() {
  local f="$1"
  [[ -f "$f" ]] || { echo "0"; return 0; }
  stat -f %m "$f" 2>/dev/null || stat -c %Y "$f" 2>/dev/null || echo 0
}

# ── Error detection ────────────────────────────────────────────────

_detect_acp_failure() {
  local log_file="$1" failure_marker="$2" network_failure_marker="$3" bridge_lost_marker="$4" bridge_log_offset="${5:-}"
  [[ -f "$log_file" ]] || return 0

  local _matched _bridge_log _net_err
  _bridge_log="$(dirname "$log_file")/../run/acp-bridge.log"

  # ── Layer 1: Network / transport failure (from cycle log) ──
  if _matched=$(grep -m1 -E '\b(Connection refused|Connection reset by peer|connection refused|connection reset|ECONNREFUSED|ENOTFOUND|ETIMEDOUT|socket hang up|timed out|connection timeout|Connection timed out|dial timeout|i/o timeout|read timeout|deadline exceeded|TLS handshake|TLS alert|TLS error|proxy error|proxy refused|proxy timeout|proxy auth|Could not connect to proxy|DNS error|DNS failure|DNS timeout|DNS resolution|Could not resolve host|name resolution failed|NXDOMAIN)\b' "$log_file" 2>/dev/null); then
    echo "[ACP-detect] network_failure matched: ${_matched:0:200}" >&2
    [[ -n "$network_failure_marker" ]] && echo "network_failure" > "$network_failure_marker"
  fi

  # ── Layer 2: Auth / rate limit failure (from cycle log) ──
  if _matched=$(grep -m1 -E '(HTTP 40[123]|HTTP 429|40[123] Unauthorized|40[123] Forbidden|429 Too Many Requests|status: 40[123]|status: 429|Unauthorized|Payment Required|insufficient_quota|rate_limit|quota exceeded|InsufficientBalance)' "$log_file" 2>/dev/null); then
    echo "[ACP-detect] auth_or_rate_limit matched: ${_matched:0:200}" >&2
    [[ -n "$failure_marker" ]] && echo "auth_or_rate_limit" > "$failure_marker"
  fi

  # ── Layer 3: Bridge log fatal error detection ──
  # MUST mirror _acp_bridge_has_fatal_error() in freely so the same error
  # patterns that drive post-cycle tool switching also trigger live detection.
  # Without this, the monitor loop hangs when run-acp-prompt.py blocks on a
  # dead bridge socket while the error is only visible in acp-bridge.log.
  #
  # Scan only NEW content (since cycle start) to avoid matching stale errors.
  _net_err='(Transport channel closed|stream disconnected before completion|error sending request for url|HandshakeFailure|received fatal alert|certificate not valid|certificate expired)'
  local _bridge_fatal
  _bridge_fatal='(exited unexpectedly|ProcessTransport.*not ready|idle timeout|worker quit with fatal|server stdout closed|Transport channel closed|stream disconnected before completion|error sending request for url|failed to refresh available models|HandshakeFailure|received fatal alert|certificate not valid|certificate expired)'

  if _matched=$(_grep_new_only "$_bridge_log" "$bridge_log_offset" -m1 -E "$_bridge_fatal" 2>/dev/null) && [[ -n "$_matched" ]]; then
    echo "[ACP-detect] bridge_fatal matched: ${_matched:0:200}" >&2
    [[ -n "$bridge_lost_marker" ]] && echo "bridge_session_lost" > "$bridge_lost_marker"
    if echo "$_matched" | grep -qE "$_net_err" 2>/dev/null; then
      [[ -n "$network_failure_marker" ]] && echo "network_failure" > "$network_failure_marker"
    fi
  elif _matched=$(grep -m1 -E "$_bridge_fatal" "$log_file" 2>/dev/null) && [[ -n "$_matched" ]]; then
    echo "[ACP-detect] bridge_fatal matched (cycle log): ${_matched:0:200}" >&2
    [[ -n "$bridge_lost_marker" ]] && echo "bridge_session_lost" > "$bridge_lost_marker"
    if echo "$_matched" | grep -qE "$_net_err" 2>/dev/null; then
      [[ -n "$network_failure_marker" ]] && echo "network_failure" > "$network_failure_marker"
    fi
  fi

  # Also scan cycle log for network-class transport errors.
  if [[ ! -f "$network_failure_marker" ]]; then
    if _matched=$(grep -m1 -E "$_net_err" "$log_file" 2>/dev/null); then
      echo "[ACP-detect] network_fatal matched (cycle): ${_matched:0:200}" >&2
      [[ -n "$network_failure_marker" ]] && echo "network_failure" > "$network_failure_marker"
    fi
  fi

  # ── Layer 4: Session-not-found (recoverable) ──
  local _session_lost_warn
  if _session_lost_warn=$(_grep_new_only "$_bridge_log" "$bridge_log_offset" -m1 -E '(session.*not found|unknown session|no such session|Session not found)' 2>/dev/null) && [[ -n "$_session_lost_warn" ]]; then
    echo "[ACP-detect] session_lost (recoverable, fallback expected): ${_session_lost_warn:0:200}" >&2
  elif _session_lost_warn=$(grep -m1 -E '(session.*not found|unknown session|no such session|Session not found)' "$log_file" 2>/dev/null) && [[ -n "$_session_lost_warn" ]]; then
    echo "[ACP-detect] session_lost (recoverable, fallback expected): ${_session_lost_warn:0:200}" >&2
  fi
}


# _grep_new_only: grep only new content added after a byte offset.
# Used to scan the persistent bridge log without matching stale errors.
_grep_new_only() {
  local file="$1" offset="$2"
  shift 2
  [[ -f "$file" ]] || return 1
  if [[ -n "$offset" && "$offset" -gt 0 ]]; then
    local cur_size
    cur_size=$(wc -c < "$file" 2>/dev/null || echo 0)
    if [[ "$cur_size" -gt "$offset" ]]; then
      tail -c +$((offset + 1)) "$file" 2>/dev/null | grep "$@"
    else
      return 1
    fi
  else
    grep "$@" "$file"
  fi
}

# ── Session state (via freely-db daemon) ────────────────────────────

_persist_session_to_store() {
  local project="$1" clean_session_id="$2" tool="$3" launch_kind="$4" resume_mode="$5"
  local role="${FREELY_ROLE_HINT:-manager}"
  local cli; cli="$(dirname "$0")/freely-db-cli"
  python3 "$cli" --project "$project" session.upsert \
    --session-id "$clean_session_id" \
    --project "$project" \
    --tool "$tool" \
    --role "$role" \
    --launch-kind "$launch_kind" \
    --tool_adapter acp \
    --resume_mode "${resume_mode:-}" \
    >/dev/null 2>&1 || {
      echo "[WARN] session upsert failed for $clean_session_id" >&2
      return 1
    }
}

_mark_session_failed() {
  local project="$1" session_id="$2" error_reason="$3"
  local cli; cli="$(dirname "$0")/freely-db-cli"
  python3 "$cli" --project "$project" session.complete \
    --session-id "$session_id" \
    --status failed \
    --error_reason "$error_reason" \
    >/dev/null 2>&1 || true
}

_mark_session_completed() {
  local project="$1" session_id="$2"
  local cli; cli="$(dirname "$0")/freely-db-cli"
  python3 "$cli" --project "$project" session.complete \
    --session-id "$session_id" \
    --status completed \
    >/dev/null 2>&1 || true
}

_tool_switch_writeback_session_id() {
  local project="$1" new_session_id="$2"
  [[ -n "$new_session_id" ]] || return 1
  local cli; cli="$(dirname "$0")/freely-db-cli"
  python3 "$cli" --project "$project" session.tool-switch-update-sid \
    --new_session_id "$new_session_id" \
    >/dev/null 2>&1 || true
}

# ── Main ───────────────────────────────────────────────────────────

main() {
  local project="" tool="" tool_adapter="acp" prompt_file=""
  local session_id="" resume_target=""
  local mode="auto" model="" reasoning_effort="" launch_kind="fresh"
  local pid_file="" log_file="" debug_log_file=""
  local failure_marker_file="" network_failure_marker_file="" bridge_lost_marker_file=""
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
      --bridge-lost-marker-file) bridge_lost_marker_file="$2"; shift 2 ;;
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

  # Load tool launchers FIRST so alias settings (model, API key, base URL)
  # are applied to the environment BEFORE starting the ACP bridge.
  # This ensures claude-agent-acp inherits the correct per-alias config,
  # not the user's interactive shell environment variables.
  _load_tool_launchers || exit 1
  _apply_tool_alias_settings "$tool"

  # Ensure persistent ACP server is running (inherits env from alias settings)
  _bridge_ensure_running "$project" "$tool" || exit 1

  # Record bridge log byte offset at cycle start so failure detection only
  # scans NEW content — avoids matching stale errors from previous cycles.
  local bridge_log_path bridge_log_offset
  bridge_log_path="$(_bridge_log_file "$project")"
  bridge_log_offset=$(wc -c < "$bridge_log_path" 2>/dev/null || echo 0)

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
  ) >>"$log_file" 2>>"${debug_log_file:-/dev/null}" &

  local child_pid=$!

  # Write bridge PID as AI PID for liveness checks
  local bridge_pid
  bridge_pid=$(cat "$(_bridge_pid_file "$project")" 2>/dev/null || echo "$child_pid")
  if [[ -n "$pid_file" ]]; then
    echo "$bridge_pid" > "$pid_file"
  fi

  echo "$child_pid"

  # ── Monitor loop (transport monitoring) ──
  while kill -0 "$child_pid" 2>/dev/null; do
    # Live failure detection (log-based patterns)
    if [[ -n "$failure_marker_file" || -n "$network_failure_marker_file" || -n "$bridge_lost_marker_file" ]]; then
      _detect_acp_failure "$log_file" "$failure_marker_file" "$network_failure_marker_file" "$bridge_lost_marker_file" "$bridge_log_offset" "$bridge_log_offset"
      if [[ -f "$failure_marker_file" || -f "$network_failure_marker_file" || -f "$bridge_lost_marker_file" ]]; then
        kill "$child_pid" 2>/dev/null || true
        break
      fi
    fi

    # Bridge-dead check: if the ACP bridge process died, kill the child.
    # The bridge has its own idle timeout (900s) for unresponsive AI.
    # Debug log mtime is NOT a liveness signal — AI thinking, reading
    # governance docs, and processing prompts all produce zero debug output.
    local _bridge_pid
    _bridge_pid=$(cat "$(_bridge_pid_file "$project")" 2>/dev/null || true)
    if [[ -n "$_bridge_pid" ]] && ! kill -0 "$_bridge_pid" 2>/dev/null; then
      echo "[ACP-detect] bridge died (pid=$_bridge_pid), killing child" >&2
      [[ -n "$bridge_lost_marker" ]] && echo "bridge_session_lost" > "$bridge_lost_marker"
      [[ -n "$network_failure_marker" ]] && echo "network_failure" > "$network_failure_marker"
      kill "$child_pid" 2>/dev/null || true
      break
    fi

    sleep 1
  done

  set +e
  wait "$child_pid"
  local child_rc=$?
  set -e

  # ── Completion detection: stopReason from ACP protocol output ──
  # Search entire file for clean UUID — cycle log line 1 may be blank.
  local session_id_clean session_id_out stop_reason
  session_id_clean=$(grep -oE '[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}' "$log_file" 2>/dev/null | head -1 || true)
  session_id_out=$(sed -n 's/^session id: //p' "$log_file" | tail -n 1 || true)
  # Fallback: if UUID pattern did not match (e.g. opencode ses_ format), use session_id_out
  if [[ -z "$session_id_clean" && -n "$session_id_out" ]]; then
    session_id_clean="$session_id_out"
  fi

  # If session/prompt fell back to session/new, the first bare UUID in the log
  # is the stale resume target. Use the NEW session ID from the fallback instead.
  if echo "$session_id_out" | grep -qE '\(fresh after (prompt|resume) failure\)'; then
    local _fallback_sid
    _fallback_sid=$(echo "$session_id_out" | grep -oE '[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}' | head -1 || true)
    if [[ -n "$_fallback_sid" ]]; then
      session_id_clean="$_fallback_sid"
    fi
  fi

  stop_reason=$(grep -o 'stop_reason=[a-z_]*' "$log_file" | head -n 1 | cut -d= -f2 || true)

  if [[ -z "$stop_reason" ]]; then
    stop_reason="unknown"
  fi

# Persist clean session ID to session-store (authoritative source)
  if [[ -n "$session_id_clean" ]]; then
    local resume_mode_detected=""
    if [[ "$launch_kind" == "resume" ]]; then
      if echo "$session_id_out" | grep -q "(fresh after resume failure)"; then
        resume_mode_detected="recreated"
      else
        resume_mode_detected="native"
      fi
    fi
    _persist_session_to_store "$project" "$session_id_clean" "$tool" "$launch_kind" "$resume_mode_detected" || true
    # Write back new session ID to tool_switch_events so _tool_switch_launch_kind()
    # can find it and return "resume" on subsequent cycles.
    _tool_switch_writeback_session_id "$project" "$session_id_clean" || true
  fi

  # Post-exit failure detection
  local failure_detected=""
  if [[ -n "$failure_marker_file" || -n "$network_failure_marker_file" || -n "$bridge_lost_marker_file" ]]; then
    _detect_acp_failure "$log_file" "$failure_marker_file" "$network_failure_marker_file" "$bridge_lost_marker_file" "$bridge_log_offset"
    if [[ -f "$failure_marker_file" ]]; then
      failure_detected="auth_or_rate_limit"
    elif [[ -f "$network_failure_marker_file" ]]; then
      failure_detected="network_failure"
    elif [[ -f "$bridge_lost_marker_file" ]]; then
      failure_detected="bridge_session_lost"
    fi
  fi

  # Completion verdict: stopReason is the authoritative signal
  # Session stays active so next cycle can resume (L1 cache hit).
  # Only mark completed on daemon stop or fresh_with_handoff rotation.
  if [[ -n "$failure_detected" ]]; then
    # Non-recoverable failure: mark session failed so next launch goes fresh
    if [[ -n "$session_id_clean" ]]; then
      _mark_session_failed "$project" "$session_id_clean" "$failure_detected"
    fi
    echo "[WARN] ACP cycle failed: session=${session_id_clean:-unknown} reason=$failure_detected" >&2
    exit 1
  elif [[ "$stop_reason" == "end_turn" ]]; then
    echo "[ACP] cycle complete: session=${session_id_clean:-unknown} stopReason=end_turn" >&2
    exit 0
  else
    # Network failure or unknown: keep session active for retry
    echo "[WARN] ACP cycle finished with stopReason=$stop_reason (rc=$child_rc)" >&2
    exit 1
  fi
}

main "$@"
