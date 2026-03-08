# Issue: state-sync-and-session-evidence-governance

- issue_id: `I-20260308-0101`
- title: 状态联动、流程标识词典与 session evidence 传播治理
- status: in_progress
- loop_stage: `ibm`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `state-sync-and-session-evidence-governance`
- issue-name: `state-sync-and-session-evidence-governance`
- source_candidate: `docs/pre-brainstorms/20260308-0145--state-sync-and-session-evidence-governance/candidates.md#c-20260308-0101`
- source_brainstorm: `docs/pre-brainstorms/20260308-0145--state-sync-and-session-evidence-governance/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `none`
- session_refs: [{tool: codex, session_id: "019ccaa2-2f48-7782-a713-7d6d6d325030", jsonl_path: "unavailable://codex-thread-only", role: "analysis"}]

## Why

收紧 Freely 自举里的状态同步规则，确保：

- 流程标识有唯一事实源
- candidate / milestone / issue / progress / recovery 的联动更新有固定矩阵
- IBM 阶段与 dev-loop 阶段不会继续共用模糊的 `in_progress`
- 会话证据能从 pre-brainstorm 传播到 issue、progress 与 recovery

## Scope

1. 在 `LAWS` 中建立流程标识词典与状态联动矩阵。
2. 更新 `PROJECT_INTENT`，明确规范语义来源和 session evidence 传播要求。
3. 更新 `milestones.md` policy，区分 `loop_stage=ibm` 与 `loop_stage=dev_in_progress`。
4. 更新核心 skills，使它们引用同一套标识和同步要求。
5. 为当前 active milestone 增加一个示范性的状态同步治理 issue。

## Acceptance

- `LAWS` 明确 `source_class`、`route_kind`、`loop_stage`、`runtime_state`、`session_refs` 的规范语义。
- 至少定义以下联动：`discovery -> pre_brainstorm`、`candidate -> milestone-owned issue`、`ibm -> ready_for_dev`、`ready_for_dev -> dev_in_progress`、`recovery`、`completed`。
- `milestones.md` 不再把所有 `in_progress` 一律要求绑定 `progress`。
- `session_refs` 的最小字段统一为 `tool/session_id/jsonl_path/role`，缺 jsonl 路径时有显式 fallback。

## Next

- 收紧规则和技能文档后，回看当前 milestone 中已发生但未同步的条目，决定哪些应补 issue materialization、哪些应直接 completion verification。
