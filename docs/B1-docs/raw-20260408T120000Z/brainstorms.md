# 预研头脑风暴：develop-push-followthrough-escalation

## 问题陈述

Freely 已经 materialize 了 `develop` 在本地 merge 后、远端尚未 push 时的显式状态面：`push_pending` 与 `push_deferred`。这解决了“本地已经合流却静默假装远端已完成”的双真相问题，但还没有回答更强的 sequencing 问题：

1. 什么时候 manager 应该把 `push_pending` 视为必须尽快处理，而不是可无限挂起的 standing-source。
2. 什么时候活跃 feature/research worktree 应先吸收最新 `develop`，再继续 doc-loop / dev-loop，而不是在陈旧上游上继续推导结论。
3. merge 到 `develop` 成功后，Freely 应该只是暴露 push debt，还是还应提供更主动的 followthrough judgment / escalation。

用户的真实担忧不是“能不能 auto-push”，而是：

- AI / runtime 可能中断，导致合法 merge 长时间只停在本地 `develop`
- 其他 worktree 继续基于旧上游推进，重复讨论已经在 `develop` absorbed 的事实
- 当前规则虽然能看见 `push_pending`，但还没有给出“何时必须先 push / 先 resync”的 canonical 触发点

## 现状真源

### 1. 已有能力

- `docs/LAWS.md` 已承认 `develop` 本地 merge 后允许存在短暂 followthrough 窗口，但必须显式暴露 `push_pending` / `push_deferred`。
- `develop-push-pending-guard-governance` 已完成；其 issue 明确把“显式状态 + defer reason + status/patrol truth”作为有意冻结的第一阶段。
- `freely develop-push status|defer|clear`、`wt-fleet-status`、`fleet-status` 已能消费这层状态。

### 2. 当前缺口

- 当前 owner 明确不做 auto-push，也不做强时限。
- manager patrol 只需“看见 push debt 并决定下一步”，没有冻结更强的 escalation contract。
- 活跃 worktree 何时必须吸收 `develop`，当前没有统一 manager-facing 规则；更多依赖临场判断。

## 为什么它属于 Freely 自身能力

这是 Freely 的开发治理与 runtime followthrough 能力，不是单次仓库操作习惯：

- 它直接影响 protected-branch canonical truth 是否及时抵达 remote。
- 它直接影响多 worktree / 多 lane 的 sequencing 与 owner 可见性。
- 未来如果 Freely 面向其他托管项目工作，同样需要回答 merge 后 push debt 和 upstream resync 的 canonical 策略。

因此它应成为 Freely 的治理/能力真源，而不是只留在某次 manager 对话里。

## 关键判断

### 1. 不应改成 hook/runtime 自动 push

现有 completed owner 的边界仍成立：

- auto-push 会把网络副作用塞进 hook/runtime 执行路径
- 会抹掉 post-merge acceptance / cleanup followthrough 的合法观察窗口
- 也会让“push 成功/失败”从显式治理动作退化成隐式副作用

所以新问题不是“要不要自动 push”，而是“在不 auto-push 的前提下，什么时候必须升级为强 followthrough”。

### 2. 应新增“push urgency + resync gating”治理，而不是 reopen 旧 owner

`I-20260401T103500Z-A` 已明确 completed，并把 future work 指向“若要更强 blocking semantics，开新 lifecycle”。当前问题正是这个 follow-on：

- 是否允许在 `push_pending` 未消费时继续创建/推进新 lane
- 是否允许活跃 feature/research tree 在未吸收最新 `develop` 的情况下继续推进 owner judgment
- 哪些 defer reason 可以继续开发，哪些只能停在 followthrough / cleanup

### 3. “先与上游同步再继续”需要独立规则，而不是临时建议

当前实践已经证明：

- 一棵 research tree 若落后太多，可能继续把“本地不可见”误判成 blocker
- protected-branch merge 之后，其他 worktree 是否应立即 merge `develop`，会影响 owner absorption 与 continuity judgment

所以需要把 resync 触发条件写成 manager 能消费的规则。

## 建议方向

### A. 冻结 `develop` push followthrough 的 urgency model

至少区分：

1. `push_pending_immediate`
   - merge 已完成，且没有合法 defer reason
   - manager 下一优先级应先完成 push followthrough，再继续新 lane sequencing
2. `push_deferred_lawful`
   - defer reason 属于白名单
   - 允许短暂继续 post-merge acceptance / cleanup，但必须保留 patrol truth
3. `push_blocked_external`
   - remote/network/credential 等外部原因阻塞
   - 允许保留 followthrough state，但需要明确恢复点与升级路径

不一定要新增三个状态名，也可以只保留 `push_pending` / `push_deferred`，但 manager/patrol truth 至少要能推导 urgency。

### B. 冻结 upstream resync 的 manager decision points

至少回答：

1. 若 `develop` 出现新的 protected-branch merge，哪些活跃 feature/research tree 必须先吸收后再继续。
2. 哪些情况只是“建议同步”，哪些情况是“不同步就不得继续 owner 推断 / verification / cleanup judgment”。
3. 如果某活跃 lane 明确依赖旧 base，如何记录允许暂缓 resync 的理由。

建议最小触发点：

- 当前 worktree 的 blocker / owner visibility 判断依赖“上游是否已 absorbed 某条 issue”
- 当前 worktree 正处于 followthrough / closeout / verification 语义，需要引用 canonical `develop` truth
- 当前 root `develop` 已有新的 protected merge，而 worktree 继续写治理结论会改变 milestone / owner state

### C. 冻结 manager patrol / live-status 的下一跳建议

目标不是直接代 operator 执行 push，而是给 manager 更强的排序信号：

- `push_pending` 且无 defer 时，把“complete remote canonical followthrough”抬到 supervisor next action
- 有活跃 worktree 明显落后 `develop` 且继续做 owner judgment 时，patrol 标记 `resync_required`
- 在 launch 新 lane 前，若已有 `push_pending` 未解释，至少需要显式 defer/clear，而不是静默越过

## 候选 owner 切分

更可能是一个 pre-brainstorm，后续拆成两个 follow-on owner：

1. `develop-push-followthrough-escalation-governance`
   - 负责 push urgency、defer 边界、manager followthrough 排序
2. `active-worktree-upstream-resync-trigger-governance`
   - 负责活跃 feature/research tree 的 resync trigger、patrol truth、允许暂缓条件

若实现面高度重合，也可能先以单一 owner 冻结判断 contract，再决定是否拆分脚本/状态落点。

## Promotion Gate

- 证明这不是 reopen `develop-push-pending-guard-governance`，而是其明确保留的 stronger followthrough semantics
- 证明“何时先 sync upstream”已经是 Freely 的多工位 sequencing 能力，而不是一次性人工习惯
- 证明第一阶段无需 auto-push，仍能通过 patrol/status/manager contract 提升及时 push 和 resync 一致性

## Open Questions

1. urgency 是新增 machine-readable state，还是仅作为 patrol-derived classification。
2. `push_pending` 未消费时，是否应阻止新 worker launch，还是只阻止新的 protected-branch merge / cleanup。
3. resync trigger 应按 `develop` 新 merge 次数、base sha 差距，还是按 owner visibility / blocker sensitivity 判断。
4. `remote_delivery_hold` 这类 defer 是否允许继续开新 lane，还是只能做最小 followthrough。
