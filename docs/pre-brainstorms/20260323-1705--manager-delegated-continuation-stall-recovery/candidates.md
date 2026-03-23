# 候选：manager-delegated-continuation-stall-recovery

- id: `C-20260323-1705-A`
- title: Detect and recover manager delegated continuation stalls after prompt absorption
- source_brainstorm: `docs/pre-brainstorms/20260323-1705--manager-delegated-continuation-stall-recovery/brainstorms.md`
- status: `needs_research`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `pending://manager-delegated-continuation-stall-recovery-materialization`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- why_now:
  - 真实 dogfood 已复现 `cleanup continuation` 进入 manager prompt 后，AI 假活但不产出 continuity / handoff 的断点
  - 现有 runtime stall gate 只看 `pending intake > cycle log`，不足以覆盖 prompt absorption 之后的假活
- expected_outcome:
  - define a runtime-visible stall contract for `delegated continuation already absorbed into prompt`
  - trigger runtime-owned recovery when no new manager continuity / worker handoff is emitted in bounded time
  - preserve the older pending-intake stall contract as a separate signal
- decision_reason:
  - 这次 gap 已超出单条 cleanup lifecycle；它属于 Freely runtime control plane 的通用自治缺口
  - 但边界还需要继续验证是否应 materialize 成独立 issue，还是吸收到现有 stall/recovery issue 族
- next_action:
  - 先让 runtime 支持 prompt-absorbed delegated continuation stall recovery，并继续真实 dogfood 验证从 cleanup 到 retirement 的 followthrough
- revisit_trigger:
  - 若后续再次出现 manager prompt 吸收 continuation 后无新 continuity / handoff 的假活
  - 或当前补丁稳定后，需要把该边界冻结成独立 issue contract
