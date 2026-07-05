# 预研头脑风暴：rust-tauri-probe-bridge-v1

- id: `20260317-0332--rust-tauri-probe-bridge-v1`
- status: `active`
- related_issue: `docs/B2-docs/human/tui/issues/frontend-probe-v0.md`
- trigger: `Frontend Probe v0` 已把前端侧的 bridge contract、transport diagnostics、manifest 暴露面基本补齐，但仓库里没有任何 Rust / Tauri backend bridge 实现。

## 问题

当前 frontend 已明确依赖三条 bridge：

- `probe_request_snapshot`
- `probe_send_command`
- `probe_server_event`

但仓库中不存在：

- `Cargo.toml`
- `src-tauri/`
- `*.rs`

所以当前真正缺的不是更多 frontend seam，而是一条新的 backend issue 边界：如何以最小 Rust/Tauri bridge v1 接上现有 `freely.probe.v1` manifest。

## 收敛结论

1. 这是边界外新问题，不能继续塞回 `I-20260317-1002`。
2. 下一跳应先走 `doc-pre-brainstorm-execution`，把 backend bridge 问题提升为正式 candidate。
3. 该 candidate 至少需要收敛：
   - Rust/Tauri 工程落点
   - 三条 bridge 的最小命令/事件签名
   - 与现有 frontend manifest 的对齐策略
   - day-1 backend 可以返回什么最小 snapshot / event
4. `Frontend Probe v0` 当前应保留在 `in_dev`，但 blocker 改成“等待 backend bridge 新 issue 收敛”。

## 工程落点候选

### 候选 A：标准 Tauri app 结构

- 根目录新增 `src-tauri/`
- 根目录新增 `Cargo.toml`
- 在 `src-tauri/src/main.rs` 注册三条 bridge：
  - `probe_request_snapshot`
  - `probe_send_command`
  - `probe_server_event`
- 优点：
  - 与 Tauri 默认结构一致
  - 前端当前的 `invoke/listen` 形状可以直接复用
- 风险：
  - 仓库目前还没有任何 Rust crate 基线，需要一次性引入最小 desktop/runtime 骨架

### 候选 B：先建独立 Rust crate，再由 Tauri 壳接入

- 先新增独立 Rust crate，承载 snapshot/command/event 的最小 backend 语义
- 之后再由 Tauri app 把它暴露给前端
- 优点：
  - backend contract 更易单测
  - runtime 语义与 Tauri UI 壳可分离
- 风险：
  - day-1 集成路径更长
  - 当前 blocker 本质上就是“前端没有 bridge 可接”，先拆 crate 可能延迟最小可运行面

### 当前倾向

- day-1 倾向先走候选 A
- 原因：当前最高价值不是 backend 抽象层优雅，而是尽快让 `freely.probe.v1` 在真实宿主上第一次跑通

## day-1 bridge 草案

### `probe_request_snapshot`

- 输入：
  - `projectId`
- 输出：
  - 最小 `Snapshot`
- day-1 要求：
  - 可先返回单项目、单 run、单 terminal target 的最小结构

### `probe_send_command`

- 输入：
  - `projectId`
  - `command`
  - `payload`
- 输出：
  - 同步确认或最小 ack
- day-1 要求：
  - 至少覆盖 `ControlRun`
  - 至少覆盖 `CreateOrResumeSession`
  - 至少覆盖 `SendChatIntervention`

### `probe_server_event`

- 事件：
  - `RunStatusChanged`
  - `AgentStatusChanged`
  - `SessionUpserted`
  - `InputArbitrationRecorded`
  - `TerminalChunkAppended`
- day-1 要求：
  - 不追求全量事件谱系
  - 先保证前端当前已消费的最小事件闭环

## 下一轮收敛问题

1. `Cargo.toml` 与 `src-tauri/` 应直接落在仓库根，还是需要先经过独立 crate 过渡。
2. `probe_send_command` 是保持单命令入口，还是 day-1 直接拆成多条 Tauri command。
3. `probe_server_event` 的 payload 是否完全复用 frontend manifest，还是允许 day-1 做最小子集。

## 证据

- frontend 已可直接暴露 `window.__FREELY_PROBE_MANIFEST__`
- frontend 已可直接抓取 `/freely-probe-bridge-manifest.json`
- `tauri-mock` / `tauri-broken` 页面级验证已通过
- 仓库扫描未发现任何 Rust / Tauri backend 代码
