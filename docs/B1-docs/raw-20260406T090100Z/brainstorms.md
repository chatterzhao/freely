# Brainstorm - 20260406-0901--codex-reconnect-probe-fast-fail

## Problem

当前 Freely 对 Codex API-key live auth 的 non-interactive `exec "hi"` probe 仍然把明显的连接失败征兆当成“等到超时再说”：

- 真实现场里 `codex exec "hi"` 会打印 banner / session id 后出现 `ERROR: Reconnecting...`
- watchdog 只对 `deactivated_workspace` 做 partial-output early exit，`Reconnecting...` 会一直拖到 `CODEX_PROBE_TIMEOUT`
- `ai status` / `ai switch codex` / manager bootstrap 都复用这条 probe，所以现场表现成“卡住很久然后 timeout”

这会把两个问题混在一起：

1. probe 明明已经看到连接失败信号，却还在等待
2. runtime 的 execution-time network taxonomy 能识别很多网络错误，但还没把 Codex 自己的 reconnect 文本纳入

## Confirmed Facts

- 当前 dogfood 环境中的 Codex live auth 是 `apikey`。
- `codex exec "hi"` 既可能成功，也可能打印多次 `ERROR: Reconnecting... N/5` 后长时间不退出。
- 该 reconnect 文本在操作层面上应视为“当前 probe 已经不可用”，不应继续占着 slot-switch probe lock 等待完整 timeout。
- 这类 reconnect 不足以证明 slot/auth 本身坏掉；更接近 runtime-network owner 已定义的 execution-time dependency failure。
- 现有 probe timeout artifact 已能保留 partial output，但它是在等待完整 timeout 之后才写出，过慢。

## Direction

### 1. Codex probe 对 reconnect/连接失败做 partial-output fast-fail

- 当 partial output 出现 `ERROR: Reconnecting...` 或明显连接失败证据时，立即终止 probe 进程树
- 立刻写 probe artifact，而不是继续等到 timeout
- 返回 canonical status `network_failure`

### 2. 这个状态属于“当前 auth 暂不可用”，不是 slot rotation 信号

- `ai status` 直接暴露 `current_auth_probe.status=network_failure`
- `ai switch codex` 对 unsaved live apikey 继续返回 `current_auth_unusable + probe_status=network_failure`
- 不把它伪装成 `timeout`，也不把它升级成 slot/account invalid

### 3. runtime execution-network classification 也要认识 reconnect 文本

- 当真实 worker/cycle log 里出现 `ERROR: Reconnecting...` 时，应落到 execution-time network taxonomy，而不是 generic exit
- 这只是扩充现有 network-failure vocabulary 的匹配面，不重开新的 recovery state machine

## Immediate Slice

- 在 `availability-watchdog.sh` 中增加 reconnect/network partial-output matcher，并做 fast-fail cleanup + artifact
- 在 probe 结果表述与 `ai-cli` 消费路径中接受 `network_failure`
- 在 `freely` 的 execution log network matcher 中纳入 reconnect 文本
- 新增回归测试覆盖：
  - probe partial-output reconnect fast-fail
  - child cleanup
  - artifact 写出
  - `ai status` / `ai switch codex` 暴露 `network_failure`
  - runtime reconnect log classified as execution network failure

## Follow-up Boundary

- 这次不尝试发明“probe 前完全不检查可用性”的新总设计；先把现有预检从“长时间挂起 + timeout”收敛为“快速失败 + 正确分类”
- 若后续仍需让 manager/start 完全依赖 execution-time failure 而不是 launch-time probe，应另开 lifecycle 重新评估 bootstrap contract
