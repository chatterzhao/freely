# 研究：Frontend Probe Day-1 与 Freely 自举狗粮闭环

日期：2026-03-08 12:44 UTC

## 背景

此前关于“后端优先、前后端解耦”的研究已经形成明确方向：

- 前后端分离仍是硬约束
- Frontend 只依赖 Backend API
- Runtime 可以替换，产品协议不能绑死在具体 runtime 上

本轮重新评审后，需要把“前后端”再定义得更准确：

- 这里的前后端首先是一种内部架构思想，而不是 day-1 就必须做成远端分布式部署
- Freely 初始形态可以只是一个带终端的桌面开发工具
- 但该工具内部也必须保留 Frontend / Backend 边界，确保开发解耦，并为未来架构扩展留空间

当前硬约束技术栈保持不变：

- Backend / runtime / orchestration: `Rust`
- Desktop shell: `Tauri`
- Frontend: `React` + `TypeScript`
- Frontend runtime / package tool: `Bun`
- 不引入 `Node.js` 作为产品运行时

但继续讨论后，暴露出一个新的产品风险：

1. 如果长期只做后端、不提供前端探针，AI 可能已经在错误方向上推进很多轮，直到很晚才被看到。
2. Freely 的目标之一正是帮助人类尽早发现 AI 跑偏，因此它自己必须从第一阶段就具备“可观察、可打断、可回放”的产品面。
3. 如果 Freely 自己开发 Freely 时都不能通过同一套前端面即时验证后端增量，那狗粮链路仍然不闭环。

因此，原先“backend-first”需要被收紧为：

- `backend-core-first`
- `frontend-probe-from-day-1`
- `dogfooding-validation-per-increment`

同时，原先“Backend API”需要被收紧为：

- 先定义 `frontend/backend boundary contract`
- day-1 可以落在单机 Tauri 应用内部
- 但契约表达不能写死为仅适用于单进程或仅适用于 HTTP 服务

## 当前问题

### 1. “先后端、后前端”容易被误解成“前端长期不可用”

这会带来两个问题：

- 后端接口虽然在实现，但没有产品面来快速验收
- 人类只能读文档、脚本和日志，难以及时发现交互语义偏差

这不符合 AI 时代的控制面需求。

### 2. Freely 缺少“每个后端增量都能被前端立即验证”的产品契约

如果没有这条门禁，团队会自然回到：

- 先做很多后端
- 再补一个“最终 UI”
- 很晚才发现 API 和交互模型不对

这会直接导致返工。

### 3. 当前 pre-brainstorm 已有 API / UI 结论，但尚未形成面向自举开发的候选批次

已有研究已经覆盖：

- Backend API 最小接口面
- 会话/流式输出/历史/状态
- 多项目 UI 隔离草案

但还缺一层“Freely 用 Freely 开发自己”的显式执行收敛：

- 哪个是 day-1 probe 范围
- 哪个是前后端边界契约冻结范围
- 哪个是硬门禁

### 4. 现有“Backend API”表述容易让架构过早网络化

如果直接把当前阶段理解成“必须先做远端后端 + HTTP API”，会带来两个偏差：

- 过早引入部署和网络复杂度
- 忽略“桌面工具内部也需要前后端解耦”的真正目的

因此当前更合理的表述是：

- 先定义 Frontend 与 Backend 的边界契约
- 该契约第一阶段可以通过 Tauri command/event、Rust sidecar、内部 stream bridge 等形式承载
- 只要 Frontend 不直接侵入 workspace/runtime 内部实现，边界目标就成立

### 5. 协议层必须从第一版开始可插拔

如果 day-1 直接把 Frontend 绑定到某一种传输方式，例如固定的 WS、SSE 或某个 Tauri 调用细节，后续替换 transport 时会把 UI 和 backend 一起拖着重写。

因此协议层需要分成三层：

1. `frontend contract`
   - Frontend 只理解统一的 command / event / snapshot 语义
2. `transport adapter`
   - 例如 `tauri_adapter`、`ws_adapter`、`local_process_adapter`
3. `backend service contract`
   - 负责 session、run、terminal、governance、skill routing 等业务能力

这样做的意义是：

- day-1 可以先落在 Tauri 内部桥接
- 以后要换成 WS 或其他 transport，不需要重写前端组件和 backend 状态机
- “可插拔协议”成为产品能力，而不是一次性实现技巧

## 收敛判断

### 1. 前端必须从第一阶段可用，但只做 Probe，不做完整产品 UI

推荐把前端分成两层：

1. `Frontend Probe`
   - 项目选择
   - 会话列表
   - 输入框
   - 流式输出
   - 当前 run/status
   - stop / retry
2. `Full Product UI`
   - 多项目复杂工作台
   - 更完整的信息架构
   - 丰富的操作流和视觉层

这意味着：

- day-1 要有 Probe
- day-1 不要求完整 UI

### 2. Backend API 仍然是唯一契约面

Probe 不能绕过后端直接读写 workspace。

必须保持：

- Frontend 只调用 Backend API
- Backend API 聚合 runtime、workspace、session、status
- Runtime 仍负责执行，不直接承载产品交互逻辑

补充约束：

- 这里的 `API` 先按“边界契约”理解，而不是先限定为网络 API
- day-1 可以是桌面应用内部的 contract layer
- 只要边界清晰，就允许未来平滑迁移到本地守护进程、sidecar 或远端服务
- contract 还必须把 transport 从业务语义中解耦，避免协议被单一 adapter 锁死

### 3. 每个后端增量都必须有一个前端可验证入口

建议把完成定义收紧为：

- 一个后端能力只有在 Probe 中可触发、可观察、可中断、可回放，才算真正完成

最小验证链路：

1. 前端发起请求
2. Backend API 接收并落状态
3. Runtime 执行
4. 前端看到流式事件和最终状态
5. 必要时可中断并回放历史

### 4. 这应成为 Freely 的狗粮能力，而不是单次开发策略

Freely 需要把这件事产品化给自己和用户项目：

- 后端能力增量化开发
- 前端探针式即时验证
- 人类和 AI 共用同一观测面
- 自举开发时不允许例外

## 候选方向

### 方向 A：冻结 Frontend / Backend Boundary Contract v1

目标：

- 把 Probe 必需的最小边界契约先冻结

当前语义：

- 优先冻结“调用面”和“事件面”
- 不要求 day-1 就固定网络协议或部署形态
- 允许 first implementation 位于 Tauri 桌面工具内部
- transport adapter 必须可替换，不能把 command/event 语义写死在某一种 transport 上

建议最小接口面：

- `POST /sessions`
- `GET /sessions`
- `POST /sessions/{id}/messages`
- `GET /sessions/{id}/stream`
- `GET /sessions/{id}/history`
- `GET /status`

可后置：

- `GET /memory/search`
- `POST /commands/run`

备注：

- 上述写法目前仍可作为 API 草案参考
- 进入 IBM 时应进一步判断第一阶段到底落成：
  - Tauri command + event stream
  - 本地 loopback API
  - sidecar bridge
- 但无论选哪一种，都不能破坏前后端边界
- 同时应显式设计：
  - `ClientCommand`
  - `ServerEvent`
  - `Snapshot`
  让 WS / Tauri / 其他 transport 只做 adapter，而不改业务协议

### 方向 B：实现 Frontend Probe v0

目标：

- 用最薄的 Tauri + React 壳承接 day-1 验收

必须包含：

- 项目切换
- session 创建/恢复
- message input
- stream output
- status panel
- stop / retry

明确不包含：

- 复杂工作台
- 完整多项目视图编排
- 高保真视觉系统
- 与 Node.js 绑定的运行时路径

### 方向 C：建立 Incremental Dogfooding Gate

目标：

- 把“每个后端增量必须在 Probe 验证”写成治理门禁

核心语义：

- 没有 Probe 验证证据的后端增量，不算完成
- Freely 自举开发 Freely 时也必须走同一条链路

### 方向 D：整体前后端架构再评审

目标：

- 在正式进入 IBM 前，把 Freely 当前产品形态下“什么算前端、什么算后端、边界如何落在 Tauri 内部”重新评审清楚

必须回答：

- 哪些能力属于 Frontend
- 哪些能力属于 Backend / runtime
- 边界第一阶段通过什么承载
- 哪些接口是同步命令，哪些是事件流
- 哪些状态由 Frontend 持有，哪些状态必须由 Backend 持有
- 如何保证未来迁移到远端或多进程时不推翻第一阶段实现

## 推荐下一跳

1. 把本研究同步进一个新的 active milestone。
2. 先提升“整体前后端架构再评审”候选，避免过早把边界等同于 HTTP 服务。
3. 再提升 `Frontend / Backend Boundary Contract v1` 与 `Frontend Probe v0` 两个 P0 candidate。
4. 同时提升一个治理 candidate，定义增量狗粮门禁。
5. 在后续 IBM 中再决定：
   - 边界第一阶段承载形态
   - API / command / stream 的字段级协议
   - Probe 事件模型
   - 验证证据写回位置
