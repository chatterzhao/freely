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

- `cc` 已经提供正向样本：每个 workcell 一个显式 `session-id`
- `codex` 有正式 `exec resume [SESSION_ID] [PROMPT]`，`--last` 只是省略 `SESSION_ID` 时的 fallback
- `iflow` 当前 CLI 同时存在：
  - `-c/--continue`：续最近一次对话
  - `-r/--resume`：按特定 session file 恢复
- `kiro-cli` 当前只暴露：
  - `--resume`：恢复当前目录最近一次会话
  - `--resume-picker`：交互式选择
  - `--list-sessions`：列出本目录会话
- `opencode` 当前不在 Freely runtime surface 内，本 issue 只记录为后续工具接入时需遵守相同 continuity contract

## Non-goal

本 issue 不把“向旧 TTY 直接写输入”发展为 canonical supervisor path。

## Decision

Freely 的 canonical continuity model 固定为：

- `tool + explicit session identifier + workcell ownership + evidence refs`

对应含义：

- `process alive` 只回答“原进程是否还活着”
- `session resumable` 只回答“该 workcell 是否还能明确接回同一个会话”
- runtime/supervisor 的默认路径应是“起新进程并显式续接指定会话”，而不是：
  - `resume --last`
  - 旧 PTY 注入
  - 目录级最近会话猜测

## Open Questions That Do Not Block Dev

1. `iflow -r/--resume` 最终应由 Freely 传 session file、session id，还是两者都保留为 evidence model。
2. `kiro-cli` 若暂缺显式 session-id 恢复，Freely 是先把它标记为 weak continuation contract，还是增加额外 session discovery/selection bridge。
3. `PTY input injection` 是否保留为仅限同一 TTY 会话仍存活时的人工/即时 fallback，而不进入 supervisor 默认重入面。

## Dev Writeback

- `cc` 的 per-workcell `--session-id` 已被抽象成和 `codex` 同构的 runtime resume-target helper，而不是继续散落在各分支里单独判断。
- delegated continuation 现在会写回 worker-scoped `SESSION_REFS`，把抽象 continuation 收敛到具体 workcell resume target。
- local continuation re-entry 现阶段采用：
  - 优先 `TERM`
  - 超时再 hard kill fallback
  - 同时落 `preemption-state.env`
