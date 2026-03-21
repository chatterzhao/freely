# Issue: explicit-session-addressed-resume-governance

- issue_id: `I-20260321-2010`
- title: Explicit session-addressed resume governance
- phase_state: `in_ibm`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `explicit-session-addressed-resume-governance`
- issue-name: `explicit-session-addressed-resume-governance`
- source_candidate: `docs/pre-brainstorms/20260321-2010--explicit-session-addressed-resume-over-last-and-pty/candidates.md#c-20260321-2010-a`
- source_brainstorm: `docs/pre-brainstorms/20260321-2010--explicit-session-addressed-resume-over-last-and-pty/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `docs/epics/workspace-routing-foundation/token-efficient-session-continuity-and-rotation-governance/issues/token-efficient-session-continuity-and-rotation-governance.md`, `docs/epics/workspace-routing-foundation/state-sync-and-session-evidence-governance/issues/state-sync-and-session-evidence-governance.md`
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://to-be-recorded-in-dev-loop", role: "author"}]

## Why

Freely 现在对不同工具的会话续接模型不一致：

- `cc` 已经使用显式 `--session-id`
- `codex` 仍默认使用 `resume --last`
- `iflow` / `kiro-cli` 也没有显式 workcell-scoped session addressing

在多进程并行下，`--last` 与弱 resume 语义都不足以表达“当前 workcell 应接哪一个会话”。

与此同时，本机研究已确认：

- `codex exec resume [SESSION_ID] [PROMPT]`

是正式 CLI primitive，并支持从 stdin 读取续发 prompt。

因此 Freely 应把：

- `explicit session-addressed resume`

定义为 canonical continuity model，而不是把：

- `resume --last`
- PTY 输入框注入

当作默认 supervisor/runtime 路径。

## Scope

1. 明确 `process alive` 与 `session resumable` 的区别。
2. 明确 Freely 的 canonical continuity model 是 `tool + explicit session id`。
3. 审视 `codex` 当前 `--last` 的风险并定义替代 contract。
4. 盘点 `iflow` / `kiro-cli` 的当前 resume 语义是否满足多进程并行。
5. 将 PTY 注入降级为 fallback，而不是 canonical product path。

## Acceptance

- truth sources 明确写出 canonical continuity model = explicit session-addressed resume
- `codex` 的默认并发 resume 不再依赖 `--last`
- `cc` 的现有显式 `session-id` 模式被记录为正向参照
- `iflow` / `kiro-cli` 当前 contract 被明确标注为：
  - 已满足
  - 或暂未满足、需后续 issue
- PTY 注入仅作为 fallback 被说明

## Completion

- `docs/system/workspace/tools.md`
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/runtime/tool-launchers.sh`
- `docs/epics/workspace-routing-foundation/explicit-session-addressed-resume-governance/code-reviews/20260321-explicit-session-addressed-resume-verification.md`

## Verification

- `./bin/governance-check`
- runtime continuity tests to be selected in IBM

## Next

- 先完成 IBM，冻结工具差异、truth-source 落点、runtime 改动面和最小验证面，再进入 dev-loop。
