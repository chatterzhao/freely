# IBM Brainstorm: explicit-session-addressed-resume-governance

## Core Question

Freely 是否应把会话续接默认建模成“最近一个会话”，还是“当前 workcell 指定的那个会话”？

## Answer

默认必须是后者：

- 当前 workcell 指定的那个会话

否则并发时：

- `--last`
- 弱 resume

都可能把新进程接到错误 session 上。

## Tool Interpretation

- `cc` 已经提供正向样本：每个 workcell 一个 `session-id`
- `codex` 有正式 `exec resume [SESSION_ID] [PROMPT]`
- `iflow` / `kiro-cli` 需要单独判定其 continuation contract 是否足够强

## Non-goal

本 issue 不把“向旧 TTY 直接写输入”发展为 canonical supervisor path。
