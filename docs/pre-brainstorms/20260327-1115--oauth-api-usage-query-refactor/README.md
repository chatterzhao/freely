# OAuth API Usage Query 重构预研

## 核心判断

这条 lane 的核心不是“把 OAuth API 接进来”，而是把 Freely 的 `limit -> recover` 主链收紧成一个闭环：

1. **命中 limit 后先找现在可用的 slot**：只要维护好的恢复账本里存在 `usable`，立即切换并重启 AI tool，不进入睡眠。
2. **只有在全部 slot 都不可用时才进入睡眠**：这时才看 cooldown / `reset_at`，选择最早恢复的 slot 作为 sleep target。
3. **OAuth usage sweep 是为了维护恢复账本，不是目标本身**：它负责提前知道哪些 auth 现在可用、哪些最早恢复，从而让 limit 时的切换变成“直接拿一个”而不是现场慢探测。
4. **`~/.codex/` 变化要按语义处理，不是看到变化就 wake**：
   - `usable switch`：代表现在可运行，应继续恢复到重启 tool。
   - `earliest-reset parking`：代表全部不可用时预停到最近恢复 slot，应继续睡到 `reset_at`。

## 主需求

Freely 真正要满足的是：

1. 当前运行 slot 命中 `limit`。
2. 尽快切到“现在可用”的另一个 slot。
3. 切换后重启 AI tool 进程继续跑。
4. 如果全部不可用，就睡到最近恢复时间。
5. 如果 `~/.codex/` 活跃授权发生有意义变化，恢复闭环要继续推进，而不是卡死或自唤醒死循环。
6. 手工执行无参 `switch codex` 时，也要刷新同一份账本并直接切一个可用 slot。

## OAuth API 的价值

通过研究 CodexBar 项目，发现 OpenAI 提供内部 API：

```text
GET https://chatgpt.com/backend-api/wham/usage
Authorization: Bearer <access_token>
ChatGPT-Account-Id: <account_id>
User-Agent: codex-cli
```

返回体不只包含 rate-limit 信息，也可能直接返回：

```json
{"detail":{"code":"deactivated_workspace"}}
```

它的价值不在于“又多了一条 API”，而在于：

1. 可以直接扫 `.ai-auth/codex-*/auth.json`
2. 不需要切活跃 `~/.codex/auth.json`
3. 不消耗 token
4. 可以并行，把 limit 时的候选选择从慢串行试错改成提前维护好的 recovery ledger

## 本轮实测结论

使用本机 `.ai-auth/codex-*/auth.json` 直接并行请求 `wham/usage`：

- 扫描总量：25 个 slots
- 总耗时：约 3.7 秒
- `~/.codex/auth.json` 前后 hash 不变，说明扫描路径不会触碰当前活跃授权位
- 返回分布：
  - `usable`: 8
  - `rate_limited`: 1
  - `deactivated_workspace`: 16

这证明 OAuth sweep 可以承担 “提前维护谁现在可用、谁最近恢复” 的恢复账本更新面。

## 正确闭环

```text
run current slot
  -> hit limit
  -> read maintained recovery ledger
  -> if usable exists:
       switch usable auth into ~/.codex/
       restart AI tool
  -> else:
       refresh sweep if ledger stale or missing
       choose earliest reset slot
       optional parking switch into ~/.codex/
       sleep until reset_at
  -> wake
  -> continue same recovery loop
```

### 睡眠何时允许出现

只有一个前提：

- **已经确认所有 slots 当前都不是 `usable`**

这时 cooldown 才有资格参与决策。  
如果存在任何 `usable` slot，就必须先切它，而不是先看最近恢复。

### `.codex` 变化的语义

不能再把 `.codex/auth.json` 的变化简单当成 “wake signal”。要区分两种恢复语义：

1. `usable switch`
- watchdog 已经找到现在可用的 slot
- 把对应 auth 切进 `~/.codex/`
- 这意味着下一步是重启 AI tool，不是睡眠

2. `earliest-reset parking`
- 所有 slot 都不可用
- 只是把最近恢复的 auth 预停到 `~/.codex/`
- 这不是“现在可运行”，因此不能因为这次变化把睡眠打断

## 设计边界

### `login/save`

- 负责沉淀 `.ai-auth` inventory
- 让 Freely 平时就知道有哪些 slots / auth files 可扫描

### OAuth sweep

- 直接扫 `.ai-auth/*/auth.json`
- 并行请求 `wham/usage`
- 半小时周期维护 recovery ledger
- 手工无参 `switch codex` 时也主动刷新一次
- 全量覆盖写回 availability cache 与 cooldown ledger

### cooldown

- 不是孤立旧账本，而是恢复账本的一部分
- 需要持续维护，不能靠命中 limit 后临时残留
- 账本里至少要能快速看出：
  - 谁现在 `usable`
  - 谁 `rate_limited`
  - 谁最早恢复
- 真正进入 “sleep” 时，只使用其中的 earliest-reset 信息

### 活跃 auth copy

- 只有在两种情况下才碰 `~/.codex/auth.json`
  - 切到 `usable` slot 并继续运行
  - 全部不可用时，为最近恢复 slot 做 parking

### 无参 `switch codex`

- 必须扫描所有授权文件目录并刷新账本
- 若刷新结果里有 `usable`，直接选一个替换到 `~/.codex/auth.json`
- 若刷新后仍全部不可用，再返回最近恢复信息

## 结论

这条 lane 的真问题是 “Freely 如何在 limit 后最快恢复服务”，不是 “是否要支持一个新 API”。  
OAuth usage sweep、availability cache、cooldown ledger、无参 `switch codex`、`~/.codex/` 语义处理，都应围绕“维护好恢复账本并在 limit 时直接拿一个可用 slot”服务。

## 文件

- `brainstorms.md`：详细状态机与恢复闭环
- `candidates.md`：可执行候选与落地顺序
