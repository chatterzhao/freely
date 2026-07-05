---
local_id: I-20260317-1001
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '11'
    url: https://github.com/chatterzhao/freely/issues/11
    synced_at: '2026-04-27T11:12:36Z'
  gitee:
    issue_id: IJFO4Y
    url: https://gitee.com/zhaoquan/freely/issues/IJFO4Y
    synced_at: '2026-04-27T13:13:51Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/human/tui/issues/frontend-backend-boundary-contract-v1-for-frontend-probe.md
last_synced_comment_at:
  github: '2026-04-27T11:12:36Z'
hash: ''
created_at: '2026-04-27T11:12:36Z'
updated_at: '2026-04-27T11:12:36Z'
platform_state: closed
---

# Issue: frontend-probe-v0

- issue_id: `I-20260308-1244-03`
- title: Frontend Probe v0
- phase_state: `completed`
- milestone: `M-20260308-frontend-probe-dogfooding-loop`
- epic-name: `frontend-probe-dogfooding-loop`
- story-name: `frontend-probe-v0`
- issue-name: `frontend-probe-v0`
- source_candidate: `docs/B1-docs/raw-20260308/candidates.md#c-20260308-1244-03`
- source_brainstorm: `docs/B1-docs/raw-20260308/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/human/tui/pre-tests.md`
- verification_artifact_dir: `docs/B2-docs/human/tui/code-reviews`
- depends_on: `none`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "doc-ibm"}

## Why

在 `Frontend/Backend Boundary Contract v1` 已冻结后，Freely 仍缺少一个极薄但真正可运行的产品面：

- 人类还不能在同一产品界面里观察、打断和回放 run
- 后端增量仍容易只靠脚本与日志验收
- Freely 还不能通过自己的 Probe day-1 能力来开发自己

## Scope

1. 收敛 `Frontend Probe v0` 的最小产品范围。
2. 基于现有 boundary contract 明确 Probe 必需的 UI 面板与交互流。
3. 明确 Probe 只消费 `ClientCommand` / `ServerEvent` / `Snapshot`，不侵入 backend 内部实现。
4. 锁定 day-1 技术栈为 Tauri + React + TypeScript + Bun。

## Acceptance

- 文档明确 Probe v0 至少包含：project switch、session create/resume、message input、stream output、status、stop/retry/resume。
- 文档明确 day-1 主入口是应用内终端 / 控制台，而不是外部 shell。
- 文档明确 `control bar`、`chat intervention panel`、`agent roster`、`embedded terminal` 的最小职责。
- 文档明确 Probe 只通过 boundary contract 调用 backend，不直接读取 runtime/workspace。
- 文档明确实现进入 dev-loop 前所需的最小 UI 与 contract 依赖。

## Minimal UI surface

### Control bar

- actions:
  - `start`
  - `pause`
  - `terminate`
  - `resume`
  - `retry`
- backend dependency:
  - `ControlRun`

### Chat intervention panel

- responsibilities:
  - 输入人类消息
  - 显示最近一次介入结果
  - 提示高优先级纠偏语义
- backend dependency:
  - `SendChatIntervention`
  - `InputArbitr
