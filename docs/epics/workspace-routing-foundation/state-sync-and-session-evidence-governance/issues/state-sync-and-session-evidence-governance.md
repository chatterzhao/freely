# Issue: state-sync-and-session-evidence-governance

- issue_id: `I-20260308-0101`
- title: 状态联动、流程标识词典与 session evidence 传播治理
- phase_state: `in_verification`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `state-sync-and-session-evidence-governance`
- issue-name: `state-sync-and-session-evidence-governance`
- source_candidate: `docs/pre-brainstorms/20260308-0145--state-sync-and-session-evidence-governance/candidates.md#c-20260308-0101`
- source_brainstorm: `docs/pre-brainstorms/20260308-0145--state-sync-and-session-evidence-governance/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `none`
- session_refs:
  - {tool: codex, session_id: "019ccaa2-2f48-7782-a713-7d6d6d325030", jsonl_path: "unavailable://codex-thread-only", role: "analysis"}
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "lead-agent-reentry"}

## Why

收紧 Freely 自举里的状态同步规则，确保：

- 流程标识有唯一事实源
- candidate / milestone / issue / progress / recovery 的联动更新有固定矩阵
- IBM 阶段与 dev-loop 阶段不会继续共用模糊的 `in_progress`
- 会话证据能从 pre-brainstorm 传播到 issue、progress 与 recovery

## Scope

1. 在 `LAWS` 中建立流程标识词典与状态联动矩阵。
2. 更新 `PROJECT_INTENT`，明确规范语义来源和 session evidence 传播要求。
3. 更新 `milestones.md` policy，区分 `phase_state=in_ibm` 与 `phase_state=in_dev`。
4. 更新核心 skills，使它们引用同一套标识和同步要求。
5. 为当前 active milestone 增加一个示范性的状态同步治理 issue。

## Acceptance

- `LAWS` 明确 `source_class`、`route_kind`、`phase_state`、`runtime_state`、`session_refs` 的规范语义。
- 至少定义以下联动：`discovery -> pre_brainstorm`、`candidate -> milestone-owned issue`、`in_ibm -> done_ibm`、`done_ibm -> in_dev`、`recovery`、`completed`。
- `milestones.md` 不再把所有 `in_progress` 一律要求绑定 `progress`。
- `session_refs` 的最小字段统一为 `tool/session_id/jsonl_path/role`，缺 jsonl 路径时有显式 fallback。

## IBM Handoff

- implementation_scope_summary:
  - 继续承接已经落盘的 `LAWS`、`PROJECT_INTENT`、`milestones.md` 与核心 skills 改动，不重新发明状态词典或 session evidence 语义。
  - 进入实现时优先验证正式产物是否统一使用 `source_class / route_kind / phase_state / runtime_state / session_refs`，并确保 `done_ibm -> in_dev` handoff 口径一致。
- required_doc_refs:
  - `docs/LAWS.md`
  - `docs/PROJECT_INTENT.md`
  - `docs/milestones.md`
  - `docs/system/workspace/skills/context-source-skill/SKILL.md`
  - `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`
  - `docs/system/workspace/skills/dev-loop-execution/SKILL.md`

## Next

- 2026-03-16 fresh session handoff 已重新执行 `constitution-guard -> laws-enforcer -> lead-agent -> context-source-skill`。
- 需求池优先级仍为 `milestones > progress/recovery(等价 continuity) > review/test > human chat/session evidence > github issue > PROJECT_INTENT`。
- 当前问题仍判定为 `issue continuation`，下一跳仍为 `skill:dev-loop-execution` 下的 `completion_verification`，不回退到 `pre-brainstorm` 或 `doc-ibm-execution`。
- `selected_tool=codex` 与当前 `AI_TOOL` 相同，因此本轮只继续维护 verification continuity，不把 `next_prompt` 当作 handoff 结束。

## Verification

- 当前验证重点是：正式治理产物是否一致引用 `source_class / route_kind / phase_state / runtime_state / session_refs`，并且 committed issue 的 handoff 已统一到 `done_ibm -> dev-loop / in_verification -> completed` 口径。
- 已执行验证检查：
  - `rg -n "source_class|route_kind|phase_state|runtime_state|session_refs|done_ibm -> in_dev|in_verification|completion verification" docs/LAWS.md docs/PROJECT_INTENT.md docs/milestones.md docs/system/workspace/skills/context-source-skill/SKILL.md docs/system/workspace/skills/doc-ibm-execution/SKILL.md docs/system/workspace/skills/dev-loop-execution/SKILL.md`
- 已写入 review 证据：
  - `docs/epics/workspace-routing-foundation/state-sync-and-session-evidence-governance/code-reviews/20260316-state-sync-verification.md`
  - `docs/epics/workspace-routing-foundation/state-sync-and-session-evidence-governance/code-reviews/20260317-lead-agent-reentry-verification.md`
- 当前研究阶段尚未启用正式 `docs/progress/**`，本轮等价执行证据写入 `docs/pre-brainstorms/CONVERGENCE.md`。

## Next

- 2026-03-17 首跳闭环复核已再次执行 `constitution-guard -> laws-enforcer -> lead-agent -> context-source-skill`。
- 需求池优先级仍为 `milestones > progress/recovery(等价 continuity) > review/test > human chat/session evidence > github issue > PROJECT_INTENT`。
- 当前问题继续判定为 `issue continuation`，不回退到 `pre-brainstorm` 或 issue-bound brainstorm。
- `selected_tool=codex`，因为当前动作仍是仓库内 verification continuity 回写；`target_skill_or_loop=skill:dev-loop-execution`，具体 route 为 `completion_verification`。
- 本轮新增检查结果：
  - `./bin/wt-status-all` 仍返回 `Summary: total=6, dirty=1`
  - `./bin/governance-check` 当前在本机环境下因 `mapfile` / `find -printf` 兼容性失败，不能计作通过证据
- 需求池缺席/未命中事实：
  - `progress/recovery`: `find docs -maxdepth 2 \( -type d -name progress -o -type d -name recovery \) -print` 无输出，说明研究阶段仍未启用正式 continuity 目录
  - `github issue`: 仓库内仅存在 policy / brainstorm 对 `github-issue` 的规则描述，当前没有比 milestone continuation 更高优先的本地 issue 落点
- 当前 dirty blocker 不是单个零散文件，而是仍包含多类未提交改动：
  - `docs/system/workspace/**` 与 `tests/**` 下的 runtime / monitor / tests 改动
  - `docs/epics/workspace-routing-foundation/**` 下的 verification / review / issue 文档改动
  - `docs/pre-brainstorms/**` 下的新 session-rotation / first-hop 研究与 continuity 留痕
- 保持 `in_verification`。`./bin/wt-status-all` 已确认当前 `feature/dogfood-codex-auto-20260316` worktree 仍为 `DIRTY`，因此本轮不能进入 promote / cleanup；待 worktree 清洁并补齐 completion verification / cleanup 证据后再进入 `completed`。
