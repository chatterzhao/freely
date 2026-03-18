#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  monitor-ai-cli.sh \
    --project <abs_path> \
    --tool <tool> \
    --model <model_or_empty> \
    --reasoning-effort <effort_or_empty> \
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
    *) usage; exit 1 ;;
  esac
done

[[ -n "$project" && -n "$tool" && -n "$mode" && -n "$prompt_file" && -n "$pid_file" && -n "$log_file" && -n "$launch_kind" ]] || {
  usage
  exit 1
}

[[ -d "$project" ]] || { echo "[ERROR] project not found: $project" >&2; exit 1; }
[[ -f "$prompt_file" ]] || { echo "[ERROR] prompt file not found: $prompt_file" >&2; exit 1; }
mkdir -p "$(dirname "$pid_file")" "$(dirname "$log_file")"

launch_codex() {
  local -a args=(exec --skip-git-repo-check -C "$project")
  if [[ "$launch_kind" == "resume" ]]; then
    args=(exec resume --last --skip-git-repo-check)
  fi
  [[ -n "$model" ]] && args+=(-m "$model")
  [[ -n "$reasoning_effort" ]] && args+=(-c "model_reasoning_effort=\"$reasoning_effort\"")
  [[ "$mode" == "auto" ]] && args+=(--dangerously-bypass-approvals-and-sandbox)
  exec codex "${args[@]}" - <"$prompt_file"
}

launch_iflow() {
  local -a args=()
  [[ -n "$model" ]] && args+=(-m "$model")
  if [[ "$launch_kind" == "resume" ]]; then
    args+=(-c)
  fi
  if [[ "$mode" == "auto" ]]; then
    exec iflow "${args[@]}" -p "$(cat "$prompt_file")" -y --max-turns 100
  else
    exec iflow "${args[@]}" -p "$(cat "$prompt_file")" --default --max-turns 100
  fi
}

launch_kiro_cli() {
  local selected_model="${model:-claude-opus-4.6}"
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
}

launch_test_sleep() {
  exec bash -lc 'echo "[TEST] mock AI CLI started"; sleep 5'
}

launch_test_compact() {
  exec bash -lc 'echo "[TEST] mock AI CLI started"; echo "context compacted"; sleep 1'
}

launch_test_once() {
  exec bash -lc 'echo "[TEST] mock AI CLI started"; sleep 1'
}

launch_test_session() {
  exec bash -lc 'echo "session id: test-session"; echo "[TEST] mock AI CLI started"; sleep 1'
}

launch_test_route_only() {
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
}

(
  cd "$project"
  case "$tool" in
    codex) launch_codex ;;
    iflow) launch_iflow ;;
    kiro-cli) launch_kiro_cli ;;
    test-sleep) launch_test_sleep ;;
    test-compact) launch_test_compact ;;
    test-once) launch_test_once ;;
    test-session) launch_test_session ;;
    test-route-only) launch_test_route_only ;;
    *)
      echo "[ERROR] unsupported tool: $tool" >&2
      exit 1
      ;;
  esac
) >>"$log_file" 2>&1 &

child_pid=$!
echo "$child_pid" >"$pid_file"
echo "$child_pid"

wait "$child_pid"
