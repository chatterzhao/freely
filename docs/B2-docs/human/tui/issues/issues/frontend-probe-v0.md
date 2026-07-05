# Issue: frontend-probe-v0

- issue_id: `I-20260308-1244-03`
- title: Frontend Probe v0
- phase_state: `completed`
- milestone: `M-20260308-frontend-probe-dogfooding-loop`
- epic-name: `frontend-probe-dogfooding-loop`
- story-name: `frontend-probe-v0`
- issue-name: `frontend-probe-v0`
- source_candidate: `docs/B1-docs/raw-20260308T163000Z/candidates.md#c-20260308-1244-03`
- source_brainstorm: `docs/B1-docs/raw-20260308T163000Z/brainstorms.md`
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
  - `InputArbitrationRecorded`

### Agent roster

- responsibilities:
  - 展示 active agents / runs
  - 展示当前阶段、最近动作、阻塞原因
- backend dependency:
  - `AgentStatusChanged`
  - `RunStatusChanged`
  - `Snapshot.active_agents`

### Embedded terminal

- responsibilities:
  - 展示流式输出
  - 附着到当前 terminal target
  - 支持 resume 后重新附着
- backend dependency:
  - `AttachTerminal`
  - `TerminalChunkAppended`
  - `Snapshot.terminal_targets`

## Minimal interaction flows

1. project switch
   - 选择项目
   - 请求 `Snapshot`
   - 渲染该项目的 active sessions / runs
2. session create / resume
   - 调用 `CreateOrResumeSession`
   - 接收 `SessionUpserted`
   - 若存在 run，则继续显示 `RunStatusChanged`
3. message input
   - 发送 `SendChatIntervention`
   - 在 panel 中显示仲裁结果
4. stream observation
   - 调用 `AttachTerminal`
   - 持续渲染 `TerminalChunkAppended`
5. stop / retry / resume
   - 通过 `ControlRun` 发起
   - 等待 `RunStatusChanged` 回写结果

## Ready-for-dev boundary

- layout 只冻结最小 panel 组合，不进入高保真视觉系统
- 不要求完整多项目工作台
- 不要求复杂历史搜索或 memory 面板
- 只要上述交互流与 boundary contract 依赖已稳定，就可进入实现

## IBM Handoff

- implementation_scope_summary:
  - 继续承接 `I-20260317-1001` 已冻结的 boundary contract，把 Probe 的最小产品面收敛成可实现 issue。
  - 当前阶段仍是 issue-bound IBM 收敛，不进入前端实现代码。
- required_doc_refs:
  - `docs/B2-docs/human/tui/issues/frontend-backend-boundary-contract-v1-for-frontend-probe.md`
  - `docs/B2-docs/human/tui/brainstorms/b-frontend-probe-v0.md`
  - `docs/B2-docs/human/tui/prd.md`
  - `docs/B2-docs/human/tui/pre-tests.md`
  - `docs/B2-docs/human/tui/tasks.md`

## Next

- 当前 owner 已完成 canonical closeout；后续若继续扩大 frontend UX、multi-project workbench 或更高保真 control surface，另开新 lifecycle。

## Dev Loop

- current_impl_files:
  - `src/frontend_probe_v0/contracts.ts`
  - `src/frontend_probe_v0/panels.ts`
  - `src/frontend_probe_v0/mockSnapshot.ts`
  - `src/frontend_probe_v0/AppShell.tsx`
  - `src/frontend_probe_v0/adapter.ts`
  - `src/frontend_probe_v0/tauriAdapter.ts`
  - `src/frontend_probe_v0/createAdapter.ts`
  - `src/frontend_probe_v0/commands.ts`
  - `src/frontend_probe_v0/useProbeRuntime.ts`
  - `src/frontend_probe_v0/useProbeControls.ts`
  - `src/frontend_probe_v0/events.ts`
  - `src/frontend_probe_v0/useProbeEvents.ts`
  - `src/frontend_probe_v0/useProbeTerminalAttach.ts`
  - `src/frontend_probe_v0/bootstrap.tsx`
  - `src/frontend_probe_v0/entry.ts`
  - `src/frontend_probe_v0/mount.tsx`
  - `src/frontend_probe_v0/host.tsx`
- current_status:
  - 已具备 contract、panel model、mock snapshot、shell、control actions、event seam、Tauri bridge skeleton、adapter factory、bootstrap / entry / mount / host 入口
  - `useProbeRuntime` 已改为稳定保留首次注入的 adapter，避免 render 期间反复重建 adapter 导致 snapshot 请求循环抖动
  - `mount` / `host` 已改为向宿主 render React element，而不是把组件类型直接当作 render payload
  - `MockProbeAdapter` 已从静态只读 snapshot 推进为最小 stateful mock，可对 `ControlRun` 产出 `RunStatusChanged` / `AgentStatusChanged` / `TerminalChunkAppended`
  - `useProbeRuntime` 现会在 adapter 事件到达后自动 refresh snapshot；`TauriProbeAdapter.subscribe` 也已改成适配 React effect cleanup 的同步退订形式
  - `AppShell` 现已把四个最小 panel 从 summary 文本推进到具体视图：control bar 显示当前 run，chat panel 显示 session / recent decisions，agent roster 显示 phase / lastAction / blocker，embedded terminal 显示 attachable target 与 recent stream
  - `chat intervention panel` 现已具备最小输入路径：用户可提交 intervention draft，mock adapter 会回写 `InputArbitrationRecorded`，并把介入内容反映到 recent decisions 与 agent lastAction
  - `session create/resume` 现已具备最小交互路径：UI 可触发 `CreateOrResumeSession`，mock adapter 会回写 `SessionUpserted`
  - `project switch` 现已具备最小交互路径：UI 可切换当前 `projectId`，并驱动后续 snapshot / control / session / chat 操作一起切换上下文
  - `MockProbeAdapter` 现按 `projectId` 分桶维护 snapshot；project switch 不再只是切换 label，而是切到不同 project 的 run/session/terminal state
  - header 现会展示 `projectName`、`governanceSummary` 与 `recoverySummary`；event buffer 也已收紧为有限窗口，避免 Probe 自己无限堆积事件
  - `governanceSummary` 与 `recoverySummary` 现在会随 mock runtime 动作变化：session upsert / chat intervention 会刷新 governance summary，pause 会刷新 recovery summary
  - header 现已新增 `Recent Activity` 时间线，可总览最近事件类型与时间，而不必只从各 panel 局部推断变化
  - `Recent Activity` 现已从 `type + 时间` 提升为带最小业务语义的摘要，例如 session upsert、run status change、chat arbitration 和 terminal chunk
  - `Recent Activity` 现还会显示 `event.source`，可区分 human-control、human-chat 与其他来源
  - header 现会显示 `lastEventId`，为当前 project snapshot 提供一个最小事件锚点
  - 当前 mock-only shell 已具备最小产品面骨架；继续只在 mock 层加 UI 细节的边际价值正在下降，下一步应优先接入真实 runtime / build baseline
  - 已补最小 Bun + React + Vite build baseline：根目录现有 `package.json`、`tsconfig.json`、`vite.config.ts`、`index.html` 与 `src/frontend_probe_v0/main.tsx`
  - 已确认 `~/.npmrc` 把 bun 默认 registry 指向 `registry.npmmirror.com`；显式使用 `BUN_CONFIG_REGISTRY=https://registry.npmjs.org` 后，`bun install --verbose` 成功落盘 `node_modules` 与 `bun.lock`
  - `bun run typecheck` 已通过
  - `bun run build` 已通过，生成 `dist/index.html` 与 `dist/assets/index-*.js`
  - Probe 入口现已支持解析两类宿主 runtime 形状：直接 `invoke/listen` 与 Tauri v2 常见的 `core.invoke` / `event.listen`
  - Tauri bridge 名称现已从前端入口层收口成可配置绑定：默认使用 `probe_request_snapshot` / `probe_send_command` / `probe_server_event`，也允许宿主通过全局覆盖注入
  - frontend 现已内建代码级 bridge manifest，显式声明 `freely.probe.v1` 以及当前三条默认 bridge 绑定，后续 Rust/Tauri 接线不必再从 scattered strings 里反推 contract
  - 浏览器 runtime 现在也会直接暴露 `window.__FREELY_PROBE_MANIFEST__`，宿主或调试脚本不需要 import 前端模块就能读取当前 bridge contract
  - 静态宿主入口现在也可直接抓取 `/freely-probe-bridge-manifest.json`，不需要先加载应用页面就能拿到当前 bridge manifest
  - shell header 现会直接显示 `runtime mode` 与当前生效的 bridge 绑定，后续接真实宿主时不必再靠代码阅读判断前端到底吃的是哪组接口
  - shell header 现也会显示当前 `Bridge contract` 版本
  - 新增可选 `tauri-mock` transport：浏览器环境下可通过 query/global 标记注入一层 `invoke/listen` 形状的 mock runtime，让前端可以走一遍 Tauri transport，而不是永远只走 `MockProbeAdapter` 直连路径
  - 页面级验证已通过：默认 URL 显示 `Runtime mode: mock`；`?transport=tauri-mock` 显示 `Runtime mode: tauri`，且触发 `start` 后会出现 `RunStatusChanged` / `AgentStatusChanged` / `TerminalChunkAppended`
  - 失败面也已验证：当宿主提供了 Tauri 形状但 `invoke` 抛错时，header 会直接显示 `Runtime error: bridge offline`，不再静默卡在 loading
  - 现在不需要额外注入脚本也能验证失败面：`?transport=tauri-broken` 会直接进入 tauri-shaped error path，并显示 `Runtime error: bridge offline`
  - shell 现已具备内建 `Transport` 下拉；切换到 `tauri-broken` 会直接把 URL 改成 `?transport=tauri-broken` 并进入对应 transport，无需手改地址栏
  - embedded terminal 现已不再只展示 `terminalTargets`；UI 可对当前 target 真实发送 `AttachTerminal`，并把附着中的 target 置为当前观察面
  - `MockProbeAdapter` 与 Rust bridge 现都已消费 `AttachTerminal`：attach 会把目标 target 置顶、写回 `governanceSummary`，并发出新的 `TerminalChunkAppended`
  - 真实 `bun run tauri:validate:probe` 现已扩到 `start -> create/resume session -> attach terminal -> chat intervention`；validation report 的 `observedCommands` 已包含 `AttachTerminal`
- current_blocker:
  - backend bridge blocker 与 embedded terminal attach 缺口都已解除；当前剩余工作主要是 canonical verification / closeout 判断，而不是继续补 day-1 command surface
- reroute_required:
  - `next_recommended_route=dev-loop-execution`
  - reason: `Rust/Tauri Probe Bridge v1` 已完成最小 IBM 收敛，后续应由 `I-20260317-0332` 进入 backend dev-loop 实现
- unblock_status:
  - `I-20260317-1004` 已完成最小 IBM 收敛，frontend runtime baseline 现已成为可引用依赖
  - 当前 issue 不再只是可从 `in_dev` 推进到 `in_verification`；最小 Probe product surface 与真实 Tauri interaction evidence 已被 `develop` 吸收

## Closeout

- 当前 owner 已完成 canonical closeout：`src/frontend_probe_v0/` 的 day-1 product surface、真实 `Transport=tauri` 下的 `start -> create/resume session -> attach terminal -> chat intervention` 证据，以及 Recent Activity 的本地时区显示层收口都已落在 `develop`。
- `I-20260317-0332` 与 `I-20260317-1004` 的下游依赖都已被消化，不再需要保留 `frontend-probe-v0` 为 active verification owner。
- 后续如果要继续扩大到更完整 UX、multi-project shell、history/memory surface 或新的 backend increment gate enforcement，应另开新 lifecycle，而不是重新打开本 owner。
