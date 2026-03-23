# Brainstorm: manager-watchdog-trigger-and-drift-reconcile-governance

## Focus

把这轮关于主管 watchdog 双入口、动态 restart-point routing 与 external drift reconcile 的讨论，收敛成正式治理 issue 产物。

## Key Decisions

1. 不新增第四层 loop。
2. `auto-loop` 同时有 `patrol-driven` 与 `event-driven` 两类入口。
3. 主管始终只做判断、解释、委派、监督完成，不直接施工。
4. delegated owner 返回结果后，主管继续决定下一跳 restart point。
5. `external drift / out-of-band reconcile` 属于主管 patrol 检查面，而不是平行新 skill。

## Open Checks

1. 哪些表述应放在 `three-loop-capability-lifecycle`，哪些应留给 `manager-agent` 或 `auto-loop-orchestrator`。
2. patrol reference 是否已足够覆盖 external drift 的分流语义。
