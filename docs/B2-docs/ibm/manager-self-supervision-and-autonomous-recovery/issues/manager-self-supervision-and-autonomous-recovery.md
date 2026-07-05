# Issue: manager-self-supervision-and-autonomous-recovery

- issue_id: `I-20260318-1408`
- title: Manager self-supervision and autonomous recovery
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `manager-self-supervision-and-autonomous-recovery`
- issue-name: `manager-self-supervision-and-autonomous-recovery`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/manager-self-supervision-and-autonomous-recovery/code-reviews`
- source_candidate: `docs/pre-brainstorms/20260318-1408--manager-self-supervision-and-autonomous-recovery/candidates.md#c-20260318-a`
- source_brainstorm: `docs/pre-brainstorms/20260318-1408--manager-self-supervision-and-autonomous-recovery/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `docs/epics/workspace-routing-foundation/checkpoint-commit-and-multi-worktree-supervision-governance/issues/checkpoint-commit-and-multi-worktree-supervision-governance.md`
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}]

## Why

Freely 已经具备局部的 worker supervision、account switch、session rotation 和 fleet status，但此前仍需要人工提醒才发现主管和 worker 实际已经停摆。这说明 Freely 缺：

- 主管对整个工位舰队的自检与异常识别
- 对“应运行但掉线”与“故意冻结”之间的显式区分
- 清晰的角色边界，避免主管越权变成执行者

## Scope

1. 给每个工位增加 durable `workcell-state`，记录期望运行态、角色和退出原因。
2. 让主管在下一轮 prompt 前就能看到 `expected running but down` 的结构化告警。
3. 修正 PID 归属误判，避免 `develop` 把其他 worktree 的 supervisor 认成自己。
4. 在 fleet 视图中显式展示 `desired runtime / role / exit reason`。
5. 把 `manager-agent` / `worker-agent` 的职责边界物化为正式角色文档。
6. 明确列出哪些恢复场景属于 AI 无能为力，必须由 runtime / scripts 接管。
7. 让 `freely start` 在主管工位自动启动 manager watchdog 脚本，在 worker supervisor 掉线时先做脚本级恢复，只有恢复不了的异常才继续交给主管 AI 告警与编排。

## Acceptance

- `freely baseline-status` 不再把其他 worktree 的 PID 误报为当前工位 supervisor / ai。
- `wt-fleet-status` 能区分 `expected running but down` 与 `intentionally stopped/frozen`。
- 主管 prompt 在发现应运行工位掉线时，优先进入 supervision / recovery / delegation，而不是继续普通路由。
- 主管只做监督、编排、委派和告警；若判断需要恢复，只输出 `runtime_recovery_requested` 一类管理决策，账号切换、等待和重启仍归 runtime。
- manager / worker runtime 不再执行全局 Codex 账号切换；若命中限额，只记录 `runtime-owned` 异常并等待外层 global watchdog/account controller 接管。
- 仓库内存在显式的 `manager-agent` 与 `worker-agent` 角色文档，而不是只靠 lead-agent 隐式约定。
- 文档明确规定：响应结束、进程退出、限额/认证失败、`context compacted` 后的新进程续接，都属于 `runtime-owned`，而不是要求 manager/worker 自行恢复。
- 当应运行的 worker supervisor 已掉线时，manager runtime 会先尝试脚本级拉起该 worker；只有脚本恢复后仍异常的情况，才继续留给主管 AI 做告警与后续编排。

## Completion

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/worktree/wt-fleet-status`
- `docs/system/workspace/scripts/start-lead-agent.sh`
- `docs/system/workspace/scripts/tests/test-freely-manager-supervision-alert`
- `docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery`
- `docs/system/workspace/scripts/tests/test-freely-manager-runtime-does-not-switch-accounts`
- `docs/system/workspace/scripts/tests/test-freely-status-pid-ownership`
- `docs/system/workspace/scripts/tests/test-wt-fleet-status`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/agents/worker-agent.md`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`

## Verification

- 已执行 `TEST`：
  - `./bin/governance-check`
  - `bash docs/system/workspace/scripts/tests/test-freely-supervisor-loop`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-supervision-alert`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-does-not-switch-accounts`
  - `bash docs/system/workspace/scripts/tests/test-freely-status-pid-ownership`
  - `bash docs/system/workspace/scripts/tests/test-wt-fleet-status`
  - `bash docs/system/workspace/scripts/tests/test-routing-foundation-loop`
- 已写入 review 证据：
  - `docs/epics/workspace-routing-foundation/manager-self-supervision-and-autonomous-recovery/code-reviews/20260326-manager-self-supervision-canonical-replay-verification.md`
- 当前验证重点：
  - 主管是否在 worker 掉线时优先进入 supervision alert
  - 工位状态是否能正确保留 `desired runtime` 和 `exit reason`
  - 角色边界是否已经从预研提升为正式能力文档
  - manager / worker runtime 是否已经停止直接操作全局 Codex 账号
- 最新验证事实：
  - `test-freely-manager-runtime-does-not-switch-accounts` 已覆盖 worker 命中 auth failure 时不再执行 `ai switch`，而是留下 `runtime-owned` 退出原因并退出本地 supervisor
  - 主管/worker 的全局账号恢复 owner 已进一步收紧到外层 global watchdog / account controller

## Verification Summary

- canonical replay 继续证明：主管会先看到 `expected running but down` worker 告警，runtime 会优先做脚本级恢复，而不是把 supervisor 掉线直接甩给 AI 即兴处理。
- PID 归属、fleet desired runtime / exit reason 暴露、manager/worker 角色文档，以及“runtime 不直接切全局账号”的边界均未回退。
- 更外层的 global watchdog / ensure 仍是边界外后续能力，已由同族 issue `I-20260318-1630` 承接，不再阻塞当前 issue 收口。
- 当前批次据此把本 issue 从 `in_verification` 关闭为 `completed`。
