# Issue: watchdog-live-status-surface-and-manager-supervision

- issue_id: `I-20260320-1945`
- title: Watchdog live status surface and manager supervision
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `watchdog-live-status-surface-and-manager-supervision`
- issue-name: `watchdog-live-status-surface-and-manager-supervision`
- source_candidate: `docs/B1-docs/raw-20260320/candidates.md#c-20260320-1945-a`
- source_brainstorm: `docs/B1-docs/raw-20260320/brainstorms.md`
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

- `freely live-status --project <path>` 存在。
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
