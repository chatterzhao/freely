# IBM Brainstorm: global-ai-account-watchdog-and-manager-bootstrap slot-switch global launch gate

## Context

2026-03-26 live dogfood 暴露出两条同族缺口：

1. `bin/ai switch` 已报告某个 slot `usable`，但紧随其后的真实 Codex 使用仍可能先命中一次 `402 deactivated_workspace`；再执行一次 switch 才恢复。
2. `baseline-status` / `session-state` / `whoami` 相关可视面里混入了 `[WARN] codex slot switch is already in progress ...` 文本，说明 warning/log 与机器可读状态没有彻底隔离。

这两条都落在 `I-20260318-1630` 的同一条恢复 contract 里，而不是新的 capability island。

## Latest intent

1. `.ai-auth/<slot>` 是唯一身份；auth email 只是不可信的 metadata。
2. `cooldown` 已退出任何主恢复逻辑；真实可用性必须通过具体 probe 决定。
3. 只要正在执行 slot switch / probe sweep，就不允许任何新的 Codex AI 进程拉起。
4. 只有在某个 slot 被真实 probe 证明可用、并且 switch lock 已释放后，新的 manager / worker `codex exec` 才能启动。
5. 如果所有 slot 当前都不可用，watchdog 保持低频真实 reprobe；`earliest reset` 仅作观测 hint。
6. 监控面可以利用 auth inventory 变化作为唤醒信号，但不能在 inventory 变化尚未验证可用前抢拉新的 AI。

## Findings

1. 现有 serialization 主要覆盖 `switch` / `whoami` / `list` / watchdog probe / `ensure-manager`，但没有覆盖真正的 `codex exec` launch path。
2. `tool-launchers.sh` 当前直接 `exec codex ...`，没有等待 slot switch lock。
3. `availability-watchdog.sh` 中的 `wait_for_codex_slot_switch_idle()` 会发 warning，而 `freely` 的 `log_warn` 走 stdout；因此 command substitution 读取 slot/state 时会把 warning 一起吃进去。
4. 这解释了两个现场现象：
   - machine-readable slot 状态被 warning 污染
   - switch/probe 窗口里若有新的 AI launch 抢跑，可能在坏/瞬时 auth 下命中一次 `402`，随后二次 switch 或下一轮恢复才成功

## Decision

1. 该 continuation 不新开 issue，直接吸收到 `I-20260318-1630`。
2. 本轮实现要补两层 gate：
   - 全局 launch gate：任何新的 Codex launch 必须等待 slot switch lock 清空
   - 输出隔离 gate：warning/log 一律不得污染 slot/session/launch 等机器可读字段
3. 测试必须升级到能够直接验收上面两个 gate，而不再只测 watchdog/ensure-manager 层面的局部串行化。

## Required implementation slices

1. 在实际 Codex 启动路径上增加 switch-lock wait/defer，而不是只在 watchdog probe 路径等待。
2. 让 command-substitution-facing 的 slot/status 读取只输出机器可读结果，warning 走 stderr 或单独 observability sink。
3. 让 `auto switch -> first subsequent codex launch` 形成一个稳定、可测试的 contract。

## Risks

1. 只修 warning 输出而不补 launch gate，会继续保留第一次 switch 后偶发 `402`。
2. 只补 launch gate 而不修 stdout/stderr contract，会继续污染 session/baseline truth，导致 manager 的状态面漂移。
3. 只在 `ensure-manager` 层补 gate 不够，因为 worker / monitor / tool launcher 仍可绕路直接启动 Codex。
