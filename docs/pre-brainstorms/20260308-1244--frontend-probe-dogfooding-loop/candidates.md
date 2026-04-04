# Candidates - 20260308-1244--frontend-probe-dogfooding-loop

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260308-1244-01
- title: Freely Internal Frontend/Backend Architecture Review
- problem: 之前的“前后端分离”研究更偏方向性，尚未把 Freely 当前桌面工具形态下的内部前后端边界重新评审清楚，容易把边界过早等同于远端 HTTP 服务。
- why_now: 如果不先把内部边界思想收敛清楚，后续 API、Probe 和实现层都会建立在模糊假设上。
- acceptance_hint: 明确 Tauri 桌面工具内部的 frontend/backend 职责边界、状态归属、命令/事件流模型、可插拔协议层分层，以及未来迁移到多进程/远端时保持兼容的原则。
- priority: P0
- status: promoted
- decision_reason: 这是这轮重评项目架构的总入口，先把“前后端是解耦思想，不等于 day-1 分布式部署”落成正式 issue。
- promoted_issue_path: docs/epics/frontend-probe-dogfooding-loop/internal-frontend-backend-architecture-review/issues/internal-frontend-backend-architecture-review.md
- legacy_id_mapping: I-20260308-1245  # 历史遗留的 issue id
- milestone: M-20260308-frontend-probe-dogfooding-loop
- session_refs: []

### C-20260308-1244-02
- title: Frontend/Backend Boundary Contract v1 for Frontend Probe
- problem: 前后端解耦方向已形成共识，但 Probe day-1 真正依赖的边界契约仍未冻结，后端实现缺少稳定验收面。
- why_now: 如果不先冻结最小边界契约，Probe 会反复追着后端改，无法形成持续狗粮闭环。
- acceptance_hint: 明确 sessions / stream / history / status 的最小调用面、事件语义与错误面；前端只通过该边界访问系统；第一阶段允许采用 Tauri 内部 contract layer，不引入 Node.js。
- priority: P0
- status: promoted
- decision_reason: 这是“前端从第一天可用”与“后端仍保持解耦”同时成立的最小契约，也避免把 day-1 方案误锁为某种网络部署形态。
- promoted_issue_path: docs/epics/frontend-probe-dogfooding-loop/frontend-backend-boundary-contract-v1-for-frontend-probe/issues/frontend-backend-boundary-contract-v1-for-frontend-probe.md
- legacy_id_mapping: I-20260317-1001  # 历史遗留的 issue id
- milestone: M-20260308-frontend-probe-dogfooding-loop
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "doc-ibm"}]

### C-20260308-1244-03
- title: Frontend Probe v0
- problem: 没有一个极薄但可运行的产品面，后端增量只能靠文档、脚本和日志验收，无法及时发现 AI 跑偏。
- why_now: Freely 必须从第一阶段就具备“可观察、可打断、可回放”的狗粮能力。
- acceptance_hint: 提供最薄的 Tauri + React + TypeScript Probe，覆盖 project switch、session create/resume、message input、stream output、status、stop/retry；前端运行时使用 Bun，不走 Node.js。
- priority: P0
- status: promoted
- decision_reason: 这是把“防止 AI 跑偏”落成产品能力的最直接载体，也是 Freely 自举开发自己的必需面。
- promoted_issue_path: docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md
- milestone: M-20260308-frontend-probe-dogfooding-loop
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "doc-ibm"}]

### C-20260308-1244-04
- title: Incremental Dogfooding Gate for Backend Increments
- problem: 即使有 Probe 和边界契约，如果没有正式门禁，团队仍可能先堆很多后端能力，最后才补前端验证。
- why_now: 需要把“后端每个增量都要在 Probe 中验证”固化为 Freely 自举治理的一部分。
- acceptance_hint: 定义后端能力进入完成态前必须具备的 Probe 验证证据、回写位置和阻断条件。
- priority: P0
- status: promoted
- decision_reason: 它把这次讨论从“开发建议”提升为“Freely 自己必须具备的产品与治理能力”。
- promoted_issue_path: docs/epics/frontend-probe-dogfooding-loop/incremental-dogfooding-gate-for-backend-increments/issues/incremental-dogfooding-gate-for-backend-increments.md
- milestone: M-20260308-frontend-probe-dogfooding-loop
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "doc-ibm"}]
