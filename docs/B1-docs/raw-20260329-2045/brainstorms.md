# Brainstorms - 20260329-2045--ai-auth-change-wake-recursion-and-command-lifecycle

## Context

在 `2026-03-29` 的本地实测中，`bin/ai` 的账号相关命令出现了一个新的命令生命周期问题：

- `list`
- `whoami`
- `status`

都能自行退出，其中 `status codex` 在缓存不新鲜时会先做 inventory refresh，但最终仍能退出。

真正异常集中在：

- `bin/ai switch codex <slot>`
- `bin/ai login codex`

它们在“用户可见成功输出已经出现后”仍不退出，并且需要 `Ctrl+C`。

## Reproduced Facts

### 1. `switch codex` 已打印成功 JSON 但前台不退出

在独立工位中执行：

- `./bin/ai --yes --format json switch codex worahe1000@outlook-com-3`

前台已经输出：

- `{"switched": true, ...}`

但命令仍未结束。

继续检查进程树后发现：

- 前台 `ai-cli` 仍在
- 它的子进程是 `freely auth-change-wake --tool codex --slot ... --reason switch_success`
- 该 `auth-change-wake` 又继续派生更多同样的 `auth-change-wake`

这不是单纯“输出后忘记 exit”，而是同步 wake 链没有收口。

### 2. 不需要真实登录，也不需要切到别的 slot，问题仍可复现

为了避免把问题误判成 OAuth 交互或 slot 切换副作用，后续又做了一次更窄复现：

- 先用 `./bin/ai --format json whoami codex` 读出当前 slot
- 再执行 `./bin/ai --yes --format json switch codex <current-slot>`

这次是 no-op switch，仍然出现同一现象：

- 成功 JSON 已打印
- 前台 `ai-cli` 5 秒后仍未退出
- 其子进程仍是 `freely auth-change-wake --reason switch_success`

因此当前问题不依赖：

- 真实 OAuth 登录
- 切到一个不同 slot
- slot 删除或清理动作

只要成功路径进入 `switch_success -> auth-change-wake`，问题就成立。

### 3. `login codex` 本身先进入正常交互等待

短时观察 `./bin/ai login codex` 时，先看到的是正常的：

- `Starting local login server on http://localhost:1455`

这一步本身不能视为泄漏，因为它确实在等待用户完成 OAuth。

### 4. `login codex` 的后成功阶段高度疑似会进入同类 wake 链

对 `login codex` 发送 `Ctrl+C` 后，前台仍继续打印了：

- `Auto-saved auth email: ...`
- `Slot: ...`
- `Location: ...`

随后检查进程，发现：

- 前台 `ai-cli login codex` 仍存活
- 它的子进程是 `freely auth-change-wake --tool codex --slot ... --reason login_success`
- 该 wake 进程再次递归派生更多相同 `auth-change-wake`

这说明 `login` 的后成功阶段至少高度疑似与 `switch` 共享同一个同步 wake 问题，但当前最干净、最稳定的硬复现仍然是 `switch`。

## Root Cause Hypothesis

当前问题更像“命令生命周期设计错误 + wake 递归”，而不只是一般意义上的泄漏。

已知链条是：

1. `bin/ai` 只是一层薄包装，真正逻辑在 `docs/system/workspace/scripts/runtime/ai-cli`
2. `cmd_login()` 和 `cmd_switch()` 在成功后都会同步调用：
   - `notify_freely_auth_change()`
3. `notify_freely_auth_change()` 直接执行：
   - `bin/freely auth-change-wake ...`
4. `auth-change-wake` 会遍历所有 registered 且 `desired=running` 的 manager project，并同步跑：
   - `ensure_manager_once`
5. watchdog 路径中的 `switch_to_codex_slot()` 又会调用：
   - `ai switch codex <slot>`
6. `ai switch` 成功后再次触发：
   - `notify_freely_auth_change()`

因此当前最强嫌疑是：

- `ai switch/login -> auth-change-wake -> ensure_manager/watchdog -> ai switch -> auth-change-wake`

形成了自激递归链。

但这里仍应区分：

- `switch -> auth-change-wake` 的进程树证据已经直接看到
- `auth-change-wake -> ensure_manager/watchdog -> ai switch -> notify` 作为完整闭环，目前是强嫌疑，不应在 pre-brainstorm 中写成已完全抓到的既成事实

## Boundary

本条研究应保持边界清晰：

- 它不是当前 invalid resume evidence 问题
- 它不首先是账号池可用性问题
- 它也不首先是 OAuth 登录能力问题
- 它当前也还不是“已证实的长期后台进程泄漏”

当前最小问题面是：

- 账号命令成功后是否应该同步阻塞在全局 auth-change wake 上
- auth-change wake 是否允许再次触发会回调到同一路径的 `ai switch`
- 操作者 `Ctrl+C` 后是否仍会留下递归 helper 进程
- no-op switch 为什么仍会被拉进同样的同步 wake 链

## Initial Decision

这条线值得作为独立 pre-brainstorm 保留，最小结论是：

1. `bin/ai switch codex` 的“输出成功但不退出”不是假问题，且 no-op switch 即可复现
2. `bin/ai login codex` 的“正常等待登录”本身不是 bug；当前只把它记录为共享同类 wake 问题的高嫌疑路径，不作为第一阶段修复入口
3. 目前最稳妥的归类是“命令生命周期与 wake 递归问题”，而不是已经坐实的长期进程泄漏
4. 当前问题更准确地应命名为：
   - `auth-change-wake recursion and command lifecycle`
5. 后续如果进入 issue，第一跳应优先冻结：
   - success-path 是否改为 async wake
   - wake 内部是否禁止再触发 notify
   - no-op switch 的最小退出 contract
   - operator interruption 后的 residual helper cleanup contract
