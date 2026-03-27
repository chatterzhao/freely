# OAuth API Usage Query 重构预研

## 问题陈述

当前 Freely 的问题，不是“有没有 OAuth API 可接”，而是 `limit` 后的恢复闭环不够清楚：

1. 什么时候应立即切换到别的 slot
2. 什么时候才允许睡眠
3. `cooldown` 在决策里到底是什么角色
4. `~/.codex/` 变化代表“现在可运行”，还是只是在为最近恢复做 parking

如果这几个点不钉死，就会出现两种坏结果：

1. 本来有 `usable` slot，却还去看最近恢复，恢复变慢
2. 为最近恢复做的 `.codex` parking 被 watcher 当成 wake signal，形成假唤醒 / 死循环

## 主恢复闭环

正确闭环应只有一条：

```text
current slot hits limit
  -> query inventory truth
  -> if any usable slot exists:
       switch to usable slot
       restart AI tool
  -> else:
       choose earliest reset slot
       optionally park that auth into ~/.codex/
       sleep until reset_at
  -> wake
  -> continue same recovery loop
```

### 关键决策顺序

1. **先看 `usable`**
- 只要 inventory 里存在任何 `usable` slot
- 就立即切换
- 不允许先看 cooldown

2. **只有全部不可用时才看 cooldown**
- `cooldown` 不是孤立旧账本
- 它是 recovery ledger 的 reset 面
- 但它只在 “all unavailable” 时提供 earliest-reset 决策

3. **sleep 不是常规动作**
- 只有确认所有 slot 当前都不可用，且存在最近 `reset_at`
- 才允许进入 `sleep_until_reset`

4. **limit 时优先读取维护好的账本**
- 不能默认每次命中 limit 才现场重扫
- 正常路径应先读最近 30 分钟维护好的 recovery ledger
- 只有账本缺失、过期、或结果不可信时，才触发即时 refresh

## OAuth usage API 的真正位置

通过研究 CodexBar 项目，发现 OpenAI 的 `wham/usage` 可直接基于 `.ai-auth/codex-*/auth.json` 中的 `access_token` 查询账号状态：

```text
GET https://chatgpt.com/backend-api/wham/usage
Authorization: Bearer <access_token>
ChatGPT-Account-Id: <account_id>
User-Agent: codex-cli
```

它的作用不是替代整个恢复 contract，而是让 Freely 能提前知道：

1. 哪些 auth **现在就是 `usable`**
2. 哪些 auth **rate-limited 且何时恢复**
3. 哪些 auth 已经是 `deactivated_workspace`

所以 OAuth sweep 应被定义为：

- `limit` 恢复闭环的 inventory truth layer
- 负责半小时维护 recovery ledger，并在无参 `switch codex` 时做即时 refresh
- 负责加快选择，不负责改变恢复主链的语义

## 本轮实测

对本机 25 个 `.ai-auth/codex-*/auth.json` 并行调用 `wham/usage`：

- wall time 约 3.7 秒
- `~/.codex/auth.json` 前后 hash 保持一致
- 状态分布：
  - `usable`: 8
  - `rate_limited`: 1
  - `deactivated_workspace`: 16

这证明 OAuth 路径适合承担“提前知道谁能切、谁该等”的职责。

## `.codex` 变化的正确语义

问题不是“自己写的还是外部写的”，而是这次变化在恢复闭环里代表什么。

### A. `usable switch`

语义：

- watchdog 已找到当前可用的 slot
- 把该 auth 切入 `~/.codex/auth.json`
- 下一步应重启 AI tool 并恢复运行

结果：

- 这类变化不能继续睡
- 它是恢复成功链条的一部分

### B. `earliest-reset parking`

语义：

- 所有 slot 当前都不可用
- 只是把最近恢复的 auth 预停到 `~/.codex/`
- 目的是到点后更快恢复

结果：

- 这类变化不能被 watcher 误当成 wake signal
- 否则就会自唤醒死循环

所以 `.codex` watcher 必须按 “当前恢复意图” 解释变化，而不是只要变了就 wake。

## 分层重构

### 1. Inventory sweep layer

统一入口，例如：

```bash
codex_oauth_sweep_all_slots() {
  # 1. 遍历 ~/.ai-auth/codex-*/auth.json
  # 2. 提取 access_token / account_id
  # 3. 并行请求 wham/usage
  # 4. 分类 usable / rate_limited / deactivated_workspace / unauthorized / unknown
  # 5. 覆盖写 availability cache
  # 6. 覆盖写 cooldown ledger
}
```

这个函数的职责是“提前知道所有 slot 的现在状态”，供：

- watchdog recovery
- `freely ai status`
- `freely ai switch codex auto`

共同消费。

### 2. Availability cache layer

维护：

```text
$project/.freely/run/codex-availability-cache.tsv
```

记录至少这些字段：

- `slot`
- `status`
- `auth_email`
- `primary_reset_at`
- `secondary_reset_at`
- `refreshed_at`
- `source=oauth_usage`

它的用途是：

- `limit` 发生时直接读取当前可用候选
- `switch codex` 无参时快速选目标
- `freely ai status` 有统一输出面

### 3. Cooldown ledger layer

保留：

```text
$project/.freely/run/codex-slot-cooldowns.tsv
```

但职责要明确：

- 它应是持续维护的 recovery ledger 的 reset 面，不是偶然残留
- 至少每 30 分钟全量更新一次
- 无参 `switch codex` 时也会即时更新一次
- 只在 “all unavailable” 时直接参与决策
- 用于 earliest-reset 选择
- 不应单独覆盖 availability truth，但要和 availability cache 保持同轮刷新

### 4. Active auth switch layer

只有两种合法写入 `~/.codex/auth.json` 的理由：

1. **切到 `usable` slot**
2. **全部不可用时，为 earliest-reset slot 做 parking**

除此之外，inventory sweep 不应触碰活跃 auth。

### 5. Launch continuation layer

切到 `usable` slot 后，要继续完成：

1. 更新 active slot
2. 重启 AI tool 进程
3. 让 manager/worker 恢复推进

所以“切号”不是终点；“切号后恢复运行”才是终点。

### 6. Switch auto layer

`freely ai switch codex` 无参应成为统一入口：

1. 刷新所有授权文件目录的 inventory truth
2. 更新 availability cache + cooldown ledger
3. 若存在 `usable`，直接选一个并替换到 `~/.codex/auth.json`
4. 若全部不可用，则返回最近恢复信息，而不是假装切换成功

## 关键调用路径

### watchdog

遇到 `limit` / `deactivated_workspace` / 明确不可继续时：

1. 先读 recovery ledger
2. 若账本 stale/missing，再调 `codex_oauth_sweep_all_slots`
3. 先找 `usable`
3. 若存在 `usable`：
   - 切换 auth
   - 重启 AI tool
   - 退出 recovery loop
4. 若不存在 `usable`：
   - 选 earliest reset
   - 可选 parking 到 `~/.codex/`
   - 睡到 `reset_at`

### `freely ai status`

1. 默认读 availability cache
2. cache 过期时触发一次 OAuth sweep
3. 展示：
   - `usable` 数量
   - `rate_limited` 数量
   - `deactivated_workspace` 数量
   - 最近恢复时间

### `freely ai switch codex auto`

1. 刷新所有授权文件目录并更新账本
2. 若存在 `usable`，切到最佳 `usable`
3. 若全部不可用，返回最近恢复提示，而不是假装切换成功

## 兼容边界

### `deactivated_workspace`

这类 slot 应在 inventory 层直接判为 hard unavailable，不应再进入可切换候选。

### fallback

如果 OAuth 接口异常或结构变化：

- 当前 sweep 可标记 `unknown`
- 允许 launch-time confirmation / fallback probe 兜底
- 但 fallback 不应重新升级为默认全量扫描路径

## 推荐落地顺序

1. 先重写 watchdog 恢复状态机，明确：
   - `usable` 优先
   - `all unavailable -> earliest reset -> sleep`
   - `.codex` 变化的 `usable switch` / `parking` 语义
2. 再把 OAuth sweep 接成 30 分钟维护 + switch-on-demand refresh 的 inventory truth
3. 再让 cooldown 成为和 availability cache 同步更新的 recovery ledger reset 面
4. 最后补真实环境验证：
   - 命中 limit 后切到 `usable`
   - 无参 `switch codex` 会刷新全部 auth 目录并直接切一个可用 slot
   - 全部不可用时进入 sleep
   - parking 不会造成假 wake

## 结论

OAuth 不是这个 lane 的中心；`limit` 后如何最快恢复服务才是中心。  
正确重构应围绕 recovery loop 展开，再把 OAuth sweep、cooldown、`~/.codex/` watcher 都降成服务这条主链的辅助层。
