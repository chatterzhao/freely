# Candidates - 20260308-1244--frontend-probe-dogfooding-loop

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260308-1244-A: legacy issue
- title: Freely Internal Frontend/Backend Architecture Review
- problem: 之前的“前后端分离”研究更偏方向性，尚未把 Freely 当前桌面工具形态下的内部前后端边界重新评审清楚，容易把边界过早等同于远端 HTTP 服务。
- why_now: 如果不先把内部边界思想收敛清楚，后续 API、Probe 和实现层都会建立在模糊假设上。
- acceptance_hint: 明确 Tauri 桌面工具内部的 frontend/backend 职责边界、状态归属、命令/事件流模型、可插拔协议层分层，以及未来迁移到多进程/远端时保持兼容的原则。
- priority: P0
- status: completed
- decision_reason: 这条架构总入口已经 materialize 为正式 owner，并由 `I-20260308-1245` 完成 canonical closeout。当前 candidate 仅保留为来源 provenance，不再代表活跃待办。
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260308-1244-A/issue.md
- legacy_id_mapping: I-20260308-1245  # 历史遗留的 issue id
- milestone: M-20260308-1244-A
- next_action: 保留为历史来源记录。若未来前后端边界或可插拔协议层需要重新总论收敛，应从当前 canonical truth 新开 candidate/issue，而不是恢复这条 candidate。
- completion_note: `I-20260308-1245` 已完成 canonical closeout；frontend/backend 边界、状态归属矩阵与协议分层已被下游 boundary/probe/bridge owner 复用，因此该 candidate 不再构成活跃 queue。
- session_refs: []

### C-20260308-1244-A: legacy issue
- title: Frontend/Backend Boundary Contract v1 for Frontend Probe
- problem: 前后端解耦方向已形成共识，但 Probe day-1 真正依赖的边界契约仍未冻结，后端实现缺少稳定验收面。
- why_now: 如果不先冻结最小边界契约，Probe 会反复追着后端改，无法形成持续狗粮闭环。
- acceptance_hint: 明确 sessions / stream / history / status 的最小调用面、事件语义与错误面；前端只通过该边界访问系统；第一阶段允许采用 Tauri 内部 contract layer，不引入 Node.js。
- priority: P0
- status: completed
- decision_reason: 这条最小 boundary contract 候选已经 materialize 为正式 owner，并由 `I-20260317-1001` 完成 canonical closeout。当前 candidate 仅保留为来源 provenance，不再代表活跃待办。
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260308-1244-A/issue.md
- legacy_id_mapping: I-20260317-1001  # 历史遗留的 issue id
- milestone: M-20260308-1244-A
- next_action: 保留为历史来源记录。若未来 Probe 边界契约需要新的对象族、transport 兼容层或错误面扩展，应从当前 canonical truth 新开 candidate/issue，而不是恢复这条 candidate。
- completion_note: `I-20260317-1001` 已完成 canonical closeout；最小 boundary contract 已被 `frontend-probe-v0` 与 `rust-tauri-probe-bridge-v1` 直接复用，因此该 candidate 不再构成活跃 queue。
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "doc-ibm"}]

### C-20260308-1244-A: legacy issue
- title: Frontend Probe v0
- problem: 没有一个极薄但可运行的产品面，后端增量只能靠文档、脚本和日志验收，无法及时发现 AI 跑偏。
- why_now: Freely 必须从第一阶段就具备“可观察、可打断、可回放”的狗粮能力。
- acceptance_hint: 提供最薄的 Tauri + React + TypeScript Probe，覆盖 project switch、session create/resume、message input、stream output、status、stop/retry；前端运行时使用 Bun，不走 Node.js。
- priority: P0
- status: completed
- decision_reason: 这条 probe 候选已经 materialize 为正式 owner，并由 `I-20260308-1244-03` 完成 canonical closeout。当前 candidate 仅保留为来源 provenance，不再代表活跃待办。
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260308-1244-A/issue.md
- milestone: M-20260308-1244-A
- next_action: 保留为历史来源记录。若未来要继续扩展 frontend UX、multi-project shell 或更宽的交互闭环，应从当前 canonical truth 新开 candidate/issue，而不是恢复这条 candidate。
- completion_note: `I-20260308-1244-03` 已完成 canonical closeout；day-1 probe surface 与真实 `Transport=tauri` 闭环已经吸收到 `develop`，因此该 candidate 不再构成活跃 queue。
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "doc-ibm"}]

### C-20260308-1244-A: legacy issue
- title: Incremental Dogfooding Gate for Backend Increments
- problem: 即使有 Probe 和边界契约，如果没有正式门禁，团队仍可能先堆很多后端能力，最后才补前端验证。
- why_now: 需要把“后端每个增量都要在 Probe 中验证”固化为 Freely 自举治理的一部分。
- acceptance_hint: 定义后端能力进入完成态前必须具备的 Probe 验证证据、回写位置和阻断条件。
- priority: P0
- status: completed
- decision_reason: 这条门禁候选已经 materialize 为正式 owner，并由 `I-20260317-1003` 的 canonical closeout 写回 completed。当前 candidate 只保留为历史 provenance，不再代表待执行 owner。
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260308-1244-A/issue.md
- legacy_id_mapping: I-20260317-1003  # 历史遗留的 issue id
- milestone: M-20260308-1244-A
- next_action: 保留为历史来源记录。后续若 backend increment review gate 需要扩展到更强 enforcement 或新的 probe 能力，应从当前 canonical truth 新开 candidate/issue。
- completion_note: `I-20260317-1003` 已从 parked `done_ibm` owner 显式收口为 completed，并补齐 progress、verification 与 milestone writeback；该 candidate 不再构成活跃 queue。
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "doc-ibm"}]
