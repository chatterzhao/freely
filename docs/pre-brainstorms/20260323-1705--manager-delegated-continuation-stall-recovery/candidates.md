# 候选：manager-delegated-continuation-stall-recovery

- candidate_format_version: `v2`
- id: `C-20260323-1705-A`
- title: Detect and recover manager delegated continuation stalls after prompt absorption
- source_brainstorm: `docs/pre-brainstorms/20260323-1705--manager-delegated-continuation-stall-recovery/brainstorms.md`
- status: `needs_research`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `pending://manager-delegated-continuation-stall-recovery-materialization`
- session_refs:
  - tool: `codex`
    session_id: `019d1d6a-2319-7952-9c01-8606f51dc59c`
    jsonl_path: `/Users/zhaoyu/.codex/sessions/2026/03/23/rollout-2026-03-23T18-16-28-019d1d6a-2319-7952-9c01-8606f51dc59c.jsonl`
    role: `author-handoff`
  - tool: `codex`
    session_id: `019d1da9-7cc2-7421-8849-5aa0a9a9a0c9`
    jsonl_path: `/Users/zhaoyu/.codex/sessions/2026/03/23/rollout-2026-03-23T19-25-40-019d1da9-7cc2-7421-8849-5aa0a9a9a0c9.jsonl`
    role: `continuity-review-before-compaction`
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://fresh-session-thread-id-not-exposed`
    role: `worker-closeout-current-round`
  - tool: `codex`
    session_id: `019d1e3f-644c-7de3-84be-3ec5f2552c74`
    jsonl_path: `/Users/zhaoyu/.codex/sessions/2026/03/23/rollout-2026-03-23T22-09-24-019d1e3f-644c-7de3-84be-3ec5f2552c74.jsonl`
    role: `context-compacted-handoff-source`
- why_now:
  - 真实 dogfood 已复现 `cleanup continuation` 进入 manager prompt 后，AI 假活但不产出 continuity / handoff 的断点。
  - 当前 runtime state surface 已能稳定暴露 `current_prompt_has_delegated_continuation=1`、当前 `prompt_excerpt` 含 `Delegated continuation handoff`、`latest_manager_worker_prompts_generated=none`，且 delegated continuation ids 会同时出现在 `pending_delegated_continuation_ids` 与 `last_consumed_delegated_continuation_ids`；说明 runtime 已能看到 prompt-level absorption，也开始暴露 consumed truth，但还没把 consumed truth 稳定绑定到当前 prompt cycle。
- pool_scan:
  - prioritized_pool: `candidate_issues + source pre-brainstorm artifacts`
  - why_prioritized: 当前 delegated continuation handoff 直接指向 `C-20260323-1705-A`，且 `docs/milestones.md` 仍将其标记为 `candidate` / `in_pre_brainstorm`
  - checked_but_not_owner:
    - `docs/epics/**`: 未发现 milestone-owned issue 接管
    - `docs/progress/**`: 未发现 dev-loop continuation 接管
    - `docs/recovery/**`: 未发现 recovery artifact 接管
    - `review/test`: 仅提供 supporting evidence，不改变 canonical route
    - `human chat/session evidence`: 仅证明 continuation 来源，不替代 candidate 真源
    - `github issue`: 未发现外部 issue 接管
- runtime_visible_evidence:
  - prompt-level proof:
    - `current_prompt_has_delegated_continuation=1`
    - `current_focus.prompt_excerpt` 包含 `Delegated continuation handoff`
    - `intake_snapshot` 中存在当前 delegated continuation intake ids，可追溯到当前 prompt 周期
  - partial consumed-id proof:
    - `intake_delegated_items=30`，且 `last_consumed_delegated_continuation_ids` 已覆盖当前观察窗口中的全部 30 个 delegated continuation ids，其中包括 `20260323-204333...`、`20260323-204334...`、`20260323-205242...`、`20260323-205340...`、`20260323-220921...`、`20260323-222254...`、`20260323-222255...`、`20260323-225022...`、`20260323-225032...` 与 `20260323-234407...`
    - 说明 runtime 已经开始把 delegated continuation consumption 暴露为 canonical truth，而不是只剩 prompt excerpt 可读证据
  - stall-level proof:
    - `latest_manager_continuity_generated=unavailable`
    - `latest_manager_worker_prompts_generated=none`
    - manager prompt 进入 delegated continuation 后仍无新的 continuity / handoff / launch-state 前进
  - current runtime continuity surface:
    - `activity_state=ai_active`
    - `last_ai_state=down`
    - `last_exit_reason=ai_exit_rc_0`
    - `last_launch_kind=fresh_with_handoff`
    - `last_rotation_reason=context_compacted`
    - 说明 runtime 当前同时暴露“本轮 worker 仍处于 active 视图”和“上一跳 AI 退出/轮换留痕”；这层 continuity surface 证明 runtime 还在维护当前 lane，但仍不等于当前 manager prompt cycle 对 stalled intake 的稳定 binding proof
  - runtime/test scope proof:
    - `docs/system/workspace/scripts/runtime/freely` 已把 `LAST_MANAGER_CONTINUITY_GENERATED/CONSUMED`、`LAST_MANAGER_WORKER_PROMPTS_GENERATED/CONSUMED` 与 delegated pending/consumed ids 写入状态面，并由 `live-status` 暴露
    - `manager_ai_stalled_after_delegated_continuation_prompt` 仍主要依据 prompt 已含 delegated continuation，且 prompt / cycle log 之后没有更新的 manager continuity 继续推进
    - 对应脚本测试已证明 pending/consumed ids 与 generated/consumed continuity truth 会进入 state surface，也证明“prompt-absorbed stall 会触发 recovery”；但仍没有冻结 `consumed` truth 与当前 prompt cycle / 当前 stalled intake 的绑定语义
- missing_evidence:
  - 当前 delegated continuation ids 仍会同时停留在 `pending_delegated_continuation_ids` 与 `last_consumed_delegated_continuation_ids`
  - 仍缺少一个稳定、可验收的 runtime-visible anchor，用来严格证明“哪个 consumed 事件对应当前 manager prompt cycle / 当前 stalled intake”，而不是只知道 runtime 曾经记录过 consumed truth
  - 当前还缺少一个可重复的等价 proof，来说明在 `pending/consumed` 长期并存时，为什么本轮可以确认“当前 stalled intake 已被当前 prompt cycle 吸收”
- acceptance_criteria:
  - 明确区分当前候选与 `pending intake > cycle log`、latest continuity consumption、worker active reentry 这几条相邻治理 issue 的边界。
  - 冻结这条候选的最小 contract：`delegated continuation` 已进入 manager prompt，但在有界时间内没有新的 manager continuity / worker handoff 产出。
  - 冻结最小 runtime-visible evidence：至少要有 prompt-level absorption proof；若 `pending` 与 `consumed` 并存，则必须明确记录当前仍缺“consumed truth 绑定到当前 prompt cycle / stalled intake”的稳定 anchor，而不是把这组并存状态直接当作已完成吸收。
  - 保持 `docs/pre-brainstorms/**` 与 `docs/milestones.md` 对 candidate 状态、下一跳和重判条件的一致性，不让该研究项从扫描面消失。
- promotion_gate:
  - 至少再有一轮真实 dogfood 证明这条 stall contract 能稳定解释 cleanup / retirement followthrough 中的假活，而不是一次性偶发现象。
  - 确认这条 contract 不会被更高层的 manager recovery / stall issue 自然吸收，或者已经具备清晰的 issue-owned 承接位置。
  - 冻结用于 issue-level acceptance 的 runtime-visible absorption anchor；若 `pending` 与 `consumed` 仍并存，至少要明确一个可重复的 prompt-cycle binding proof，而不是只靠人工读 prompt excerpt 或只看 consumed 列表命中。
  - 明确区分“watchdog 已能基于 prompt-level signal 触发 recovery”与“candidate 已具备可 materialize 的 issue-level acceptance anchor”；前者不能自动替代后者。
  - 若准备 promotion，需要至少一轮独立 acceptance review，而不是仅凭当前 worktree 的自我判断直接 materialize。
- open_questions:
  - 这条 contract 最终应独立 materialize，还是并入更高层的 manager recovery issue family？
  - 真实 cleanup / retirement followthrough 是否还会再次命中同一类“prompt 已吸收 continuation 但无新 continuity / handoff”的假活？
  - `live-status` 当前暴露的 prompt-level signal 加 `pending/consumed` 并存 truth 是否足以成为 acceptance anchor，还是仍必须补上 prompt-cycle / stalled-intake 级别的 binding 真源？
  - 若 consumed truth 会长期与 pending 并存，什么等价 proof 才足以把这条候选从 pre-brainstorm 提升到 IBM？
- acceptance_reviews:
  - reviewer: `codex-explorer:Cicero`
    mode: `subagent-review`
    summary: `独立复核确认当前 evidence 只足以支撑继续留在 pre_brainstorm：promotion_gate 仍要求真实 dogfood followthrough，open_questions 尚未收口，当前 dirty delta 是 canonical candidate writeback，不应丢弃。`
    verdict: `keep-in-pre-brainstorm`
  - reviewer: `codex-explorer:Zeno`
    mode: `subagent-runtime-surface-review`
    summary: `独立复核确认当前已不只是 prompt 文本证据：runtime 已把 pending/consumed ids 与 continuity generated/consumed truth 写入状态面并暴露给 live-status；但这些证据仍未 materialize 成“当前 prompt cycle / 当前 stalled intake 一一绑定”的稳定锚点。`
    verdict: `keep-in-pre-brainstorm`
  - reviewer: `codex-explorer:Goodall`
    mode: `subagent-owner-scan`
    summary: `独立只读扫描确认 `docs/epics/**`、`docs/progress/**` 与缺失的 `docs/recovery/**` 中都没有接管 `C-20260323-1705-A` 的 canonical owner；当前最关键缺口仍是把 consumed truth 稳定绑定到当前 manager prompt cycle / 当前 stalled intake 的 runtime-visible anchor。`
    verdict: `keep-in-pre-brainstorm`
  - reviewer: `codex-explorer:Ramanujan`
    mode: `subagent-owner-scan`
    summary: `本轮 fresh session 的独立只读 owner scan 再次确认：`docs/milestones.md` 仍把 `C-20260323-1705-A` 保留为 `candidate/in_pre_brainstorm`，`docs/recovery/` 目录也尚未启用；最接近的相邻 issue 仍只是 worker active reentry、latest manager continuity consumption 与 worker launch linkage 这些前置/相邻控制面，不构成对当前 prompt-absorbed stall contract 的 canonical 接管。`
    verdict: `keep-in-pre-brainstorm`
  - reviewer: `codex:gpt-5.4`
    mode: `worker-closeout`
    summary: `本轮首跳复核确认 canonical pre-brainstorm writeback 已继续收敛到当前 `HEAD` `16182d6`，当前工位已 clean；最新 `live-status` 同时显示 `activity_state=ai_active` 与 `last_ai_state=down/ai_exit_rc_0`，并保持 `fresh_with_handoff/context_compacted`、`pending`/`consumed` delegated continuation ids 30/30 全量重叠。结合独立 owner scan 与 `HEAD...develop = 9 28`，结论仍是 route 保持 pre_brainstorm，cleanup 不能判定为 retire-now。`
    verdict: `keep-and-merge-writeback-first`
- expected_outcome:
  - define a runtime-visible stall contract for `delegated continuation already absorbed into prompt`
  - trigger runtime-owned recovery when no new manager continuity / worker handoff is emitted in bounded time
  - preserve the older pending-intake stall contract as a separate signal
- decision_reason:
  - 这次 gap 已超出单条 cleanup lifecycle；它属于 Freely runtime control plane 的通用自治缺口。
  - 当前已有 runtime / skill / test 证据，但还缺少一轮真实 dogfood followthrough 来冻结边界，因此不应因为仓库里已经有补丁就直接提升到 IBM。
  - 与 `I-20260322-0445` 的边界仍然清楚：后者处理“已生成新 continuity / prompt set 但 worker 仍消费旧轮次”，当前候选处理的是“manager prompt 已吸收 delegated continuation，但没有继续产出新的 continuity / handoff”。
  - 当前仓库复核仍未发现 issue/progress/recovery 真源接管该候选；因此这轮只能补 continuity writeback，不能把 route_kind 提前改成 `ibm`、`dev_loop` 或 `recovery`。
  - 当前 runtime 已给出 prompt-level absorption proof，并开始暴露 delegated continuation consumed truth；但它还没有把这层 truth 稳定绑定到当前 prompt cycle / 当前 stalled intake，所以 promotion 后的 acceptance anchor 仍不稳定，candidate 继续保持 `needs_research`。
  - 当前 watchdog/runtime/tests 证明的是“prompt-level absorption 加 runtime state surface 足以触发 recovery”，不是“prompt-cycle binding 已经稳定到足以 materialize issue”；这两层证据不能混用。
- next_action:
  - 保持 active candidate；继续用真实 dogfood 验证 prompt-absorbed delegated continuation stall 是否能被 runtime recovery 稳定推进到 cleanup / retirement followthrough，然后再判断是 materialize 为独立 issue，还是吸收到更高层 stall/recovery issue 族。
  - 下一轮优先验证 runtime 能否把当前 `pending/consumed` 并存状态绑定到当前 prompt cycle，明确哪一个 stalled delegated continuation 真的被本轮 prompt 吸收；若不能，至少冻结一个不依赖人工解释 prompt excerpt 的等价 proof。
  - 将当前 `fresh_with_handoff/context_compacted` 的 continuity 事实继续视为 supporting evidence：它证明 runtime 已因上下文压缩做过续接，但不证明当前 prompt cycle 对 stalled intake 的 binding 已稳定；因此后续仍要把续接事实与 prompt-cycle absorption proof 分开验收。
  - 在 manager/runtime cleanup 判断中，不再沿用“本树已被 develop 吸收、只剩 dirty writeback”的旧前提；当前 canonical writeback 已继续收敛到 `16182d6`，下一步应先把这些独有提交吸收到上游，再决定 retirement。
  - 若再次发生会话轮换或 `context_compacted`，先把最新 continuity 结论写回当前 pre-brainstorm canonical artifacts，再继续扩大实现或 cleanup 判断。
- revisit_trigger:
  - 当再次复现 manager prompt 已吸收 continuation 但无新 continuity / handoff 的假活，且 runtime 能给出当前 prompt cycle / stalled intake 的 binding proof 时，重新进入 materialization 判断。
  - 当当前 runtime 补丁在真实 followthrough 中验证稳定，且边界已可冻结成独立 issue contract 时，重新进入 materialization 判断。
  - 当 manager 已吸收当前分支上的 canonical writeback 提交并重新做 cleanup 巡检时，重新判断该 worktree 是否满足 `retire-now`。
- route_kind: `pre_brainstorm`
- next_recommended_route: `doc-pre-brainstorm-execution`
- restart_point: `continuation`
- ownership: `worker-canonical-pre-brainstorm-writeback`
- cleanup_disposition: `retain-for-followthrough`
- safe_for_retirement: `false`
