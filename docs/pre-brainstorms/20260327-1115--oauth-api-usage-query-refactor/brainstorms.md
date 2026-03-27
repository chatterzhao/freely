# OAuth API Usage Query 重构预研

## 问题陈述

当前 Freely 的 slot 可用性治理还绑在“切活跃 auth -> 真实 probe -> 恢复”的老路径上，这有四个明显问题：

1. **消耗 token**：全量扫描会消耗真实 Codex probe
2. **速度慢**：串行扫描所有 slots，时延随 slot 数线性增长
3. **入侵活跃工作位**：扫描时会复制授权文件到 `~/.codex/auth.json`
4. **账本稀疏**：`codex-slot-cooldowns.tsv` 目前更多是被动残留，而不是持续维护的 inventory 状态

## 新发现

OpenAI 的 `wham/usage` 接口可以直接基于 `.ai-auth/codex-*/auth.json` 中的 `access_token` 查询账号状态，不需要切换活跃 auth：

```text
GET https://chatgpt.com/backend-api/wham/usage
Authorization: Bearer <access_token>
```

这条路径有三个决定性价值：

1. **不消耗 token**
2. **不需要复制 auth.json 到 `~/.codex/auth.json`**
3. **可以并行扫全部 `.ai-auth` inventory**

## 本轮实测

对本机 25 个 `.ai-auth/codex-*/auth.json` 并行调用 `wham/usage`：

- wall time 约 3.7 秒
- `~/.codex/auth.json` 前后 hash 保持一致
- 状态分布：
  - `usable`: 8
  - `rate_limited`: 1
  - `deactivated_workspace`: 16

因此这条 API 已经不仅能看 quota，还能直接提供不少 hard-failure 信号。

## 关键设计判断

### 1. OAuth sweep 应取代“全量真实 probe”成为一级真相层

以后“全量扫所有 slots”的动作应该是：

```text
scan ~/.ai-auth/codex-*/auth.json
  -> extract access_token
  -> parallel OAuth usage requests
  -> classify all slots
  -> overwrite cache + cooldown ledger
```

而不应该再是：

```text
for each slot:
  copy auth -> ~/.codex/auth.json
  run codex exec probe
  parse result
  restore auth
```

### 2. cooldown 要保留，但职责要重构

`codex-slot-cooldowns.tsv` 不应删除，因为它仍然是 watchdog 的重要账本。但它不再承担“直接决定切哪个号”的职责，而应变成 sweep 驱动的 ledger：

- 由 OAuth sweep 全量覆盖写回
- 只保留需要 reset 的 slot
- 保存 normalized slot 与 reset 时间
- 作为 earliest-reset hint / inventory ledger，而不是单独的恢复真相

这意味着 cooldown 不再是“过期猜测”，而是“由 30 分钟周期 sweep 持续维护的状态面”。

### 3. 活跃 auth 切换只保留到 launch-time

只有以下场景才允许把某个 slot 的授权文件复制到 `~/.codex/auth.json`：

1. watchdog 已经从 OAuth sweep 选定一个 `usable` candidate
2. `freely ai switch codex auto` 最终决定切到该 slot
3. launch-time 需要最小真实确认

也就是说：

- inventory sweep 不碰活跃 auth
- final launch/switch 才碰活跃 auth

## 建议的新分层

### A. Inventory sweep layer

统一入口，例如：

```bash
codex_oauth_sweep_all_slots() {
  # 1. 遍历 ~/.ai-auth/codex-*/auth.json
  # 2. 并行请求 wham/usage
  # 3. 分类 usable / rate_limited / deactivated_workspace / unauthorized / unknown
  # 4. 一次性写 availability cache
  # 5. 一次性覆盖写 cooldown ledger
  # 6. 输出 machine-readable summary
}
```

这个函数是共享真相入口，供：

- watchdog recovery
- `freely ai status`
- `freely ai switch codex auto`

共同消费。

### B. Availability cache layer

新增或强化：

```text
$project/.freely/run/codex-availability-cache.env
```

记录每个 slot 的：

- `status`
- `email`
- `plan`
- `primary_used`
- `primary_reset`
- `secondary_used`
- `secondary_reset`
- `last_refresh_at`
- `source=oauth_usage`

TTL 建议 30 分钟，因为这条路径不消耗 token。

### C. Cooldown ledger layer

保留：

```text
$project/.freely/run/codex-slot-cooldowns.tsv
```

但改成 sweep overwrite 模式，而不是增量残留。建议格式至少保持兼容：

```text
<normalized_slot>\t<reset_at>\t<human_readable>
```

必要时可追加 source/status 列，但第一阶段可先兼容旧格式。

### D. Launch-time confirmation layer

真实 probe 不删，但降级为最终确认层，只处理：

1. OAuth 不能表达的故障
2. 被选中 slot 的真实 exec-path 可用性
3. launch 前最小确认

它不再负责扫全量 inventory。

## 关键调用路径重构

### watchdog

遇到 limit / auth failure / inventory change 时：

1. 调 `codex_oauth_sweep_all_slots`
2. 更新 availability cache 与 cooldown ledger
3. 选择 `usable` candidate
4. 若存在 candidate，才执行 launch-time auth copy
5. 若没有 `usable`，保持 manager/worker down，靠后续周期 sweep 再判

### `freely ai status`

1. 默认读 availability cache
2. cache 过期时触发一次 OAuth sweep
3. 直接展示 sweep 结果，而不是临时触发重型真实 probe

### `freely ai switch codex auto`

1. 调用同一个 OAuth sweep / cache 入口
2. 选最佳 `usable` slot
3. 仅在最终切换时复制对应 `auth.json` 到 `~/.codex/auth.json`

## 兼容边界

### `deactivated_workspace`

本轮实测表明 `wham/usage` 已经能直接返回：

```json
{"detail":{"code":"deactivated_workspace"}}
```

因此这类 slot 可以直接在 inventory 层判为 hard unavailable，无需先切到活跃 auth 再发现。

### rate-limited slot

rate-limited slot 不应被直接切换，只应：

- 写回 cooldown ledger
- 在 availability cache 中记录 reset 时间
- 作为排序 / hint 使用

### fallback

若 OAuth 接口异常或返回无法识别的结构：

- 当前 sweep 可标记 `unknown`
- 由 launch-time confirmation 或 fallback probe 兜底
- 但不应把 fallback 重新升级为默认全量扫描路径

## 推荐落地顺序

1. 在 `availability-watchdog.sh` 新增 `codex_oauth_sweep_all_slots`
2. 增加 availability cache 写回函数
3. 改造 cooldown ledger 为 sweep overwrite 模式
4. 改写 `probe_all_codex_slots_and_update_cooldown()`，让它从“全量真实 probe”转成“OAuth inventory sweep + launch-time confirmation”
5. 改写 `freely ai status` 与 `switch codex auto` 共用同一套结果

## 结论

这次 OAuth 方案不是小优化，而是值得重构 control plane 的新主路径。真正应该保留的旧能力，不是“全量串行真实 probe”，而是“最终 launch-time 确认”。前者该被 OAuth sweep 吸收，后者继续作为最后一道守门。 
