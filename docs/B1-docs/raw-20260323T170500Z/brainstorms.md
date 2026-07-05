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

## remaining binding proof gap

- 当前还缺的不是泛泛的 “runtime 再多给一点状态”，而是一条精确的 runtime-visible binding proof：
  - 同一轮真实 dogfood 中，先观察某个具体 stalled delegated continuation intake id 进入当前 manager prompt cycle
  - 然后由 runtime 给出稳定锚点，明确“当前 `last_consumed_delegated_continuation_ids` 中的哪一次 consumed 事件，正对应这个 prompt cycle / 这个 stalled intake”
  - 再证明这条绑定之后，若 manager 仍无新 continuity / worker handoff，watchdog recovery 命中的是“当前 prompt 已吸收但未继续产出”的 stall，而不是历史 consumed truth 的回放
- 现在缺的正是这一跳一一绑定：
  - `pending_delegated_continuation_ids` 与 `last_consumed_delegated_continuation_ids` 长期并存
  - prompt excerpt 只能证明“当前 prompt 有 delegated continuation 语义”
  - consumed 列表只能证明“runtime 某时记录过 consumed truth”
  - 但两者之间还没有一个稳定、可重复复核的 current-cycle binding anchor
- 因此当前缺口必须保持显式：
  - missing proof: `current stalled intake id -> current prompt cycle -> consumed event anchor -> no-new-continuity/handoff stall verdict`
  - 只要这条链还不能稳定观察，本候选就不能进入 IBM，也不能被 cleanup/retirement 视为已完成 proof

### 当前最小 blocker 集合

- `specimen-chain binding proof`
  - 需要把具体 stalled intake、当前 prompt cycle、consumed anchor 与 stall verdict 固定到同一条可复核链上
- `one real dogfood followthrough`
  - 需要一轮真实 recovery/cleanup 推进，证明这条链不只是静态状态面，而能继续驱动 followthrough

- 在这两个 blocker 没完成前，本候选继续保持 active pre-brainstorm owner

### 这条 proof gap 现在应按三段 specimen-chain 理解

- 当前真正未冻结的不是一个模糊“大 gap”，而是同一条 specimen-chain 上的三个并列证明点：
  1. `specific stalled intake specimen`
     - 必须先从 `20260323-234407...`、`20260324-002656...`、`20260324-021757...` 等并存 pending ids 中固定本轮 stall specimen。
  2. `current prompt-cycle / consumed-anchor binding`
     - 必须证明 `.freely/run/prompt-20260324-024527.txt` 与 `last_consumed_delegated_continuation_at=2026-03-24T09:41:25Z` 代表的是同一当前 prompt cycle，而不是历史 surface 的再次显现。
  3. `same-chain stall verdict`
     - 必须把 `latest_manager_continuity_generated=unavailable`、`latest_manager_worker_prompts_generated=none` 这类 no-new-continuity/handoff verdict 绑定回同一 specimen-chain，而不是仅作为背景性 supporting evidence。

- 只要三段里任意一段还不能稳定复核，这条候选就仍然是 active pre-brainstorm owner，而不是 evidence-only 历史树。

## binding proof chain（当前冻结版本）

- 目标不是证明 “某次 delegated continuation 曾被 consumed 过”，而是冻结一条可重复复核的单链：
  1. `specific stalled intake id`
     - 先固定本轮 stall 关注的 delegated continuation intake id，而不是只看聚合计数。
     - 当前可追踪的 stalled intake specimen 仍包括 `20260323-234407...`、`20260324-002656...` 与 `20260324-021757...`，因为它们在最新 worker `live-status` 中继续位于 `pending_delegated_continuation_ids`。
  2. `current prompt cycle`
     - 再固定当前真正承载 delegated continuation 语义的 prompt cycle。
     - 当前锚点是 `current_focus.prompt_file=.freely/run/prompt-20260324-024527.txt`，并且 `current_prompt_has_delegated_continuation=1`。
  3. `consumed event anchor`
     - 然后需要一个稳定锚点，说明“当前 prompt cycle 吸收 stalled intake”对应哪一次 consumed 事件，而不是仅仅看到历史 `consumed` truth 又出现了。
     - 当前最接近的 surface 只有 `last_consumed_delegated_continuation_ids` 与 `last_consumed_delegated_continuation_at=2026-03-24T09:41:25Z`；但它们仍只是并存 surface，尚未把某个 stalled intake id 一一绑定到当前 prompt cycle。
  4. `no-new-continuity/handoff stall verdict`
     - 最后才是 stall 裁决：在上述 intake / prompt / consumed anchor 已绑定之后，仍然没有新的 manager continuity / worker handoff / launch-state 前进，才能判成当前 prompt-absorbed stall。
- 这条链的关键在顺序：
  - 不能从 “没有新 continuity/handoff” 倒推出 intake 已被当前 prompt 吸收；
  - 也不能从 `pending/consumed` 并存倒推出当前 stalled intake 已拥有 consumed anchor；
  - 必须先固定 `specific intake -> current prompt cycle -> consumed event anchor`，再允许进入 stall verdict。

## 当前 specimen 链为何仍不足

- 当前证据最多只能稳定回答两件事：
  - 当前 delegated continuation 语义确实已经进入当前 prompt cycle；
  - `consumed` surface 当前再次出现，并与 `pending` 32/32 全量重叠。
- 但它仍无法稳定回答这两个 acceptance 关键问题：
  - 当前 `pending` 集合里的哪一个 stalled intake id，真正被 `.freely/run/prompt-20260324-024527.txt` 这一轮 prompt 吸收？
  - `2026-03-24T09:41:25Z` 这次 consumed anchor 与当前 prompt cycle 的关系，是当前吸收事件，还是历史 surface 再次暴露？
- 因而当前 verdict 只能保持：
  - `prompt absorption visible`
  - `consumed surface visible but unbound`
  - `stall verdict not yet promotable`

## next dogfood experiment required

- 下一轮必须做的不是脚本级回归，而是一轮真实 Freely dogfood：
  - 从 `develop` 启动 runtime
  - 通过 `freely chat --project <project-root> ...` 注入一条可追踪的 delegated continuation
  - 在 manager prompt 已吸收该 intake 后，持续抓取 `live-status` / continuity / worker prompt surface
  - 要求这轮证据能同时回答四件事：
    - 哪个 stalled intake id 被当前 prompt cycle 吸收
    - 哪个 consumed 事件与这个 prompt cycle 绑定，而不是历史 surface 再次出现
    - 在无新 continuity / handoff 的窗口内，watchdog 是否按这条绑定触发 recovery
    - recovery 后 cleanup / followthrough 是否继续推进，而不是只留下历史 consumed truth
- 若这轮 dogfood 仍只能看到 `pending/consumed` 并存，却无法稳定回答上述四件事，则本候选继续留在 pre-brainstorm

## retirement gate remains blocked

- 当前这棵树的 delete / retirement gate 仍然阻塞，原因不是 worktree hygiene，而是 proof hygiene：
  - 当前 canonical writeback 仍是这条候选的唯一 owner-facing continuity anchor
  - 上游还没有吸收并固定“current prompt cycle / current stalled intake”所需的 binding proof 结论
  - 也还没有完成上述真实 dogfood followthrough
- 因此当前只能判：
  - `cleanup_disposition=retain-for-followthrough`
  - `safe_for_retirement=false`
  - 不得把“本树 clean”或“已有 runtime tests”误读成可删除

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
- 当前仓库扫描未发现 `docs/progress/**`、`docs/B2-docs/**` 或其他 issue/progress/recovery 真源已经接管本候选；因此这轮 continuity 仍应写回 pre-brainstorm，而不是误切到 IBM、dev-loop 或 recovery
- 当前分支 `feature/manager-delegated-continuation-stall-materialization-20260323` 仍未被 `develop` 吸收；这说明 worktree cleanup 与 candidate materialization 仍应分开判断，不能因为已有 canonical writeback 提交就把该候选视为已关闭

## 需求池扫描与优先级

- 本轮优先池：`docs/B1-docs/raw-**` + `docs/milestones.md`
  - delegated continuation handoff 明确把当前输入收束到 `C-20260323T170500Z-A` 的 continuation
  - `milestones.md` 仍把该条目保留在 `candidate_issues`，且 `phase_state=in_pre_brainstorm`
- 已核对但未接管的池：
  - `docs/B2-docs/**`：未发现该候选的 milestone-owned issue 真源
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
  - `docs/milestones.md` 仍把 `C-20260323T170500Z-A` 保留在 `candidate_issues`
  - 未发现 `docs/progress/**`、`docs/recovery/**`、`docs/B2-docs/**` 的 issue/progress/recovery 真源接管该候选
  - `freely live-status` 当前显示 `role_hint: worker`、`activity_state: ai_active`、`last_ai_state: down`、`last_exit_reason: ai_exit_rc_0`、`last_launch_kind: fresh_with_handoff`、`last_rotation_reason: context_compacted`，且 delegated continuation 仍在当前 prompt 上下文中
- 结论：
  - route_kind 继续保持 `pre_brainstorm`
  - 当前分支的独有提交仍是 canonical candidate writeback，而不是可直接丢弃的噪音
  - 但在这些提交尚未被上游吸收前，这棵树不满足 `retire-now`

## 吸收更新（2026-03-25）

- 当前 source tree `feature/manager-delegated-continuation-stall-materialization-20260323` 上的 canonical pre-brainstorm writeback 已被 develop-facing merge-prep owner line 吸收。
- 这次吸收只关闭 source-tree 独有提交的 cleanup gate，不关闭 candidate 本身：
  - `C-20260323T170500Z-A` 仍然是 `candidate / in_pre_brainstorm`
  - `specimen-chain binding proof` 与 `one real dogfood followthrough` 仍然是 promotion blocker
  - retained-with-reason 继续挂在 merge-prep owner line，而不是旧 source tree
- 因此后续 cleanup/retirement 判断要拆开看：
  - 旧 source tree 现在可以按 absorbed source lane 退休
  - candidate owner 仍继续存在，直到 canonical manager surface 吸收 merge-prep owner line 并补完真实 dogfood followthrough

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

## continuity guard writeback（2026-03-24 02:18 PST）

- 本轮再次先执行 worker-side `live-status` 复核，再决定是否还能沿用前几轮记录下来的 `consumed` 证据表述。
- 当前 worker lane 的最新 `live-status` 显示：
  - `role_hint=worker`
  - `activity_state=ai_active`
  - `last_ai_state=down`
  - `last_exit_reason=starting`
  - `intake_active_items=32`
  - `intake_delegated_items=32`
  - `current_prompt_has_delegated_continuation=1`
  - `latest_manager_continuity_generated=unavailable`
  - `latest_manager_worker_prompts_generated=none`
  - `pending_delegated_continuation_ids` 继续包含当前 lane 的 `20260323-234407...`、`20260324-002656...` 与 `20260324-021757...`
  - 但 `last_consumed_delegated_continuation_ids=none`
  - 且 `last_consumed_delegated_continuation_at=unavailable`
  - `current_focus.prompt_file=.freely/run/prompt-20260324-021757.txt`
  - `deep_refs.last_tool_session_id=unavailable`
- 这说明两件事：
  - prompt-level absorption 与 active worker lane 仍然存在，当前 candidate 继续有 canonical owner，不能静默丢弃
  - 但前几轮文档里记录的 “已有 partial consumed-id proof” 在当前 worker lane 上并不稳定；runtime 这轮已经退回到“只有 pending + prompt absorption proof，没有当前 consumed anchor”的状态
- 因此当前 proof gap 需要进一步收紧：
  - 不仅缺少 `specific stalled delegated continuation intake id -> current manager prompt cycle -> consumed event anchor -> no-new-continuity/handoff stall verdict` 的稳定绑定链
  - 当前这一轮甚至不能假设 `consumed` truth 仍持续暴露在 live-status 上
- 这也再次证明：
  - 当前 route 仍应保持 `pre_brainstorm`
  - 当前 worktree 仍应保持 `retain-for-followthrough`
  - delete / retirement gate 仍不能打开

## continuity guard writeback（2026-03-24 02:23 PST）

- 本轮 fresh session 继续先执行 worker-side `live-status` 复核，再决定 canonical writeback 是否需要沿用上一轮“当前 consumed truth 缺席”的表述。
- 最新 worker lane 的 `live-status` 现在显示：
  - `last_state_updated_at=2026-03-24T09:23:30Z`
  - `activity_state=ai_active`
  - `last_ai_state=down`
  - `last_exit_reason=ai_exit_rc_0`
  - `last_launch_kind=fresh`
  - `last_rotation_reason=initial_start`
  - `intake_active_items=32`
  - `intake_delegated_items=32`
  - `current_prompt_has_delegated_continuation=1`
  - `latest_manager_continuity_generated=unavailable`
  - `latest_manager_worker_prompts_generated=none`
  - `pending_delegated_continuation_ids` 继续包含当前 lane 的 `20260323-234407...`、`20260324-002656...` 与 `20260324-021757...`
  - `last_consumed_delegated_continuation_ids` 也再次覆盖同一批 32 个 delegated continuation ids
  - `last_consumed_delegated_continuation_at=2026-03-24T09:18:01Z`
  - `current_focus.prompt_file=.freely/run/prompt-20260324-022330.txt`
  - `deep_refs.last_tool_session_id=019d1f23-0255-7c83-b56f-cffe2c64ab40`
- 这说明当前 proof gap 需要进一步被精确表述成“摇摆而非单向缺失”：
  - 上一轮 worker lane 一度退回到 `last_consumed_delegated_continuation_ids=none`
  - 本轮又重新回到 `pending` / `consumed` 32/32 全量重叠
  - 因此问题不再只是“consumed truth 当前缺席”，而是“consumed truth 既不稳定，也没有被稳定绑定到当前 prompt cycle / 当前 stalled intake”
- 所以当前 canonical 结论依旧不变：
  - prompt-level absorption 仍可见，candidate 继续有 canonical owner，不能静默丢弃
  - consumed truth 即使再次出现，也仍只能证明 runtime 记录过某批 consumed ids；它还不能稳定回答“当前 prompt cycle 真正吸收的是哪个 stalled intake”
  - `specific stalled intake id -> current manager prompt cycle -> consumed event anchor -> no-new-continuity/handoff stall verdict` 这条绑定链仍未冻结成稳定 acceptance anchor
  - 当前 route 继续保持 `pre_brainstorm`
  - cleanup 继续保持 `retain-for-followthrough`
  - delete / retirement gate 仍不能打开

## continuity guard writeback（2026-03-24 02:28 PT）

- 本轮 fresh session 继续遵守 `context_compacted -> 先更新 doc-loop continuity artifact`，因此再次先跑 worker-side `live-status`，只刷新当前 candidate 的 canonical 锚点，不扩大到 IBM / dev-loop。
- 最新 worker lane 的 `live-status` 现在显示：
  - `last_state_updated_at=2026-03-24T09:28:58Z`
  - `activity_state=ai_active`
  - `last_ai_state=down`
  - `last_exit_reason=ai_exit_rc_0`
  - `last_launch_kind=fresh_with_handoff`
  - `last_rotation_reason=context_compacted`
  - `intake_active_items=32`
  - `intake_delegated_items=32`
  - `current_prompt_has_delegated_continuation=1`
  - `latest_manager_continuity_generated=unavailable`
  - `latest_manager_worker_prompts_generated=none`
  - `pending_delegated_continuation_ids` 与 `last_consumed_delegated_continuation_ids` 继续 32/32 全量重叠，其中仍包含当前 lane 的 `20260323-234407...`、`20260324-002656...` 与 `20260324-021757...`
  - `last_consumed_delegated_continuation_at=2026-03-24T09:23:35Z`
  - `current_focus.prompt_file=.freely/run/prompt-20260324-022858.txt`
  - `deep_refs.last_tool_session_id=019d1f28-1cc7-71d0-8c09-ee89cf6a25cd`
  - `deep_refs.last_tool_jsonl_path=/Users/zhaoyu/.codex/sessions/2026/03/24/rollout-2026-03-24T02-23-35-019d1f28-1cc7-71d0-8c09-ee89cf6a25cd.jsonl`
- 这进一步说明：
  - 当前 worker continuation lane 仍被 runtime 维护，且最新 prompt 仍直接承接同一条 delegated continuation canonical writeback 线
  - `consumed` truth 目前又重新出现，并且继续与 `pending` 全量并存；因此缺口仍不是“有没有 consumed surface”，而是“这个 consumed surface 是否稳定绑定到当前 prompt cycle / 当前 stalled intake”
  - `fresh_with_handoff` 与 `context_compacted` 只证明 runtime 正在做 continuity rotation，不证明 `specific stalled intake id -> current manager prompt cycle -> consumed event anchor -> no-new-continuity/handoff stall verdict` 这条链已经稳定
- 因此这轮仍应保持：
  - route_kind: `pre_brainstorm`
  - cleanup_disposition: `retain-for-followthrough`
  - safe_for_retirement: `false`

## continuity guard writeback（2026-03-24 02:32 PT）

- 本轮 fresh session 继续先执行 worker-side `live-status` 复核，再决定是否能把这条候选从 canonical pre-brainstorm writeback 转交给别的 loop。
- 最新 worker lane 的 `live-status` 现在显示：
  - `last_state_updated_at=2026-03-24T09:32:59Z`
  - `activity_state=ai_active`
  - `last_ai_state=down`
  - `last_exit_reason=ai_exit_rc_0`
  - `last_launch_kind=fresh_with_handoff`
  - `last_rotation_reason=context_compacted`
  - `intake_active_items=32`
  - `intake_delegated_items=32`
  - `current_prompt_has_delegated_continuation=1`
  - `latest_manager_continuity_generated=unavailable`
  - `latest_manager_worker_prompts_generated=none`
  - `pending_delegated_continuation_ids` 与 `last_consumed_delegated_continuation_ids` 继续 32/32 全量重叠，其中仍包含当前 lane 的 `20260323-234407...`、`20260324-002656...` 与 `20260324-021757...`
  - `last_consumed_delegated_continuation_at=2026-03-24T09:29:02Z`
  - `current_focus.prompt_file=.freely/run/prompt-20260324-023259.txt`
  - `deep_refs.last_tool_session_id=019d1f2d-1b3f-7c23-92ca-30f5389315fc`
  - `deep_refs.last_tool_jsonl_path=/Users/zhaoyu/.codex/sessions/2026/03/24/rollout-2026-03-24T02-29-03-019d1f2d-1b3f-7c23-92ca-30f5389315fc.jsonl`
- 这轮新增事实只进一步加强了同一个结论：
  - runtime 继续把当前 worker lane 当作 active continuation 维护，说明 canonical owner 仍是当前 candidate
  - `consumed` truth 仍与 `pending` 全量并存，且只是随着 prompt/cycle 前移滚动；它依旧没有冻结成 `specific stalled intake id -> current manager prompt cycle -> consumed event anchor -> no-new-continuity/handoff stall verdict` 这条稳定绑定链
  - 因此这轮仍不能转去 IBM、dev-loop 或 cleanup retirement 判定
- 所以当前仍应保持：
  - route_kind: `pre_brainstorm`
  - cleanup_disposition: `retain-for-followthrough`
  - safe_for_retirement: `false`

## continuity guard writeback（2026-03-24 02:37 PT）

- 本轮 fresh session 继续先执行 worker-side `live-status` 复核，再决定是否能把这条候选从 canonical pre-brainstorm writeback 转交给别的 loop。
- 最新 worker lane 的 `live-status` 现在显示：
  - `last_state_updated_at=2026-03-24T09:37:20Z`
  - `activity_state=ai_active`
  - `last_ai_state=down`
  - `last_exit_reason=ai_exit_rc_0`
  - `last_launch_kind=fresh_with_handoff`
  - `last_rotation_reason=context_compacted`
  - `intake_active_items=32`
  - `intake_delegated_items=32`
  - `current_prompt_has_delegated_continuation=1`
  - `latest_manager_continuity_generated=unavailable`
  - `latest_manager_worker_prompts_generated=none`
  - `pending_delegated_continuation_ids` 与 `last_consumed_delegated_continuation_ids` 继续 32/32 全量重叠，其中仍包含当前 lane 的 `20260323-234407...`、`20260324-002656...` 与 `20260324-021757...`
  - `last_consumed_delegated_continuation_at=2026-03-24T09:33:04Z`
  - `current_focus.prompt_file=.freely/run/prompt-20260324-023720.txt`
  - `deep_refs.last_tool_session_id=019d1f30-ca23-7eb2-bbf8-95d50650f4c1`
  - `deep_refs.last_tool_jsonl_path=/Users/zhaoyu/.codex/sessions/2026/03/24/rollout-2026-03-24T02-33-04-019d1f30-ca23-7eb2-bbf8-95d50650f4c1.jsonl`
- 这轮新增事实仍只加强同一个结论：
  - runtime 继续把当前 worker lane 当作 active continuation 维护，说明 canonical owner 仍是当前 candidate
  - `consumed` truth 仍与 `pending` 全量并存，并随 prompt/cycle 前移继续滚动；它依旧没有冻结成 `specific stalled intake id -> current manager prompt cycle -> consumed event anchor -> no-new-continuity/handoff stall verdict` 这条稳定绑定链
  - 因此这轮仍不能转去 IBM、dev-loop 或 cleanup retirement 判定
- 所以当前仍应保持：
  - route_kind: `pre_brainstorm`
  - cleanup_disposition: `retain-for-followthrough`
  - safe_for_retirement: `false`

## continuity guard writeback（2026-03-24 02:41 PT）

- fresh session 本轮继续遵守 `context_compacted -> 先更新 doc-loop continuity artifact`，因此先刷新当前 worker lane 的 canonical 锚点，而不扩大到 IBM / dev-loop / cleanup-only。
- 最新 worker lane 的 `live-status` 现在显示：
  - `last_state_updated_at=2026-03-24T09:45:27Z`
  - `activity_state=ai_active`
  - `last_ai_state=down`
  - `last_exit_reason=ai_exit_rc_0`
  - `last_launch_kind=fresh_with_handoff`
  - `last_rotation_reason=context_compacted`
  - `intake_active_items=32`
  - `intake_delegated_items=32`
  - `current_prompt_has_delegated_continuation=1`
  - `latest_manager_continuity_generated=unavailable`
  - `latest_manager_worker_prompts_generated=none`
  - `pending_delegated_continuation_ids` 与 `last_consumed_delegated_continuation_ids` 仍继续 32/32 全量重叠，其中仍包含当前 lane 的 `20260323-234407...`、`20260324-002656...` 与 `20260324-021757...`
  - `last_consumed_delegated_continuation_at=2026-03-24T09:41:25Z`
  - `current_focus.prompt_file=.freely/run/prompt-20260324-024527.txt`
  - `deep_refs.last_tool_session_id=019d1f38-6e78-7e62-af16-547d3eb16ea5`
  - `deep_refs.last_tool_jsonl_path=/Users/zhaoyu/.codex/sessions/2026/03/24/rollout-2026-03-24T02-41-25-019d1f38-6e78-7e62-af16-547d3eb16ea5.jsonl`
- 这轮新增事实仍只加强同一个结论：
  - runtime 继续把当前 worker lane 当作 active continuation 维护，说明 canonical owner 仍是当前 candidate
  - `consumed` truth 继续与 `pending` 全量并存，并且只是随着 prompt/cycle 前移继续滚动；它依旧没有冻结成 `specific stalled intake id -> current manager prompt cycle -> consumed event anchor -> no-new-continuity/handoff stall verdict` 这条稳定绑定链
  - 因此这轮仍不能转去 IBM、dev-loop、recovery 或 cleanup retirement 判定
- 所以当前仍应保持：
  - route_kind: `pre_brainstorm`
  - cleanup_disposition: `retain-for-followthrough`
  - safe_for_retirement: `false`

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
- 在完成这轮真实 dogfood 并固定 binding proof 之前，不得把该候选对应 worktree 视为可 delete / retire
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
