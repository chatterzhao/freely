---
local_id: I-20260308-1631
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '6'
    url: https://github.com/chatterzhao/freely/issues/6
    synced_at: '2026-04-27T11:12:15Z'
  gitee:
    issue_id: IJFO4I
    url: https://gitee.com/zhaoquan/freely/issues/IJFO4I
    synced_at: '2026-04-27T13:13:15Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/stage-prefixed-progress-identifier/issues/stage-prefixed-progress-identifier.md
last_synced_comment_at:
  github: '2026-04-27T11:12:15Z'
hash: ''
created_at: '2026-04-27T11:12:15Z'
updated_at: '2026-04-27T11:12:15Z'
platform_state: closed
---

# Issue: stage-prefixed-progress-identifier

- issue_id: `I-20260308-1631`
- title: 阶段前缀式主进度标识治理
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `stage-prefixed-progress-identifier`
- issue-name: `stage-prefixed-progress-identifier`
- source_candidate: `docs/pre-brainstorms/20260308-1630--stage-prefixed-progress-identifier/candidates.md#c-20260308-1631`
- source_brainstorm: `docs/pre-brainstorms/20260308-1630--stage-prefixed-progress-identifier/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `docs/epics/workspace-routing-foundation/state-sync-and-session-evidence-governance/issues/state-sync-and-session-evidence-governance.md`
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "analysis"}]

## Why

Freely 当前还在使用 `in_progress` / `completed` 这类泛化状态词，无法从值本身读出 IBM、dev、verification 等执行阶段。对于 AI 自治系统，这会增加路由猜测成本，降低状态机可读性和可执行性。

## Scope

1. 定义阶段前缀式主进度标识，例如 `todo_ibm`、`in_ibm`、`done_ibm`、`in_dev`。
2. 明确阶段前缀固定为 `todo/in/done/blocked`，而 `completed` 只用于整个 issue 生命周期终态。
3. 明确 `pending_*`、`ready_*`、`todo_for_*` 不进入主词典。
4. 收紧 `milestone_state`，让它只表达 milestone 队列归属。
5. 设计 `loop_stage` / `status` 到新主标识的迁移路径，并用状态流转图表达 handoff 与 blocked/recovery 续接规则。

## Acceptance

- 主进度词典中不再以 `in_progress` / `active` 作为主执行状态。
- `todo_*` 与 `pending_*` 不同时作为“未开始”主状态并存，且本轮结论是不采用 `pending_*`。
- `done_*` 只表示阶段完成，`completed` 只表示整个 issue 生命周期完成。
- `done_ibm` 作为 IBM->dev handoff 真源，不保留 `ready_for_dev` / `todo_for_dev`。
- 可以从单个主进度值读出阶段，不再依赖 `status + loop_stage` 拼读。
- `milestone_state` 的职责边界与主进度标识分离清晰。

## Completion

- `docs/LAWS.md` 已把 `phase_state` 收紧为主执行标识词典，并定义 `todo/in/done/blocked/completed` 的边界。
- `docs/PROJECT_INTENT.md` 与 `docs/milestones.md` 已改为按 `phase_state` 路由，不再把 `status + loop_stage` 作为主执行态。
- `docs/system/workspace/skills/context-source-skill/SKILL.md`、`docs/system/workspace/skills/doc-ibm-executi
