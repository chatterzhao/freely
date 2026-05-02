# 预研头脑风暴：runtime forensic time alignment and stall observability

## 背景与问题

这轮 `freely` manager stall 追查暴露出一个新的治理缺口，但它不等于“时间显示治理失效”。

现场真实情况是：

1. 同一轮 run 的主要证据面混用了不同时间表达：
   - `.freely/logs/runtime-events.log` 使用 UTC RFC3339
   - `prompt` / `cycle log` / `jsonl` 常通过文件 mtime 以宿主本地时间观察
   - `.freely/run/preemption-state.env` 也保留 RFC3339 UTC
2. 这导致首轮人工取证时，很容易先把 `2026-04-13T01:12:03Z` 与 `2026-04-12 18:12:03 PDT` 当成两批不同 run 的现场。
3. 进一步对齐后确认：并不是看错旧日志；是同一轮 run 内 watchdog 的 stall recovery 与人工 `stop` 在同一秒发生。
4. 更大的问题不是“时区显示错了”，而是 stall recovery 原先没有显式 runtime event，因此即使 recovery 已触发，`runtime-events.log` 也看不出来，只能靠残留 state file 倒推。

## 已确认事实

1. 现有时间治理 owner 已冻结正确边界：
   - UTC naming truth
   - RFC3339/epoch storage truth
   - host-local human display truth with timezone label
   - 代表 owner: `runtime-human-readable-time-display-governance`

2. 这次误读并非由“旧 run 被错认成当前 run”造成，而是同一轮证据跨面后缺少直接可对齐锚点：
   - `runtime-events.log` 中启动时间：`2026-04-13T01:12:03Z`
   - 同一 prompt mtime：`2026-04-12 18:12:03 PDT`
   - 同一 preemption state mtime：`2026-04-12 18:17:03 PDT`
   - `preemption-state.env` 明确记录了 `runtime-stalled-ai-recovery`

3. 这说明真正缺的是 forensic/observability contract，而不是 display formatting contract：
   - 人类可读 status 输出是否本地化
   - 与多证据面取证时是否可一眼对齐
   这是两类不同能力。

4. 本 worktree 已先补一个最小 runtime 侧 observability fix：
   - stall recovery 触发时写 `runtime_stalled_ai_recovery_triggered`
   - 这样以后无需依赖 `preemption-state.env` 残留倒推

## 当前判断

这条问题不应直接写进 `CONSTITUTION` / `LAWS`，也不应重开 display-time owner。

更合适的归属是：

1. 先作为 pre-brainstorm 记录“forensic alignment”是一个独立 follow-on。
2. 若继续 materialize，应挂到 runtime observation / observability family，而不是 runtime time display family。

## 最小正确设计方向

### 1. 明确区分三种时间面

- naming truth: UTC / filename timestamp
- storage truth: RFC3339 or epoch
- forensic alignment surface: 让不同证据面能直接互相定位为同一轮 run

### 2. 补 runtime-level correlation anchors

优先级高于再改更多 display 文案：

- stall / recovery / operator stop / supervisor cleanup 等关键事件必须都进入同一个 runtime event ledger
- 关键事件应带足以跨面关联的字段，例如：
  - prompt path
  - cycle log path
  - session id / jsonl path
  - role
  - reason

### 3. 明确人工取证约束

对需要跨 `runtime-events.log`、文件 mtime、state env、session jsonl 做判断的场景，应有一条明确规则：

- 不能只看一种时间表达
- 必须先把 UTC RFC3339 与 host-local mtime 对齐到同一绝对时间线，再判断是否为同一 run

### 4. 不把 display owner 扩大成 forensic owner

非目标：

- 不把“给人看”的本地化时间输出治理，混成“调试取证”契约
- 不要求所有 runtime artifact 都同时打印双时区
- 不重写现有 UTC filename / RFC3339 storage 规则

## 推荐吸收边界

首选 follow-on owner 应落在 runtime observation / observability family，可能是：

- reopen `application-native-runtime-observation-contract-and-observability-planes`
或
- 新开一个更窄的 runtime forensic correlation / stall recovery observability owner

判断标准：

- 如果 scope 只是“关键恢复事件必须显式可见并可跨面关联”，新窄 owner 更合适
- 如果要把取证对齐规则正式升成 observation plane contract，则可作为 observation owner 的 reopen/follow-on

## Landing Zones

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-manager-stall-recovery`
- `docs/system/workspace/scripts/tests/` 下新增取证对齐 / event emission regression
- runtime observation owner docs

## 建议的下一步

1. 先把本次确认的 runtime event emission 修复合并。
2. 再决定是否需要一条独立 owner 去冻结：
   - forensic time-alignment checklist
   - cross-surface correlation minimum fields
   - stall recovery observability minimum contract
