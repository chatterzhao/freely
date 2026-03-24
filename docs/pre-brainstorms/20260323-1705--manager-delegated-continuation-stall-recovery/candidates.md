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
    session_id: `current-thread`
    jsonl_path: `unavailable://fresh-session-thread-id-not-exposed`
    role: `author-continuation`
- why_now:
  - 真实 dogfood 已复现 `cleanup continuation` 进入 manager prompt 后，AI 假活但不产出 continuity / handoff 的断点。
  - 当前 `live-status` 已能稳定暴露 `current_prompt_has_delegated_continuation=1`、`latest_manager_worker_prompts_generated=none` 与 `last_consumed_delegated_continuation_ids=none`，说明这不是纯会话内现象，而是 runtime control plane 可观测的 gap。
- acceptance_criteria:
  - 明确区分当前候选与 `pending intake > cycle log`、latest continuity consumption、worker active reentry 这几条相邻治理 issue 的边界。
  - 冻结这条候选的最小 contract：`delegated continuation` 已进入 manager prompt，但在有界时间内没有新的 manager continuity / worker handoff 产出。
  - 保持 `docs/pre-brainstorms/**` 与 `docs/milestones.md` 对 candidate 状态、下一跳和重判条件的一致性，不让该研究项从扫描面消失。
- promotion_gate:
  - 至少再有一轮真实 dogfood 证明这条 stall contract 能稳定解释 cleanup / retirement followthrough 中的假活，而不是一次性偶发现象。
  - 确认这条 contract 不会被更高层的 manager recovery / stall issue 自然吸收，或者已经具备清晰的 issue-owned 承接位置。
  - 若准备 promotion，需要至少一轮独立 acceptance review，而不是仅凭当前 worktree 的自我判断直接 materialize。
- open_questions:
  - 这条 contract 最终应独立 materialize，还是并入更高层的 manager recovery issue family？
  - 真实 cleanup / retirement followthrough 是否还会再次命中同一类“prompt 已吸收 continuation 但无新 continuity / handoff”的假活？
  - `live-status` 当前暴露的 generated/consumed 信号是否已足以成为后续 issue 的 acceptance anchor？
- acceptance_reviews:
  - reviewer: `codex-explorer:Cicero`
    mode: `subagent-review`
    summary: `独立复核确认当前 evidence 只足以支撑继续留在 pre_brainstorm：promotion_gate 仍要求真实 dogfood followthrough，open_questions 尚未收口，当前 dirty delta 是 canonical candidate writeback，不应丢弃。`
    verdict: `keep-in-pre-brainstorm`
- expected_outcome:
  - define a runtime-visible stall contract for `delegated continuation already absorbed into prompt`
  - trigger runtime-owned recovery when no new manager continuity / worker handoff is emitted in bounded time
  - preserve the older pending-intake stall contract as a separate signal
- decision_reason:
  - 这次 gap 已超出单条 cleanup lifecycle；它属于 Freely runtime control plane 的通用自治缺口。
  - 当前已有 runtime / skill / test 证据，但还缺少一轮真实 dogfood followthrough 来冻结边界，因此不应因为仓库里已经有补丁就直接提升到 IBM。
  - 与 `I-20260322-0445` 的边界仍然清楚：后者处理“已生成新 continuity / prompt set 但 worker 仍消费旧轮次”，当前候选处理的是“manager prompt 已吸收 delegated continuation，但没有继续产出新的 continuity / handoff”。
- next_action:
  - 保持 active candidate；继续用真实 dogfood 验证 prompt-absorbed delegated continuation stall 是否能被 runtime recovery 稳定推进到 cleanup / retirement followthrough，然后再判断是 materialize 为独立 issue，还是吸收到更高层 stall/recovery issue 族。
- revisit_trigger:
  - 当再次复现 manager prompt 已吸收 continuation 但无新 continuity / handoff 的假活时，重新进入 materialization 判断。
  - 当当前 runtime 补丁在真实 followthrough 中验证稳定，且边界已可冻结成独立 issue contract 时，重新进入 materialization 判断。
