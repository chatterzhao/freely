# Candidates - 20260319-0018--token-efficient-session-continuity-and-rotation

## Context
- Source brainstorm: ./brainstorms.md
- Status: in_research

## Candidates

### C-20260319-0018-A
- title: token-efficient continuity before session rotation
- problem: Freely 当前在 context pressure 下已经能 `fresh_with_handoff`，但缺少“先主动写 continuity，再低 token 轮换”的统一策略。
- why_now: 这是把当前 `context_ratio` / `fresh_with_handoff` / manager continuity 真正融合成高质量自治链的前提。
- acceptance_hint:
  - `context warn` 先推动 AI 更新 phase-appropriate continuity artifact
  - `fresh_with_handoff` 只在 rotate 条件满足时触发
  - handoff 明确区分 continuity 主体与旧会话证据引用
  - 正式口径明确：该能力是 `auto-loop` 的上下文治理子控制面，而不是新的平行 loop
  - 形成一份 `trigger -> owner -> artifact -> action -> fallback` 统一矩阵
- priority: P0
- status: promoted
- promoted_issue_path: `docs/B2-docs/ibm/token-efficient-session-continuity-and-rotation-governance/issues/token-efficient-session-continuity-and-rotation-governance.md`
- legacy_id_mapping: I-20260319-0018  # 历史遗留的 issue id
- milestone: `M-20260306-workspace-routing-foundation`
- session_refs:
  - `feature/token-efficient-session-continuity-20260319`

### C-20260319-0018-B
- title: session evidence references as fallback, not prompt payload
- problem: 若把整份旧 `jsonl` / log 直接重喂，会浪费 token；但完全丢掉旧证据又会降低恢复质量。
- why_now: 这是“节省 token”和“保留恢复证据”之间的关键平衡点。
- acceptance_hint:
  - handoff 始终保留 `previous_tool_session_id` / `previous_tool_jsonl_path` / `previous_cycle_log`
  - 新会话默认不全文读取这些文件
  - 仅在 continuity/handoff 无法覆盖时，按需读取旧证据片段
  - 进程重启与账号恢复 owner 仍归 runtime/watchdog，旧证据引用只负责上下文续接
- priority: P1
- status: proposed
- next_action: 调研 token 高效会话旋转的具体实现方案
- revisit_trigger: 当有新的 token 效率需求时
- promoted_issue_path: `docs/B2-docs/ibm/token-efficient-session-continuity-and-rotation-governance/issues/token-efficient-session-continuity-and-rotation-governance.md`
- milestone: `M-20260306-workspace-routing-foundation`
- session_refs:
  - `feature/token-efficient-session-continuity-20260319`
