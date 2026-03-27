# Pre-tests

## Pre-merge acceptance

1. 当 OAuth inventory sweep 扫描 `.ai-auth/codex-*/auth.json` 时，`~/.codex/auth.json` 的内容不得被修改。
2. 同一轮 full sweep 必须统一分类至少四类结果：
   - `usable`
   - `rate_limited`
   - `deactivated_workspace`
   - `unknown` / `unauthorized`
3. full sweep 结束后：
   - availability cache 必须写回完整 sweep 结果
   - `codex-slot-cooldowns.tsv` 必须以 overwrite 方式重建，而不是保留旧脏账本
4. `freely ai switch codex auto` 与 watchdog recovery 必须先消费 sweep/cached 结果，再决定是否对目标 slot 执行真实 auth copy / launch-time confirmation。
5. rate-limited slot 的 reset 时间必须保留在 cooldown ledger 中，但不得因为 earliest reset 就在未确认 usable 前直接切到该 slot。

## Post-merge acceptance

1. 在 canonical `develop` 上，`freely ai status` 不应再通过全量真实 probe 才给出 inventory 结果；cache 过期时触发的默认刷新应优先走 OAuth sweep。
2. 当当前 slot 命中 limit 后，watchdog 的恢复路径应先刷新 OAuth availability truth，再决定是否切到新 slot；不能回退为单靠 cooldown 账本直接切号。
3. canonical `develop` 上的 dogfood recheck 必须能证明：
   - sweep 不会污染当前活跃 auth
   - rate-limited slot reset 账本保持更新
   - `deactivated_workspace` slot 不会在 inventory 层被误判为可切换目标
