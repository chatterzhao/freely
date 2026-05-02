# Candidates - 20260319-2315--cli-tui-human-interruption-input

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260319-2315-A
- title: CLI TUI interruption input box for Freely
- problem: Freely 已经有 human interruption 的 CLI-first intake 链，但真实人类入口仍偏脚本化；缺少一个启动即有输入框、输入即成为 interruption、且支持中文的 TUI 前端，导致“插话”能力还不够可用。
- why_now: 如果要让接下来的对话真正进入“插话模式”，就必须先给人一个稳定前台入口，而不是继续依赖手动拼 `freely intake chat` 命令。
- acceptance_hint:
- 明确 TUI 是 `freely intake chat` / `freely intake status` / `freely baseline-status` 的 presentation shell，而不是第二套入口系统
  - 明确第一版只做输入与状态展示，不做人类侧 claim / resolve
  - 明确底部输入框是第一优先级能力，启动后默认聚焦
  - 明确第一版至少支持 UTF-8 中文输入、全角显示和多行编辑
  - 明确输入提交后必须走现有 `.freely/intake/**` durable intake，而不是直接注入 AI 会话
  - 明确第一版的最小布局：顶部状态条、中间 intake/resolution/status 区、底部输入框
  - 明确提交交互与换行交互，避免输入框不可用
  - 明确 TUI 与 manager contract 的边界，避免越权处理 reaction / absorption
- priority: P0
- status: promoted
- decision_reason: 这条需求已经在 Freely runtime 中 materialize 为 `freely tui`，并补齐了中文/多行提交的脚本回归；现在应以正式 issue 记录完成态，而不是继续留在 research 状态。
- promoted_issue_path: `docs/epics/workspace-routing-foundation/cli-tui-human-interruption-input/issues/cli-tui-human-interruption-input.md`
- legacy_id_mapping: I-20260319-2315  # 历史遗留的 issue id
- milestone: `M-20260306-workspace-routing-foundation`
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
