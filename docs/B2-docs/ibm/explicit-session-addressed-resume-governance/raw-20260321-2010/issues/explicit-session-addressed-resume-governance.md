# Issue: explicit-session-addressed-resume-governance

- issue_id: `I-20260321-2010`
- title: Explicit session-addressed resume governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `explicit-session-addressed-resume-governance`
- issue-name: `explicit-session-addressed-resume-governance`
- verification_artifact_dir: docs/B2-docs/ibm/explicit-session-addressed-resume-governance/raw-20260321-2010/code-reviews
- priority: P1
- source_candidate: `docs/B1-docs/raw-20260321T170600Z/candidates.md#c-20260321-2010-a`
- source_brainstorm: `docs/B1-docs/raw-20260321T170600Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/B2-docs/ibm/token-efficient-session-continuity-and-rotation-governance/issues/token-efficient-session-continuity-and-rotation-governance.md`
  - `docs/B2-docs/ibm/state-sync-and-session-evidence-governance/issues/state-sync-and-session-evidence-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://current-manual-codex-thread-id-not-exposed", role: "author"}
  - {tool: codex, session_id: "019d12c4-479f-7d02-9061-b6dc92bb2fd2", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/21/rollout-2026-03-21T16-39-06-019d12c4-479f-7d02-9061-b6dc92bb2fd2.jsonl", role: "fresh_with_handoff_source"}

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
6. 定义 manager 理解 signal 后，如何把 handoff 绑定到具体 worker/session target。
7. 定义 graceful preemption 与 hard kill fallback 的边界，避免未落盘内容直接丢失。

## Acceptance

- truth sources 明确写出 canonical continuity model = explicit session-addressed resume
- `process alive` 与 `session resumable` 被明确拆开，不再混成一个状态
- `codex` 的默认并发 resume 不再依赖 `--last`
- `cc` 的现有显式 `session-id` 模式被记录为正向参照
- `iflow` / `kiro-cli` 当前 contract 被明确标注为：
  - 已满足
  - 或暂未满足、需后续 issue
- manager -> worker handoff 能表达具体 resume target，而不是只给“继续做”这种抽象文字
- continuity contract 明确区分：
  - graceful preemption
  - hard kill fallback
- PTY 注入仅作为 fallback 被说明

## Completion

- `docs/system/workspace/tools.md`
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/runtime/tool-launchers.sh`
- `docs/system/workspace/scripts/monitor-ai-cli.sh`
- `docs/progress/workspace-routing-foundation/p-explicit-session-addressed-resume-governance.md`
- `docs/B2-docs/ibm/explicit-session-addressed-resume-governance/code-reviews/20260321-explicit-session-addressed-resume-verification.md`

## Verification

- `./bin/governance-check`
- runtime continuity tests to be selected in IBM

## IBM Outcome

当前 IBM 已收敛出以下正式结论：

1. Freely 的 canonical continuity model 固定为：
   - `tool + explicit session identifier + workcell ownership + evidence refs`
2. `codex` 当前已有正式 CLI primitive 可承接该模型：
   - `codex exec resume [SESSION_ID] [PROMPT]`
3. `cc` / `cc-use-codex-cli` 已是正向样本：
   - 每个 workcell 一个 `--session-id`
4. `iflow` 当前只部分满足：
   - `--continue` 只是 recent conversation
   - `--resume` 可指向 specific session file
   - Freely 仍需把它 materialize 成 workcell-scoped contract
5. `kiro-cli` 当前未满足 canonical contract：
   - `--resume` 只恢复当前目录最近会话
   - `--resume-picker` 是交互 fallback，不适合作为 supervisor 默认路径
6. PTY input injection 只保留为 fallback，不进入默认 runtime/supervisor 重入面
7. manager 的 delegated handoff 不只是 restart point，还必须能继续收敛为具体 worker session target
8. 当前 runtime 若用 hard kill 触发 re-entry，只能作为临时 fallback；后续 dev-loop 必须继续收敛 graceful preemption / flush contract

## Implementation References

- `docs/B2-docs/ibm/explicit-session-addressed-resume-governance/brainstorms/b-explicit-session-addressed-resume-governance.md`
- `docs/B2-docs/ibm/explicit-session-addressed-resume-governance/prd.md`
- `docs/B2-docs/ibm/explicit-session-addressed-resume-governance/raw-20260321-2010/verification/pre-tests.md`
- `docs/B2-docs/ibm/explicit-session-addressed-resume-governance/tasks.md`
- `docs/system/workspace/tools.md`
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/runtime/tool-launchers.sh`

## Ready For Dev

当前 issue 已具备进入 `dev-loop` 的最小上下文：

1. truth-source contract 已冻结
2. 工具差异与缺口已明确
3. runtime 改动面已定位
4. 最小验证面已明确

## Verification Outcome

- `codex` runtime resume 已改为显式 `SESSION_ID`，无 target 时明确失败，不再静默退回 `--last`
- shared runtime helper 已统一 `codex` / `cc` 的 resume target 获取与持久化逻辑
- delegated continuation 已写回 worker-scoped `SESSION_REFS`
- local continuation re-entry 已优先 `TERM` 当前 AI，并在 fallback 时写入 preemption evidence
- `iflow` / `kiro-cli` 的弱 contract 已在 truth sources 中明示，不再冒充并发安全 canonical path

## Next

- 当前批次已完成。
- 若后续要继续增强 cross-worktree worker targeting 或更强 flush contract，应通过新生命周期承接，而不是在本 issue 上继续扩 scope
