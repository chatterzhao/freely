#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  start-lead-agent.sh \
    --project <abs_path> \
    --intent <abs_file> \
    --constitution <abs_file> \
    --ai <tool[:model][:mode]> \
    [--workspace-root <abs_dir>] \
    [--reasoning-effort <effort>]
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
    codex|kiro-cli|iflow|test-sleep|test-compact|test-once|test-session|test-route-only) ;;
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
workspace_root=""
reasoning_effort=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project) project="$(abs_path_or_fail "${2:-}")"; shift 2 ;;
    --intent) intent="$(abs_path_or_fail "${2:-}")"; shift 2 ;;
    --constitution) constitution="$(abs_path_or_fail "${2:-}")"; shift 2 ;;
    --ai) ai_spec="${2:-}"; shift 2 ;;
    --workspace-root) workspace_root="$(abs_path_or_fail "${2:-}")"; shift 2 ;;
    --reasoning-effort) reasoning_effort="${2:-}"; shift 2 ;;
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
if [[ -z "$workspace_root" ]]; then
  if [[ -d "$project/docs/system/workspace" ]]; then
    workspace_root="$project/docs/system/workspace"
  else
    workspace_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
  fi
fi
[[ -d "$workspace_root" ]] || { echo "[ERROR] workspace root not found: $workspace_root" >&2; exit 1; }

IFS='|' read -r ai_tool ai_model ai_mode <<<"$(parse_ai_spec_or_fail "$ai_spec")"

cat <<EOF
你现在进入 Freely 的首跳闭环。

先读取以下文档：
- 项目意图：$intent
- 宪法：$constitution
- 里程碑扫描入口：$project/docs/milestones.md
- workspace 根：$workspace_root
- 工具清单：workspace/tools.md
- 首跳代理：workspace/agents/lead-agent.md

运行上下文：
- PROJECT_ROOT=$project
- WORKSPACE_ROOT=$workspace_root
- AI_TOOL=$ai_tool
- AI_MODEL=${ai_model:-}
- AI_MODE=$ai_mode
- AI_REASONING_EFFORT=${reasoning_effort:-}

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
   - \`workspace/skills/doc-pre-brainstorm-execution/SKILL.md\`
   - \`workspace/skills/doc-ibm-execution/SKILL.md\`
   - \`workspace/skills/dev-loop-execution/SKILL.md\`
8. 若没有稳定 issue 边界，下一跳应阅读 \`workspace/skills/doc-pre-brainstorm-execution/SKILL.md\`。
9. 若已有稳定 issue 边界但文档仍需 issue-bound 收敛，下一跳应阅读 \`workspace/skills/doc-ibm-execution/SKILL.md\`。
10. 若 issue 已 ready 或 in-progress，且文档和验收边界足够，下一跳应阅读 \`workspace/skills/dev-loop-execution/SKILL.md\`。
11. 你需要解释为什么选择当前工具、为什么当前池优先，以及为什么选择当前下一跳。
12. 你负责产出工具选择与下一跳提示词；CLI 的具体无交互启动参数由 Freely runtime 按 \`workspace/tools.md\` 与 \`workspace/scripts/monitor-ai-cli.sh\` 的约定执行，不要自行发明另一套命令格式。
13. 默认不要在首跳结束时只输出 \`next_prompt\` 就停下。
14. 若 \`selected_tool\` 与当前运行中的 \`AI_TOOL\` 相同，你必须在当前会话内继续执行第二跳 skill，直接完成对应的 doc-loop / dev-loop 工作，并修改仓库产物；\`next_prompt\` 只作为中间可追溯产物保留。
15. 只有当 \`selected_tool\` 与当前 \`AI_TOOL\` 不同，或你明确判断必须把执行权交回外层 runtime 时，才允许把 \`next_prompt\` 作为 handoff 输出结束当前轮次；此时必须说明为什么不能在当前会话继续执行。
EOF
