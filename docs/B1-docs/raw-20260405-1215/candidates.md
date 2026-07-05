# Candidates - 20260405-1215--runtime-audio-notifier-and-sound-semantics

## C-20260405-1215-A

- candidate_format_version: `v2`
- title: Runtime audio notifier and sound semantics
- status: `promoted`
- source_brainstorm: `docs/B1-docs/raw-20260405-1215/brainstorms.md`
- problem: Freely 缺少稳定的自治运行时声音语义系统，无法让用户通过不同提示音区分 manager / worker 的开始、结束、失败、阻塞与 interruption。
- why_now:
  - 用户明确要求“任务执行完有语音提醒”，且 manager / worker / started / completed 应有不同声音
  - 当前 runtime 已具备 event bridge 和 signal 提取基础，但还没有 canonical sound event 与 notifier 层
  - 若继续把这类能力塞进 watchdog 或 `runtime/freely`，会进一步加重 owner 混叠
- acceptance_criteria:
  - 明确 `watchdog`、`tool event source`、`event router`、`audio notifier` 的 owner boundary
  - 定义第一轮 canonical runtime sound events
  - 定义第一轮声音语义矩阵，至少覆盖 manager / worker started / completed
  - 第一轮只实现标准路径：打包音频资源 + Tauri/UI 播放，不实现 OS fallback
  - 明确 Codex/Responses 一类支持原生 lifecycle event 的路径应优先消费 native notice/event，而不是监听自然语言全文
- promotion_gate:
  - owner boundary 明确，不把 notifier 混回 watchdog
  - 第一轮标准路径边界明确，不把 fallback 一起塞进同一 owner
  - 至少冻结 manager / worker / started / completed 的 event 名称与音频策略
- open_questions:
  - 音频资源应放在 Tauri bundle resources 还是前端静态资源
  - 第一轮是否包含 `blocked` / `failed` / `interruption`
  - 现有 runtime event 面是否足够承载声音事件，还是要先补事件桥字段
  - 其他工具的原生 notice/event 是否需要同轮一并审计
- decision_reason:
  - 问题边界已经清晰到足以形成 capability owner，但第一轮仍需先收口标准路径和 contract
  - 当前已有 evidence/source 基础，适合先做最小自治声音能力，而不是全量跨工具 fallback
- next_action: materialize 一个 narrow owner，先冻结 canonical event contract、sound policy 与 Tauri 标准播放路径；manager / worker started/completed 为首批实现目标。
- revisit_trigger: 当标准路径落地后，需要扩展到 blocked/failed/interruption 全矩阵、其他工具原生 notice 审计，或 CLI/headless fallback 时。
- promoted_issue_path: `docs/epics/workspace-routing-foundation/runtime-audio-notifier-and-sound-semantics-governance/issues/runtime-audio-notifier-and-sound-semantics-governance.md`
- milestone: `M-20260306-workspace-routing-foundation`
- acceptance_reviews:
  - reviewer: `subagent:Turing`
    verdict: `promote`
    note: `Bind this as a new sibling owner under workspace-routing-foundation; closest upstream lineage is application-native runtime observation, but watchdog/supervision owners should not absorb notifier semantics.`
  - reviewer: `subagent:Zeno`
    verdict: `promote`
    note: `Use the existing Tauri bridge as the canonical seam and land audio through a dedicated frontend notifier hook rather than watchdog or transcript listeners.`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
