# Issue: state-sync-and-session-evidence-governance

- issue_id: `I-20260308-0101`
- title: 状态联动、流程标识词典与 session evidence 传播治理
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `state-sync-and-session-evidence-governance`
- issue-name: `state-sync-and-session-evidence-governance`
- verification_artifact_dir: `docs/B2-docs/- epic-name: `workspace-routing-foundation`/- story-name: `state-sync-and-session-evidence-governance`/code-reviews`
- source_candidate: `docs/B1-docs/raw-20260308/candidates.md#c-20260308-0101`
- source_brainstorm: `docs/B1-docs/raw-20260308/brainstorms.md`
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
  - `docs/B2-docs/ibm/state-sync-and-session-evidence-governance/code-reviews/20260316-state-sync-verification.md`
  - `docs/B2-docs/ibm/state-sync-and-session-evidence-governance/code-reviews/20260317-lead-agent-reentry-verification.md`
  - `docs/B2-docs/ibm/state-sync-and-session-evidence-governance/code-reviews/20260326-state-sync-canonical-replay-verification.md`
- 当前研究阶段尚未启用正式 `docs/progress/**`，本轮等价执行证据写入 `docs/B1-docs/raw-CONVERGENCE.md`。

## Verification Summary

- canonical replay 证明 `LAWS`、`PROJECT_INTENT`、`milestones.md` 与核心 skills 仍一致引用 `source_class / route_kind / phase_state / runtime_state / session_refs`，且 `done_ibm -> in_dev -> in_verification -> completed` 的 handoff 口径没有回退。
- 早先把 issue 卡在 `in_verification` 的两个理由都已失效：`governance-check` 现已在当前环境通过，`dirty=1` 也只是旧 verification worktree 的现场快照，不是当前 canonical truth 的能力缺口。
- 研究阶段未启用正式 `docs/progress/**` 属于当批次的治理现实，不再构成阻塞；当前收口证据由 issue 和 code review 补齐即可。
- 当前批次据此把本 issue 关闭为 `completed`；后续若要继续扩状态词典或 session evidence contract，应通过新 lifecycle 承接。
