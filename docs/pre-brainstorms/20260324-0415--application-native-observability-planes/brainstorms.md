# 预研：application-native observability planes

## Trigger

- 当前 Freely 自举里，`live-status`、`fleet-status`、`prompt`、`manager-continuity`、`worker-prompts`、`session jsonl`、`cycle log` 都已经是有效信号，但仍然偏碎片化。
- 用户进一步明确了产品需求：Freely 不只需要 CLI 状态面，还需要为 CLI / TUI / GUI / future API 暴露同一套可观察运行状态，给用户稳定的插话着力点。
- 这条能力还必须能泛化到 Freely 开发其他应用时的真实环境测试，而不能写死成“所有应用都看 Freely 自己的日志文件”。

## Problem

Freely 现在已经有“当前态控制面”的一部分，也有“前端 probe”方向，但缺少一份把两者桥接起来的观测平面契约。

这会带来四类问题：

1. Freely 自己的运行状态已经可观察，但还没有被表达成多平面产品能力：
   - 当前态
   - 会话映射
   - 实时流
   - 多 worktree / 多 subagent fleet
   - artifact / evidence
2. stall 判断和人工监督还容易被误写成“看某个固定日志或等 90 秒”，而不是先依据当前应用自己的观测表面。
3. 未来 Freely 开发其他应用时，若没有泛化的 observation contract，就会把 Freely 自己的 `jsonl / cycle log` 误当成通用规则。
4. CLI / TUI / GUI / future API 目前已有“统一前门”和“frontend probe”方向，但尚未冻结“同一 backend contract 提供多种 observability plane”的产品边界。

## Direction

应把这条能力收敛成两层：

### 1. 通用层：application-native runtime observation contract

不预设任何应用必须有 Freely 风格日志，而是先定义：

- `observation_surface`
  - 当前应用真实能暴露哪些运行表面
  - 可能是 CLI、UI、HTTP status、structured logs、session trace、DB row、queue depth、test runner output 等
- `progress_signal`
  - 哪些变化说明当前执行仍在推进
- `stall_signal`
  - 哪些变化说明执行已空转、冻结或重复
- `acceptance_evidence`
  - 哪些真实环境证据可以判测试通过

### 2. Freely 自举实例层：Freely observability planes

Freely 自己作为第一份 concrete profile，应该把当前已有信号映射成统一平面：

- `current-state plane`
  - `live-status`
  - 当前 supervisor / dispatcher / AI / worker 的 activity
- `fleet plane`
  - `fleet-status`
  - 多 worktree 的 branch / issue / runtime / phase / desired state
- `session plane`
  - `session_refs`
  - `jsonl_path`
  - `cycle_log`
  - `prompt_file`
- `artifact plane`
  - `manager-continuity`
  - `worker-prompts`
  - intake / resolution / verification / cleanup evidence
- `stream plane`
  - 默认折叠，按需展开实时日志 / event tail

## Product Shape

这条能力不应只停在 watchdog CLI。

它最终应支持：

- CLI：当前态查询、深挖入口、tail 入口
- TUI / GUI：点击状态可展开到对应 session / log / artifact
- future API：把同一 backend contract 暴露给前端层，而不是每个前端自己拼日志

也就是说：

- `cli-first observability` 仍成立
- 但 CLI 只是第一消费面，不是唯一消费面
- 前端 probe / GUI 应该共享同一 backend observability contract

## Coordination With Existing Lines

### `20260320-1945--watchdog-live-status-surface-and-manager-supervision`

- 这条线负责最小 `live-status` current-state surface。
- 当前新线不重复定义 `live-status` 本身，而是向上补“多平面 observability contract”。

### `20260322-0115--cli-first-entrypoint-and-observability-surface-unification`

- 这条线负责把 CLI 定成 canonical front-door/backend。
- 当前新线补的是“同一 backend contract 应暴露哪些 observability planes”，供 CLI / TUI / GUI / API 共用。

### `20260308-1244--frontend-probe-dogfooding-loop`

- 这条线负责产品 Probe/UI。
- 当前新线补的是 Probe/UI 底下应该消费怎样的 observability plane，而不是再重开 UI 范围。

### `20260322-0715--pre-test-merge-post-merge-acceptance-stall`

- 这条线继续关注 delegated acceptance stall 何时成立。
- 当前新线只提供“如何观察 progress / stall”的上游协议，不替代具体 stall candidate。

## Draft Contract

### Observation Order

对于任何应用，默认观察顺序应是：

1. 先读当前态 surface
2. 再读该应用的最近 progress/stall tail
3. 再看会话 / artifact 深挖入口
4. 时间阈值只做最后兜底

Freely 自举实例里，这一顺序当前具体落成：

1. `live-status`
2. `cycle log tail` / relevant session `jsonl` tail
3. `manager-continuity` / `worker-prompts` / intake-resolution artifacts
4. watchdog stall threshold

### Minimum Plane Set

若一个应用暂时没有完整 UI，也至少要能回答：

- 现在谁在跑
- 现在在做什么
- 当前属于哪个 worktree / issue / lane / session
- 最近一次推进信号是什么
- 若卡住，去哪里深挖

## Intended Landing

当前先留在 pre-brainstorm，不直接改 `docs/system/**`。

若边界稳定，后续可能分别落到：

- `docs/system/workspace/skills/multi-worktree-supervision/**`
- `docs/system/workspace/skills/watchdog-control-plane/**`
- `docs/system/workspace/skills/branch-management/**`
- `docs/system/workspace/agents/manager-agent.md`
- frontend probe / API contract 真源

## Non-Goals

- 本轮不直接做 GUI 设计
- 不直接实现新的 event streaming server
- 不把 Freely 自己的 `jsonl / cycle log` 写死成所有应用的唯一观察方式
- 不在本轮直接把 stall detection 全部产品化
