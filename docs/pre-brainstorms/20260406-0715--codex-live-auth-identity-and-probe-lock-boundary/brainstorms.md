# Brainstorm - 20260406-0715--codex-live-auth-identity-and-probe-lock-boundary

## Problem

Freely 现在把 Codex 当前身份过度绑定到 saved slot 元数据：

- `whoami/status/watchdog` 会优先相信 `.ai-auth/.codex-current-slot` 或 `.codex/active-slot`
- 当 live auth 已经切到 `apikey`，但当前机器并没有通过 Freely `login/save` 生成匹配 slot 时，CLI 仍可能回显陈旧 slot
- watchdog 的 manager bootstrap 只有在 `current_slot` 非空时才 probe 当前 live auth，导致“真实 live apikey 可 probe，但因为没有 saved slot 身份而被跳过”

这会把三个不同概念混在一起：

1. live auth 当前真相
2. saved slot inventory
3. slot-switch lock 的串行化边界

## Confirmed Facts

- 当前本机 live Codex auth 是 `apikey`。
- 当前本机 `whoami/status` 可能回显旧 slot 名，而不是来自 live auth 的可证实身份。
- `.ai-auth/.codex-current-slot` 与 `.codex/active-slot` 可以彼此漂移。
- watchdog 目前把“是否 probe 当前 auth”建立在 `current_slot` 是否存在上，而不是建立在 live auth 是否存在上。
- 真实 `codex exec` 在当前现场会打印 banner 与 session id 后长时间无后续输出，Freely probe 因此得到 `timeout`，这与 stale slot 误判是两个独立问题。
- 旧的 probe timeout 清理只杀外层 subshell，可能把 `codex exec` 子进程遗留成 orphan。

## Direction

### 1. 当前身份先看 live auth，再尝试映射到 saved slot

- 先从 live `auth.json/config.toml` 判定 `slot_kind/provider/account`
- 只有当某个 saved slot 的 bundle 与 live auth 真正匹配时，才把它作为当前 slot
- 若没有匹配 saved slot，则返回 `slot=null`，但仍保留 `slot_kind=apikey|account`

### 2. manager bootstrap 必须支持 unsaved live auth

- 对于当前 live auth，只要 `whoami` 已经能证明存在有效 kind，就允许 watchdog probe
- 若没有 saved slot，可用 `live-apikey` / `live-account` 作为内部 state identity，而不是直接放弃 probe

### 3. lock boundary 保持“探测要串行”，但不再让错误身份驱动 probe

- probe 仍然要持有 slot-switch lock，避免与真实 switch 并发
- 但当前 probe 的 target identity 必须来自 live auth truth，而不是 stale active-slot 文件
- 后续若还出现 probe/self-block，再单独收窄到 lock owner inheritance 与 startup waiting 语义

## Immediate Slice

- 修正 `ai-cli whoami/status/sync_current_auth/dry-run` 的 current-slot 解析
- 修正 watchdog 对 unsaved live auth 的 probe 入口
- 修正 watchdog probe timeout 的 child cleanup，避免遗留孤儿 `codex exec`
- 为 stale active-slot 与 unsaved live apikey 增加回归测试

## Follow-up Boundary

- 当前 slice 不试图“修好”真实现场里的 `codex exec` 卡住问题。
- 若 `current_auth_probe.status=timeout` 持续出现，应把它作为独立 issue 处理，重点检查：
  - 当前 Codex API key 会话是否本身就无法完成最小 `exec` 调用
  - probe 证据产物是否足以区分 banner-only stall、rate limit、workspace deactivated
  - `status` / runtime 需要不需要把这类 timeout 归类得更明确，避免被误认为 stale slot 或 lock 问题
