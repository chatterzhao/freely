# PRD - manager-delegated-continuation-stall-recovery-governance

## Product outcome

让 manager delegated continuation stall recovery 具备 idle-safe contract：

1. 合法的 `same-lane busy` 等待不会被误杀成 stalled manager
2. 旧 continuity、stale prompt target、坏的 launch-state truth 也不会反过来压住应有的 recovery

## User-visible behavior

- 当 canonical worker 正在正常推进，而 manager 只是等待该 worker 完成当前 delegated continuation 时，Freely 不再每隔几分钟自我重启 supervisor。
- 当 continuity 里其实还存在可启动的 worker prompt，或已出现 stale/missing target，Freely 仍会按原 contract 触发 recovery / relaunch，而不是继续假装在 lawful wait。

## Constraints

- 保持修复最小，只改 manager stall recovery 判据，不扩张到 broader command/control-plane semantics。
- 不回退既有 pending-intake、superseded prompt、worker relaunch、worker active reentry contract。
- `develop` manager 继续只做 supervision / delegation，不变成执行者。
