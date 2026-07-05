---
local_id: I-20260308-0101
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '3'
    url: https://github.com/chatterzhao/freely/issues/3
    synced_at: '2026-04-27T11:12:01Z'
  gitee:
    issue_id: IJFO4D
    url: https://gitee.com/zhaoquan/freely/issues/IJFO4D
    synced_at: '2026-04-27T13:13:11Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/state-sync-and-session-evidence-governance/issues/state-sync-and-session-evidence-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:12:01Z'
hash: ''
created_at: '2026-04-27T11:12:01Z'
updated_at: '2026-04-27T11:12:01Z'
platform_state: closed
---

# Issue: state-sync-and-session-evidence-governance

- issue_id: `I-20260308-0101`
- title: 状态联动、流程标识词典与 session evidence 传播治理
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `state-sync-and-session-evidence-governance`
- issue-name: `state-sync-and-session-evidence-governance`
- verification_artifact_dir: `docs/epics/- epic-name: `workspace-routing-foundation`/- story-name: `state-sync-and-session-evidence-governance`/code-reviews`
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

## IBM Ha
