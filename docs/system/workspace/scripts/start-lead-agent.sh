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
  local first="" second="" third=""

  IFS=':' read -r first second third <<<"$spec"
  tool="$first"
  [[ -n "${tool:-}" ]] || {
    echo "[ERROR] invalid --ai spec: $spec" >&2
    exit 1
  }

  # Support both tool:model:mode and tool:mode forms.
  if [[ -n "${third:-}" ]]; then
    model="$second"
    mode="$third"
  elif [[ "$second" == "auto" || "$second" == "step" ]]; then
    model=""
    mode="$second"
  else
    model="${second:-}"
    mode="auto"
  fi

  [[ "$mode" == "auto" || "$mode" == "step" ]] || {
    echo "[ERROR] unsupported mode: $mode" >&2
    exit 1
  }

  case "$tool" in
    codex|kiro-cli|iflow|test-sleep) ;;
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
- workspace 根：$project/docs/system/workspace
- 工具清单：workspace/tools.md
- 首跳代理：workspace/agents/lead-agent.md

运行上下文：
- PROJECT_ROOT=$project
- WORKSPACE_ROOT=$project/docs/system/workspace
- AI_TOOL=$ai_tool
- AI_MODEL=${ai_model:-}
- AI_MODE=$ai_mode

执行要求：
1. 先执行 \`skill:constitution-guard\` 与 \`skill:laws-enforcer\`。
2. 进入 \`lead-agent\`，不要绕过首跳代理。
3. 由 \`lead-agent\` 委托 \`skill:context-source-skill\` 进行需求池扫描、优先级判断与下一跳提示词组装。
4. 你的需求池至少包括：
   - \`docs/milestones.md\`
   - progress / recovery
   - review / test
   - human chat / session evidence
   - github issue
   - \`docs/PROJECT_INTENT.md\`
5. 你需要自主判断：
   - 当前先看哪个池
   - 哪个池优先级更高
   - 当前问题是 \`pre-brainstorm\`、\`issue-bound brainstorm\` 还是 \`issue continuation\`
6. 不要把路由当作脚本硬编码分支；脚本只负责启动和托管 AI，会话中的需求发现与路由判断由你完成。
7. 读取 workspace 下的 agent 与 skill 时，统一按相对路径理解，例如：
   - \`workspace/agents/lead-agent.md\`
   - \`workspace/skills/context-source-skill/SKILL.md\`
   - \`workspace/skills/no-usable-issue-skill/SKILL.md\`
   - \`workspace/skills/has-usable-issue-skill/SKILL.md\`
8. 若没有稳定 issue 边界，下一跳应阅读 \`workspace/skills/no-usable-issue-skill/SKILL.md\`。
9. 若已有稳定 issue 边界，下一跳应阅读 \`workspace/skills/has-usable-issue-skill/SKILL.md\`，再决定进入 issue-bound IBM 或 \`dev-loop-execution\`。
10. 你需要解释为什么选择当前工具、为什么当前池优先，以及为什么选择当前下一跳。
11. 你负责产出工具选择与下一跳提示词；CLI 的具体无交互启动参数由 Freely runtime 按 \`workspace/tools.md\` 与 \`workspace/scripts/monitor-ai-cli.sh\` 的约定执行，不要自行发明另一套命令格式。
EOF
