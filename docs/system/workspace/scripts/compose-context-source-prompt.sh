#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  compose-context-source-prompt.sh \
    --project <abs_path> \
    --source-input-file <abs_file> \
    --milestone <path_or_abs_file>
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
source_input_file=""
milestone_path=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project) project="$(abs_path_or_fail "${2:-}")"; shift 2 ;;
    --source-input-file) source_input_file="$(abs_path_or_fail "${2:-}")"; shift 2 ;;
    --milestone) milestone_path="${2:-}"; shift 2 ;;
    *) usage; exit 1 ;;
  esac
done

[[ -n "$project" && -n "$source_input_file" && -n "$milestone_path" ]] || {
  usage
  exit 1
}

[[ -d "$project" ]] || { echo "[ERROR] project not found: $project" >&2; exit 1; }
[[ -f "$source_input_file" ]] || { echo "[ERROR] source input file not found: $source_input_file" >&2; exit 1; }

cat <<EOF
你现在在 Freely 的第二层 auto-loop 编排阶段。

请阅读：
- source input：$source_input_file
- 里程碑：$milestone_path
- workspace 根：$project/docs/system/workspace
- 工具清单：workspace/tools.md
- 来源编排技能：workspace/skills/context-source-skill/SKILL.md

你的任务：
1. 读取 source input，理解当前 human chat 的真实意图。
2. 阅读 milestone，判断是否存在 usable issue。
3. 阅读 workspace/tools.md，根据任务强度、工具优先级和当前可用性，自主选择下一跳工具。
4. 你要输出：
   - selected_tool
   - why_selected
   - target_skill_or_loop
   - next_prompt
5. 若 milestone 中没有 usable issue：
   - 阅读 workspace/skills/no-usable-issue-skill/SKILL.md
   - 严格按指南继续 pre-brainstorm 或候选收敛
6. 若 milestone 中已有 usable issue：
   - 阅读 workspace/skills/has-usable-issue-skill/SKILL.md
   - 严格按指南先接入 issue-bound doc-loop-execution(IBM+G)
7. 不要把路由理解成脚本硬编码分支；应由你基于输入和文档理解后决定。
EOF
