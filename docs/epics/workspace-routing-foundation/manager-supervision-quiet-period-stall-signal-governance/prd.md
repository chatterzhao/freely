# PRD - manager-supervision-quiet-period-stall-signal-governance

## Product outcome

让 Freely 的 manager watchdog 在 delegated-supervision 场景下不再把合法 quiet-period 误杀成 stalled，同时保留真 stall 的自动恢复能力。

## User-visible behavior

- Freely 在 manager 正常监督 active worker 时，不会因为短时间没有新的 `cycle log` 输出就自杀式重入。
- 当 manager 真 stalled，或者出现更强的 stale / missing runtime evidence 时，runtime 仍会恢复，不需要人工 `stop/start`。
- runtime-owned recovery 的事件命名和可观测性区分保留为 follow-on，不阻塞本轮最小行为修复。

## Constraints

- 不降低已有 delegated continuation stall recovery 的真阳性覆盖。
- 不先依赖简单调大全局阈值来掩盖问题。
- 不让 `develop` manager 直接施工。
