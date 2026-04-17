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

log_has_runtime_network_failure() {
  local current_log_file="$1" current_debug_log_file="${2:-}"
  runtime_error_signal_excerpt "$current_log_file" "$current_debug_log_file" "$prompt_file" | rg -qi \
    'ERROR:\s*Reconnecting|worker quit with fatal: Transport channel closed|invalid peer certificate|certificate was not trusted|certificate expired|received fatal alert|websocket: failed to connect|connection closed via error|curl: \((7|28|35|52|56)\)|timed out|timeout|connection reset|connection refused|connection aborted|network is unreachable|temporary failure in name resolution|eai_again|enotfound|tls handshake|proxyconnect tcp|proxy error|bad gateway|service unavailable|gateway timeout|upstream connect error'
}

log_has_runtime_tool_failure() {
  local current_tool="$1" current_log_file="$2" current_debug_log_file="${3:-}"
  case "$current_tool" in
    codex)
      runtime_error_signal_excerpt "$current_log_file" "$current_debug_log_file" "$prompt_file" | rg -qi \
        '401|402 payment required|403 forbidden|429 too many requests|exceeded retry limit|auth error: 402|unauthorized|invalid.?token|token.?expired|authentication.?failed|deactivated_workspace|workspace deactivated|请先登录|subscription.?expired|login required|usage limit|try again|预扣费额度失败|剩余额度不足|余额不足|insufficient balance|insufficient credit|pre.?charge.*failed|billing hard limit|quota exceeded|cannot access session files|permission denied|thread/start failed'
      ;;
    cc|cc-use-codex-cli|kiro-cli)
      runtime_error_signal_excerpt "$current_log_file" "$current_debug_log_file" "$prompt_file" | rg -qi \
        'API error \(attempt [0-9]+/[0-9]+\): (401|402|403|429)|provider_response_error|insufficient_quota|quota exceeded|insufficient balance|insufficient credit|payment required|authentication.?failed|auth error:\s*no api key available|no api key available|api key required|missing api key|unauthorized|invalid.?token|token.?expired|subscription.?expired|login required|deactivated_workspace|workspace deactivated|monthly request limit reached|unable to verify subscription status:\s*service error'
      ;;
    iflow)
      runtime_error_signal_excerpt "$current_log_file" "$current_debug_log_file" "$prompt_file" | rg -qi \
        'auth error:\s*no api key available|no api key available|api key required|missing api key|unauthorized|invalid.?token|token.?expired|subscription.?expired|login required|deactivated_workspace|workspace deactivated|insufficient_quota|quota exceeded|insufficient balance|insufficient credit|payment required|平台并发限制|请控制单并发使用|并发限制|concurrency limit|concurrent limit|too many concurrent'
      ;;
    *)
      return 1
      ;;
  esac
}

live_runtime_failure_reason() {
  local current_tool="$1" current_log_file="$2" current_debug_log_file="${3:-}"
  if log_has_runtime_network_failure "$current_log_file" "$current_debug_log_file"; then
    printf 'tool_runtime_failure\n'
    return 0
  fi
  if log_has_runtime_tool_failure "$current_tool" "$current_log_file" "$current_debug_log_file"; then
    printf 'tool_runtime_failure\n'
    return 0
  fi
  return 1
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
echo "$child_pid"

if [[ -n "$network_failure_marker_file" || -n "$failure_marker_file" ]]; then
  while kill -0 "$child_pid" 2>/dev/null; do
    live_failure_reason=""
    live_failure_reason="$(live_runtime_failure_reason "$tool" "$log_file" "$debug_log_file" || true)"
    if [[ -n "$live_failure_reason" ]]; then
      if [[ -n "$network_failure_marker_file" ]]; then
        printf 'network_failure\n' >"$network_failure_marker_file"
      fi
      if [[ -n "$failure_marker_file" ]]; then
        printf '%s\n' "$live_failure_reason" >"$failure_marker_file"
      fi
      kill "$child_pid" 2>/dev/null || true
      break
    fi
    sleep 1
  done
fi

set +e
wait "$child_pid"
child_rc=$?
set -e

if [[ -n "$network_failure_marker_file" || -n "$failure_marker_file" ]]; then
  live_failure_reason=""
  live_failure_reason="$(live_runtime_failure_reason "$tool" "$log_file" "$debug_log_file" || true)"
  if [[ -n "$live_failure_reason" ]]; then
    if [[ -n "$network_failure_marker_file" ]]; then
      printf 'network_failure\n' >"$network_failure_marker_file"
    fi
    if [[ -n "$failure_marker_file" ]]; then
      printf '%s\n' "$live_failure_reason" >"$failure_marker_file"
    fi
  fi
fi

exit "$child_rc"
