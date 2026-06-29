# 预研头脑风暴：foreground-background-runtime-entrypoint-semantics

## 背景

近期对 `freely` runtime 的实测暴露出一个产品语义与实现入口不一致的问题：

- 产品 intent 明确要求 runtime 持续运行，除非明确停止
- 当前 `freely start` 实际上是前台 supervisor，附着在调用会话上
- 在前台会话结束或被清理时，supervisor 会收到 `INT/TERM`，记录为 `operator_stop`
- 这会让用户误以为 Freely “自己停了”，但直接原因其实是入口 ownership 与产品语义不一致

同时，Freely 不是纯 CLI 工具。`PROJECT_INTENT` 已明确包含：

- CLI
- TUI
- GUI

因此当前问题不能只按“shell 命令怎么起”来修，而必须先定义一套能同时覆盖 CLI first 与未来 UI 前端的启动/关闭 contract。

## 已确认事实

### 1. 当前 `start` 是前台语义，不是后台自治入口

`bin/freely` 只是：

- `exec bash "$ROOT_DIR/docs/system/workspace/scripts/runtime/freely" "$@"`

而 `cmd_start()` 会直接进入 project runtime supervisor 主循环，没有默认 detach。

这意味着：

- 从当前终端直接执行 `freely start`
- 当前终端 / 外层命令生命周期结束时
- supervisor 也会跟着收到信号并停掉

### 2. 本次观察中的 continuity 不是 fallback 代写

新生成的 continuity 文件记录为：

- `continuity_written_by: codex-manager`

因此最近新增的 stop 前 fallback continuity 逻辑不是这次现象的主因。

### 3. `operator_stop` 在当前现场里表示 supervisor 收到外部信号

`request_stop()` 只由 `INT/TERM` trap 触发。当前看到：

- `ai_cycle_finished ... rc=0`
- 随后 `operator_stop_requested`
- 最后 `supervisor_cleanup ... exit_reason=operator_stop`

这更接近“前台入口绑定会话，被会话清理带死”，而不是 manager 自己完成一轮后主动决定停机。

### 4. detached 对照能消除这类 `operator_stop`

同样代码路径下，使用真正 detached 的独立 session 启动 supervisor 后：

- 不再出现 `operator_stop_requested`
- 说明问题不在 continuity 逻辑本身
- 而在前台入口的 ownership / session contract

### 5. 这条问题不能和其他 runtime recovery 问题混修

detached 对照中还暴露了另一条独立问题：

- `primary_rate_limit_exhausted` 后 supervisor 退出
- 但恢复链没有把 runtime 拉回稳定 running

这说明：

- “前台入口被外层会话带死”
- 和 “rate-limit 后的 recovery gap”

是两条不同的问题线，不能用一个入口改动一起糊掉。

## 需求边界

### 1. 产品级目标不是“只有一种 start”

从整体产品形态看，Freely 需要同时支持两种模式：

- 前台附着运行：给开发者调试、直接盯日志、现场排障
- 后台自治运行：给长期 runtime、自举、TUI/GUI 控制面

如果只保留其中一种：

- 只保留前台，会违背“持续运行，除非明确停止”的产品心智
- 只保留后台，会削弱 CLI first 的调试与前台可观测性

### 2. UI 关闭默认只关闭前端，不默认停止后台

未来 UI 关闭行为需要满足：

- 关闭窗口 / 退出前端应用
- 默认不停止 Freely 后台 runtime
- 若用户想同时停止后台，必须显式选择

这要求 CLI / runtime 先定义清楚“后台 runtime 是独立存活的产品对象”，而不是 UI 附属进程。

### 3. 状态真源必须统一

不管前台还是后台，不管 CLI 还是 UI，状态都应统一来自：

- runtime state files
- `live-status`
- `fleet-status`

UI 只能消费同一套真源，不能维护一套自己的并行状态判断。

## 需要先冻结的语义 contract

### 1. 前台模式

前台模式应满足：

- runtime 附着在当前终端
- `Ctrl+C` 停止当前前台 runtime
- 命令输出可直接展示实时日志
- 适合调试、复现、观察单轮行为

### 2. 后台模式

后台模式应满足：

- 启动命令返回后 runtime 持续存活
- 关闭终端不会停止后台
- `Ctrl+C` 只影响当前启动命令或日志附着，不影响后台 runtime 本体
- 停止后台必须走显式 stop/kill/down 命令面

这里的关键决议是：

- 后台模式不能再由当前顶层 `start` 隐式承担
- 必须由显式 `daemon` 命令面承担
- 也就是说，只有明确写出 `daemon ...` 才表示后台 runtime contract

### 3. UI 关闭模式

UI 关闭时应区分两件事：

- 关闭前端 shell / window
- 停止后台 runtime

默认只做前者，不自动做后者。

### 4. 观测模式

即使运行在后台，也需要一套清晰观测入口，例如：

- `status`
- `live-status`
- `logs`

其中 `logs -f` 或类似附着命令在 `Ctrl+C` 时，应该只退出附着，不停止后台 runtime。

## 当前命令面的真实语义

基于当前实现和测试依赖，可以先冻结一条事实：

- `freely start` 现在是前台模式
- `freely restart` 也沿用同一套前台 supervisor 语义
- `freely stop` / `status` / `live-status` / `fleet-status` 是围绕当前 project runtime 的控制与观测面

这不是推测，而是现有实现和测试共同锁住的行为：

- `cmd_start()` 直接进入 `start_project_runtime()`
- `start_project_runtime()` 进入 supervisor 主循环，不做默认 detach
- 现有多条测试直接把 `runtime/freely start --project ...` 当作前台 supervisor 进程假设来做 `wait`、PID、attach、stop 相关验证

因此这次重构不应表述成：

- “把 `start` 改成后台”

而应表述成：

- “保留 `start` 的前台 contract”
- “新增并推广显式 `daemon` 后台 contract”
- “再决定顶层默认文档与 UI 应把哪条路径视为主入口”

## 命令面候选方向

当前更稳的候选不是多组并列，而是先收敛到一条低回归方向：

### 方向 A：保留现有顶层命令为前台/控制面，新增显式 daemon 子命令

示例：

- `freely start`
- `freely restart`
- `freely stop`
- `freely status`
- `freely daemon start`
- `freely daemon stop`
- `freely daemon status`
- `freely daemon logs`

优点：

- 不会悄悄改变现有 `start/restart/stop/status` 的前台与控制面语义
- 对现有测试与 command semantics 冲击最小
- UI/TUI 能直接映射到 `daemon start/stop/status/logs`
- “后台模式必须显式写出 daemon” 的用户心智清晰

代价：

- 命令更长
- 产品文案里需要同时解释 foreground 和 daemon 两套入口

### 当前不建议的方向

当前阶段不建议直接做两类变化：

- 直接把 `freely start` 改成后台
- 直接把顶层命令整体迁移为 `up/down/run/ps/logs`

原因不是这些名字绝对不行，而是它们会把“入口 contract 重定义”与“命令面迁移”捆成一次大改，回归面过大。

## 主要风险

### 1. 不能偷改当前 `start` 默认行为

现有测试和控制面明显把 `start` 当作前台 supervisor command 使用。

如果直接把 `start` 变成默认后台化，可能打破：

- `wait` / PID / 退出码预期
- `stop` 和 `operator_stop` 相关测试
- attach / repair / restart 语义

更具体地说，当前至少已有三类既有 contract 会被直接触碰：

- 启动类测试默认把 `freely start` 当作活的 supervisor 进程
- 停止类测试默认让 `freely stop` 去杀当前 project supervisor
- 状态与 ownership 测试默认通过 `runtime/freely start --project` 识别 project runtime

### 2. 不能把“前台入口 ownership”与“后台恢复缺口”混成一个修复

否则很容易：

- 把会话绑定问题藏掉
- 同时引入新的 recovery regressions
- 让状态面更难解释

### 3. UI 默认关闭语义一旦定错，后面很难回收

如果 UI 第一个版本默认“关窗口即停后台”，会直接把产品心智拉回前台工具，而不是持续自治 runtime。

## 当前测试面审计

为避免后续 issue materialization 时把“产品 contract”和“回归保护”混说，需要先把当前测试面拆成两组。

### 1. 必须继续保护的前台 contract tests

以下类型说明 `start/restart/stop/status` 已经不是空白命令面，不能静默重定义：

- `test-freely-runtime-supervisor-event-log`
  - 直接后台拉起 `freely start`，等待 supervisor 产生日志
  - 再调用 `freely stop`
  - 断言 `operator_stop_requested` 与 `supervisor_cleanup exit_reason=operator_stop`
  - 这锁住了“`start` 是活的 supervisor，`stop` 会把它停掉”的前台 contract

- `test-freely-project-command-semantics`
  - 直接验证 `cmd_start()`、`cmd_restart()`、`start --force`
  - 同时验证 attach / repair / discovered supervisor 相关语义
  - 这锁住了“`start/restart` 是 project runtime 的同步控制入口”

- `test-freely-stop-terminates-all-same-project-supervisors`
  - 通过伪造多个 `runtime/freely start --project ...` 进程
  - 验证 `freely stop` 会终止同 project 的全部 supervisor
  - 这锁住了 `stop` 对前台/同项目 supervisor 的 kill semantics

此外还有大量同类测试依赖以下事实：

- `runtime/freely start --project ...` 是可识别的 supervisor 进程标识
- `status/live-status/fleet-status` 通过这类进程与 pid file 推导 runtime truth
- attach / ownership / foreign pid 防护都围绕当前 `start` 进程形态建模

因此，当前更稳的策略不是改写这些测试的基本假设，而是保持它们继续描述 foreground contract。

### 2. 必须新增的 daemon contract tests

如果新增 `freely daemon ...`，则至少需要新增一套与 foreground 分离的验收面：

- `daemon start` 返回后，后台 runtime 仍存活
- 调用 `daemon start` 的 shell/PTY 结束后，后台 runtime 仍存活
- `daemon stop` 能显式停止后台 runtime
- `daemon status` 能读到后台 runtime 状态，并与 `live-status` 真源一致
- `daemon logs` 或附着模式的 `Ctrl+C` 只退出附着，不停止后台 runtime
- UI/TUI 如果对接 daemon 模式，其关闭前端默认不导致后台 runtime 停机

### 3. 前后台测试边界

最关键的一条边界是：

- 不要把现有 `start` 测试整体迁移成 daemon 测试

更稳的是：

- 现有测试继续锁前台 contract
- daemon 新增独立测试族
- status 真源继续共用，不产生两套 runtime truth

## 暂时性结论

当前最合理的产品方向是：

1. Freely 必须同时支持前台模式和后台模式
2. 当前 `start/restart/stop/status` 应继续被视为前台/控制面 contract，不能静默重定义
3. 后台 runtime 应通过显式 `daemon` 命令面 materialize，并成为长期自治与 UI 控制面的标准对象
4. UI 关闭默认只关前端，不停后台
5. 状态真源统一走 runtime state files / `live-status`

## 这轮 bug 与命令语义重构的关系

当前复现到的核心 bug 是：

- 用户按产品心智把 `freely start` 当作“把 Freely 跑起来”
- 但实现上它其实是前台附着 supervisor
- 因此外层会话结束后，runtime 被带死并记录为 `operator_stop`

如果命令语义重构明确为：

- `freely start` = 前台模式
- `freely daemon start` = 后台模式

那么这轮 bug 将不再表现为“Freely 自己停了”，而会变成两条清晰语义：

### 1. 前台模式下

如果用户执行：

- `freely start`

随后终端关闭或 `Ctrl+C`，runtime 停止就是预期行为，不再是 bug。

### 2. 后台模式下

如果用户执行：

- `freely daemon start`

随后关闭终端、退出前端、断开 attach，会话不应再把后台 runtime 带死。  
因此这轮此前观察到的 `operator_stop_requested` 不应再出现为 daemon 模式的主路径故障。

也就是说，这次重构不是“给现有 bug 打补丁”，而是通过把前台/后台 contract 分离，消除用户把前台入口误当后台入口的歧义来源。

## 成功标准

这条线后续 materialize 为 owner issue 时，最低成功标准应至少覆盖：

### 1. 语义成功标准

- `freely start` 被明确文档化为前台模式
- `freely daemon start` 被明确文档化为后台模式
- UI/TUI 的启动/停止默认对接 daemon 模式，而不是前台 `start`
- UI 关闭默认只关闭前端，不默认执行 `daemon stop`

### 2. 行为成功标准

- 前台 `freely start` 在 `Ctrl+C` 或终端关闭时停止 runtime，且这是预期行为
- 后台 `freely daemon start` 在命令返回后继续存活
- 后台 runtime 在调用它的 shell/PTY 结束后仍保持运行
- `freely daemon stop` 能显式停止后台 runtime
- `freely daemon status` 或等效状态入口能读到后台 runtime 真状态

### 3. 本轮 bug 消失的判定标准

- 使用前台 `freely start` 观察到的会话绑定停机，不再被归类为 runtime bug，而是前台 contract
- 使用后台 `freely daemon start` 进行同类 5 分钟观察时，不应再出现因父会话结束而触发的 `operator_stop_requested`
- 若后台 runtime 后续停机，必须能归因到其他独立原因，例如 rate-limit recovery gap，而不是调用会话 ownership

### 4. 回归控制标准

- 现有围绕 `freely start` 的前台 supervisor tests 继续成立，或只做最小、显式、可解释的调整
- 新增一组独立的 `freely daemon ...` tests，覆盖后台存活、显式 stop、状态读取与 attach-detach 语义
- 现有 `stop/status/live-status/fleet-status` 的 project/runtime 真源不被 UI 或 daemon 入口分叉
- 不把“daemon 后台入口”修复与“rate-limit recovery gap”或其他 recovery 问题绑成一个 issue 一起改

## 待继续研究的问题

1. Freely 的长期主命令面应选择：
   - 只公开 `daemon start/stop/status/logs`
   - 还是后续再补短别名
2. 顶层 `restart` 在前台 contract 下是否继续保留，还是需要 daemon 对应的 restart
3. `logs -f` / attach 模式的 `Ctrl+C` 文案与退出语义如何统一
4. 后台模式与现有 watchdog / dispatcher / recovery contract 的边界如何冻结，避免修入口时误伤恢复链

## Audit Receipt

本轮已补齐把候选停在 pre-brainstorm 的关键证据：

1. `docs/system/workspace/scripts/runtime/freely`
   - `cmd_start()` / `cmd_restart()` 直接进入 `start_project_runtime()`
   - `start_project_runtime()` 在当前 supervisor 进程内主循环运行，并通过 `trap request_stop INT TERM` 处理前台停止
2. `docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
   - 锁定 `start/restart` 仍是同步 project runtime 控制入口
3. `docs/system/workspace/scripts/tests/test-freely-runtime-supervisor-event-log`
   - 锁定 `freely start` 启动的是可被 `freely stop` 结束的前台 supervisor
4. `docs/system/workspace/scripts/tests/test-freely-stop-terminates-all-same-project-supervisors`
   - 锁定 `freely stop` 面向同 project supervisor 族的 kill semantics
5. 仓库内当前不存在独立 `daemon` owner 已吸收这条边界

结论：

- 这条问题已经不是“继续观察”级别，而是可进入 IBM 的产品 contract owner
- 后续 owner 必须先保持 foreground contract 稳定，再新增显式 `daemon` 后台 control plane

## Materialization Readiness

ready_for_materialization: `yes`

理由：

1. 前台/后台/UI close/state truth 的边界已冻结，且不再与 rate-limit recovery gap 混题
2. 现有前台 command semantics 的 canonical evidence 已明确，足以支撑最小回归实现方向
3. `daemon` 作为唯一显式后台模式标记已收敛成单一路径，不再停留在并列方案比较
4. 成功标准、非目标、回归保护面和后续测试分层都已可直接转写为 issue / PRD / pre-tests / tasks
