# PRD: worker-active-reentry-for-manager-delegated-continuation-governance

## Objective

让 manager runtime 在把 worker handoff 写入目标 worker 后，能正确处理 “worker 已经活着” 的情况，避免 delegated continuation 长期 pending。

## Product behavior

1. target worker inactive:
   - 维持现有 bootstrap + supervisor start。
2. target worker active:
   - runtime 触发 local continuation reentry；
   - 不重复启动 supervisor；
   - delegated continuation 由下一轮 prompt 消费。
