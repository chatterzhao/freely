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

write_workcell_launch_state_if_possible() {
  local current_project="$1"
  local state_file tmp_file updated_at
  local desired_state supervisor_state ai_state exit_reason role_hint
  local verification_contract_file verification_metadata_present verification_missing_fields
  local verification_owner_issue verification_pre_tests_path verification_artifact_dir
  local verification_test_lanes verification_acceptance_ids verification_evidence_level
  local verification_target_environment verification_closeout_gate verification_closeout_gate_command
  local verification_closeout_target_lane verification_closeout_promotion_gate
  local verification_closeout_requires_adequacy verification_closeout_review_artifact_policy

  state_file="$(workcell_state_file_for_project "$current_project")"
  mkdir -p "$(dirname "$state_file")"

  desired_state="running"
  supervisor_state="up"
  ai_state="down"
  exit_reason="starting"
  role_hint="worker"
  verification_contract_file="$current_project/.freely/run/worker-verification-contract.env"
  verification_metadata_present="false"
  verification_missing_fields=""
  verification_owner_issue=""
  verification_pre_tests_path=""
  verification_artifact_dir=""
  verification_test_lanes=""
  verification_acceptance_ids=""
  verification_evidence_level=""
  verification_target_environment=""
  verification_closeout_gate=""
  verification_closeout_gate_command=""
  verification_closeout_target_lane=""
  verification_closeout_promotion_gate=""
  verification_closeout_requires_adequacy=""
  verification_closeout_review_artifact_policy=""

  if [[ -f "$state_file" ]]; then
    unset DESIRED_RUNTIME_STATE LAST_SUPERVISOR_STATE LAST_AI_STATE LAST_EXIT_REASON LAST_ROLE_HINT LAST_WORKER_VERIFICATION_CONTRACT_FILE LAST_WORKER_VERIFICATION_METADATA_PRESENT LAST_WORKER_VERIFICATION_METADATA_MISSING_FIELDS LAST_WORKER_OWNER_ISSUE LAST_WORKER_PRE_TESTS_PATH LAST_WORKER_VERIFICATION_ARTIFACT_DIR LAST_WORKER_REQUIRED_TEST_LANES_CSV LAST_WORKER_REQUIRED_ACCEPTANCE_ITEM_IDS_CSV LAST_WORKER_MINIMUM_EVIDENCE_LEVEL LAST_WORKER_TARGET_ENVIRONMENT LAST_WORKER_CLOSEOUT_GATE LAST_WORKER_CLOSEOUT_GATE_COMMAND LAST_WORKER_CLOSEOUT_TARGET_LANE LAST_WORKER_CLOSEOUT_PROMOTION_GATE LAST_WORKER_CLOSEOUT_REQUIRES_ADEQUACY LAST_WORKER_CLOSEOUT_REVIEW_ARTIFACT_POLICY
    # shellcheck disable=SC1090
    source "$state_file"
    desired_state="${DESIRED_RUNTIME_STATE:-running}"
    supervisor_state="${LAST_SUPERVISOR_STATE:-up}"
    role_hint="${LAST_ROLE_HINT:-worker}"
    verification_contract_file="${LAST_WORKER_VERIFICATION_CONTRACT_FILE:-$verification_contract_file}"
    verification_metadata_present="${LAST_WORKER_VERIFICATION_METADATA_PRESENT:-false}"
    verification_missing_fields="${LAST_WORKER_VERIFICATION_METADATA_MISSING_FIELDS:-}"
    verification_owner_issue="${LAST_WORKER_OWNER_ISSUE:-}"
    verification_pre_tests_path="${LAST_WORKER_PRE_TESTS_PATH:-}"
    verification_artifact_dir="${LAST_WORKER_VERIFICATION_ARTIFACT_DIR:-}"
    verification_test_lanes="${LAST_WORKER_REQUIRED_TEST_LANES_CSV:-}"
    verification_acceptance_ids="${LAST_WORKER_REQUIRED_ACCEPTANCE_ITEM_IDS_CSV:-}"
    verification_evidence_level="${LAST_WORKER_MINIMUM_EVIDENCE_LEVEL:-}"
    verification_target_environment="${LAST_WORKER_TARGET_ENVIRONMENT:-}"
    verification_closeout_gate="${LAST_WORKER_CLOSEOUT_GATE:-}"
    verification_closeout_gate_command="${LAST_WORKER_CLOSEOUT_GATE_COMMAND:-}"
    verification_closeout_target_lane="${LAST_WORKER_CLOSEOUT_TARGET_LANE:-}"
    verification_closeout_promotion_gate="${LAST_WORKER_CLOSEOUT_PROMOTION_GATE:-}"
    verification_closeout_requires_adequacy="${LAST_WORKER_CLOSEOUT_REQUIRES_ADEQUACY:-}"
    verification_closeout_review_artifact_policy="${LAST_WORKER_CLOSEOUT_REVIEW_ARTIFACT_POLICY:-}"
  fi

  updated_at="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  tmp_file="$(mktemp "${state_file}.tmp.XXXXXX")"
  cat >"$tmp_file" <<EOF
DESIRED_RUNTIME_STATE="${desired_state:-running}"
LAST_SUPERVISOR_STATE="${supervisor_state:-up}"
LAST_AI_STATE="up"
LAST_EXIT_REASON="ai_launch_in_flight"
LAST_ROLE_HINT="${role_hint:-worker}"
LAST_STATE_UPDATED_AT="$updated_at"
LAST_WORKER_VERIFICATION_CONTRACT_FILE="${verification_contract_file:-$current_project/.freely/run/worker-verification-contract.env}"
LAST_WORKER_VERIFICATION_METADATA_PRESENT="${verification_metadata_present:-false}"
LAST_WORKER_VERIFICATION_METADATA_MISSING_FIELDS="${verification_missing_fields:-}"
LAST_WORKER_OWNER_ISSUE="${verification_owner_issue:-}"
LAST_WORKER_PRE_TESTS_PATH="${verification_pre_tests_path:-}"
LAST_WORKER_VERIFICATION_ARTIFACT_DIR="${verification_artifact_dir:-}"
LAST_WORKER_REQUIRED_TEST_LANES_CSV="${verification_test_lanes:-}"
LAST_WORKER_REQUIRED_ACCEPTANCE_ITEM_IDS_CSV="${verification_acceptance_ids:-}"
LAST_WORKER_MINIMUM_EVIDENCE_LEVEL="${verification_evidence_level:-}"
LAST_WORKER_TARGET_ENVIRONMENT="${verification_target_environment:-}"
LAST_WORKER_CLOSEOUT_GATE="${verification_closeout_gate:-}"
LAST_WORKER_CLOSEOUT_GATE_COMMAND="${verification_closeout_gate_command:-}"
LAST_WORKER_CLOSEOUT_TARGET_LANE="${verification_closeout_target_lane:-}"
LAST_WORKER_CLOSEOUT_PROMOTION_GATE="${verification_closeout_promotion_gate:-}"
LAST_WORKER_CLOSEOUT_REQUIRES_ADEQUACY="${verification_closeout_requires_adequacy:-}"
LAST_WORKER_CLOSEOUT_REVIEW_ARTIFACT_POLICY="${verification_closeout_review_artifact_policy:-}"
EOF
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
    'worker quit with fatal: Transport channel closed|invalid peer certificate|certificate was not trusted|certificate expired|received fatal alert|websocket: failed to connect|connection closed via error|curl: \((7|28|35|52|56)\)|timed out|timeout|connection reset|connection refused|connection aborted|network is unreachable|temporary failure in name resolution|eai_again|enotfound|tls handshake|proxyconnect tcp|proxy error|bad gateway|service unavailable|gateway timeout|upstream connect error'; then
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

live_runtime_failure_reason() {
  local current_tool="$1" current_log_file="$2" current_debug_log_file="${3:-}"
  if log_has_runtime_network_failure "$current_tool" "$current_log_file" "$current_debug_log_file"; then
    printf 'tool_runtime_failure\n'
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
      terminate_pid_tree "$child_pid" TERM
      break
    fi
    sleep 1
  done
fi

set +e
wait "$child_pid"
child_rc=$?
set -e

if [[ "$child_rc" -ne 0 ]]; then
  terminate_pid_tree "$child_pid" KILL
fi

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
