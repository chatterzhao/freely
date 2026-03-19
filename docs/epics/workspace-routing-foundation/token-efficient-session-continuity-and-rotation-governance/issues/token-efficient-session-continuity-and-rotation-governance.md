# Issue: token-efficient session continuity and rotation governance

## Metadata
- issue_id: `I-20260319-0018`
- milestone: `M-20260306-workspace-routing-foundation`
- phase_state: `in_ibm`
- priority: P0
- depends_on:
  - `docs/epics/workspace-routing-foundation/session-lifecycle-rotation-and-handoff-governance/issues/session-lifecycle-rotation-and-handoff-governance.md`
  - `docs/epics/workspace-routing-foundation/manager-self-supervision-and-autonomous-recovery/issues/manager-self-supervision-and-autonomous-recovery.md`
  - `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
- source_brainstorm: `docs/pre-brainstorms/20260319-0018--token-efficient-session-continuity-and-rotation/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-0018--token-efficient-session-continuity-and-rotation/candidates.md`

## Problem

Freely 现在已经有：
- `context_ratio` 预警
- `context compacted` 触发
- `fresh_with_handoff`
- session handoff
- manager bootstrap handoff

但这些能力还没有收敛成“自动、低 token、统一边界”的上下文管理控制面。

当前缺口：
1. `context warn` 与 `fresh_with_handoff` 之间缺少统一的主动 continuity 策略。
2. 旧会话证据（`session_id` / `jsonl_path` / `cycle_log`）还没有形成“按需引用而不是默认重喂”的正式规则。
3. manager continuity 与 worker continuity 的目标对象不同，但当前还没有一套明确的正式口径。
4. 在官方未公开非交互压缩参数前，Freely 需要有明确 fallback；若官方未来支持，应优先重构采用。

## Why Now

Freely 已经把 manager / worker / watchdog / worktree hygiene / checkpoint governance 接入 `develop`。如果上下文管理不统一，主管与 worker 的长会话质量仍会退化，并继续依赖人工提醒“先写进度再换会话”。

## Desired Outcome

把 Freely 的上下文管理收敛成一条自动能力链：

1. `context warn`
   - 当前 AI 先更新 phase-appropriate continuity artifact
   - 不立即强制重启

2. `context rotate`
   - runtime 触发 `fresh_with_handoff`
   - 新会话默认消费 continuity artifact + handoff

3. `deep recovery`
   - 新会话保留对旧 `jsonl` / log 的路径引用
   - 仅在必要时按需读取，不把整份旧证据塞进 prompt

4. `AI powerless`
   - watchdog 只负责恢复，不负责替 AI 做语义压缩

并形成统一触发矩阵，至少明确：

| trigger | owner | artifact | action | fallback |
| --- | --- | --- | --- | --- |
| `context warn`, 当前 AI 仍健康 | current worker/manager session | phase-appropriate continuity artifact | 先更新 continuity，不立刻 rotate | 若会话随后自然结束，则 handoff 仅引用 continuity 与旧证据路径 |
| `context rotate` / `context compacted` / `context_ratio >= rotate` | worktree runtime | session handoff + continuity | `fresh_with_handoff` | 新会话默认只消费 continuity + handoff，旧 `jsonl/log` 只按需读取 |
| AI 已退出但 auto-loop runtime 仍在 | worktree runtime | session-state + handoff + `previous_*_path` | 拉起新进程，选择 `resume` 或 `fresh_with_handoff` | 若 resume 证据不足，退化到 `fresh_with_handoff` |
| manager / worker runtime 不存在 | outer watchdog / ensure-manager | manager bootstrap handoff | 先拉起主管，不做语义压缩 | 主管再读取 fleet 并决定哪些 worker 需恢复 |
| global account/service unavailable | global watchdog | account recovery state + manager bootstrap handoff | 切到真实可用账号，或选最早恢复账号并等待 | 账号恢复后再拉起主管 |

## Acceptance

- `context warn` 与 `context rotate` 有清晰分层，不再混成“任何预警都立即新开会话”。
- worker continuity 与 manager continuity 的目标对象、内容结构和默认落点被正式写清。
- handoff 默认只保留必要结构化摘要与旧证据路径，不把整份旧 `jsonl` / log` 当作主 prompt 内容。
- 若官方未来公开支持非交互压缩/总结参数，Freely 的正式口径明确要求优先评估并重构采用官方能力，而不是长期固化外部 fallback。
- 统一触发矩阵被正式写入实现参考，后续 runtime / prompt / watchdog 改动必须遵循同一矩阵。

## Notes

- 当前这条 issue 优先处理治理与控制面口径，不要求立即引入新的 UI。
- 这条 issue 不是否定现有 `fresh_with_handoff`；它的目标是把现有能力和 continuity / session evidence 融合成更高质量、低 token 的自动策略。
