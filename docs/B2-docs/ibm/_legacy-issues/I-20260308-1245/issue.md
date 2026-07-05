---
local_id: I-20260308-1245
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '5'
    url: https://github.com/chatterzhao/freely/issues/5
    synced_at: '2026-04-27T11:12:11Z'
  gitee:
    issue_id: IJFO4H
    url: https://gitee.com/zhaoquan/freely/issues/IJFO4H
    synced_at: '2026-04-27T13:13:14Z'
primary_platform: github
canonical_issue_path: docs/epics/frontend-probe-dogfooding-loop/internal-frontend-backend-architecture-review/issues/internal-frontend-backend-architecture-review.md
last_synced_comment_at:
  github: '2026-04-27T11:12:11Z'
hash: ''
created_at: '2026-04-27T11:12:11Z'
updated_at: '2026-04-27T11:12:11Z'
platform_state: closed
---

# Issue: internal-frontend-backend-architecture-review

- issue_id: `I-20260308-1245`
- title: Freely 内部前后端架构复评与可插拔协议边界
- phase_state: `completed`
- milestone: `M-20260308-frontend-probe-dogfooding-loop`
- epic-name: `frontend-probe-dogfooding-loop`
- story-name: `internal-frontend-backend-architecture-review`
- issue-name: `internal-frontend-backend-architecture-review`
- verification_artifact_dir: `docs/epics/frontend-probe-dogfooding-loop/internal-frontend-backend-architecture-review/code-reviews`
- source_candidate: `docs/B1-docs/raw-20260308-1244/candidates.md#c-20260308-1244-01`
- source_brainstorm: `docs/B1-docs/raw-20260308-1244/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `none`
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "analysis"}]

## Why

重新评审 Freely 当前产品形态下的前后端边界，确保：

- “前后端”首先是一种内部解耦思想，而不是 day-1 就要求远端服务化
- Freely 可以先作为带终端的桌面开发工具落地，但内部仍保持明确 frontend/backend 边界
- 协议层从第一版开始可插拔，不把 UI 和 backend 绑定到单一 transport
- 后续切换到 WS、sidecar 或远端服务时，不需要推翻第一版 Frontend Probe
- 人类在 loop 中默认不阻塞，但依然拥有高优先级纠偏入口
- UI 要把多个 AI 执行单元呈现成“一个团队”，让人能观察谁在做什么、做到哪一步、是否阻塞

## Scope

1. 明确 Tauri 桌面工具内部的 frontend / backend 职责边界。
2. 明确哪些状态由 frontend 持有，哪些状态必须由 backend 持有。
3. 收敛 day-1 命令面、事件流和快照面。
4. 定义可插拔协议分层：
   - frontend contract
   - transport adapter
   - backend service contract
5. 约束第一阶段技术栈与运行时：
   - Rust
   - Tauri
   - Bun
   - React
   - TypeScript
   - 不引入 Node.js 作为产品运行时
6. 定义“Freely 何时达到可自治开发并开始自己开发自己”的 MVP 里程碑。
7. 定义人类控制面：
   - 启动
   - 暂停
   - 终止
   - resume
   - chat input 介入
8. 定义多输入源优先级模型，至少覆盖：
   - human chat input
   - auto-loop generated actions
   - recovery / monitor signals
   - system-triggered governance events
9. 定义 AI 团队态势 UI 的最小展示模型。

## Acceptance

- issue-bound 文档明确 day-1 形态下的 frontend/backend 边界，不把“边界”误写成“必须远端 HTTP 化”。
- issue-bound 文档明确 `ClientCommand`、`ServerEvent`、`Snapshot`
