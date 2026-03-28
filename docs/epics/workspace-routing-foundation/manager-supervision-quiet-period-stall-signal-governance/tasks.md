# Tasks - manager-supervision-quiet-period-stall-signal-governance

1. 补一条直接冻结当前 dogfood 现场的负向测试：quiet-period lawful wait 不得 recovery。
2. 补两条相关性负例：无关 active worker、以及 active 但 non-busy worker 都不得错误 suppress recovery。
3. 补一条 paired positive 测试：quiet-period 一旦叠加强 stall evidence，仍应 recovery。
4. 选择最小 delegated-supervision idle-safe contract 修法，不做全局阈值放大。
5. 跑 focused regressions 与现有 delegated continuation 回归批次。
6. 把 restart-storm 复核与 runtime-owned recovery stop observability 区分留作 follow-on，不与本 issue 混补。
