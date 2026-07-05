# 预研头脑风暴：kiro-cli monthly request limit runtime loop governance

## 背景

这轮 dogfood 里，`freely` 在使用 `kiro-cli` 作为 AI 工具时出现了一个很具体的异常：

- `kiro-cli` 输出 `Unable to verify subscription status: service error`
- 随后输出 `Monthly request limit reached`
- root `develop` 侧 supervisor 和 worker worktree 侧 supervisor 都把这类会话记成 `ai_exit_rc_0`
- `slot_switch_reason=none`
- `rate_limit_reason=none`
- 之后 runtime 立即 relaunch，形成短周期空转

这不是单纯的“看见限额提示”这么简单。现在的问题是：

1. 现场已经明确暴露了服务/订阅不可用信号
2. 但 Freely 当前没有把 `kiro-cli` 的这类信号提升成 canonical runtime availability state
3. 结果是 supervisor 把明显不可继续的会话当成正常退出，继续重启

## 已确认事实

### 1. root 和 worker 都复现了同样的现象

root 侧在 `.freely/logs/runtime-events.log` 和连续的 `cycle-20260331-1826*.log` / `cycle-20260331-1827*.log` 中反复出现同一类输出。

worker 侧在对应 worktree 的 `.freely/logs/runtime-events.log` 和 `cycle-20260331-1827*.log` 中也出现同样的输出。

两个 runtime 都表现为：

- 会话看起来“正常结束”
- 但真实原因不是完成任务，而是 Kiro 月度请求额度耗尽或订阅状态校验失败
- 然后立刻进入下一轮 resume / fresh_with_handoff

### 2. 当前 runtime 分类没有把这类 Kiro 输出当成可恢复故障

`docs/system/workspace/scripts/runtime/freely` 目前对 `codex` 有：

- `log_has_auth_failure`
- `log_has_codex_usage_limit`
- `codex_rate_limit_reason_from_usage`

但这条路径没有对 `kiro-cli` 输出的：

- `Unable to verify subscription status: service error`
- `Monthly request limit reached`

做同等级分类。

因此，Kiro 的月度限额/订阅失败在当前 runtime 里更像是“普通退出”，不是“不可继续的 availability failure”。

### 3. 现有治理文档已经承认 `kiro-cli` 不是无限可用的黑盒

`docs/system/workspace/skills/ai-cli-availability-manager/references/limit-patterns.md` 已经把 `kiro` 的限流模式列进去了，说明项目层面早就认为它需要 availability 管理。

但这个 knowledge 还没有明显落到当前主 runtime 的故障分流上。

## 为什么这是 bug，不只是优化

如果只是“用户体验不够好”，那还能算优化。

但现在它已经是 runtime correctness 问题，因为：

1. supervisor 明知道会话不能继续，却把它记成 `ai_exit_rc_0`
2. 这会污染 `live-status` / `workcell-state.env` / `runtime-events.log` 的真相
3. relaunch 继续打到同一条不可用路径，制造短周期空转
4. root 和 worker 两层 supervisor 都会放大这个假健康状态

这不是“应该更聪明一点”的问题，而是“故障分类缺失导致控制面误判”的问题。

## 可能的家族关系

这条预研大概率和以下家族相关，但不是简单重复：

- `ai-cli-availability-manager`
- `watchdog-control-plane`
- `watchdog-slot-sweep-without-cooldown-governance`
- `global-ai-account-watchdog-and-manager-bootstrap`

它们已经覆盖了：

- `402 / deactivated_workspace`
- `auth_failure`
- `rate_limit`
- `oauth_unreachable`

但当前这条是 `kiro-cli` 的月度请求限额 / 订阅状态校验失败落不到分类上的问题。更像是 availability taxonomy 的缺口，而不是已完成家族的简单 replay。

## 开放问题

1. `kiro-cli` 的 `Monthly request limit reached` 应该归入通用 `rate_limit`，还是单独建成 `kiro_subscription_limit`？
2. `Unable to verify subscription status: service error` 是 launch-blocking、retryable，还是应该直接进入 cooldown？
3. root 和 worker 两层 supervisor 是否都需要同一套分类，还是只要 root 侧做 availability gate？
4. 这类错误是否应该像 `codex` 那样写入明确的 cooldown/reset 语义，而不是仅靠 restart-storm 兜底？
5. 现有 `ai-cli-availability-manager` 的 contract 是否足够，只是 runtime 没接上，还是需要补一层针对 `kiro-cli` 的实现面？

## 预研路由

这条先按 pre-brainstorm 处理，不直接进修复。

下一跳只需要先确认：

- 现有 runtime 分类是否真的缺失
- 缺失是 classification 问题，还是 restart policy 问题，还是两者都有
- 这条是否应该 materialize 成独立 issue，还是吸收到现有 `ai-cli-availability-manager` / watchdog 家族
