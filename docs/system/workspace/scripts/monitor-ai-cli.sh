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

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project) project="$(abs_path_or_fail "${2:-}")"; shift 2 ;;
    --tool) tool="${2:-}"; shift 2 ;;
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
    *) usage; exit 1 ;;
  esac
done

[[ -n "$project" && -n "$tool" && -n "$mode" && -n "$prompt_file" && -n "$pid_file" && -n "$log_file" && -n "$launch_kind" ]] || {
  usage
  exit 1
}

[[ -d "$project" ]] || { echo "[ERROR] project not found: $project" >&2; exit 1; }
[[ -f "$prompt_file" ]] || { echo "[ERROR] prompt file not found: $prompt_file" >&2; exit 1; }
if [[ "$launch_kind" == "resume" ]] && tool_requires_explicit_resume_target "$tool" && [[ -z "$tool_resume_target" ]]; then
  echo "[ERROR] $tool resume requires --tool-resume-target" >&2
  exit 1
fi
mkdir -p "$(dirname "$pid_file")" "$(dirname "$log_file")"

(
  cd "$project"
  tool_run_from_prompt_file "$project" "$tool" "$model" "$reasoning_effort" "$mode" "$prompt_file" "$launch_kind" "$tool_capabilities" "$tool_policy" "$codex_capability_model" "$codex_capability_sandbox" "$codex_capability_approval_policy" "$codex_capability_cwd_mode" "$debug_log_file" "$claude_session_id" "$tool_resume_target"
) >>"$log_file" 2>&1 &

child_pid=$!
echo "$child_pid" >"$pid_file"
echo "$child_pid"

wait "$child_pid"
