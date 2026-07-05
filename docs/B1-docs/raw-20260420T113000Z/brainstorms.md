# Brainstorms - 20260420-1130--manager-task-source-scan-replan-boundary

- date: `2026-04-20`
- status: `pre-brainstorm`
- source: `freely self-host runtime patrol gap`

## Context

Freely 当前已经具备三类彼此相关但边界还不够稳定的任务面：

1. durable raw source families
   - `human interruption`
   - `external issue`（GitHub / Gitee 作为 provider 变体，而不是新的顶层 family）
2. standing / continuation surfaces
   - delegated continuation
   - milestone unresolved queue
   - pre-brainstorm unresolved candidate queue
   - progress / recovery / worktree continuity
3. discovery mechanisms
   - review
   - test
   - runtime anomaly

这几类面都可能让主管“有事可做”，但它们不应该在每轮 prompt build 时被无条件全量重扫。

最近的真实 dogfooding 暴露了两个相反的失败形态：

1. manager 会被过时 delegated continuation 吸住，启动后没有回到更高层任务面找事做。
2. 一旦把 patrol 提醒加粗，如果没有明确 trigger boundary，manager 又可能在已有 lane 正在推进时被 broad patrol 牵走，浪费 token，并造成 lane 不连续。

所以真正缺的不是“再多一个 source”，而是：

- 一条 runtime-owned 的 replan transaction contract
- 明确什么时候可以重扫任务面
- 明确什么时候必须继续当前 continuity / worker lane
- 明确 scan 只提供 patrol seed，不提供完成证明

## Problem Statement

Freely 需要让主管在启动后和收口后都能“自己找事做”，但不能把项目变成每轮都重新做一次全局调度。

当前缺口可分成两个层次：

1. source completeness 缺口
   - manager 应能把 `human interruption`、`external issue`、milestone unresolved queue、pre-brainstorm unresolved candidate queue、delegated continuation、progress/recovery 等看成可巡检任务面
2. replanning trigger 缺口
   - 并不是任何时刻都应该重新扫描这些任务面
   - 扫描应该只发生在 idle / replan 边界，而不是 worker 稳定运行中的每一轮

如果没有第二层 contract，第一层越完整，runtime 越容易把主管拉成 token 浪费和 lane 抖动机器。

## Boundary Freeze

本预研冻结如下边界：

### 1. `task-source scan` 是 replan step，不是 every-cycle step

scan 的职责是给 manager 一份结构化 patrol seed，用于：

- startup 后第一轮找事
- worker closeout 后重新排班
- manager 被重新激活且当前没有 active worker 时重新找下一条 lane
- idle manager 发现有新 durable delta 时重新判断下一跳

它不是：

- 每轮 prompt build 都必须执行的项目级巡检
- 当前已有 continuity / worker lane 稳定推进时的默认动作

### 2. durable raw source 与 standing surface 不混名

顶层 durable raw family 仍保持：

- `human interruption`
- `external issue`

而 milestone / progress / recovery / delegated continuation 不是新的 raw family；它们是 standing / continuation surfaces。

这意味着：

- GitHub / Gitee 应建模为 `external issue` 的 provider 变体
- milestone/progress/recovery 是 manager patrol 要扫的 surface，但不是 raw intake family

### 3. AI 写的状态默认可疑

scan json 里任何 phase / status / queue state 都只能当 advisory。

必须区分：

- `observed_state`
- `trust_level`
- `needs_reconcile`

尤其是：

- delegated continuation 需要核对当前 continuity 是否已吸收或过时
- pre-brainstorm unresolved candidate 需要核对 candidate 是否已被吸收到 issue / milestone，还是仍应停留在 research
- milestone / progress / recovery 的旧标签不能直接当完成证明
- review/test/runtime anomaly 发现的问题，若当前 lifecycle 能吸收，优先回到当前 line，不直接长成新 raw source

## Replanning Trigger Contract

本轮先冻结保守触发条件，优先避免 lane 抖动：

### 应触发 full scan json 重生成

1. `bootstrap_missing_scan`
   - 本地还没有 scan json
2. `new_active_intake_since_last_scan`
   - 有新的 active intake 晚于最近一次 scan
3. `continuity_advanced_since_last_scan`
   - 最近 manager continuity 晚于最近一次 scan，且当前没有 active worker

### 应允许复用现有 scan json，但不必重生成

1. manager 当前 idle，且已有 scan json 可用
2. 当前没有新的 intake / continuity delta，但 manager 需要继续 patrol / choose-next-work

### 应抑制 broad patrol / full scan

1. 当前存在 active worker，且没有新的 idle/replan boundary
2. manager 刚刚完成 delegation，当前 continuity 仍是主要真相
3. 当前 worker 正在稳定推进，没有 closeout/restart/reconcile 信号

这里的关键不是“永远不看别的 source”，而是：

- active worker 期间允许 intake/continuation 局部信号存在
- 但 broad patrol 不能抢占 continuity-first 的当前轮次

## Structured Output Contract

runtime 生成的 `manager-task-source-scan-latest.json` 应作为主管 patrol 的 machine-readable 输入。

本轮冻结最小字段：

- `schema_version`
- `generated_at`
- `scan_reason`
- `continuity_anchor`
- `manager_context.active_running_workers`
 - `surfaces[]`
  - `surface`
  - `source_class`
  - `active_count`
  - `trust_level`
  - `needs_reconcile`
  - `summary_lines`

当前 runtime 的首个 bounded surface set 包含：

- `human_chat_intake`
- `delegated_continuation`
- `active_milestone_queue`
- `active_pre_brainstorm_queue`
- `active_progress_queue`

注意：

- 这份 json 是 patrol seed，不是 canonical owner truth
- `context-source-skill` 应先消费它，再回到 linked docs/evidence 做核对

## Worktree Governance Implication

这条线属于 protected-root manager runtime / product capability contract。

因此：

1. 设计先落 `pre-brainstorm`
2. 当前 feature worktree 可以实现 bounded runtime slice 和测试
3. 若后续要把 `external issue` provider scan / writeback / gh/gitee publication 真正落地，应进入新的 owner，不在本 slice 偷偷扩 scope

## Success Criteria

只有同时满足以下条件，这个 slice 才算完成：

1. 预研真源收敛
   - 任务面分类、状态怀疑原则、scan trigger、scan suppress 条件写清
   - 说明 raw family 与 standing surface 的边界
2. runtime 行为收敛
   - 启动后 idle manager 能拿到结构化 patrol seed
   - stale delegated continuation 不再把主管困住
   - active worker 稳定推进时不会每轮 broad patrol
3. 测试收敛
   - 至少覆盖：
     - startup / missing scan -> 生成 scan
     - active worker running -> broad patrol suppressed
     - idle after continuity advance -> scan regenerated
     - stale delegated continuation 不计入 current-round active intake
4. worktree 治理收敛
   - 改动只落当前 dedicated feature worktree
   - 预研与实现边界一致，不偷偷扩到外部 issue provider automation

## Next Question

若这一层稳定，下一条 owner 才应继续回答：

- external issue provider（GitHub / Gitee）如何 scan / label / publish / write back
- recovery / external issue provider 是否也要进入统一 machine-readable patrol snapshot
- scan state 是否进一步进入 `live-status` / `fleet-status` 观测面
