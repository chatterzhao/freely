# Issue: cli-tui-human-interruption-input

- issue_id: `I-20260319-2315`
- title: CLI TUI interruption input box for Freely
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `cli-tui-human-interruption-input`
- issue-name: `cli-tui-human-interruption-input`
- verification_artifact_dir: `docs/B2-docs/human/cli-tui-human-interruption-input/code-reviews`
- source_candidate: `docs/B1-docs/raw-20260319T050000Z/candidates.md#c-20260319-2315-a`
- source_brainstorm: `docs/B1-docs/raw-20260319T050000Z/brainstorms.md`
- execution_base: `feature/cli-tui-input-interruption-20260319-2310`
- integration_target: `develop`
- depends_on: `docs/B2-docs/ibm/state-sync-and-session-evidence-governance/issues/state-sync-and-session-evidence-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 需要一个真正可用的 CLI 前台插话入口，但这个入口必须继续服从既有 human interruption 架构：

- 人类输入最终仍然进入 `.freely/intake/**`
- TUI 只是 `freely intake chat` / `freely intake status` / `freely status` 的 presentation shell
- 人类侧不直接 claim / resolve
- 中文输入与展示必须可用
- 输入框应支持多行内容，而不是只接受单行脚本式输入

## Scope

1. 在 `freely tui` 中提供可直接输入插话内容的 composer。
2. 支持中文和多行输入，避免把 TUI 退化成单行 shell prompt。
3. 保持 `channel=tui` 的 durable intake 语义不变。
4. 用脚本测试锁住 `freely tui --once` 的中文与多行提交行为。
5. 继续保持 TUI 仅作为输入与状态展示壳，不引入 manager claim/resolve 逻辑。

## Acceptance

- `freely tui --project <abs_path>` 会先渲染 dashboard，再接受多行插话输入。
- 用户输入的内容最终仍写入 `.freely/intake/**`。
- 中文与中英混排内容能在提交后被原样保留。
- `freely tui --once` 可以在非交互场景下提交同样的插话内容。
- TUI 不越权承担 claim / resolve / reaction 选择。

## Completion

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-chat-and-tui`

## Verification

- 已执行脚本级回归：
  - `bash docs/system/workspace/scripts/tests/test-freely-chat-and-tui`
- 回归覆盖：
  - `freely chat` durable intake
  - `freely tui --once` 中文提交
  - `freely tui --once` 多行输入提交
- 当前实现将 TUI composer 绑定到现有 intake chat 路径，没有引入第二套持久化协议。
