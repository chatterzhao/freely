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

project_dirty_entries() {
  local project="$1"
  git -C "$project" status --porcelain 2>/dev/null | wc -l | tr -d ' '
}

project_clean_state() {
  local project="$1"
  local dirty_count
  dirty_count="$(project_dirty_entries "$project")"
  if [[ "${dirty_count:-0}" =~ ^[0-9]+$ ]] && (( dirty_count == 0 )); then
    printf 'CLEAN\n'
  else
    printf 'DIRTY\n'
  fi
}

checkpoint_guard_summary() {
  local project="$1"
  local guard_bin output required reasons
  guard_bin="$project/bin/checkpoint-guard"
  if [[ ! -x "$guard_bin" ]]; then
    printf 'checkpoint_required=unknown; reason_codes=unavailable\n'
    return 0
  fi
  output="$("$guard_bin" --project "$project" --format json 2>/dev/null || true)"
  required="$(printf '%s\n' "$output" | sed -n 's/.*"checkpoint_required":\(true\|false\).*/\1/p')"
  reasons="$(printf '%s\n' "$output" | sed -n 's/.*"reason_codes":\[\([^]]*\)\].*/\1/p' | tr -d '"' | sed 's/, */,/g')"
  [[ -n "$required" ]] || required="unknown"
  [[ -n "$reasons" ]] || reasons="none"
  printf 'checkpoint_required=%s; reason_codes=%s\n' "$required" "$reasons"
}

is_manager_branch() {
  local branch="$1"
  case "$branch" in
    develop|main|pre-test-merge) return 0 ;;
    *) return 1 ;;
  esac
}

worktree_fleet_brief() {
  local project="$1" repo_root total dirty
  repo_root="$(git -C "$project" rev-parse --show-toplevel 2>/dev/null || true)"
  [[ -n "$repo_root" ]] || {
    printf 'total=unknown; dirty=unknown\n'
    return 0
  }
  total=0
  dirty=0
  while IFS= read -r wt_path; do
    [[ -n "$wt_path" ]] || continue
    total=$((total + 1))
    if [[ -n "$(git -C "$wt_path" status --porcelain 2>/dev/null)" ]]; then
      dirty=$((dirty + 1))
    fi
  done < <(git -C "$repo_root" worktree list --porcelain 2>/dev/null | awk '/^worktree / {print substr($0, 10)}')
  printf 'total=%s; dirty=%s\n' "$total" "$dirty"
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

current_branch="$(git -C "$project" branch --show-current 2>/dev/null || printf 'unknown')"
current_clean_state="$(project_clean_state "$project")"
current_dirty_entries="$(project_dirty_entries "$project")"
current_checkpoint_summary="$(checkpoint_guard_summary "$project")"
current_fleet_summary="$(worktree_fleet_brief "$project")"
manager_mode="false"
execution_rule_15="15. 默认不要在首跳结束时只输出 \`next_prompt\` 就停下。"
execution_rule_16="16. 若 \`selected_tool\` 与当前运行中的 \`AI_TOOL\` 相同，你必须在当前会话内继续执行第二跳 skill，直接完成对应的 doc-loop / dev-loop 工作，并修改仓库产物；\`next_prompt\` 只作为中间可追溯产物保留。"
execution_rule_17="17. 只有当 \`selected_tool\` 与当前 \`AI_TOOL\` 不同，或你明确判断必须把执行权交回外层 runtime 时，才允许把 \`next_prompt\` 作为 handoff 输出结束当前轮次；此时必须说明为什么不能在当前会话继续执行。"

if is_manager_branch "$current_branch"; then
  manager_mode="true"
  execution_rule_15="15. 当前分支是受保护主管工位；你不得在当前 worktree 直接修改受版本管理的仓库产物。"
  execution_rule_16="16. 若 \`selected_tool\` 与当前运行中的 \`AI_TOOL\` 相同，也不要在当前会话内直接执行第二跳实现；你必须先选择或创建对应 feature worktree，并把执行权委派到那个工位的 worker AI/tool 进程。"
  execution_rule_17="17. 你在当前会话中的交付应是监督判断、delegation handoff、需要启动的 worker 命令与 continuity 留痕；只有 worker 工位可以继续实际 doc-loop / dev-loop。"
fi

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
- CURRENT_BRANCH=${current_branch:-unknown}
- MANAGER_MODE=${manager_mode}
- AI_TOOL=$ai_tool
- AI_MODEL=${ai_model:-}
- AI_MODE=$ai_mode
- AI_REASONING_EFFORT=${reasoning_effort:-}

工作区治理提醒（非强制阻断，但必须纳入判断）：
- current_worktree_state: ${current_clean_state}
- current_project_dirty_entries: ${current_dirty_entries}
- ${current_checkpoint_summary}
- project_worktree_summary: ${current_fleet_summary}
- 开始当前轮次前，先判断是否需要先维护工作区卫生、切 checkpoint commit、或把无关改动分流到其他 worktree。
- 这不是强制停止开发；你需要结合 issue 边界、验证状态和当前改动范围自主决定是否先收口，再继续委派/实现。

执行要求：
1. 先执行 \`skill:constitution-guard\` 与 \`skill:laws-enforcer\`。
2. 进入 \`lead-agent\`，不要绕过首跳代理。
3. 由 \`lead-agent\` 委托 \`skill:context-source-skill\` 进行需求池扫描、优先级判断与下一跳提示词组装。
4. 若当前轮次承担项目级监督职责，先基于项目级工位视图做排班、冻结、集成与 cleanup 判断；不要直接把自己降级成单工位写代码代理。
5. 在可并行的 doc-loop、verification、review、日志诊断或互不冲突的代码任务上，使用 subagent 提高效率。
6. 你的需求池至少包括：
   - \`docs/milestones.md\`
   - progress / recovery
   - review / test
   - human chat / session evidence
   - github issue
   - \`docs/PROJECT_INTENT.md\`
7. 你需要自主判断：
   - 当前先看哪个池
   - 哪个池优先级更高
   - 当前问题是 \`pre-brainstorm\`、\`issue-bound brainstorm\` 还是 \`issue continuation\`
8. 不要把路由当作脚本硬编码分支；脚本只负责启动和托管 AI，会话中的需求发现与路由判断由你完成。
9. 读取 workspace 下的 agent 与 skill 时，统一按相对路径理解，例如：
   - \`workspace/agents/lead-agent.md\`
   - \`workspace/skills/context-source-skill/SKILL.md\`
   - \`workspace/skills/doc-pre-brainstorm-execution/SKILL.md\`
   - \`workspace/skills/doc-ibm-execution/SKILL.md\`
   - \`workspace/skills/dev-loop-execution/SKILL.md\`
10. 若没有稳定 issue 边界，下一跳应阅读 \`workspace/skills/doc-pre-brainstorm-execution/SKILL.md\`。
11. 若已有稳定 issue 边界但文档仍需 issue-bound 收敛，下一跳应阅读 \`workspace/skills/doc-ibm-execution/SKILL.md\`。
12. 若 issue 已 ready 或 in-progress，且文档和验收边界足够，下一跳应阅读 \`workspace/skills/dev-loop-execution/SKILL.md\`。
13. 你需要解释为什么选择当前工具、为什么当前池优先，以及为什么选择当前下一跳。
14. 你负责产出工具选择与下一跳提示词；CLI 的具体无交互启动参数由 Freely runtime 按 \`workspace/tools.md\` 与 \`workspace/scripts/monitor-ai-cli.sh\` 的约定执行，不要自行发明另一套命令格式。
${execution_rule_15}
${execution_rule_16}
${execution_rule_17}

主管模式要求：
- 若当前轮次承担项目级监督职责，先基于工位快照安排继续开发、冻结、验证、合并和清理顺序。
- 可并行且互不阻塞的任务，使用 subagent 提高效率。
- 若 \`CURRENT_BRANCH\` 是 \`develop/main/pre-test-merge\`，当前会话只做主管，不做实现；实现必须委派到 feature worktree。
- 若工位视图缺少准确 issue/phase，不要伪造；先把该工位视为需要进一步核对的监督对象。
EOF
