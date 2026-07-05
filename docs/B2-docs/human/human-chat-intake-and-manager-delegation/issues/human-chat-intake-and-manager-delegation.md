# Issue: human-chat-intake-and-manager-delegation

- issue_id: `I-20260319-1715`
- title: CLI-first human chat intake and manager delegation loop
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `human-chat-intake-and-manager-delegation`
- issue-name: `human-chat-intake-and-manager-delegation`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/human-chat-intake-and-manager-delegation/code-reviews`
- priority: P0
- source_candidate: `docs/B1-docs/raw-20260319-1715/candidates.md#c-20260319-1715-a`
- source_brainstorm: `docs/B1-docs/raw-20260319-1715/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/epics/workspace-routing-foundation/source-routing-and-derived-worktree-governance/issues/source-routing-and-derived-worktree-governance.md`
  - `docs/epics/workspace-routing-foundation/state-sync-and-session-evidence-governance/issues/state-sync-and-session-evidence-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 已经有 human chat intake 的最小闭环，但要真正“用 Freely 开发 Freely”，还必须把这条链变成正式、可恢复、可监督的 canonical issue：

- human chat 必须先进入 durable intake，而不是只存在于当前聊天线程
- manager 必须能 notice / claim / delegate，而不是仅仅“看过”
- specialized AI 必须产出 resolution artifact，并把 absorption target 写回 canonical pool
- `claim/resolve`、`skill:human-interruption-handling` 与 manager contract 必须共用同一套语义

## Scope

1. 保持 `freely intake chat/status/claim/resolve` 作为 CLI-first canonical surface。
2. 保持 manager 的 fixed reaction contract 与 specialized skill 分工。
3. 保持 `.freely/intake/**` 作为短期事件池，不把它膨胀成新的长期治理池。
4. 保持 discovery / continuation / control / noise 的 canonical 去向清晰可追踪。
5. 保持 issue / milestone / pre-brainstorm 之间的回写一致。

## Acceptance

- human chat 可以稳定写入 durable intake。
- manager 可以通过 intake queue 发现、claim 并委派处理。
- `skill:human-interruption-handling` 可以产出 resolution artifact 和 handoff。
- absorption target 必须被明确写回，并能追溯到原始 intake item。
- 相关 prompt、skill 和 runtime 表达保持一致，不再各说各话。

## Completion

- 本工位仅保留 human-chat canonical 文档物化与历史差异说明。
- `I-20260319-1715` 的正式完成态与 verification 真源位于 `feature/human-chat-intake-supervision-20260319-1030`。
- 本工位不得作为 `I-20260319-1715` 的独立 promote / merge 来源。

## Verification

- 本工位不再承载独立 verification。
- formal verification review 已落在 `feature/human-chat-intake-supervision-20260319-1030`。
- 本工位只允许保留“哪些差异仍需人工摘取”的 companion 说明，不重复宣称运行时或跨能力测试证据。

## Companion Status

- 当前 canonical worktree 显式挂起：不得作为 `I-20260319-1715` 的独立 promote / merge 来源。
- 挂起原因：本工位只重复物化了 human-chat issue 文档包，没有新增独立实现或 verification 证据；正式 verification review 已落在 `feature/human-chat-intake-supervision-20260319-1030`，而本工位的祖先历史还混入了 `CLI TUI` 与 `project-resolution` 能力线。
- next_action: 仅在人工比对后，把本工位里真正独有且仍然属于 human-chat 的文档差异摘取到 `feature/human-chat-intake-supervision-20260319-1030`；不要整支合并，也不要把 `CLI TUI` / `project-resolution` 相关历史当成本 issue 的收口依据。
- 若没有需要保留的独有人类插话文档差异，则直接退休本工位；human-chat 的 promote / cleanup 只在主收口分支完成。
