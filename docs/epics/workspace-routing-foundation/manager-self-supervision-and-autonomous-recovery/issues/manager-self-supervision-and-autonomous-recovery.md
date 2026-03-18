# Issue: manager-self-supervision-and-autonomous-recovery

- issue_id: `I-20260318-1408`
- title: Manager self-supervision and autonomous recovery
- phase_state: `in_verification`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `manager-self-supervision-and-autonomous-recovery`
- issue-name: `manager-self-supervision-and-autonomous-recovery`
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

## Acceptance

- `freely status` 不再把其他 worktree 的 PID 误报为当前工位 supervisor / ai。
- `wt-fleet-status` 能区分 `expected running but down` 与 `intentionally stopped/frozen`。
- 主管 prompt 在发现应运行工位掉线时，优先进入 supervision / recovery / delegation，而不是继续普通路由。
- 主管只做监督、编排、委派和告警；账号切换、等待和重启仍归 runtime。
- 仓库内存在显式的 `manager-agent` 与 `worker-agent` 角色文档，而不是只靠 lead-agent 隐式约定。

## Completion

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/worktree/wt-fleet-status`
- `docs/system/workspace/scripts/start-lead-agent.sh`
- `docs/system/workspace/scripts/tests/test-freely-manager-supervision-alert`
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
  - `bash docs/system/workspace/scripts/tests/test-freely-status-pid-ownership`
  - `bash docs/system/workspace/scripts/tests/test-wt-fleet-status`
  - `bash docs/system/workspace/scripts/tests/test-routing-foundation-loop`
- 当前验证重点：
  - 主管是否在 worker 掉线时优先进入 supervision alert
  - 工位状态是否能正确保留 `desired runtime` 和 `exit reason`
  - 角色边界是否已经从预研提升为正式能力文档

## Next

- 保持 `in_verification`。当前最小实现、测试和角色文档已落盘。
- 后续仍需一个更外层的 watchdog/ensure 机制，处理“主管 supervisor 自己整个进程消失”的自复活问题；这不在本 issue 当前批次内扩 scope。
