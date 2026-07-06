# Issue: token-efficient session continuity and rotation governance

- issue_id: `I-20260319-0018`
- title: Token-efficient session continuity and rotation governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `token-efficient-session-continuity-and-rotation-governance`
- issue-name: `token-efficient-session-continuity-and-rotation-governance`
- verification_artifact_dir: docs/B2-docs/ibm/token-efficient-session-continuity-and-rotation-governance/raw-20260319-0018/code-reviews
- priority: P0
- source_candidate: `docs/B1-docs/raw-20260319T050000Z/candidates.md#c-20260319-0018-a`
- source_brainstorm: `docs/B1-docs/raw-20260319T050000Z/brainstorms.md`
- source_candidate: `docs/B1-docs/raw-20260319T050000Z/candidates.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/B2-docs/ibm/session-lifecycle-rotation-and-handoff-governance/issues/session-lifecycle-rotation-and-handoff-governance.md`
  - `docs/B2-docs/ibm/manager-self-supervision-and-autonomous-recovery/issues/manager-self-supervision-and-autonomous-recovery.md`
  - `docs/B2-docs/ibm/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}
  - {tool: codex, session_id: "019d05d3-be75-7e42-bbd1-aa2b29e1bad0", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/19/rollout-2026-03-19T04-20-56-019d05d3-be75-7e42-bbd1-aa2b29e1bad0.jsonl", role: "fresh_with_handoff_source"}

## Why

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

## Scope

1. 定义 `context warn` 与 `context rotate` 的触发分层和 owner。
2. 明确 doc-loop / dev-loop / recovery 的 continuity artifact 默认落点。
3. 明确 manager continuity 与 worker continuity 的最小内容结构。
4. 规定旧 `jsonl` / cycle log 作为 fallback evidence refs 的默认使用方式。
5. 对齐 `continuity-watchdog`、`watchdog-control-plane`、`recovery-subagent-governance` 与 runtime handoff 的边界。
6. 固定“官方压缩优先”的后续演进规则。

## Acceptance

- `context warn` 与 `context rotate` 有清晰分层，不再混成“任何预警都立即新开会话”。
- worker continuity 与 manager continuity 的目标对象、内容结构和默认落点被正式写清。
- handoff 默认只保留必要结构化摘要与旧证据路径，不把整份旧 `jsonl` / `log` 当作主 prompt 内容。
- 若官方未来公开支持非交互压缩/总结参数，Freely 的正式口径明确要求优先评估并重构采用官方能力，而不是长期固化外部 fallback。
- 统一触发矩阵被正式写入实现参考，后续 runtime / prompt / watchdog 改动必须遵循同一矩阵。
- `continuity watchdog` 作为独立 skill 存在，并作为 `watchdog-control-plane` 的 continuity 子模块被角色与恢复流程引用。

## Notes

- 当前这条 issue 优先处理治理与控制面口径，不要求立即引入新的 UI。
- 这条 issue 不是否定现有 `fresh_with_handoff`；它的目标是把现有能力和 continuity / session evidence 融合成更高质量、低 token 的自动策略。
- 当前已物化落点：
  - `docs/system/workspace/skills/continuity-watchdog/SKILL.md`
  - `docs/system/workspace/skills/watchdog-control-plane/SKILL.md`
  - `docs/system/workspace/skills/recovery-subagent-governance/SKILL.md`

## Implementation References

- `docs/B2-docs/ibm/token-efficient-session-continuity-and-rotation-governance/brainstorms/b-token-efficient-session-continuity-and-rotation-governance.md`
- `docs/B2-docs/ibm/token-efficient-session-continuity-and-rotation-governance/prd.md`
- `docs/B2-docs/ibm/token-efficient-session-continuity-and-rotation-governance/pre-tests.md`
- `docs/B2-docs/ibm/token-efficient-session-continuity-and-rotation-governance/tasks.md`
- `docs/B2-docs/ibm/token-efficient-session-continuity-and-rotation-governance/references/trigger-owner-matrix.md`
- `docs/system/workspace/skills/continuity-watchdog/SKILL.md`
- `docs/system/workspace/skills/watchdog-control-plane/SKILL.md`
- `docs/system/workspace/skills/recovery-subagent-governance/SKILL.md`

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-session-rotation`
- `./bin/governance-check`
- review of `docs/system/workspace/tools.md`
- review of `docs/system/workspace/skills/continuity-watchdog/SKILL.md`
- review of `docs/system/workspace/skills/watchdog-control-plane/SKILL.md`
- review of `docs/system/workspace/skills/recovery-subagent-governance/SKILL.md`
- review of `docs/B2-docs/ibm/token-efficient-session-continuity-and-rotation-governance/references/trigger-owner-matrix.md`

## Closure Judgment

- 当前 issue 不再停留在 `done_ibm`：trigger matrix 已被 `continuity-watchdog`、`watchdog-control-plane`、`recovery-subagent-governance`、`tools.md` 与 `runtime/freely` 共同消费，warn/rotate/fresh-with-handoff 边界已成为 canonical contract。
- `test-freely-session-rotation` 已覆盖 context-compaction、resume evidence 缺失、高 context usage、manager continuity target、rate-limit defer-to-watchdog 与 route-only second-hop recovery；当前不存在要求继续停在 doc-loop 的缺口。
- manager continuity 与 worker continuity 的目标对象、以及旧 session/jsonl/log 仅作 fallback evidence ref 的规则，已被正式写进 trigger matrix 与 continuity skill；因此本 issue 可以直接收口为 `completed`。

## Ready For Dev

当前 IBM 已补齐正式 issue-bound brainstorm、PRD、pre-tests、tasks 与 trigger matrix 引用，足以驱动后续实现收口：

1. 把 `runtime/freely`、prompt 组装与相关 skill 的 continuity 触发边界对齐到统一矩阵。
2. 确保 manager/worker continuity 默认只带最小语义与旧证据路径引用。
3. 把“官方压缩优先”的规则留在实现与后续 review 中持续校验。

## Next

- 本 issue 已完成；后续若要采用官方非交互 compaction 能力，或继续演进 continuity payload / trigger schema，应作为新的 runtime/dev lifecycle 承接。
