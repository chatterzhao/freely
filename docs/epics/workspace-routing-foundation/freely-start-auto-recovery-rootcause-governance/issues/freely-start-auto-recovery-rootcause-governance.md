# Issue: freely-start-auto-recovery-rootcause-governance

- issue_id: `I-20260414-0255-A`
- title: `Freely start after-failure recovery handoff race root cause fix`
- milestone: `M-20260306-workspace-routing-foundation`
- phase_state: `done_ibm`
- priority: P1
- epic: `workspace-routing-foundation`
- source_brainstorm: `docs/pre-brainstorms/20260414-0255--freely-start-after-failure-recovery-handoff-race/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260414-0255--freely-start-after-failure-recovery-handoff-race/candidates.md`
- branch: `feature/freely-start-auto-recovery-rootcause-20260414`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260414-feature-freely-start-auto-recovery-rootcause`

## Summary

`freely start` 在真实坏号上失败后，恢复交接链没有稳定完成。根因不是 failure label 分类错误，而是 after-failure recovery handoff 没有串成单一、串行、可判定的控制面交接；旧 supervisor、watchdog、one-shot recheck、以及 operator stop 会在同一时间窗里相互竞争。

## Root Cause

最佳根因只保留这一条：

**`freely start` 的 after-failure recovery handoff 没有被串成单一、串行、可判定的控制面交接；旧 supervisor、watchdog、one-shot recheck、以及 operator stop 会在同一时间窗里相互竞争，导致恢复链既可能重复启动同一坏号，也可能在 stop 后又被重新拉起。**

## Implementation Fix

本次实现只改同一条根因，不碰既有 tool/slot 选择顺序：

1. `cleanup_supervisor()` 先读取共享 runtime 真相，而不是只信当前进程内的 stale `DESIRED_RUNTIME_STATE_VALUE`
2. 若已经有 replacement supervisor 存活，旧 supervisor cleanup 直接退出，不再覆盖共享 state，也不再去杀/重拉共享 control-plane
3. manager 失败后的续跑执行者，从 one-shot `launch_manager_control_plane_recheck()` 改成持续 `launch_manager_watchdog()`

对应真源：
- `project_cleanup_runtime_intent()`
- `cleanup_supervisor()`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh`

## Verification Evidence

已通过的回归：

1. `test-freely-start-watchdog-recovers-when-fallback-tool-appears-late`
   - 证明 `freely start` 在当前工具先失败、fallback 工具稍后才变可用时，watchdog 会持续接力直到恢复成功
2. `test-freely-worker-runtime-falls-through-to-cross-tool-after-failure`
   - 证明 worker runtime 在 same-tool slot recovery 失败后能继续进入 cross-tool fallback
3. `test-watchdog-switch-to-codex-slot-accepts-actual-slot-without-json`
   - 证明 watchdog 接受实际活跃 slot 作为成功证据，即使 switch JSON 为空

## Scope Boundary

只收敛这条问题：
- `freely start` 在真实坏号或坏工具上失败后，必须自动把恢复链跑完
- 不要求操作者手工补 `freely ensure-manager`
- 不引入新的后台空转、重复 supervisor、或 `freely stop` 后又被抢回来的竞态

不在本条 issue 里扩展：
- Codex probe `hi` 成功形状规则本身
- 旧 intake / continuity 噪音治理
- 泛化到所有 unrelated runtime bug

## Success Criteria

1. 手工把 Codex 切到真实坏号，例如 `apikey-codex-a1016-1`
2. 执行真实 `./bin/freely start --project <project>`
3. 首轮失败后，不需要人工执行 `freely ensure-manager`
4. 系统会自动继续恢复，直到切到可用工具/号并重新运行
5. 同一次恢复过程中，不允许重复重启到刚失败的同一坏号
6. `./bin/freely stop --project <project>` 后，不允许再出现被 watchdog / recheck 抢回来的新 supervisor

## Next Action

1. 创建 `prd.md`、`pre-tests.md`、`tasks.md` 补充验收细节
2. 更新 milestone 将候选提升为 committed_issue
3. 决定是否进入 dev-loop 继续完善实现，或直接进入 verification

## Session References

- tool: cc
- session_id: current-session
- jsonl_path: unavailable://cc-session-only
- role: author