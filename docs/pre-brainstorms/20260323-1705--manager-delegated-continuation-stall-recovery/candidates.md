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
  - tool: `codex`
    session_id: `019d1eb2-615d-7fe2-a617-69b95a5758ee`
    jsonl_path: `/Users/zhaoyu/.codex/sessions/2026/03/24/rollout-2026-03-24T00-15-00-019d1eb2-615d-7fe2-a617-69b95a5758ee.jsonl`
    role: `fresh-with-handoff-source-latest`
  - tool: `codex`
    session_id: `019d1f23-0255-7c83-b56f-cffe2c64ab40`
    jsonl_path: `/Users/zhaoyu/.codex/sessions/2026/03/24/rollout-2026-03-24T02-18-01-019d1f23-0255-7c83-b56f-cffe2c64ab40.jsonl`
    role: `live-status-anchor-source-latest`
- why_now:
  - 真实 dogfood 已复现 `cleanup continuation` 进入 manager prompt 后，AI 假活但不产出 continuity / handoff 的断点。
  - 当前 runtime state surface 仍能稳定暴露 `current_prompt_has_delegated_continuation=1`、当前 `prompt_excerpt` 含 `Delegated continuation handoff`、`latest_manager_worker_prompts_generated=none` 与当前 lane 的 `pending_delegated_continuation_ids`；但最新几轮 worker `live-status` 在 `last_consumed_delegated_continuation_ids=none` 与 `pending/consumed` 32/32 全量重叠之间摇摆。这说明 prompt-level absorption 已可见，而 consumed truth 既未稳定绑定到当前 prompt cycle，也未稳定成为当前 lane 的 acceptance anchor。
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
  - current worker-lane proof:
    - 最新 `live-status` 显示 `intake_delegated_items=32`
    - `pending_delegated_continuation_ids` 继续包含当前 lane 的 `20260323-234407...`、`20260324-002656...` 与 `20260324-021757...`
    - `last_consumed_delegated_continuation_ids` 当前再次覆盖同一批 32 个 delegated continuation ids
    - `last_consumed_delegated_continuation_at=2026-03-24T09:18:01Z`
    - `current_focus.prompt_file=.freely/run/prompt-20260324-022330.txt`
    - 说明当前 lane 依然有 prompt-level absorption、pending intake 与 consumed surface 证据，但 consumed surface 仍未绑定到当前 stalled intake
  - historical-but-non-stable consumed surface:
    - 前几轮 `live-status` 曾短暂暴露过 `last_consumed_delegated_continuation_ids` 与 `last_consumed_delegated_continuation_at`
    - 随后 worker lane 一度退回 `last_consumed_delegated_continuation_ids=none`
    - 本轮又重新回到 `pending` / `consumed` 32/32 全量重叠
    - 说明 consumed truth 当前不是稳定 acceptance anchor；它会出现、消失并再次出现，但始终没有成为当前 prompt cycle 的 canonical 绑定事实
  - stall-level proof:
    - `latest_manager_continuity_generated=unavailable`
    - `latest_manager_worker_prompts_generated=none`
    - manager prompt 进入 delegated continuation 后仍无新的 continuity / handoff / launch-state 前进
  - current runtime continuity surface:
    - `activity_state=ai_active`
    - `last_ai_state=down`
    - `last_exit_reason=ai_exit_rc_0`
    - `last_launch_kind=fresh`
    - `last_rotation_reason=initial_start`
    - `current_focus.prompt_file=.freely/run/prompt-20260324-022330.txt`
    - `deep_refs.last_tool_session_id=019d1f23-0255-7c83-b56f-cffe2c64ab40`
    - 说明 runtime 当前仍把本轮 worker 视为 active lane，并且最新 continuity anchor 已继续滚动；但这层 continuity surface 仍只够证明 lane 被维护，不足以证明当前 prompt cycle 对 stalled intake 的稳定 binding proof
  - runtime/test scope proof:
    - `docs/system/workspace/scripts/runtime/freely` 已把 `LAST_MANAGER_CONTINUITY_GENERATED/CONSUMED`、`LAST_MANAGER_WORKER_PROMPTS_GENERATED/CONSUMED` 与 delegated pending/consumed ids 写入状态面，并由 `live-status` 暴露
    - `manager_ai_stalled_after_delegated_continuation_prompt` 仍主要依据 prompt 已含 delegated continuation，且 prompt / cycle log 之后没有更新的 manager continuity 继续推进
    - 对应脚本测试已证明 pending/consumed ids 与 generated/consumed continuity truth 会进入 state surface，也证明“prompt-absorbed stall 会触发 recovery”；但仍没有冻结 `consumed` truth 与当前 prompt cycle / 当前 stalled intake 的绑定语义
- missing_evidence:
  - 当前 delegated continuation ids 仍同时停留在 `pending_delegated_continuation_ids` 与 `last_consumed_delegated_continuation_ids`
  - 仍缺少一个稳定、可验收的 runtime-visible anchor，用来严格证明“哪个 consumed 事件对应当前 manager prompt cycle / 当前 stalled intake”；当前也不能假设 consumed truth 会稳定停留在 live-status 上，因为它在最近几轮已出现过缺席与重现的摇摆
  - 当前还缺少一个可重复的等价 proof，来说明在 consumed surface 摇摆或与 pending 并存的情况下，为什么本轮可以确认“当前 stalled intake 已被当前 prompt cycle 吸收”
  - 精确缺口应表述为：`specific stalled delegated continuation intake id -> current manager prompt cycle -> consumed event anchor -> no-new-continuity/handoff stall verdict` 这条链还不能被稳定、重复地从 runtime state surface 中读出
- acceptance_criteria:
  - 明确区分当前候选与 `pending intake > cycle log`、latest continuity consumption、worker active reentry 这几条相邻治理 issue 的边界。
  - 冻结这条候选的最小 contract：`delegated continuation` 已进入 manager prompt，但在有界时间内没有新的 manager continuity / worker handoff 产出。
  - 冻结最小 runtime-visible evidence：至少要有 prompt-level absorption proof；若 `consumed` truth 缺席或与 `pending` 并存，都必须明确记录当前仍缺“consumed truth 绑定到当前 prompt cycle / stalled intake”的稳定 anchor，而不是把历史观测或并存状态直接当作已完成吸收。
  - 保持 `docs/pre-brainstorms/**` 与 `docs/milestones.md` 对 candidate 状态、下一跳和重判条件的一致性，不让该研究项从扫描面消失。
- promotion_gate:
  - 至少再有一轮真实 dogfood 证明这条 stall contract 能稳定解释 cleanup / retirement followthrough 中的假活，而不是一次性偶发现象。
  - 确认这条 contract 不会被更高层的 manager recovery / stall issue 自然吸收，或者已经具备清晰的 issue-owned 承接位置。
  - 冻结用于 issue-level acceptance 的 runtime-visible absorption anchor；无论 `consumed` truth 当前缺席还是与 `pending` 并存，至少都要明确一个可重复的 prompt-cycle binding proof，而不是只靠人工读 prompt excerpt。
  - 明确区分“watchdog 已能基于 prompt-level signal 触发 recovery”与“candidate 已具备可 materialize 的 issue-level acceptance anchor”；前者不能自动替代后者。
  - 若准备 promotion，需要至少一轮独立 acceptance review，而不是仅凭当前 worktree 的自我判断直接 materialize。
  - 在上述 proof 通过前，这棵 worktree 只允许 `retain-for-followthrough`，不得进入 delete / retirement。
- open_questions:
  - 这条 contract 最终应独立 materialize，还是并入更高层的 manager recovery issue family？
  - 真实 cleanup / retirement followthrough 是否还会再次命中同一类“prompt 已吸收 continuation 但无新 continuity / handoff”的假活？
  - `live-status` 当前暴露的 prompt-level signal，加上“当前 consumed truth 在缺席与 32/32 重叠之间摇摆”的状态面，是否足以成为 acceptance anchor，还是仍必须补上 prompt-cycle / stalled-intake 级别的 binding 真源？
  - 若 consumed truth 会继续以这种摇摆或与 pending 并存的方式出现，什么等价 proof 才足以把这条候选从 pre-brainstorm 提升到 IBM？
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
    summary: `本轮首跳复核确认 canonical pre-brainstorm writeback 已继续收敛为本分支上的最新 continuity anchor lineage，当前工位已 clean；最新 `live-status` 同时显示 `activity_state=ai_active` 与 `last_ai_state=down/ai_exit_rc_0`，并保持 `fresh_with_handoff/context_compacted`、`pending`/`consumed` delegated continuation ids 30/30 全量重叠。结合独立 owner scan 与“当前分支仍未被 develop 吸收”的 git 事实，结论仍是 route 保持 pre_brainstorm，cleanup 不能判定为 retire-now。`
    verdict: `keep-and-merge-writeback-first`
  - reviewer: `codex:gpt-5.4`
    mode: `worker-continuity-refresh`
    summary: `本轮 fresh session 先执行 doc-loop continuity guard，把最新 `live-status` 锚点写回 pre-brainstorm：`last_consumed_delegated_continuation_at=2026-03-24T07:12:22Z`、`current_focus.prompt_file=.freely/run/prompt-20260324-001455.txt`，且 `deep_refs.last_tool_session_id=019d1eaf-f86f-7003-9207-8e74d89af249` 再次固定上一轮 `fresh_with_handoff` 来源。这进一步证明 runtime 仍在维护当前 continuation lane，但仍未把 consumed truth 稳定绑定到当前 prompt cycle / stalled intake。`
    verdict: `keep-in-pre-brainstorm`
  - reviewer: `codex:gpt-5.4`
    mode: `worker-continuity-refresh`
    summary: `本轮继续按 doc-loop continuity guard 刷新 canonical anchor：最新 `live-status` 已滚动到 `last_consumed_delegated_continuation_at=2026-03-24T07:14:59Z`、`current_focus.prompt_file=.freely/run/prompt-20260324-001922.txt`，且 `deep_refs.last_tool_session_id=019d1eb2-615d-7fe2-a617-69b95a5758ee` 指向新的 `fresh_with_handoff` 来源。runtime 仍保持 `activity_state=ai_active` 与 `last_ai_state=down/ai_exit_rc_0` 并存，说明 continuation lane 还在被维护，但 consumed truth 依旧没有稳定绑定到当前 prompt cycle / 当前 stalled intake。`
    verdict: `keep-in-pre-brainstorm`
  - reviewer: `codex-explorer:Linnaeus`
    mode: `subagent-owner-boundary-review`
    summary: `独立复核确认 `docs/milestones.md`、当前 candidate 与 worker continuity 仍把 `C-20260323-1705-A` 定位为 `candidate/in_pre_brainstorm`；相邻 issue family 只分别覆盖 delegated continuation pending/consumed evidence、latest continuity consumption、worker active reentry 或 generic stalled-AI recovery，并没有接管“manager prompt 已吸收 continuation 但无新 continuity / handoff”的 acceptance boundary。`
    verdict: `keep-in-pre-brainstorm`
  - reviewer: `codex:gpt-5.4`
    mode: `worker-continuity-refresh`
    summary: `本轮 fresh session 再次按 doc-loop continuity guard 刷新 canonical anchor：最新 `live-status` 已滚动到 `last_consumed_delegated_continuation_at=2026-03-24T07:19:27Z`、`current_focus.prompt_file=.freely/run/prompt-20260324-002242.txt`，且 `deep_refs.last_tool_session_id=019d1eb6-7620-75a2-a5d0-fdc12afa8a55` 指向更新后的 `fresh_with_handoff` 来源。runtime 仍保持 `activity_state=ai_active` 与 `last_ai_state=down/ai_exit_rc_0` 并存，且 `pending`/`consumed` delegated continuation ids 继续全量重叠；这说明 continuation lane 仍被维护，但 consumed truth 依旧没有稳定绑定到当前 prompt cycle / 当前 stalled intake。`
    verdict: `keep-in-pre-brainstorm`
  - reviewer: `codex-explorer:Huygens`
    mode: `subagent-owner-boundary-review`
    summary: `独立只读扫描再次确认没有新的 canonical owner：`docs/recovery/**` 当前不存在，`docs/epics/**` 中最接近的相邻 issue 仍只覆盖 delegated handoff consumed/pending evidence、latest continuity consumption、worker active reentry 或 generic stalled-AI recovery；它们都没有接管“manager prompt 已吸收 continuation 但无新 continuity / handoff”的 acceptance boundary。`
    verdict: `keep-in-pre-brainstorm`
  - reviewer: `codex:gpt-5.4`
    mode: `worker-continuity-refresh`
    summary: `本轮最新 worker `live-status` 已把当前 lane 锚点滚动到 `.freely/run/prompt-20260324-021757.txt`，并确认 `pending_delegated_continuation_ids` 继续包含 `20260323-234407...`、`20260324-002656...` 与 `20260324-021757...`；但当前 `last_consumed_delegated_continuation_ids=none`、`last_consumed_delegated_continuation_at=unavailable`、`deep_refs.last_tool_session_id=unavailable`。这说明 prompt-level absorption 仍存在，但 consumed truth 在当前 lane 上并不稳定，因此 candidate 仍必须留在 pre-brainstorm。`
    verdict: `keep-in-pre-brainstorm`
  - reviewer: `codex-explorer:Kierkegaard`
    mode: `subagent-owner-scan`
    summary: `独立只读扫描确认不存在 superseding 的 issue/progress/recovery 路由：`docs/milestones.md` 仍将 `C-20260323-1705-A` 保留为 `candidate/in_pre_brainstorm`，当前仓库没有 `docs/recovery/**`，`docs/progress/**` 与最接近的 issue 只覆盖 pending/consumed evidence、worker launch linkage、active worker reentry 或 latest continuity consumption 等相邻边界，不接管当前 prompt-absorbed stall contract。`
    verdict: `keep-in-pre-brainstorm`
  - reviewer: `codex-explorer:James`
    mode: `subagent-owner-scan`
    summary: `最新只读 owner scan 再次确认不存在 superseding owner：`docs/milestones.md` 仍把 `C-20260323-1705-A` 保留在 `candidate/in_pre_brainstorm`，仓库中没有 `docs/recovery/**`，而最接近的 issue/progress 仍只覆盖 stalled AI + pending intake、worker active reentry 或 latest continuity consumption，不接管“manager prompt 已吸收 continuation 但无新 continuity / handoff”的 acceptance boundary。`
    verdict: `keep-in-pre-brainstorm`
  - reviewer: `codex:gpt-5.4`
    mode: `worker-continuity-refresh`
    summary: `本轮最新 worker `live-status` 已把 continuity 锚点滚动到 `.freely/run/prompt-20260324-022330.txt`，`deep_refs.last_tool_session_id=019d1f23-0255-7c83-b56f-cffe2c64ab40`，并再次暴露 `last_consumed_delegated_continuation_ids` 与 `pending_delegated_continuation_ids` 的 32/32 全量重叠，`last_consumed_delegated_continuation_at=2026-03-24T09:18:01Z`。这说明 consumed truth 又重新出现，但它既与 pending 并存，又在最近几轮出现过缺席，因此仍不是稳定的 prompt-cycle binding anchor。`
    verdict: `keep-in-pre-brainstorm`
- expected_outcome:
  - define a runtime-visible stall contract for `delegated continuation already absorbed into prompt`
  - trigger runtime-owned recovery when no new manager continuity / worker handoff is emitted in bounded time
  - preserve the older pending-intake stall contract as a separate signal
- decision_reason:
  - 这次 gap 已超出单条 cleanup lifecycle；它属于 Freely runtime control plane 的通用自治缺口。
  - 当前已有 runtime / skill / test 证据，但还缺少一轮真实 dogfood followthrough 来冻结边界，因此不应因为仓库里已经有补丁就直接提升到 IBM。
  - 与 `I-20260322-0445` 的边界仍然清楚：后者处理“已生成新 continuity / prompt set 但 worker 仍消费旧轮次”，当前候选处理的是“manager prompt 已吸收 delegated continuation，但没有继续产出新的 continuity / handoff”。
  - 当前仓库复核仍未发现 issue/progress/recovery 真源接管该候选；因此这轮只能补 continuity writeback，不能把 route_kind 提前改成 `ibm`、`dev_loop` 或 `recovery`。
  - 当前 runtime 已给出 prompt-level absorption proof，但 delegated continuation consumed truth 在当前 worker lane 上仍不稳定；它会在缺席与 `pending` / `consumed` 全量重叠之间摇摆，既没有稳定绑定到当前 prompt cycle / 当前 stalled intake，也没有形成独立于这种摇摆的 acceptance anchor，所以 promotion 后的 acceptance anchor 仍不稳定，candidate 继续保持 `needs_research`。
  - 当前 watchdog/runtime/tests 证明的是“prompt-level absorption 加 runtime state surface 足以触发 recovery”，不是“prompt-cycle binding 已经稳定到足以 materialize issue”；这两层证据不能混用。
- next_action:
  - 保持 active candidate；继续用真实 dogfood 验证 prompt-absorbed delegated continuation stall 是否能被 runtime recovery 稳定推进到 cleanup / retirement followthrough，然后再判断是 materialize 为独立 issue，还是吸收到更高层 stall/recovery issue 族。
  - 下一轮优先验证 runtime 能否在当前 `consumed` truth 摇摆的情况下，仍把 stalled intake 稳定绑定到当前 prompt cycle；若后续继续出现 `pending/consumed` 并存，也仍要明确哪一个 stalled delegated continuation 真的被本轮 prompt 吸收。若两条路径都做不到，至少冻结一个不依赖人工解释 prompt excerpt 的等价 proof。
  - 将当前 `fresh_with_handoff/context_compacted` 的 continuity 事实继续视为 supporting evidence：它证明 runtime 已因上下文压缩做过续接，但不证明当前 prompt cycle 对 stalled intake 的 binding 已稳定；因此后续仍要把续接事实与 prompt-cycle absorption proof 分开验收。
  - 在 manager/runtime cleanup 判断中，不再沿用“本树已被 develop 吸收、只剩 dirty writeback”的旧前提；当前 canonical writeback 已继续收敛为本分支上的最新 continuity anchor lineage，下一步应先把这些独有提交吸收到上游，再决定 retirement。
  - 若再次发生会话轮换或 `context_compacted`，先把最新 continuity 结论写回当前 pre-brainstorm canonical artifacts，再继续扩大实现或 cleanup 判断。
  - 当前最新 continuity 锚点已经滚动到 `.freely/run/prompt-20260324-022330.txt`；后续若再次轮换，优先沿这条 canonical writeback 线继续刷新 evidence，而不是切换 owner 或 loop。
  - delete / retirement gate 当前仍明确阻塞：只有在真实 dogfood 复现中固定 `current stalled intake id -> current prompt cycle -> consumed event anchor` 的 binding proof，并确认 recovery 继续推进到 followthrough 后，才允许重新判断 cleanup。
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
