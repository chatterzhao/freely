# Issue: rust-tauri-probe-bridge-v1

- issue_id: `I-20260317-0332`
- title: Rust/Tauri Probe Bridge v1
- phase_state: `completed`
- milestone: `M-20260308-frontend-probe-dogfooding-loop`
- epic-name: `frontend-probe-dogfooding-loop`
- story-name: `rust-tauri-probe-bridge-v1`
- issue-name: `rust-tauri-probe-bridge-v1`
- source_candidate: `docs/B1-docs/raw-20260317T110100Z/candidates.md#c-20260317-0332`
- source_brainstorm: `docs/B1-docs/raw-20260317T110100Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/human/tui/raw-20260308-1244pre-tests.md`
- verification_artifact_dir: `docs/B2-docs/human/tui/raw-20260308-1244code-reviews`
- depends_on: `none`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "doc-ibm"}

## Why

`Frontend Probe v0` 的 frontend contract、transport diagnostics、manifest 与错误面已基本收敛，但仓库中仍不存在真实 Rust/Tauri backend bridge 来实现 `freely.probe.v1`。

## Scope

1. 冻结 day-1 Rust/Tauri 工程落点，优先采用仓库根 `src-tauri/ + Cargo.toml` 结构。
2. 冻结三条 bridge：
   - `probe_request_snapshot`
   - `probe_send_command`
   - `probe_server_event`
3. 明确 `probe_send_command` day-1 保持单命令入口，由 payload 区分 `ControlRun`、`CreateOrResumeSession`、`SendChatIntervention`。
4. 明确 day-1 最小 snapshot/event 子集，只覆盖当前 frontend 已消费的闭环。

## Acceptance

- 文档明确 day-1 工程落点为根目录 `src-tauri/ + Cargo.toml`。
- 文档明确 `probe_request_snapshot` / `probe_send_command` / `probe_server_event` 的最小签名。
- 文档明确 day-1 最小 snapshot/event 子集，而不是要求完整 backend 语义。
- 文档明确与 `I-20260308-1244-03` 的边界：本 issue 负责 bridge，本体前端 issue 不再继续假装 backend bridge 已存在。

## Minimal bridge contract

### `probe_request_snapshot`

- input:
  - `projectId`
- output:
  - 最小 `Snapshot`
- day-1 frozen fields:
  - `projectId`
  - `projectName`
  - `governanceSummary`
  - `recoverySummary`
  - `lastEventId`
  - `activeRuns`
  - `activeAgents`
  - `sessions`
  - `terminalTargets`

### `probe_send_command`

- input:
  - `projectId`
  - `command`
  - `payload`
- output:
  - 最小 ack 或同步错误
- day-1 command subset:
  - `ControlRun`
  - `CreateOrResumeSession`
  - `SendChatIntervention`
- day-1 rule:
  - 保持单入口 `probe_send_command`
  - 由 `command` 区分动作类型
  - `payload` 只要求覆盖 frontend 当前已发出的最小字段，不提前设计完整 runtime DSL

### `probe_server_event`

- event subset:
  - `RunStatusChanged`
  - `AgentStatusChanged`
  - `SessionUpserted`
  - `InputArbitrationRecorded`
  - `TerminalChunkAppended`
- day-1 payload rule:
  - payload 与 frontend `freely.probe.v1` manifest 保持同名字段
  - 允许只实现最小子集，不要求一次性补齐完整 runtime 事件谱系

## IBM Handoff

- implementation_scope_summary:
  - 把 `Frontend Probe v0` 当前缺失的 backend bridge 独立成正式 issue，避免继续把 backend 问题混在前端 dev-loop 中。
  - 当前阶段仍是 issue-bound IBM 收敛，不进入 Rust/Tauri 实现代码。
- required_doc_refs:
  - `docs/B1-docs/raw-20260317T110100Z/brainstorms.md`
  - `docs/B2-docs/human/tui/raw-20260308-1244brainstorms/b-rust-tauri-probe-bridge-v1.md`
  - `docs/B2-docs/human/tui/raw-20260308-1244prd.md`
  - `docs/B2-docs/human/tui/raw-20260308-1244pre-tests.md`
  - `docs/B2-docs/human/tui/raw-20260308-1244tasks.md`

## Next

- 当前 bridge contract 已不再只是在 Rust 侧“长得像 frontend 想要的东西”，而是开始按 frontend 当前真实消费面回收：`probe_request_snapshot` 已改为返回 `projectSummary/activeSessions/activeRuns/activeAgents/terminalTargets/governanceSummary/recoverySummary/lastEventId` 这一组 ProbeSnapshot 字段，`terminalTargets` 也已收紧为 `terminalTarget/sessionId`，避免后续 Tauri 联调时再靠前端适配层兜底字段名漂移。
- 当前 `probe_send_command` 也已从旧的 `(project_id, command, payload)` 三段式 Tauri 参数，收紧到直接接收 frontend 已发送的单个 `ClientCommand` 形状，并在 Rust 侧再解出 `projectId/type`；这让 bridge seam 真正与 frontend `TauriProbeAdapter` 当前调用面一致，而不是继续维持一套仓库内自说自话的后端签名。
- 当前 `probe_server_event` 也已不再发出泛化包装对象，而是开始直接产出 frontend `ServerEvent` 形状；其中 `ControlRun` 现在会一次发出 `RunStatusChanged`、`AgentStatusChanged`、`TerminalChunkAppended` 三条最小事件，`CreateOrResumeSession` 发 `SessionUpserted`，`SendChatIntervention` 发 `InputArbitrationRecorded`，进一步降低了后续真 bridge 联调时的语义落差。
- 当前 typed payload 也已从“只对齐 command.type/content/action”继续收紧到 frontend 当前真实发送的字段子集：`ControlRun.runId/reason`、`CreateOrResumeSession.sessionId/resumeHint/commandSource`、`SendChatIntervention.sessionId/messageId/runId/targetAgentId/content`。这些字段现在不只被解析，还会真实影响 Rust snapshot 行为，例如指定 `runId` 会驱动 active run/terminal target，指定 `sessionId` 会驱动 active session，而 `resumeHint` 会进入 session ack 与 governance summary。
- 当前这些字段里原先仍未落地的语义也已继续接入 bridge 行为：`commandSource` 会进入 `SessionUpserted.source`，`reason` 会进入 control 的 terminal chunk 与 pause recovery 文案，`messageId` 会进入 chat event details。这样 day-1 bridge 不只是“字段名看起来对”，而是开始对齐 frontend 当前真实发送值的最小用途。
- 当前 `SendChatIntervention.targetAgentId/runId` 也已继续进入 backend snapshot 视图：指定 `targetAgentId` 会驱动 active agent 标识，指定 `runId` 会驱动 active run 与 terminal target，chat governance summary 和 event details 也会带出这两个值。这样 frontend 把 chat 发给谁、落在哪个 run，不再在 backend bridge 中丢失。
- 当前 Rust 侧的 compile hygiene 也继续收了一步：`src-tauri/src/bridge_logic.rs` 测试里残留的未使用 `ProbeEventKind` 引用已移除，避免后续进入真实 `cargo check` 时先被无关噪音打断。
- 当前 backend 默认 `projectName` 生成规则也已对齐 frontend 当前 runtime/mock 的 title-case 逻辑；例如 `my-project` 现在会在 Rust snapshot 中产出 `My Project`，避免未来浏览器 mock 与真实 Tauri bridge 对同一 projectId 展示出两套名字。
- 当前 backend 默认 `sessionId/runId/terminalTarget` 命名也已对齐 frontend mock 的初始约定：默认使用 `<projectId>-session-1`、`<projectId>-run-1`、`<projectId>-run-1:pty-0`，减少未来比较 mock transport 与真实 Tauri bridge 初始状态时的无意义差异。
- 当前 backend 默认 `lastEventId` 也已对齐 frontend mock 的初始约定，改为从 `event-1` 起步，而不是旧的 `event-0`。这样 mock 与真实 bridge 的初始 snapshot 在最小事件计数面也更一致。
- 当前 backend 的 `governance_summary/recovery_summary` 更新规则也已继续对齐 frontend mock：新条目现在会前插到已有 summary 前面，并统一截断到最近 4 条，而不是每次整段覆盖。这样 session upsert / chat intervention / pause 等动作在真实 bridge 下的 header 摘要滚动方式会更接近当前浏览器侧 mock runtime。
- 当前 backend emitted event 的 `occurredAt` 也已不再固定停在 `1970-01-01T00:00:00Z`，而是开始生成运行时 RFC3339 时间戳；同时 `src-tauri/src/event_payload.rs` 的最小测试期望也已改为匹配新的默认 `sessionId/runId` 命名，避免后续进入真实 `cargo test` 时先卡在过时断言上。
- 当前 `event_payload.rs` 在缺少活跃 session/run/terminal target 时的 fallback 命名，也已从旧的 `session-<project>` / `run-<project>` 收口到当前冻结的 `<projectId>-session-1` / `<projectId>-run-1` / `<projectId>-run-1:pty-0` 规则，避免未来空态事件与默认 snapshot 再出现两套命名体系。
- 当前 issue 已进入 `in_dev`，day-1 Rust/Tauri bridge 骨架已落到根目录 `Cargo.toml` 与 `src-tauri/`，并把 bridge contract 常量收口到 Rust 侧 `src-tauri/src/bridge_manifest.rs`，把单入口 command 子集收口到 `src-tauri/src/command_kind.rs`，把最小 server event 子集收口到 `src-tauri/src/event_kind.rs`，把 snapshot/run/session/agent/terminal 模型收口到 `src-tauri/src/model.rs`，把 app state 与默认 snapshot 生成收口到 `src-tauri/src/state.rs`，并补了最小单元测试骨架以覆盖 command/event/state 的基础 contract。
- 当前 bridge 命令处理语义已进一步从 `src-tauri/src/lib.rs` 抽到 `src-tauri/src/bridge_logic.rs`，让 Tauri 壳只保留命令注册与事件发射，后续一旦具备 `cargo` 环境即可直接围绕 reducer 追加 Rust 单测和编译验证，而不必继续在 Tauri 入口里混合桥接语义。
- 当前 day-1 `ControlRun` 语义已不再把所有 control 一律压成 `running`，而是开始读取最小 payload `action`，对齐 frontend 当前实际发送的 `start/pause/terminate/resume/retry` 子集，并同步更新 run status、agent blocker、`recovery_summary`。
- 当前 day-1 command payload 也已开始从裸 `serde_json::Value` 提升为最小 typed 解析层 `src-tauri/src/command_payload.rs`，先覆盖 `ControlRun`、`CreateOrResumeSession`、`SendChatIntervention` 三个子集，降低后端 bridge contract 漂移风险。
- 当前 day-1 server event payload 也已开始从 reducer 内联 JSON 拼装提升为统一 builder `src-tauri/src/event_payload.rs`，让后端 bridge 的出站 contract 也有最小事实源，而不是继续散落在 `bridge_logic.rs` 中。
- 当前 typed payload 已不再只是“有解析、没行为”：`CreateOrResumeSession` 已把 payload 中的 title 写回 session 与 `governance_summary`，`SendChatIntervention` 已把 content 写回 agent `last_action` 与 `governance_summary`，让 backend day-1 snapshot 语义更接近 frontend 当前消费面。
- 当前 ack 也已不再固定返回同一句 `"command accepted by day-1 bridge"`，而是开始按 `ControlRun` / `CreateOrResumeSession` / `SendChatIntervention` 返回最小语义化确认文案，减少联调阶段的模糊面。
- 2026-03-17 当前轮继续收紧了两个真实宿主风险点：`probe_request_snapshot` 现会直接兼容 frontend 当前发送的 camelCase `projectId`（并保留对旧 `project_id` 的兼容），避免 mock transport 可用但真 Tauri invoke 因参数名不匹配失联；同时 bridge reducer 内部对缺省 `runId/sessionId` 的回退规则已统一对齐到 `<projectId>-run-1` / `<projectId>-session-1`，并补了最小 Rust 单测覆盖这两条 contract。
- 2026-03-17 当前轮也把 `CreateOrResumeSession` 后的 `terminalTargets[].sessionId` 一并与当前 session 对齐，避免 session upsert 后 snapshot 仍残留旧 terminal 归属。
- 当前最直接 blocker 不是 bridge 边界未定，而是本地环境缺少 `cargo/rustc/rustup`，暂时无法执行 `cargo check` 验证 Rust 侧编译；仓库内现已提供 `bin/check-rust-toolchain`、`bin/cargo-check-probe-bridge` 以及 `bun run rust:preflight` / `bun run cargo:check:probe` 作为统一入口。
- 2026-03-17 当前轮已实际执行验证：`bun run typecheck` 通过，`bun run build` 通过；`bun run rust:preflight` 与 `bun run cargo:check:probe` 仍因环境缺少 `cargo/rustc/rustup` 失败，因此当前 blocker 继续是 toolchain 缺失而不是 frontend baseline 或 contract drift。
- 2026-03-17 当前轮又把 `bin/check-rust-toolchain` 从“只报缺失”推进成“可操作的预检入口”：现在会列出缺失命令、给出 `rustup` 安装建议、提示重新加载 `~/.cargo/env`，并明确要求回跑 `bun run rust:preflight` / `bun run cargo:check:probe`。这样当前 issue 即使仍被本机环境阻塞，也不再停留在模糊 blocker。
- 2026-03-17 当前轮还补了 `bin/test-rust-toolchain-preflight`，用 PATH 隔离方式固定验证 preflight 在缺少 Rust toolchain 时会输出缺失命令汇总、`rustup` 安装建议、shell reload 提示与重跑命令，避免后续脚本回退到“只会报错、不会给下一步”。
- 2026-03-17 当前轮又把这条回归测试接进 `package.json`，统一为 `bun run rust:preflight:test`；后续不论是 runtime 还是人工验证，都不需要再单独记 shell 测试文件路径。
- 2026-03-17 lead-agent 首跳重入后再次按 `milestones > progress/recovery > review/test > human chat/session evidence > github issue > PROJECT_INTENT` 扫描需求池；由于当前仓库仍无正式 `docs/progress/**` / `docs/recovery/**`，且不存在比 committed `in_dev` issue 更高优先的新 discovery 输入，本轮继续命中 `I-20260317-0332` 的 `issue continuation`，并在当前 `codex` 会话内直接进入 `dev-loop-execution`。
- 2026-03-17 这轮已再次执行验证：`bun run typecheck` 通过，`bun run build` 通过，`bun run rust:preflight:test` 通过；`bun run rust:preflight` 与 `bun run cargo:check:probe` 仍因环境缺少 `cargo/rustc/rustup` 失败。结论保持不变：当前 blocker 是 Rust toolchain 缺失，不需要 reroute 回 `doc-pre-brainstorm-execution` 或 `doc-ibm-execution`。
- 2026-03-17 当前轮继续向前推进了一步：已通过 `rustup` 安装把 `cargo` / `rustc` / `rustup` 命令层落到 `~/.cargo/bin`，并执行 `rustup default stable`；`bun run rust:preflight` 现已通过，说明“本机缺少 Rust 命令”这一层 blocker 已解除。
- 2026-03-17 当前最小编译验证也因此进入了下一层真实问题：`bun run cargo:check:probe` 不再卡在“缺命令”，而是失败于 `rustc -vV`，报错 `Missing manifest in toolchain 'stable-aarch64-apple-darwin'`。这说明当前 blocker 已收窄为 rustup partial install / stable toolchain manifest 缺失，而不是 bridge contract 或前端边界漂移。
- 2026-03-18 当前轮继续把这条环境 blocker 真正收掉：重新让 `stable-aarch64-apple-darwin` 回到可见状态后，`cargo --version` / `rustc --version` 已稳定输出 `1.94.0`，随后又补了 Tauri compile-time 需要的 `src-tauri/icons/icon.png` 有效 RGBA 占位图，并移除了 `src-tauri/src/event_payload.rs` 里的无用 `json` 导入。
- 2026-03-18 在这些修复后，`bun run cargo:check:probe` 已通过；当前不再是 Rust toolchain 或缺失 asset 阻塞，而是进入后续联调与 warning 收口阶段。
- 2026-03-18 当前轮继续把 bridge contract 与真实宿主接缝再收紧一步：`src-tauri/src/event_payload.rs` 已统一改用 `src-tauri/src/event_kind.rs` 的最小事件事实源；`src-tauri/src/bridge_manifest.rs` 现已提供 Rust 侧可消费的 contract 入口，并新增测试直接校验 Rust 常量与 `public/freely-probe-bridge-manifest.json` 保持一致，避免前端公开 manifest 与后端命令/事件名漂移。
- 2026-03-18 当前轮还修正了两条已经落后于当前默认 snapshot 行为的 Rust 单测断言：`last_event_id` 现在按默认 `event-1 -> event-2` 递增，`CreateOrResumeSession` 后的 `governance_summary` 也保留初始 `"bridge connected"` 再前插新条目，而不是错误地假设 summary 被整段覆盖。
- 2026-03-18 当前轮已实际完成本地 bridge 验证闭环：`bun run cargo:check:probe` 通过、`cargo test -p freely-probe-bridge` 24 项通过、`bun run typecheck` 通过、`bun run build` 通过。当前剩余缺口不再是 contract/warning，而是尚未执行真正的 Tauri 宿主启动联调。
- 2026-04-01 当前轮继续把真实宿主 blocker 正式收掉：根目录 `package.json` 新增 `tauri:preflight:probe` / `tauri:dev:probe`，`vite.config.ts` 与 `src-tauri/tauri.conf.json` 统一冻结到 `127.0.0.1:4173`，并补了 `bin/check-tauri-probe-host` / `bin/tauri-probe-dev` 作为 canonical host-validation 入口。随后已实际执行 `bun run tauri:preflight:probe` 与 `bun run tauri:dev:probe`，确认真实 Tauri 宿主能稳定完成 Vite `BeforeDevCommand`、Rust bridge 编译并进入 `target/debug/freely-probe-bridge` 运行态，不再停在 host mismatch 或 toolchain 缺失。
- 2026-04-01 当前轮也把验证基线重新回放到最新入口：`bun run typecheck`、`bun run build`、`bun run cargo:check:probe`、`cargo test -p freely-probe-bridge` 再次通过。当前 `I-20260317-0332` 已不再被“真实 Tauri 宿主无法启动”阻塞，生命周期进入 `in_verification`；剩余待写实的验收点只剩真实 `Transport=tauri` 下的最小 start / session create-resume / chat intervention 闭环证据。
- 2026-04-01 当前轮已把真实 `Transport=tauri` 的最小交互闭环实际打通：新增 `bin/tauri-validate-probe-interactions` 作为 canonical live validation 入口，前端 `useTauriValidationSequence` 在 validation mode 下会真实发出 `ControlRun(start)`、`CreateOrResumeSession`、`SendChatIntervention`，Rust 侧 `validation_report.rs` 会把 snapshot request、command ack、event subset 与 snapshot writeback 记录成结构化 report。实测 `bun run tauri:validate:probe` 已返回 `status=passed`，确认真实 Tauri transport 下最小 start / session create-resume / chat intervention 闭环成立。
- 2026-04-01 当前轮也顺手收掉了两条真实 seam bug：`TauriProbeAdapter.requestSnapshot()` 现按 Rust 命令参数名传递 `{ payload: { projectId } }`，不再在真实宿主里因为 invoke 参数形状错误而丢失初始 snapshot；validation sequence 则不再把成功与否绑死在前端事件订阅 race 上，而是通过真实 `requestSnapshot` 轮询确认 run/session/chat 写回，确保 live validation 反映的是真 bridge state，而不是 React effect 时序。
- `I-20260308-1244-03` 曾作为 frontend dev issue 承接本 bridge closeout 之后的 host integration / UX 收口；当前两条 owner 都已完成，后续若要扩展 bridge beyond day-1 subset，应另开新 lifecycle。

## Closeout

- 当前 owner 已完成 canonical closeout：真实宿主 bring-up 与真实 `Transport=tauri` 最小交互闭环都已取得 live evidence，并已被 `develop` 吸收。
- 后续 frontier 不再停留在 backend bridge day-1 subset；相关 frontend host integration / UX day-1 收口已由 `I-20260308-1244-03` 完成 closeout。若要扩展 bridge beyond day-1 subset，另开新 lifecycle。
