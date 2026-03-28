# Issue: watchdog-live-status-surface-and-manager-supervision

- issue_id: `I-20260320-1945`
- title: Watchdog live status surface and manager supervision
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `watchdog-live-status-surface-and-manager-supervision`
- issue-name: `watchdog-live-status-surface-and-manager-supervision`
- source_candidate: `docs/pre-brainstorms/20260320-1945--watchdog-live-status-surface-and-manager-supervision/candidates.md#c-20260320-1945-a`
- source_brainstorm: `docs/pre-brainstorms/20260320-1945--watchdog-live-status-surface-and-manager-supervision/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `docs/epics/workspace-routing-foundation/manager-self-supervision-and-autonomous-recovery/issues/manager-self-supervision-and-autonomous-recovery.md`
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}]

## Why

Freely 已经有 runtime watchdog、manager continuity、interruption intake 和 fleet supervision，但还没有一个统一的“当前态控制面”。

结果是：

- 进程活着但是否在推进不清楚
- 主管监督缺少 canonical current-state 入口
- 用户需要手工拼 `baseline-status + prompt + continuity + ps + jsonl`

## Scope

1. 新增 `freely live-status --project <path>` 当前态视图。
2. 只展示活跃 pid，不展示已退出 pid。
3. 输出最小的当前 activity surface：
   - branch / role / activity_state
   - supervisor / dispatcher / ai pid + command
   - prompt excerpt
   - manager continuity excerpt
   - active intake / latest resolution 摘要
   - jsonl / cycle_log / prompt_file deep refs
4. 将该接口接入主管监督协议：
   - `manager-agent`
   - `multi-worktree-supervision`
   - `start-lead-agent.sh`
5. 增加脚本级测试，锁住输出和接线。

## Acceptance

- `./bin/freely live-status --project <path>` 存在。
- 输出只展示仍活跃的 `supervisor / interruption dispatcher / ai` pid。
- 输出包含 prompt excerpt，能帮助识别“这个 pid 当前在干什么”。
- 输出包含 `last_tool_jsonl_path` 与 `last_cycle_log` 作为深挖入口。
- `manager-agent` 与相关 skill 明确要求主管轮次先读 live-status 当前态。
- 首跳 prompt 在主管模式下明确提示优先读取该接口。

## Completion

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/skills/multi-worktree-supervision/SKILL.md`
- `docs/system/workspace/skills/watchdog-control-plane/SKILL.md`
- `docs/system/workspace/scripts/start-lead-agent.sh`
- `docs/system/workspace/scripts/README.md`
- `docs/system/workspace/scripts/tests/test-freely-live-status`
- `docs/system/workspace/scripts/tests/test-watchdog-control-plane-skills`
- `docs/system/workspace/scripts/tests/test-routing-foundation-loop`

## Verification

- `./bin/governance-check`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status`
- `bash docs/system/workspace/scripts/tests/test-watchdog-control-plane-skills`
- `bash docs/system/workspace/scripts/tests/test-routing-foundation-loop`

## Next

- 当前批次已完成并并入 `develop`。
- 若后续仍需 `--format json`、`--watch` 或 stall scoring，再从同一预研线继续 materialize，不在本 issue 当前批次扩 scope。

## 2026-03-28 Runtime State Reconciliation Addendum

- same_family_followthrough: `true`
- regression_summary: `live-status` 会同时显示 `activity_state: ai_active` 与陈旧的 `last_ai_state: down` / `last_exit_reason: starting`，因为当前态来自 PID 探活，而历史字段只读 `workcell-state.env`，没有在读取时按当前项目自有进程做保守校正。
- judgement: 这仍属于本 issue 的 current-state surface contract 内部修复，而不是新的 status family 扩 scope。

### Scope Narrowing

1. 只修 `live-status` 读路径。
2. 仅当当前 project-owned `supervisor` / `ai` PID 被正向确认存在时，才把输出中的 `last_supervisor_state` / `last_ai_state` 校正为 `up`。
3. 仅当 AI 已确认活着且历史退出原因为 `starting` 时，才把 `last_exit_reason` 收敛为 `none`。
4. 不回写 `workcell-state.env`。
5. 不改变 watchdog、recovery、operator stop、restart storm 或 auth failure 的持久化语义。

### Completion Addendum

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-live-status`

### Verification Addendum

- `bash docs/system/workspace/scripts/tests/test-freely-live-status`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-watchdog-survival`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery`

### Addendum Result

- `live-status` 现在在 current-state surface 上保持自洽：当 project-owned AI 正在运行时，不再同时显示 `last_ai_state: down`。
- 该修复保持单向、只读、面向当前态的校正，不会把“当前无 PID”误写成新的失败结论。
