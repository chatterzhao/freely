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
  (git -C "$project" status --porcelain 2>/dev/null || true) | wc -l | tr -d ' '
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
    codex|kiro-cli|iflow|cc|cc-use-codex-cli|test-sleep|test-compact|test-once|test-session|test-route-only) ;;
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
artifact_stamp="$(date '+%Y%m%d-%H%M%S')"
manager_continuity_path="$project/.freely/run/manager-continuity-${artifact_stamp}.md"
worker_prompt_dir="$project/.freely/run/worker-prompts"
worker_prompt_path_example="$worker_prompt_dir/${artifact_stamp}-worker-<slug>-${ai_tool}.txt"
manager_artifact_rule=""
role_scope_rule_5a="5A. 当 \`MANAGER_MODE=false\` 且当前分支是 \`feature/*\` 时，不要把 \`./bin/freely live-status --project $project\`、\`./bin/freely fleet-status --project $project\`、根 \`develop\` 的 live-status/fleet-state，或项目级 patrol 当作默认首跳；保持 worker reentry scope，只在当前工位问题直接需要时读取最小必要证据。"
role_scope_rule_5b="5B. 当 \`MANAGER_MODE=false\` 且当前分支是 \`feature/*\` 时，不要写 \`.freely/run/manager-continuity-*.md\`、\`.freely/run/worker-prompts/*.txt\`、cleanup queue 或其他 manager-only handoff 产物；worker 只回写本工位 issue / progress / recovery / worker continuity / verification evidence。"
additional_requirements="$(cat <<'EOF'
- 若 `MANAGER_MODE=false` 且当前分支是 `feature/*`，当前会话保持 worker scope：不要升级成项目级监督者；若发现需要主管裁决的 fleet / merge / cleanup 问题，只记录 evidence 与 reroute 建议。
EOF
)"
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

if is_manager_branch "$current_branch"; then
  manager_mode="true"
  execution_rule_15="15. 当前分支是受保护主管工位；你不得在当前 worktree 直接修改受版本管理的仓库产物。"
  execution_rule_16="16. 若 \`selected_tool\` 与当前运行中的 \`AI_TOOL\` 相同，也不要在当前会话内直接执行第二跳实现；你必须先选择或创建对应 feature worktree，并把执行权委派到那个工位的 worker AI/tool 进程。"
  execution_rule_17="17. 你在当前会话中的交付应是监督判断、delegation handoff、需要启动的 worker 命令与 continuity 留痕；只有 worker 工位可以继续实际 doc-loop / dev-loop。"
  role_scope_rule_5a="5A. 若当前轮次承担项目级监督职责，先读取 \`./bin/freely live-status --project $project\`，把它当作 supervisor / dispatcher / AI 当前态入口；只有在它提示需要继续深挖时，才展开 \`fleet-status\`、prompt、continuity、jsonl 等细节。"
  role_scope_rule_5b="$(cat <<'EOF'
5B. 若本轮是主管被 runtime 重新激活后的第一轮，先做一轮 patrol：
   - `live-status -> fleet-status -> milestone / issue / progress / recovery`
   - 主动寻找 `candidate stuck`、`phase orphaned`、`completion without closure`
   - 若 `live-status` 暴露 `develop_push_followthrough_push_urgency=immediate|deferred` 或 `develop_push_followthrough_resync_required=true`，先判断 push/resync followthrough 是否应前置
   - 对 owner / verification / promotion / cleanup / stale-batch retirement 这类 latest-develop-sensitive judgment，不得在 canonical `develop` 未同步时直接下结论
   - 把发现结果加工为 `ownership + restart_point + next_action`
EOF
)"
  manager_artifact_rule="$(cat <<EOF
18. 当前轮次若形成了 manager judgement / worker delegation / cleanup queue，你必须把它 materialize 成 runtime 可消费的非版本化产物，不能只停在自然语言回答。
19. 至少创建一个 manager continuity 文件：\`$manager_continuity_path\`。
20. 若需要委派 worker，再在 \`$worker_prompt_dir\` 下创建 worker prompt 文件；命名格式参考：\`$worker_prompt_path_example\`。
21. 每个 worker prompt 除正文外，必须带 machine-readable header：
   - \`Worktree:\`
   - \`- \\\`/abs/path/to/target-worktree\\\`\`
   - \`Branch:\`
   - \`- \\\`feature/target-branch\\\`\`
   自然语言说明可以补充，但不能替代这两个 header。
22. manager continuity 必须显式引用每个 worker prompt 的绝对路径；runtime 只会从 continuity 中消费这些 \`.freely/run/worker-prompts/*.txt\` 路径，不会从普通回答里自动提炼 handoff。
23. 若本轮存在多个 lane，worker prompt 不能只写业务内容；每个 prompt 还必须附带最小 dispatch metadata：\`dispatch_priority\`、\`parallel_safe\`、\`write_scope\`。若该 prompt 会授予 mutate authority，还必须补 machine-readable \`intent_kind\` 与 \`intent_target\`，明确当前 lane 取得的是 \`edit\`、\`cleanup\` 还是 \`promotion\` authority。若 lane 因 same-lane busy guard、显式 freeze、写域冲突或 supersede 暂不派发，未派发 lane 也必须留在 manager continuity 的 queue / frozen queue 中。
24. 对会产生 mutate authority 的 lane，worker prompt 还必须附带 machine-readable ownership metadata：\`intent_kind\`、\`intent_target\`。\`write_scope\` 只用于 launch-time scheduling，不替代长期 mutate ownership truth。
25. 若 worker lane 需要承担 verification / closeout 义务，worker prompt 还必须附带 machine-readable verification metadata：
   - \`Owner-Issue:\`
   - \`Pre-Tests-Path:\`
   - \`Verification-Artifact-Dir:\`
   - \`Required-Test-Lanes:\`
   - \`Required-Acceptance-Item-Ids:\`
   - \`Minimum-Evidence-Level:\`
   - \`Target-Environment:\`
   - \`Closeout-Gate:\`
   其中 \`Required-Test-Lanes\` 与 \`Required-Acceptance-Item-Ids\` 必须写成可枚举列表；不得只写“see issue”或“follow pre-tests”.
   runtime 会把这组字段结构化写入 delegated intake 与 worker runtime state，所以不要把它们写成只适合人眼理解的散文。
26. 若本轮结论是 manager-only cleanup queue、暂不发 worker，也仍然必须写 manager continuity，至少包含：fleet inventory、route_kind / restart_point / ownership / next_action、cleanup queue 或 frozen queue、以及 next supervision priority。
27. 你的最终回答必须列出本轮新写入的 manager continuity / worker prompt 路径；若没有写这些产物，就不算完成主管交付。
28. 若当前输入包含 delegated continuation、cleanup followthrough、或明确的 project-level restart point，在主 handoff artifact 落盘前不要先 spawn subagent，也不要先等待子任务结果。
29. 先用当前已足够的现场证据写出 primary manager continuity / worker prompts；subagent 只能用于不阻塞首个 handoff 的二次核对或次优先研究。
EOF
)"
  additional_requirements="$(cat <<'EOF'
- 若当前轮次承担项目级监督职责，先基于工位快照安排继续开发、冻结、验证、合并和清理顺序。
- 可并行且互不阻塞的任务，使用 subagent 提高效率。
- 若 `CURRENT_BRANCH` 是 `develop/main/test-pre-merge-*`，当前会话只做主管，不做实现；实现必须委派到 feature worktree。
- 若工位视图缺少准确 issue/phase，不要伪造；先把该工位视为需要进一步核对的监督对象。
- 若当前 AI 响应已经结束、目标进程已退出、命中限额/认证失败、或发生 `context compacted` 需要新进程续接，这类问题一律视为 `runtime-owned`。
- 主管只输出恢复判定和委派；worker 只回写 blocker / continuity；真正的切号、sleep/recheck 和新进程启动由 Freely runtime / scripts 处理。
- 若你编写 shell 命令给 `zsh` 执行，不要把 `status` 当作临时变量名；它在 `zsh` 中是只读特殊变量。需要保存退出码时统一改用 `exit_code`、`cmd_status` 等非保留名字。
- 若活跃 owner 的 issue / progress / pre-tests 只存在于某个 dirty feature worktree，不要在 root `develop` 里直接读取同名相对路径并把 `No such file or directory` 当成 owner 缺失；应先锚定该 feature worktree，再从那个工位读取 owner 真相并生成 handoff。
EOF
)"
  startup_bounded_patrol_rule="$(cat <<'EOF'
启动首轮有界巡检契约：
- 若当前没有 launchable manager continuity、也没有 active worker，先把这轮视为 `fresh_startup_patrol`，不要直接展开全量治理阅读。
- `fresh_startup_patrol` 的首批必读证据只允许包含：
  - `PROJECT_ROOT/AGENTS.md`
  - `machine_readable_scan_json`
  - `./bin/freely live-status --project <project>`
  - `workspace/agents/lead-agent.md`
  - `workspace/skills/context-source-skill/SKILL.md`
- 在写出 primary manager continuity 前，不要整文件读取 `docs/milestones.md`，不要并行展开多个 skill，也不要为每个 surface 预读 issue / progress / pre-brainstorm 原文。
- 首轮先用 `machine_readable_scan_json` 的 active counts 和 summary 选出至多一个 highest-leverage source；只对该 source 做定点核对，再写 primary manager continuity。
- primary manager continuity 必须先回答四件事：`route_kind`、`restart_point`、`ownership`、`next_action`。如果证据仍不足，再把“需要补读的具体文档路径”写进 continuity / queue，而不是在首轮继续扩读。
- 若 scan json 已经证明 backlog 非空，但首轮没有形成 continuity 或 worker prompt，这一轮应视为失败；不要把“继续读更多文档”当作默认下一步。
EOF
)"
  initial_read_targets="$(cat <<EOF
- 项目治理入口：$project/AGENTS.md
- runtime 当前态入口：./bin/freely live-status --project $project
- 结构化巡检入口：machine_readable_scan_json（若 prompt 尾部已给出路径，先消费该 json）
- workspace 根：$workspace_root
- 首跳代理：workspace/agents/lead-agent.md
- 巡检技能：workspace/skills/context-source-skill/SKILL.md

按需再读，不要在首轮默认展开：
- 项目意图：$intent
- 宪法：$constitution
- 里程碑扫描入口：$project/docs/milestones.md
- 工具清单：workspace/tools.md
- 技能索引：workspace/skills/README.md
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

cat <<EOF
你现在进入 Freely 的首跳闭环。

读取约定：
- skill:<name> 只是 workspace 技能文档的引用名，不是当前 CLI 一定存在的原生 tool。默认做法是打开对应的 workspace/skills/<name>/SKILL.md，而不是调用一个名为 skill 的工具。
- workspace/skills/README.md 是技能索引；先从这里确认技能路径，再按需打开具体 SKILL.md。
- 对大型文档不要整文件硬读。尤其 docs/milestones.md，先用 patrol seed、rg、标题定位或分段读取，按命中的 issue / progress / queue 做定点核对。
- 若当前工具的读文件接口支持分页/范围参数，只在确实需要时填写有效值；不要传空字符串。

先读取以下文档或索引：
${initial_read_targets_escaped}

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

执行要求：
1. 先遵守 \`PROJECT_ROOT/AGENTS.md\`；它是当前目标项目的治理入口，不要在 workspace 能力文档里重复发明第二套项目规则。
2. 再完成 \`skill:constitution-guard\` 与 \`skill:laws-enforcer\` 预检：默认做法是阅读 \`workspace/skills/constitution-guard/SKILL.md\` 与 \`workspace/skills/laws-enforcer/SKILL.md\` 并按其约束执行；不要假设存在可直接调用的 \`skill\` 工具。
3. 进入 \`lead-agent\`，不要绕过首跳代理。
4. 由 \`lead-agent\` 参照 \`workspace/skills/context-source-skill/SKILL.md\` 完成需求池扫描、优先级判断与下一跳提示词组装；若当前工具没有原生 skill executor，就直接读取该技能文档并在当前会话按它执行。
4A. 若 runtime 在 prompt 尾部附加了 \`machine_readable_scan_json\`，先把它当作本轮 idle / replan patrol 的结构化入口；其中状态只算 routing hint，phase judgement 仍需回到 linked evidence 核对。
${startup_bounded_patrol_rule_escaped}
5. 若当前轮次承担项目级监督职责，先基于项目级工位视图做排班、冻结、集成与 cleanup 判断；不要直接把自己降级成单工位写代码代理。
${role_scope_rule_5a_escaped}
${role_scope_rule_5b_escaped}
6. 在可并行的 doc-loop、verification、review、日志诊断或互不冲突的代码任务上，使用 subagent 提高效率。
7. 你的需求池至少包括：
   - \`docs/milestones.md\`
   - progress / recovery
   - review / test / acceptance review
   - milestone planning / state maintenance
   - human chat / session evidence
   - github issue
   - \`docs/PROJECT_INTENT.md\`
8. 你需要自主判断：
   - 当前先看哪个池
   - 哪个池优先级更高
   - 当前问题是 \`pre-brainstorm\`、\`issue-bound brainstorm\` 还是 \`issue continuation\`
   - 对暂不能收口的研究项，不允许因为本轮不继续实现就跳过；必须明确它继续停留在 \`candidate_issues\`、issue-bound brainstorm 或 blocked state，并写清 \`next_action\` 与 \`revisit_trigger\`
9. 不要把路由当作脚本硬编码分支；脚本只负责启动和托管 AI，会话中的需求发现与路由判断由你完成。
10. 读取 workspace 下的 agent 与 skill 时，统一按相对路径理解，例如：
   - \`workspace/agents/lead-agent.md\`
   - \`workspace/skills/context-source-skill/SKILL.md\`
   - \`workspace/skills/doc-pre-brainstorm-execution/SKILL.md\`
   - \`workspace/skills/doc-ibm-execution/SKILL.md\`
   - \`workspace/skills/dev-loop-execution/SKILL.md\`
10A. 除非当前工具明确暴露了兼容的原生 skill tool，否则所有 \`skill:<name>\` 都按“去读对应 \`SKILL.md\` 并照此执行”解释。
11. 若没有稳定 issue 边界，下一跳应阅读 \`workspace/skills/doc-pre-brainstorm-execution/SKILL.md\`。
12. 若已有稳定 issue 边界但文档仍需 issue-bound 收敛，下一跳应阅读 \`workspace/skills/doc-ibm-execution/SKILL.md\`。
13. 若 issue 已 ready 或 in-progress，且文档和验收边界足够，下一跳应阅读 \`workspace/skills/dev-loop-execution/SKILL.md\`。
13A. 若当前 route 已收敛为 \`completion_verification\` 或 \`cleanup_governance\`，不要把它伪装成新的 doc-loop / dev-loop；优先由主管在当前 \`auto-loop\` 侧产出 verification / cleanup judgement、continuity 与 handoff，必要时再委派 worker。
13B. 若当前问题本身是 worktree 维护：例如“哪些 worktree 已完成 / 哪些该 merge / 哪些只应退休或保留 research-only / 当前所有 worktree 这轮哪些该 cleanup”，优先阅读 \`workspace/skills/worktree-maintenance-governance/SKILL.md\`，先完成 \`audit / merge_prep / stacked_merge_chain / fleet_closure / retirement_handoff\` 判断，再决定是否进入 doc/dev-loop。
13C. 若当前目标分支不是直接从 \`develop\` 派生，而是依赖未合并父分支，不要直接给出“并入 develop”的结论；先按 \`child -> parent -> merge-prep-from-develop -> develop\` 的 stacked merge-chain 逐层检查。
14. 你需要解释为什么选择当前工具、为什么当前池优先，以及为什么选择当前下一跳。
15. 你负责产出工具选择与下一跳提示词；CLI 的具体无交互启动参数由 Freely runtime 按 \`workspace/tools.md\` 与 \`workspace/scripts/monitor-ai-cli.sh\` 的约定执行，不要自行发明另一套命令格式。
${execution_rule_15_escaped}
${execution_rule_16_escaped}
${execution_rule_17_escaped}
${manager_artifact_rule_escaped}

补充要求：
${additional_requirements_escaped}
EOF
