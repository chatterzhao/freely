# PRD: explicit-session-addressed-resume-governance

## Goal

让 Freely 的多进程 continuity 以显式会话寻址为基础，而不是依赖 `--last` 或旧终端输入框。

## Why Now

- 当前 `cc` 已经采用 workcell-scoped `--session-id`，但 `codex` 仍默认走 `resume --last`
- 当前 runtime 对 `iflow` / `kiro-cli` 也仍偏向“最近会话”或弱 continuation 语义
- 多 worktree / 多 worker 并行时，`--last` 与目录级最近会话都不足以表达“当前 workcell 应接回哪一个 session”
- 本机已确认 `codex exec resume [SESSION_ID] [PROMPT]` 是正式 CLI primitive，并支持 stdin prompt，因此替代路径已经成熟
- 当前 supervisor/worker handoff 还主要是 restart point / ownership 语义，尚未稳定表达“把哪一个 session target 交给哪一个 worker”
- 当前 runtime 若靠直接杀进程触发下一轮，存在未落盘内容丢失风险

## Product Surface

- `docs/system/workspace/tools.md`
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/runtime/tool-launchers.sh`
- `docs/system/workspace/scripts/tests/test-monitor-ai-cli-codex-args`
- 与 continuity / session evidence 相关的 runtime tests

## Non-Goals

- 不把 PTY 输入注入升级成默认 supervisor/runtime 重入模型
- 不在本 issue 内完成所有工具的完整接入重构；只冻结 canonical contract 与当前最小实现边界
- 不把 `process alive` 和 `session resumable` 混写成同一个状态
- 不扩展到新的 AI 工具接入，只要求未来新工具遵守同一 continuity contract

## Non-Negotiables

- canonical continuity model 必须是 `tool + explicit session identifier`
- `resume --last` 只能作为人工/单链路 fallback，不得继续作为 Freely 默认并发 resume 路径
- `session evidence` 至少要能追溯 `tool + session_id + jsonl/rollout path + role`，并尽量保留 `branch/worktree`
- delegated handoff 若要继续当前 worker，必须能收敛到明确的 worker-scoped resume target
- continuity contract 必须定义 graceful preemption 优先，hard kill 只作 fallback
- `progress` 仍只服务 dev-loop；本轮 IBM 不伪造 progress
- PTY 注入最多保留为 fallback，不得与 canonical path 混淆

## Context Pack

- 当前 `cc` / `cc-use-codex-cli` 已通过 `--session-id <uuid>` 维持 workcell continuity
- 当前 `codex` runtime 仍使用 `codex exec resume --last`
- 本机 `codex exec resume --help` 明确支持：
  - `[SESSION_ID]`
  - `[PROMPT]`
  - `PROMPT=-` 从 stdin 读取
- 本机 `iflow --help` 明确支持：
  - `-c/--continue` 续最近会话
  - `-r/--resume` 从特定 session file 恢复
- 本机 `kiro-cli chat --help` 明确支持：
  - `--resume` 恢复当前目录最近会话
  - `--resume-picker` 交互式选择
  - `--list-sessions`
- `opencode` 当前仅是研究候选，不在 Freely runtime surface 内

## Decomposition Tree

1. continuity truth-source freeze
   - 定义 canonical continuity model
   - 区分 `process alive` 与 `session resumable`
2. tool contract matrix
   - `cc` 作为显式 session-addressed 正向基线
   - `codex` 从 `--last` 迁移到显式 session id
   - `iflow` / `kiro-cli` 标注当前 contract 强弱与后续缺口
3. runtime materialization
  - `freely` 保存并传递显式 resume target
  - `tool-launchers.sh` 改为按 tool contract 组装 resume 命令
  - delegated continuation 需要能把 handoff 交给具体 worker session
  - 若必须打断当前进程，优先保留 checkpoint/flush evidence
4. verification
   - 覆盖 codex 参数拼装
   - 覆盖 continuity 证据和弱 contract 判定不被误写成强保证

## Prototype Path

最小原型先只收敛 `codex`：

1. runtime 能从现有 session evidence 中解析并保存 Codex session id
2. `tool-launchers.sh` 用 `codex exec resume <SESSION_ID> -` 取代 `--last`
3. 测试明确失败于缺失会话 id，而不是悄悄退回 `--last`

这条原型跑通后，再把同一 contract 写回 truth sources，并对 `iflow` / `kiro-cli` 给出治理判定。

## Eval Plan

成功：

- `tools.md`、lifecycle、issue 文档一致声明 canonical continuity model = explicit session-addressed resume
- `codex` 默认 resume 路径不再依赖 `--last`
- `cc` 继续作为显式 session-id 正向样本
- `iflow` / `kiro-cli` 被明确归类为“已满足”或“当前仅弱 contract，需后续增强”
- PTY 注入仅保留 fallback 语义

失败：

- truth sources 仍同时把 `--last` 和显式 session-id 当成等价默认方案
- runtime 仍在无 session target 时静默退回 `--last`
- `process alive` / `session resumable` / `resume target missing` 混成同一类判断

不可接受退化：

- supervisor 继续默认向旧 PTY 写输入
- 在多 worker 并行时使用目录级“最近一个”会话冒充 workcell continuity

## Execution Slices

### Slice A: contract and truth-source alignment

- 更新 `tools.md`
- 更新 `three-loop-capability-lifecycle.md`
- 固定 `codex`、`cc`、`iflow`、`kiro-cli` 的 contract 解释

### Slice B: codex runtime resume migration

- 在 runtime state / evidence 中明确 Codex resume target
- `tool-launchers.sh` 改为显式 `SESSION_ID`
- 缺失 resume target 时给出明确治理信号，而非继续 `--last`

### Slice C: weak-contract tool handling

- 对 `iflow` 标注当前可用 `session file` 级恢复，但尚未完全由 Freely workcell contract 物化
- 对 `kiro-cli` 标注当前只有目录级 recent-session resume，不足以作为并发安全 canonical path

### Slice D: tests and review

- 更新 runtime / launcher 参数测试
- 为后续 verification 产出 review 证据

## Current Implementation Snapshot

- runtime 现在通过共享 helper 统一计算：
  - launch 前的 per-tool resume target
  - cycle 结束后的 observed session anchor
  - persisted session id / resume target
- `codex` 不再允许在 supervisor/runtime resume 路径里静默退回 `--last`
- delegated continuation 现在会把当前 workcell 的 resume target 写入 intake `SESSION_REFS`
- 本地 continuation re-entry 现在优先 `TERM` 当前 AI 进程；若超时，再落到 hard kill fallback，并写入 `preemption-state.env`

## Revisit Triggers

- Codex CLI 改变 `resume` 参数面或 session evidence 获取方式
- `iflow` / `kiro-cli` 新增显式 session-id 级恢复参数
- Freely 新接入新的 AI tool profile
- supervisor 需要支持 event-driven re-entry 到仍存活的同一 PTY，而不只是新进程 resume

## Dev-Loop Handoff

后续 `dev-loop` 直接消费以下最小上下文：

- canonical model: `tool + explicit session identifier`
- `codex` 目标实现：停止默认 `resume --last`
- `cc` 继续保持 `--session-id`
- `iflow` / `kiro-cli` 先按当前弱 contract 留痕，不伪装成并发安全
- handoff 目标要能表达 worker + session target，而不是只给抽象 continuation
- 当前如果采用 hard kill 触发 re-entry，需要在 review 中明确它只是临时 fallback
- 需要修改：
  - `docs/system/workspace/tools.md`
  - `docs/system/workspace/three-loop-capability-lifecycle.md`
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/system/workspace/scripts/runtime/tool-launchers.sh`
  - 至少一个 codex runtime 参数测试
