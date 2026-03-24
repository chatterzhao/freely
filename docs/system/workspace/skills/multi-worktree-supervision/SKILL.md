---
name: multi-worktree-supervision
description: 当需要像项目负责人一样同时监督多个 Freely worktree、安排哪些工位继续开发、哪些先 checkpoint、哪些进入集成批次时使用。
---

# skill:multi-worktree-supervision

## 何时使用

- 同一仓库存在多个活跃 worktree
- 需要项目级判断工位的脏树压力、runtime 状态与合并节奏
- 需要决定继续开发、先 checkpoint、冻结等待、进入集成批次

## 工作流

1. 先看项目级当前态。
   - `./bin/freely live-status --project <主管工位>`
   - 先用它看当前活跃 supervisor / dispatcher / ai、prompt excerpt、continuity excerpt 与 deep refs
   - 它负责回答“现在谁在干活、在干什么”

2. 再看项目级工位总览。
   - `./bin/wt-fleet-status`
   - 或 `./bin/freely fleet-status --project <任一该仓库 worktree>`

3. 看单个工位 checkpoint 压力。
   - `./bin/checkpoint-guard`
   - commit 前用 `./bin/checkpoint-guard --staged-only`

4. 看单个工位 baseline snapshot。
   - `./bin/freely baseline-status --project <worktree>`
   - 它负责 durable / baseline / session-state 视图，而不是当前谁在干活

5. 决策规则。
   - `checkpoint_required=true`：先 continuity / review / integration test / checkpoint commit
   - staged commit 超预算：拆分提交或分流到新 worktree
   - `supervisor` 或 `ai` 不活跃：先恢复 runtime
   - 上游依赖未进入要求路径：下游工位冻结或只做 doc-loop
6. 若当前会话承担主管职责，优先做项目级排班，并在可并行任务上使用 subagent 提高效率。
7. 若主管刚被 runtime 重新激活，先做一轮 manager reactivation patrol：
   - 先读 `live-status`
   - 再读 `fleet-status`
   - 再读 milestone / issue / progress / recovery
   - 主动找出 `candidate stuck / phase orphaned / completion without closure`
   - 发现后明确输出 `ownership + restart_point + next_action`
   - 详细检查面见 `references/manager-reactivation-patrol.md`
8. 当某条线已经被稳定判定为 `retire-only`、`retire-now` 或 `continue-dev` 时，默认下一跳不是继续 patrol，而是：
   - `retire-only / retire-now` -> cleanup / retirement handoff worker
   - `continue-dev` -> verification / dev continuation worker
   - 只有关键事实仍缺失或 blocker 未明时，主管才继续停留在 manager-only supervision
9. 若同轮存在多个互不冲突 lane，主管必须先做排班而不是串行化所有动作：
   - 为每条 lane 写清 `dispatch_priority`
   - 标记是否 `parallel_safe`
   - 标记最小 `write_scope`
   - 有剩余 worker capacity 时并发推进
   - 无剩余 capacity 时进入 queue，并在 continuity 中保留 `next_action` / `revisit_trigger`

## 边界

- 本 skill 负责监督和调度，不代替具体 issue 的 doc/dev skill
- 最终 promote / cleanup 前仍必须过 `./bin/wt-status-all`
