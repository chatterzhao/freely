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
  (git_status_porcelain_with_runtime_hygiene "$project") | wc -l | tr -d ' '
}

git_status_entry_path_is_disposable_runtime_residue() {
  local rel_path="$1"
  [[ -n "$rel_path" ]] || return 1
  case "$rel_path" in
    __pycache__|__pycache__/*|*/__pycache__|*/__pycache__/*|*.pyc) return 0 ;;
  esac
  return 1
}

cleanup_disposable_runtime_residue_for_project() {
  local project="$1"
  local -a cleanup_targets=()
  local porcelain status_path abs_target
  while IFS= read -r porcelain; do
    [[ -n "$porcelain" ]] || continue
    [[ "$porcelain" == '?? '* ]] || continue
    status_path="${porcelain#?? }"
    git_status_entry_path_is_disposable_runtime_residue "$status_path" || continue
    abs_target="$project/$status_path"
    [[ -e "$abs_target" ]] || continue
    cleanup_targets+=("$abs_target")
  done < <(git -C "$project" status --porcelain 2>/dev/null || true)

  ((${#cleanup_targets[@]} > 0)) || return 0
  rm -rf -- "${cleanup_targets[@]}"
}

git_status_porcelain_with_runtime_hygiene() {
  local project="$1"
  cleanup_disposable_runtime_residue_for_project "$project"
  git -C "$project" status --porcelain 2>/dev/null || true
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
  [[ "$branch" == test-pre-merge-* ]] && return 0
  case "$branch" in
    develop|main) return 0 ;;
    *) return 1 ;;
  esac
}

workcell_state_file() {
  local project="$1"
  printf '%s\n' "$project/.freely/run/workcell-state.env"
}

worker_verification_contract_file() {
  local project="$1"
  printf '%s\n' "$project/.freely/run/worker-verification-contract.env"
}

worker_verification_contract_launchable() {
  local project="$1" contract_file metadata_present missing_fields_csv
  local owner_issue pre_tests_path artifact_dir test_lanes_csv acceptance_csv evidence_level
  local target_environment closeout_gate_command closeout_target_lane closeout_promotion_gate
  local closeout_requires_adequacy closeout_review_artifact_policy
  contract_file="$(worker_verification_contract_file "$project")"
  [[ -f "$contract_file" ]] || return 1
  unset VERIFICATION_METADATA_PRESENT VERIFICATION_METADATA_MISSING_FIELDS OWNER_ISSUE PRE_TESTS_PATH \
    VERIFICATION_ARTIFACT_DIR REQUIRED_TEST_LANES_CSV REQUIRED_ACCEPTANCE_ITEM_IDS_CSV \
    MINIMUM_EVIDENCE_LEVEL TARGET_ENVIRONMENT CLOSEOUT_GATE_COMMAND CLOSEOUT_TARGET_LANE \
    CLOSEOUT_PROMOTION_GATE CLOSEOUT_REQUIRES_ADEQUACY CLOSEOUT_REVIEW_ARTIFACT_POLICY
  # shellcheck disable=SC1090
  source "$contract_file"
  metadata_present="${VERIFICATION_METADATA_PRESENT:-}"
  missing_fields_csv="${VERIFICATION_METADATA_MISSING_FIELDS:-}"
  owner_issue="${OWNER_ISSUE:-}"
  pre_tests_path="${PRE_TESTS_PATH:-}"
  artifact_dir="${VERIFICATION_ARTIFACT_DIR:-}"
  test_lanes_csv="${REQUIRED_TEST_LANES_CSV:-}"
  acceptance_csv="${REQUIRED_ACCEPTANCE_ITEM_IDS_CSV:-}"
  evidence_level="${MINIMUM_EVIDENCE_LEVEL:-}"
  target_environment="${TARGET_ENVIRONMENT:-}"
  closeout_gate_command="${CLOSEOUT_GATE_COMMAND:-}"
  closeout_target_lane="${CLOSEOUT_TARGET_LANE:-}"
  closeout_promotion_gate="${CLOSEOUT_PROMOTION_GATE:-}"
  closeout_requires_adequacy="${CLOSEOUT_REQUIRES_ADEQUACY:-}"
  closeout_review_artifact_policy="${CLOSEOUT_REVIEW_ARTIFACT_POLICY:-}"
  [[ "$metadata_present" == "true" ]] || return 1
  [[ -z "$missing_fields_csv" ]] || return 1
  [[ -n "$owner_issue" && -n "$pre_tests_path" && -n "$artifact_dir" && -n "$test_lanes_csv" && -n "$acceptance_csv" && -n "$evidence_level" && -n "$target_environment" && -n "$closeout_gate_command" && -n "$closeout_target_lane" && -n "$closeout_promotion_gate" && -n "$closeout_requires_adequacy" && -n "$closeout_review_artifact_policy" ]]
}

# start-lead-agent.sh runs as subprocess — define helpers inline.
_meta_env_value() {
  local meta_file="$1" key="$2"
  [[ -f "$meta_file" ]] || return 0
  awk -F '"' -v key="$key" '$1 == key "=" { print $2; exit }' "$meta_file"
}

prompt_role_for_project() {
  local project="$1" branch="$2" state_file role_hint=""
  state_file="$(workcell_state_file "$project")"
  if [[ -f "$state_file" ]]; then
    role_hint="$(_meta_env_value "$state_file" "LAST_ROLE_HINT")"
    if [[ "$role_hint" == "manager" || "$role_hint" == "worker" ]]; then
      printf '%s\n' "$role_hint"
      return 0
    fi
  fi
  if is_manager_branch "$branch" && worker_verification_contract_launchable "$project"; then
    printf 'worker\n'
    return 0
  fi
  if is_manager_branch "$branch"; then
    printf 'manager\n'
  else
    printf 'worker\n'
  fi
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
    if [[ -n "$(git_status_porcelain_with_runtime_hygiene "$wt_path")" ]]; then
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

  # Normalize slot-suffixed tool names: strip -suffix to get base name.
  # Registry is the authority — any registered tool with slots gets normalized.
  local _case_tool="$tool"
  local _reg_tools _t
  # Inline tool registry query — start-lead-agent.sh runs as a subprocess,
  # it doesn't have access to _tool_registry_tools from the runtime script.
  _script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
  _runtime_dir="$_script_dir/runtime"
  _reg_tools="$("$_runtime_dir/tool-registry-query.py" "$_runtime_dir/tool-registry.toml" --list 2>/dev/null || true)"
  for _t in $_reg_tools; do
    [[ -n "$_t" ]] || continue
    if [[ "$_case_tool" == "$_t"-* || "$_case_tool" == "$_t" ]]; then
      _case_tool="$_t"
      break
    fi
  done

  # Validation: check if tool is registered
  local _is_known=0
  for _t in $_reg_tools test-; do
    if [[ "$_case_tool" == "$_t" || "$_case_tool" == "$_t"* ]]; then
      _is_known=1; break
    fi
  done
  if [[ "$_is_known" == "0" ]]; then
    cat >&2 <<SLOT_ERR
[ERROR] slot 对应的工具 '$tool' 未在 tool-registry.toml 中注册。

  已注册的工具: $_reg_tools

  slot 是 ~/.ai-auth/ 下的鉴权目录，命名约定为 {tool-name}-{apikey|account}-{custom}。
  tool-name 必须是已注册的工具名（首段 -apikey- 或 -account- 之前的部分）。

  例: claude-apikey-ds-pro-auto → 工具=claude
      opencode-apikey-ds-flash-auto → 工具=opencode
      codex-account-user@example-com-1 → 工具=codex

  请检查 agent-table.toml 中 {role}_slot 字段是否使用了已注册的 tool-name。
SLOT_ERR
    exit 1
  fi

  printf '%s|%s|%s\n' "$tool" "${model:-}" "$mode"
}

project=""
intent=""
constitution=""
ai_spec=""
workspace_root=""
reasoning_effort=""
delta_mode="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project) project="$(abs_path_or_fail "${2:-}")"; shift 2 ;;
    --intent) intent="$(abs_path_or_fail "${2:-}")"; shift 2 ;;
    --constitution) constitution="$(abs_path_or_fail "${2:-}")"; shift 2 ;;
    --ai) ai_spec="${2:-}"; shift 2 ;;
    --workspace-root) workspace_root="$(abs_path_or_fail "${2:-}")"; shift 2 ;;
    --reasoning-effort) reasoning_effort="${2:-}"; shift 2 ;;
    --delta) delta_mode="true"; shift ;;
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
prompt_role="$(prompt_role_for_project "$project" "$current_branch")"
current_clean_state="$(project_clean_state "$project")"
current_dirty_entries="$(project_dirty_entries "$project")"
current_checkpoint_summary="$(checkpoint_guard_summary "$project")"
current_fleet_summary="$(worktree_fleet_brief "$project")"
manager_mode="false"
execution_rule_15="15. 默认不要在首跳结束时只输出 \`next_prompt\` 就停下。"
execution_rule_16="16. 若 \`selected_tool\` 与当前运行中的 \`AI_TOOL\` 相同，你必须在当前会话内继续执行第二跳 skill，直接完成对应的 doc-loop / dev-loop 工作，并修改仓库产物；\`next_prompt\` 只作为中间可追溯产物保留。"
execution_rule_17="17. 只有当 \`selected_tool\` 与当前 \`AI_TOOL\` 不同，或你明确判断必须把执行权交回外层 runtime 时，才允许把 \`next_prompt\` 作为 handoff 输出结束当前轮次；此时必须说明为什么不能在当前会话继续执行。"
artifact_stamp="$(date -u '+%Y%m%dT%H%M%SZ')"
manager_continuity_path="$project/.freely/run/manager-continuity-${artifact_stamp}.md"
worker_prompt_dir="$project/.freely/run/worker-prompts"
worker_prompt_path_example="$worker_prompt_dir/${artifact_stamp}-worker-<slug>-${ai_tool}.txt"
manager_artifact_rule=""
	role_scope_rule_5a="5A. 你是 Worker Agent（见 workspace/agents/worker-agent.md）。保持 worker scope，不升级成主管。"
	role_scope_rule_5b="5B. 只回写本工位产物。发现需主管裁决的问题只记录 evidence + reroute。"
worker_agent_def="$(cat "$workspace_root/agents/worker-agent.md" 2>/dev/null || true)"
	additional_requirements="=== Agent 角色定义 ===
${worker_agent_def}
==="
startup_bounded_patrol_rule=""
initial_read_targets="$(cat <<EOF
- 项目治理入口：$project/AGENTS.md
- 项目意图：$intent
- 宪法：$constitution
- 里程碑扫描入口：$project/docs/milestones.md
- workspace 根：$workspace_root
- 工具清单：workspace/tools.md
- 技能索引：workspace/skills/README.md
- 首跳代理：workspace/agents/lead-agent.md
EOF
)"

	if [[ "$prompt_role" == "manager" ]]; then
	  manager_mode="true"
	  execution_rule_15="15. 你是 Manager Agent（见 workspace/agents/manager-agent.md）。不得直接 commit——通过委派 Worker。"
	  execution_rule_16="16. 交付物：continuity + worker prompt + 在回复末尾输出 \`\`\`json (handoff 内容) 块。自主决策优先级和分批。"
	  execution_rule_17="17. subagent 并行不冲突的任务。runtime-owned 问题交给 runtime。"
	  role_scope_rule_5a=""
	  role_scope_rule_5b=""
	  manager_artifact_rule="\`\`\`
Worktree:
- /abs/path/to/worktree
Branch:
- fix|feature/raw-{key}-{slug}
dispatch_priority: P2
parallel_safe: true
write_scope: worktree
intent_kind: edit|cleanup|promotion
intent_target: <简短描述>
\`\`\`"
	  manager_agent_def="$(cat "$workspace_root/agents/manager-agent.md" 2>/dev/null || true)"
	  additional_requirements="=== Agent 角色定义 ===
${manager_agent_def}
==="
	  startup_bounded_patrol_rule=""
	  initial_read_targets="$(cat <<EOF
- 项目治理：$project/AGENTS.md
- Manager Agent：$workspace_root/agents/manager-agent.md
- 当前态：freely live-status --project $project
- Scan：machine_readable_scan_json
- workspace：$workspace_root
EOF
)"
	fi

escape_prompt_backticks() {
  local value="${1-}"
  printf '%s' "${value//\`/\\\`}"
}

execution_rule_15_escaped="$(escape_prompt_backticks "$execution_rule_15")"
execution_rule_16_escaped="$(escape_prompt_backticks "$execution_rule_16")"
execution_rule_17_escaped="$(escape_prompt_backticks "$execution_rule_17")"
role_scope_rule_5a_escaped="$(escape_prompt_backticks "$role_scope_rule_5a")"
role_scope_rule_5b_escaped="$(escape_prompt_backticks "$role_scope_rule_5b")"
manager_artifact_rule_escaped="$(escape_prompt_backticks "$manager_artifact_rule")"
additional_requirements_escaped="$(escape_prompt_backticks "$additional_requirements")"
startup_bounded_patrol_rule_escaped="$(escape_prompt_backticks "$startup_bounded_patrol_rule")"
initial_read_targets_escaped="$(escape_prompt_backticks "$initial_read_targets")"

# Delta mode: minimal resume prompt
if [[ "$delta_mode" == "true" ]]; then
  cat <<DELTA
你现在继续 Freely 会话。

本轮是 resume——完整对话历史已在 session 中，不要重新开始 patrol。
优先消费上轮 continuity 中锚定的 route_kind 和 next_action。
按 exit contract directive 要求在结束前写出退出合同。

=== Agent 角色定义（每轮必须重新确认） ===
${manager_agent_def:-${worker_agent_def:-}}
===
DELTA
  exit 0
fi

cat <<EOF
你现在进入 Freely 的首跳闭环。

读取约定：
- skill:<name> 优先通过 Skill 工具加载（skills 已通过 deploy-skills 部署到工具目录）。若当前 CLI 无 Skill 工具，回退读取 workspace/skills/<name>/SKILL.md。
- workspace/skills/README.md 是技能索引，用于浏览可用技能列表。
- 对大型文档不要整文件硬读。尤其 docs/milestones.md，先用 patrol seed、rg、标题定位或分段读取，按命中的 issue / progress / queue 做定点核对。
- 若当前工具的读文件接口支持分页/范围参数，只在确实需要时填写有效值；不要传空字符串。

先读取以下文档或索引：
${initial_read_targets_escaped}

执行要求：
1. 先遵守 \`PROJECT_ROOT/AGENTS.md\`；它是当前目标项目的治理入口，不要在 workspace 能力文档里重复发明第二套项目规则。
2. 再完成 \`skill:freely-constitution-guard\` 与 \`skill:freely-laws-enforcer\` 预检：默认做法是阅读 \`skill:freely-constitution-guard\` 与 \`skill:freely-laws-enforcer\` 并按其约束执行；不要假设存在可直接调用的 \`skill\` 工具。
3. 进入 \`lead-agent\`，不要绕过首跳代理。
4. 先运行 \`freely task-source-scan --project $project --json\`，把最新 scan JSON 当作 standing-source 现场，再由 \`lead-agent\` 参照 \`skill:freely-context-source-skill\` 完成优先级判断与下一跳提示词组装；若当前工具没有原生 skill executor，就直接读取该技能文档并在当前会话按它执行。
4A. 若 runtime 在 prompt 尾部附加了 \`machine_readable_scan_json\`，优先把它当作本轮 idle / replan patrol 的结构化入口；仅当该 json 缺失、过时或不足以裁决时，才回退到重新运行 \`task-source-scan\`。其中状态只算 routing hint，phase judgement 仍需回到 linked evidence 核对。
${startup_bounded_patrol_rule_escaped}
5. 若当前轮次承担项目级监督职责，先基于项目级工位视图做排班、冻结、集成与 cleanup 判断；不要直接把自己降级成单工位写代码代理。
${role_scope_rule_5a_escaped}
${role_scope_rule_5b_escaped}
6. 在可并行的 doc-loop、verification、review、日志诊断或互不冲突的代码任务上，使用 subagent 提高效率。
6A. \`task-source-scan\` 的推荐消费方式：
   - 默认技能：\`freely-auto-loop-orchestrator\`
   - 来源解释技能：\`freely-context-source-skill\`
   - 先看 JSON 里的 \`sources[]\`、\`restart_point\`、\`status_markers\`、\`next_action\`
   - 不要把 scan 当成最终裁决；它是 patrol 输入，不替代 issue/progress/milestone 真相
6B. 不要在每轮都机械重跑 scan。优先在这些时机运行：
   - 启动后的第一轮 patrol
   - 某条 lane 刚完成 verification / closeout 并改写了 canonical truth 之后
   - 当前 worker 未满载，或没有 worker 在跑时
6C. 若所有 worker slot 都在推进未收口的 active lane，且没有新的 source/event truth，不要只为了“再扫一遍”打断当前主线、浪费 token。
7. 你的需求池至少包括：
   - \`docs/milestones.md\`
   - progress / recovery
   - review / test / acceptance review
   - milestone planning / state maintenance
   - human chat / session evidence
   - external issue
   - \`docs/PROJECT_INTENT.md\`
8. 你需要自主判断：
   - 当前先看哪个池
   - 哪个池优先级更高
   - 当前问题是 \`pre-brainstorm\`、\`issue-bound brainstorm\` 还是 \`issue continuation\`
   - 对暂不能收口的研究项，不允许因为本轮不继续实现就跳过；必须明确它继续停留在 \`candidate_issues\`、issue-bound brainstorm 或 blocked state，并写清 \`next_action\` 与 \`revisit_trigger\`
9. 不要把路由当作脚本硬编码分支；脚本只负责启动和托管 AI，会话中的需求发现与路由判断由你完成。
10. 读取 workspace 下的 agent 与 skill 时，统一按相对路径理解，例如：
   - \`workspace/agents/lead-agent.md\`
   - \`skill:freely-context-source-skill\`
   - \`skill:freely-doc-B1_IBM-execution\`
   - \`skill:freely-doc-B2_IBM-execution\`
   - \`skill:freely-dev-loop-execution\`
10A. 除非当前工具明确暴露了兼容的原生 skill tool，否则所有 \`skill:<name>\` 都按“去读对应 \`SKILL.md\` 并照此执行”解释。
11. 若没有稳定 issue 边界，下一跳应阅读 \`skill:freely-doc-B1_IBM-execution\`。
12. 若已有稳定 issue 边界但文档仍需 issue-bound 收敛，下一跳应阅读 \`skill:freely-doc-B2_IBM-execution\`。
13. 若 issue 已 ready 或 in-progress，且文档和验收边界足够，下一跳应阅读 \`skill:freely-dev-loop-execution\`。
13A. 若当前 route 已收敛为 \`completion_verification\` 或 \`cleanup_governance\`，不要把它伪装成新的 doc-loop / dev-loop；优先由主管在当前 \`auto-loop\` 侧产出 verification / cleanup judgement、continuity 与 handoff，必要时再委派 worker。
13B. 若当前问题本身是 worktree 维护：例如“哪些 worktree 已完成 / 哪些该 merge / 哪些只应退休或保留 research-only / 当前所有 worktree 这轮哪些该 cleanup”，优先阅读 \`skill:freely-worktree-maintenance-governance\`，先完成 \`audit / merge_prep / stacked_merge_chain / fleet_closure / retirement_handoff\` 判断，再决定是否进入 doc/dev-loop。
13C. 若当前目标分支不是直接从 \`develop\` 派生，而是依赖未合并父分支，不要直接给出“并入 develop”的结论；先按 \`child -> parent -> merge-prep-from-develop -> develop\` 的 stacked merge-chain 逐层检查。
14. 你需要解释为什么选择当前工具、为什么当前池优先，以及为什么选择当前下一跳。
15. 你负责产出工具选择与下一跳提示词；CLI 的具体无交互启动参数由 Freely runtime 按 \`workspace/tools.md\` 与 \`workspace/scripts/monitor-ai-cli.sh\` 的约定执行，不要自行发明另一套命令格式。
${execution_rule_15_escaped}
${execution_rule_16_escaped}
${execution_rule_17_escaped}
${manager_artifact_rule_escaped}

运行上下文：
- PROJECT_ROOT=$project
- WORKSPACE_ROOT=$workspace_root
- CURRENT_BRANCH=${current_branch:-unknown}
- MANAGER_MODE=${manager_mode}
- AI_TOOL=$ai_tool
- AI_MODEL=${ai_model:-}
- AI_MODE=$ai_mode
- AI_REASONING_EFFORT=${reasoning_effort:-}
- AI_TOOL_CAPABILITIES=${AI_TOOL_CAPABILITIES:-}
- AI_TOOL_POLICY=${AI_TOOL_POLICY:-}
- AI_CAPABILITY_CODEX_MODEL=${AI_CAPABILITY_CODEX_MODEL:-}
- AI_CAPABILITY_CODEX_SANDBOX=${AI_CAPABILITY_CODEX_SANDBOX:-}
- AI_CAPABILITY_CODEX_APPROVAL_POLICY=${AI_CAPABILITY_CODEX_APPROVAL_POLICY:-}
- AI_CAPABILITY_CODEX_CWD_MODE=${AI_CAPABILITY_CODEX_CWD_MODE:-}

工作区治理提醒（非强制阻断，但必须纳入判断）：
- current_worktree_state: ${current_clean_state}
- current_project_dirty_entries: ${current_dirty_entries}
- ${current_checkpoint_summary}
- project_worktree_summary: ${current_fleet_summary}
- 开始当前轮次前，先判断是否需要先维护工作区卫生、切 checkpoint commit、或把无关改动分流到其他 worktree。
- 若上一轮 handoff、当前运行输出、或工具自身提示出现 \`context compacted\`、compact、上下文压缩/摘要信号，不要继续扩 scope；先更新当前阶段对应的 continuity artifact，再决定是继续、checkpoint，还是交给外层 runtime 做 \`fresh_with_handoff\`。
- 若 runtime 已注入 \`上下文容量预警\` 或 \`会话轮换交接\`，优先按该治理提示收口；不要把它当作可忽略的背景信息。
- 这不是强制停止开发；你需要结合 issue 边界、验证状态和当前改动范围自主决定是否先收口，再继续委派/实现。

EOF
