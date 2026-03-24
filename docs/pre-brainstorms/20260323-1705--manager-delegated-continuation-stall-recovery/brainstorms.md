# 预研头脑风暴：manager-delegated-continuation-stall-recovery

## 背景

这轮在 `develop` 上做 Freely 自举端到端 dogfood 时，主管已经收到 cleanup continuation，并把它吸收到当前 prompt：

- `freely chat` 成功写入 human interruption intake
- interruption manager 成功把它 claim / delegate 成 `handoff://cleanup`
- 最新 manager prompt 明确包含 `Delegated continuation handoff`

但随后 runtime 暴露出新的假活断点：

- manager AI 进程仍然存活
- cycle log 长时间不再更新
- 没有新的 manager continuity
- 没有新的 worker handoff / launch state
- cleanup followthrough 因此停在 prompt 内部，外层 control plane 看不到下一跳

## 问题定义

当前 runtime stall detection 只覆盖：

`pending intake` 比 `cycle log` 更新，且 manager AI 长时间无输出

这不足以覆盖更常见的 continuation 假活：

`delegated continuation already entered prompt -> manager emits no new continuity / handoff -> AI process still alive`

如果没有更硬的 runtime-owned stall contract，Freely 会把“进程还活着”误判成“自治还在推进”，无法完成从 worktree 创建、交接、cleanup 到 retirement 的闭环。

## 候选方向

1. 把 `delegated continuation already entered prompt` 视为可监督状态，而不是纯会话内部细节
2. 若 prompt 已含 delegated continuation，且超过阈值没有新的 manager continuity / worker handoff，runtime 应触发 recovery
3. 保留现有 `pending intake > cycle log` 检测，两条 stall contract 并存
4. 这条能力属于 runtime control plane，不应只留在一次性 dogfood 结论里

## 当前证据收敛

- `freely live-status` 已能稳定暴露：
  - `current_prompt_has_delegated_continuation=1`
  - 当前 `prompt_excerpt` 明确包含 `Delegated continuation handoff`
  - `latest_manager_worker_prompts_generated=none`
  - `intake_delegated_items=30`，且 `last_consumed_delegated_continuation_ids` 已覆盖当前观察窗口中的全部 30 个 delegated continuation ids；这些 ids 仍同时保留在 `pending_delegated_continuation_ids`
- `docs/system/workspace/scripts/runtime/freely` 已有专门的
  - `manager_ai_stalled_after_delegated_continuation_prompt`
  - `recover_stalled_manager_ai_if_needed`
- `docs/system/workspace/skills/watchdog-control-plane/SKILL.md` 已把这条 contract 写成 runtime watchdog 的职责边界
- `docs/system/workspace/scripts/tests/test-freely-manager-delegated-continuation-stall-recovery`
  与 `docs/system/workspace/scripts/tests/test-freely-manager-generated-handoff-stall-recovery`
  已覆盖：
  - prompt 已吸收 delegated continuation 但无新 continuity / handoff 的 recovery
  - prompt 之后已有新 continuity / worker prompt 但 launch-state 仍停旧锚点的 recovery
  - 相关 state / live-status / rotation 测试还证明 runtime 已经持久化并暴露 `pending_delegated_continuation_ids`、`last_consumed_delegated_continuation_ids`、`latest_manager_continuity_generated/consumed` 等状态，而不是只剩 prompt 文本可读证据
  - 但这些 runtime / test 证据仍没有冻结 `consumed` truth 与当前 prompt cycle / 当前 stalled intake 的稳定绑定；它们更像“状态面已存在，但强锚点仍缺失”

## prompt-absorbed stall 与旧 pending-intake 症状的边界

- 旧 `pending intake > cycle log` 症状：
  - runtime 只知道有新的 delegated continuation 还在 pending
  - 但看不到当前 manager prompt 已吸收它
  - 常见信号是 `pending_delegated_continuation_ids` 增长，且 `current_prompt_has_delegated_continuation!=1` 或当前 prompt 没有 delegated continuation 证据
- 当前候选关注的 `prompt-absorbed manager stall`：
  - runtime 已看到当前 manager prompt 带有 delegated continuation 语义
  - 但 prompt 进入后，在有界时间内没有新的 manager continuity / worker handoff / launch state 继续推进
  - 当前最小可见证据至少包括：
    - `current_prompt_has_delegated_continuation=1`
    - 当前 prompt 文件或 excerpt 能指向 `Delegated continuation handoff`
    - 随后仍没有新的 manager continuity / worker prompt / launch-state 前进

## 当前最小证据与缺口

- 本轮 `live-status` 证明了 prompt-level absorption：
  - `current_prompt_has_delegated_continuation=1`
  - `current_focus.prompt_excerpt` 包含 `Delegated continuation handoff`
  - `intake_snapshot` 中对应 delegated continuation 仍可追溯到当前 prompt 上下文
- 本轮 `live-status` 也已经给出部分 id-level consumption：
  - `intake_delegated_items=30`，且 `last_consumed_delegated_continuation_ids` 已覆盖当前观察窗口中的全部 30 个 delegated continuation ids，其中包括 `20260323-204333...`、`20260323-204334...`、`20260323-205242...`、`20260323-205340...`、`20260323-220921...`、`20260323-222254...`、`20260323-222255...`、`20260323-225022...`、`20260323-225032...` 与 `20260323-234407...`
  - 说明“runtime 完全没有暴露 consumed truth”这个旧缺口已经失效
- 但当前 promotion gate 仍未收口：
  - 同一批 delegated continuation ids 现在同时出现在 `pending_delegated_continuation_ids` 与 `last_consumed_delegated_continuation_ids`
  - runtime 还没有给出一个稳定、可验收的 prompt-bound 锚点，去证明“哪个 consumed 事件对应当前 manager prompt cycle，以及它是否已经完成对当前 stalled intake 的吸收”
  - 因此当前控制面仍不能稳定地区分“旧 consumed truth 只是历史回放”与“当前 stalled intake 已被当前 prompt cycle 吸收并进入下一跳”
- 这也是当前候选继续停留在 `needs_research` 的直接原因：
  - stall contract 的方向已经清楚
  - 但 promotion 仍缺一层针对当前 prompt cycle / 当前 stalled continuation 的稳定 runtime-visible absorption proof，避免未来把“pending 与 consumed 并存”的状态误当成已经完成 issue-level acceptance
  - 现有 runtime / test 已经提供 prompt-level absorption 加 state-surface evidence；这足以支撑 watchdog 行为，但仍不足以充当后续 IBM issue-level acceptance anchor

## continuity guard writeback

- 上一轮确实经历过 `fresh_with_handoff`，直接原因是旧 `codex` 会话命中 `context_compacted`
- 但本轮重新核对当前 worker 工位的最新 `live-status` 后，当前运行态已经变成：
  - `role_hint: worker`
  - `activity_state: ai_active`
  - `last_launch_kind: fresh_with_handoff`
  - `last_rotation_reason: context_compacted`
  - `last_ai_state: down`
  - `last_exit_reason: ai_exit_rc_0`
  - `intake_active_items: 30`
  - `intake_delegated_items: 30`
  - `current_prompt_has_delegated_continuation: 1`
  - `pending_delegated_continuation_ids` 与 `last_consumed_delegated_continuation_ids` 仍全量重叠，且最新 delegated continuation intake 仍可见于 pending 集合
  - `last_consumed_delegated_continuation_at: 2026-03-24T07:19:27Z`
  - `current_focus.prompt_file: .freely/run/prompt-20260324-002242.txt`
  - 当前 prompt excerpt 仍直接指向这条候选前一轮 writeback diff，说明 delegated continuation 语义仍在当前 worker prompt 上下文中，而不是只停留在历史 handoff；同时也说明 fresh session 仍沿用同一条 canonical writeback 线
- 当前最新 `live-status` 还补足了两层 continuity 事实：
  - `active_processes` 中仍能看到当前 `codex exec` 进程，说明 runtime 继续把本工位当作 active worker lane 维护
  - `deep_refs.last_tool_session_id=019d1eb6-7620-75a2-a5d0-fdc12afa8a55` 与 `deep_refs.last_tool_jsonl_path=/Users/zhaoyu/.codex/sessions/2026/03/24/rollout-2026-03-24T00-19-27-019d1eb6-7620-75a2-a5d0-fdc12afa8a55.jsonl` 把上一轮 `context_compacted -> fresh_with_handoff` 的来源再次固定下来
- 这层 worker-side `live-status` 说明 runtime 当前仍在沿用 `context_compacted -> fresh_with_handoff` 的 continuity 策略，而且 current process view 已经出现 `activity_state=ai_active` 与 `last_ai_state=down/ai_exit_rc_0` 并存；它证明运行态切面仍在推进或轮换，但仍不能替代当前候选所需的 manager-side prompt-cycle binding acceptance anchor
- 当前 worktree hygiene 事实：
  - canonical writeback 已继续收敛为本分支上的最新 continuity anchor lineage，而不是未提交 dirty delta
  - 当前 `git status --short` 已 clean，没有发现超出本候选 write scope 的残留脏项
  - 因此这轮不再需要额外 checkpoint/commit；后续 cleanup 判断的关键前提改为“这些提交何时被上游吸收”，而不是“是否还有未提交 dirty delta”
- 当前仓库扫描未发现 `docs/progress/**`、`docs/epics/**` 或其他 issue/progress/recovery 真源已经接管本候选；因此这轮 continuity 仍应写回 pre-brainstorm，而不是误切到 IBM、dev-loop 或 recovery
- 当前分支 `feature/manager-delegated-continuation-stall-materialization-20260323` 仍未被 `develop` 吸收；这说明 worktree cleanup 与 candidate materialization 仍应分开判断，不能因为已有 canonical writeback 提交就把该候选视为已关闭

## 需求池扫描与优先级

- 本轮优先池：`docs/pre-brainstorms/**` + `docs/milestones.md`
  - delegated continuation handoff 明确把当前输入收束到 `C-20260323-1705-A` 的 continuation
  - `milestones.md` 仍把该条目保留在 `candidate_issues`，且 `phase_state=in_pre_brainstorm`
- 已核对但未接管的池：
  - `docs/epics/**`：未发现该候选的 milestone-owned issue 真源
  - `docs/progress/**` / `docs/recovery/**`：未发现接管这条线的 continuation artifact；按法律这也说明当前不能降级成 dev-loop / recovery continuation
  - review / test / acceptance review：只提供相邻 issue 与 runtime patch 的 supporting evidence，不构成对本候选的 canonical owner
  - human chat / session evidence：当前 handoff 与 `session_refs` 只证明 continuation 来源和 fresh re-entry 背景，不足以替代 pre-brainstorm canonical artifacts
  - GitHub issue：当前未发现外部 issue 已接管该 contract
- 因此当前 route 仍应保持：
  - source_class: `continuation`
  - route_kind: `pre_brainstorm`
  - target_skill: `doc-pre-brainstorm-execution`

## 本轮首跳复核（2026-03-23）

- 当前 handoff 中“这棵树已被 `develop` 吸收、只剩 dirty writeback”的前提已失效：
  - 当前 worktree 已 clean，但该 clean 状态来自本地 checkpoint commit，而不是 `develop` 已吸收当前分支
  - `git merge-base --is-ancestor HEAD develop` 返回非零
  - 当前分支仍有独有提交；当前 writeback lineage 已至少包括：
    - `a4f31f3 docs: preserve delegated continuation stall candidate`
    - `b6f5e6a docs: refresh delegated continuation continuity`
    - `80526aa docs: close delegated continuation writeback routing`
    - `7fc7b24 docs: checkpoint delegated continuation stall writeback`
    - `473075b docs: refresh delegated continuation evidence counts`
    - `114a6a4 docs: refresh delegated continuation continuity state`
- 因此当前真实问题不是“是否保留 dirty delta”，而是“这些 canonical pre-brainstorm writeback 提交是否仍应保留为独有分支提交，还是应该冻结/丢弃”
- 本轮再次核对：
  - `docs/milestones.md` 仍把 `C-20260323-1705-A` 保留在 `candidate_issues`
  - 未发现 `docs/progress/**`、`docs/recovery/**`、`docs/epics/**` 的 issue/progress/recovery 真源接管该候选
  - `freely live-status` 当前显示 `role_hint: worker`、`activity_state: ai_active`、`last_ai_state: down`、`last_exit_reason: ai_exit_rc_0`、`last_launch_kind: fresh_with_handoff`、`last_rotation_reason: context_compacted`，且 delegated continuation 仍在当前 prompt 上下文中
- 结论：
  - route_kind 继续保持 `pre_brainstorm`
  - 当前分支的独有提交仍是 canonical candidate writeback，而不是可直接丢弃的噪音
  - 但在这些提交尚未被上游吸收前，这棵树不满足 `retire-now`

## continuity guard writeback（2026-03-24 00:22 PST）

- 本轮 fresh session 继续命中 handoff 中要求的 doc-loop continuity guard，因此先刷新 pre-brainstorm canonical artifacts，而不是扩大到 IBM / dev-loop
- 最新 `live-status` 已把 continuity 锚点继续滚动到：
  - `last_consumed_delegated_continuation_at: 2026-03-24T07:19:27Z`
  - `current_focus.prompt_file: .freely/run/prompt-20260324-002242.txt`
  - `deep_refs.last_tool_session_id: 019d1eb6-7620-75a2-a5d0-fdc12afa8a55`
  - `deep_refs.last_tool_jsonl_path: /Users/zhaoyu/.codex/sessions/2026/03/24/rollout-2026-03-24T00-19-27-019d1eb6-7620-75a2-a5d0-fdc12afa8a55.jsonl`
- 当前 worker 视图仍保持：
  - `activity_state=ai_active`
  - `last_ai_state=down`
  - `last_exit_reason=ai_exit_rc_0`
  - `latest_manager_continuity_generated=unavailable`
  - `latest_manager_worker_prompts_generated=none`
- `pending_delegated_continuation_ids` 与 `last_consumed_delegated_continuation_ids` 仍是 30/30 全量重叠，其中继续包含当前 lane 的 `20260323-225022...`、`20260323-225032...` 与 `20260323-234407...`
- 这再次证明 runtime 仍在维护当前 continuation lane，并且 delegated continuation 仍位于当前 prompt 语义层；但它依旧没有给出稳定的 prompt-cycle binding proof，来说明哪个 consumed 事件对应当前 stalled intake
- 因此本轮结论不变：
  - current route 继续保持 `pre_brainstorm`
  - candidate 继续保持 `needs_research`
  - cleanup 继续保持 `retain-for-followthrough`

## 与相邻 issue 的边界

- 不吸收到 `runtime-worker-launch-linkage-and-stall-recovery-governance`
  - 该 issue 冻结的是 `pending intake > cycle log` 的 stalled-AI recovery，与 manager prompt 已吸收 continuation 之后的假活不同
- 不吸收到 `latest-manager-continuity-worker-consumption-governance`
  - 该 issue 关注“已经生成了新的 continuity / prompt set，但 worker 仍消费旧轮次”
  - 当前候选关注的是“manager prompt 已吸收 delegated continuation，但没有继续产出新的 continuity / handoff”
- 不吸收到 `worker-active-reentry-for-manager-delegated-continuation-governance`
  - 该 issue 关注 worker 已活着时如何消费 delegated continuation，不覆盖 manager 侧 prompt absorption 后的 stalled manager AI

## 当前判断

- status: `needs_research`
- 这条 contract 已经从“模糊现象”收敛为“可描述、可测试、可观测”的 runtime gap
- 但本轮仍不直接 materialize：
  - 仓库里已有 runtime / skill / test 证据，但尚未形成 milestone-owned issue 真源
  - 仍需再做一轮真实 dogfood，确认该 contract 在 cleanup / retirement followthrough 上稳定，不会被吸收到更大的 manager recovery 家族
  - 还需把“pending 与 consumed 同时出现”的 current truth 与“当前 prompt cycle 真正吸收了哪个 stalled intake”的 prompt-bound proof 之间的最小 runtime-visible evidence 冻结清楚，否则 promotion 后 acceptance anchor 仍会摇摆
  - 当前 runtime / test 已证明 watchdog 可以结合 prompt-level signal 与状态面做 recovery，但仍未证明 consumed truth 对当前 prompt cycle 的绑定足够稳定
- 因此当前继续保留在 `pre-brainstorm`
  - route_kind: `pre_brainstorm`
  - target_skill: `workspace/skills/doc-pre-brainstorm-execution/SKILL.md`
  - next_recommended_route: `doc-pre-brainstorm-execution`

## 建议承接位置

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/skills/watchdog-control-plane/SKILL.md`
- 相关 runtime script tests

## 生命周期判断

- 这不是单条 cleanup issue 的业务阻塞
- 这是 Freely 自举中暴露的通用 runtime orchestration gap
- 应先留在 pre-brainstorm / candidate 队列，再根据边界稳定度决定是否 materialize 为独立 issue
- 下一次重判重点：
  - 真实 dogfood 是否再次命中相同假活
  - runtime patch 是否把 cleanup / retirement followthrough 稳定推进到可关闭
  - 是否出现一个更高层的 manager recovery issue 能自然吸收这条 contract，而不是事后硬并
