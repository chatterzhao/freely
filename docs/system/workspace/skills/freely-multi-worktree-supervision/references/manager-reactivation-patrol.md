# Manager Reactivation Patrol

用于主管被 runtime 拉起后，先做一轮项目级巡检，而不是直接等下一条 signal。

## 输入顺序

1. `./bin/freely live-status --project <develop>`
2. `./bin/freely fleet-status --project <develop>` 或等价工位总览
3. `docs/milestones.md`
4. 当前 active milestone 阶段对应的 worktree / issue / progress / recovery
5. interruption backlog、external issue source backlog、resume / handoff 证据、以及 relevant candidate / pre-brainstorm artifacts

## 巡检目标

主管每轮至少检查四类“应推进但没人推进”的点位：

1. `candidate stuck`
- 仍在 `candidate_issues`
- 有明确 `next_action`
- 但没有新的 worker 在继续 pre-brainstorm / IBM materialization

2. `phase orphaned`
- `phase_state=in_b2_ibm|done_b2_ibm|in_dev|in_verification`
- 但对应 worktree 没有活跃 supervisor / ai
- 且没有 recovery / handoff 正在接管

3. `completion without closure`
- issue / verification 已完成
- 但没有 merge-up / cleanup followthrough
- worktree 仍停在 active 状态

4. `runtime visible but owner missing`
- live-status 显示 supervisor / dispatcher / ai 已下线或异常
- 但没有明确 `runtime-owned` 恢复动作

5. `worker dispatch-only with delegated local handoff`
- worker 工位 `live-status` 停在 `dispatch_only`
- intake 已存在本工位 delegated continuation / verification target
- 但没有新的 worker 主循环接棒

6. `external drift / out-of-band reconcile`
- 仓库、docs 或 cleanup 现实已经前进
- 但 `.freely` / intake / continuity / worktree 视图仍停留在旧状态
- 主管需要先解释当前 drift，再把它分流到 maintenance worker、execution worker 或 runtime owner

7. `stale validation batch`
- 某个 `test-pre-merge-*` worktree 仍在，但 `develop` 已前进到让它不再权威，或批次只剩 protected-env 独有差异 / 断裂的 cleanup 证据
- 主管应将 ownership 判为 `manager-owned`
- restart_point 应回到 `runtime supervision / cleanup`，并在需要继续验证时把“从当前 `develop` 重建权威批次，并重新吸收对应 source feature / premerge 集合”作为下一跳委派给对应 writable worktree
- stale 批次不得继续作为当前真相面；它必须先 retire，再决定是否 rebuild

8. `unclosed interruption or unsynced pre-brainstorm`
- human interruption 已 durable 落盘，但仍未完成分类、吸收、写回或 resolution note
- 或 pre-brainstorm 已形成稳定结论，但尚未产出 candidate / 未写回 milestone / 缺少 `next_action` 与 `revisit_trigger`
- 主管应把这类点位视为 standing-source completeness drift，而不是“以后再看”

9. `external source not consumed or not closed out`
- raw external issue 仍 open，但 canonical owner truth 中没有可验证的 source linkage
- 或 source 已被 consume/accept/discard，但外部 closeout/comment/publication linkage 明显漂移
- 主管应先判定这是 source intake 还是 external drift reconcile，再决定走 pre-brainstorm/materialization 还是 maintenance followthrough

10. `candidate visible but not consumable`
- candidate 虽然已经出现在 milestone，但仍处于 `unassigned` 思维、错误 milestone、或当前 milestone 中长期无人继续研究
- `next_action` / `revisit_trigger` 无法指向近期消费节奏
- 当前 milestone 已经确定不会消费它，但也没有后移到更合适的 active milestone，或显式标记为 `dropped`
- 主管应将其分流给 `freely-milestone-planning-state-maintenance` 或新的 pre-brainstorm/materialization worker，而不是继续让它停留在静态可见状态

11. `develop push followthrough drift`
- canonical `develop` 本地已经领先 tracked remote
- 但没有显式 defer reason，或 defer window 长期未被重新消费
- 主管应将其视为 `manager-owned` 的 standing-source followthrough，而不是把本地 merge 误判为远端 canonical closure
- 若当前只是合法的 `post_merge_acceptance` / cleanup window，应要求留下结构化 defer reason 与下一跳 followthrough，再决定是否 push / 继续验收 / cleanup
- patrol 输入若已给出 `develop_push_followthrough_push_urgency=immediate|deferred`、`develop_push_followthrough_resync_required=true`，或 `develop_push_followthrough_state=push_blocked`，说明 latest-develop-sensitive judgment 不能继续假定 remote 已同步；必须先显式处理 push/resync followthrough，并区分是尚未尝试、合法 defer，还是最近一次受控 attempt 已被 gate/remote 明确挡住
- `latest-develop-sensitive judgment` 至少包括：owner/absorption sequencing、verification/promotion、cleanup/retirement、stale `test-pre-merge-*` rebuild 判定，以及任何声称“基于当前 develop 已完成对齐”的结论

## Trigger Model

主管 patrol 不应被理解成只有单一轮询入口。

- `patrol-driven`
  - 来源：standing-source scan
  - 典型输入：`live-status` / `fleet-status` / interruption / external issue / milestone / issue / progress / recovery / pre-brainstorm

- `event-driven`
  - 来源：human interruption / worker result / runtime anomaly / review/test signal
  - 这些事件进入系统后，也应回到同一套 `ownership + restart_point + next_action` contract

两类入口最终都应汇聚到主管的统一 routing，而不是形成两套平行流程。

## 输出

主管必须把巡检结果加工成：

- `ownership`
  - `runtime-owned`
  - `worker-owned`
  - `manager-owned`
- `restart_point`
  - `pre-brainstorm`
  - `candidate / milestone intake`
  - `IBM`
  - `dev`
  - `verification`
  - `progress / recovery continuation`
  - `runtime supervision / cleanup`
- `next_action`
  - `delegate`
  - `runtime_recovery_requested`
  - `freeze`
  - `merge`
  - `cleanup`

补充：
- 主管先输出状态解释与 ownership 判断，再委派对应 owner。
- delegated owner 返回结果后，主管继续决定下一跳 restart point，直到当前问题被正确吸收或完成收口。
- 对 `progress`，续接前优先读取，确认是否已有主动记录。
- 对 `pre-brainstorm`，主管不只检查“有没有这个目录”，还要检查 candidate 与 milestone 同步是否完整。
- 对 `milestone`，主管不只检查“candidate 在不在队列里”，还要检查它是否被放进了正确且仍 active 的消费队列。

## 硬规则

- 主管重激活后，不得只确认“进程活着”就算完成。
- 主管必须先做一轮 standing-source patrol，再决定这轮最重要的 worker 动作。
- issue 已 completed 但 worktree 未收口，也属于 patrol 必查项。
- 不要求每轮关闭所有 worktree；但不得让 stalled/orphaned 点位继续无人认领。
- 若 patrol 发现 worker-local delegated handoff 因 `operator_stop` 后 runtime 未恢复而悬空，应要求 runtime 走本工位 reactivation gate，而不是继续把问题留在 delegated intake 中。
- 若 patrol 发现 `test-pre-merge-*` 批次 stale，不能把它继续当成验证真相；必须先 retire，再按需要从当前 `develop` 重建新的权威批次并重新吸收来源 feature / premerge 集合。
