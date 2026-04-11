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

log_has_slot_local_network_failure() {
  local current_tool="$1" current_log_file="$2"
  [[ "$current_tool" == "codex" && -f "$current_log_file" ]] || return 1
  rg -qi \
    'ERROR:\s*Reconnecting|worker quit with fatal: Transport channel closed|invalid peer certificate|certificate was not trusted|certificate expired|received fatal alert: UnrecognisedName|websocket: failed to connect|connection closed via error|tls handshake|proxy error|bad gateway|service unavailable|gateway timeout|upstream connect error' \
    "$current_log_file"
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

if [[ -n "$network_failure_marker_file" ]]; then
  while kill -0 "$child_pid" 2>/dev/null; do
    if log_has_slot_local_network_failure "$tool" "$log_file"; then
      printf 'network_failure\n' >"$network_failure_marker_file"
      kill "$child_pid" 2>/dev/null || true
      break
    fi
    sleep 1
  done
fi

wait "$child_pid"
