#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  start-lead-agent.sh \
    --project <abs_path> \
    --intent <abs_file> \
    --constitution <abs_file> \
    --ai <tool[:model][:mode]>
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

parse_ai_spec_or_fail() {
  local spec="$1"
  local tool="" model="" mode="auto"

  IFS=':' read -r tool model mode <<<"$spec"
  [[ -n "${tool:-}" ]] || {
    echo "[ERROR] invalid --ai spec: $spec" >&2
    exit 1
  }
  [[ -n "${mode:-}" ]] || mode="auto"
  [[ "$mode" == "auto" || "$mode" == "step" ]] || {
    echo "[ERROR] unsupported mode: $mode" >&2
    exit 1
  }

  case "$tool" in
    codex|kiro-cli|iflow) ;;
    *)
      echo "[ERROR] unsupported tool: $tool" >&2
      exit 1
      ;;
  esac

  printf '%s|%s|%s\n' "$tool" "${model:-}" "$mode"
}

project=""
intent=""
constitution=""
ai_spec=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project) project="$(abs_path_or_fail "${2:-}")"; shift 2 ;;
    --intent) intent="$(abs_path_or_fail "${2:-}")"; shift 2 ;;
    --constitution) constitution="$(abs_path_or_fail "${2:-}")"; shift 2 ;;
    --ai) ai_spec="${2:-}"; shift 2 ;;
    *) usage; exit 1 ;;
  esac
done

[[ -n "$project" && -n "$intent" && -n "$constitution" && -n "$ai_spec" ]] || {
  usage
  exit 1
}

[[ -d "$project" ]] || { echo "[ERROR] project not found: $project" >&2; exit 1; }
[[ -f "$intent" ]] || { echo "[ERROR] intent file not found: $intent" >&2; exit 1; }
[[ -f "$constitution" ]] || { echo "[ERROR] constitution file not found: $constitution" >&2; exit 1; }

IFS='|' read -r ai_tool ai_model ai_mode <<<"$(parse_ai_spec_or_fail "$ai_spec")"

cat <<EOF
你现在进入 Freely 的首跳闭环。

先读取以下文档：
- 项目意图：$intent
- 宪法：$constitution
- 里程碑扫描入口：$project/docs/milestones.md
- 首跳代理：$project/docs/system/workspace/agents/lead-agent.md

运行上下文：
- PROJECT_ROOT=$project
- AI_TOOL=$ai_tool
- AI_MODEL=${ai_model:-}
- AI_MODE=$ai_mode

执行要求：
1. 先执行 \`skill:constitution-guard\` 与 \`skill:laws-enforcer\`。
2. 进入 \`lead-agent\`，不要绕过首跳代理。
3. 用 \`skill:context-source-skill\` 读取当前输入上下文和 milestone。
4. 若没有 usable issue，进入 \`skill:no-usable-issue-skill\`。
5. 若已有 usable issue，进入 \`skill:has-usable-issue-skill\`，再分流到 \`doc-loop-execution\` 或 \`dev-loop-execution\`。
EOF
