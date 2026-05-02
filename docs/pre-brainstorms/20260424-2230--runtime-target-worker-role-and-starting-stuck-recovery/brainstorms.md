# Brainstorms - 20260424-2230--runtime-target-worker-role-and-starting-stuck-recovery

## Context

Dogfooding on `2026-04-24` exposed a structural blocker that prevents `freely daemon start` from completing its autonomous self-loop on canonical `develop`. 表面症状不是“daemon 根本没启动”，而是 daemon 启动后 supervisor 能活着、manager 也会继续写 continuity / worker prompt，但 delegated target 不能稳定进入正确 worker execution path，导致系统不会自己 finish 当前任务、收口 worktree、再接下一个任务。现有 architecture（PID table + watchdog + exit-contract artifact next-action protocol）方向是对的，但三处同一路径上的 runtime seam 让第一轮 dispatch 之后断链：

1. **runtime 角色真相只看 branch 默认值，没有把 worker contract 提升为 effective role**: 父 manager 通过 worker prompt 产出 `Worktree:` / `Branch:` / dispatch metadata / verification metadata，runtime 再把这些 machine-readable 字段写入 target 的 worker verification contract，并由 `start_workcell_supervisor_async`（5648）拉起 target supervisor。也就是说，agent / skill / prompt 负责生成 delegation 产物，runtime 负责消费产物并启动 AI；真正的运行时角色判定仍在 runtime control plane。当前 target 进入 `cmd_daemon_run`（15632）后，以及后续 recovery / exit-contract / cleanup 等控制面判断里，仍直接按 `role_hint_for_project` 决定 manager / worker 分支；当 target 是 `test-pre-merge-*` worktree 时，branch 默认角色被硬编码成 `manager`，于是 target 又去 `launch_manager_watchdog` + `ensure_manager_watchdog_ready_or_fail` 启动自己的 manager AI，与父项目 codex slot (`~/.codex/slot-switch.lock`) 互斥。尽管 `LAST_WORKER_VERIFICATION_METADATA_PRESENT=true` 且全套 worker contract (`LAST_WORKER_OWNER_ISSUE`、`LAST_WORKER_CLOSEOUT_GATE_COMMAND` …) 已写入 workcell-state，runtime 没有把它升级成 unified effective runtime role。

2. **存在更窄的 `starting`-stuck 缝，不是完全“无看门人”**: 现有 runtime 已有 `supervisor_startup_truth_ready_for_project`、`project_bootstrap_launch_in_flight`、worker ai stall recovery 等启动/恢复语义，所以问题不是所有 `LAST_EXIT_REASON=starting` 都没人管。真正漏掉的是：target supervisor 还活着，但 target 长时间没有成功写出 `ai.pid`，同时 launch state 仍把它当成 expected-running worker。此时 `monitor_ai_pid_for_workcell_state`（2103）因为没有 pid 可监控，不会进入 `detect_post_run_handoff`/exit-contract 路径；父端 `manager_runtime_recover_workers_if_needed`（manager-watchdog.sh）又只看 supervisor 是否 alive，看到 supervisor pid 仍在就认为 worker 还在启动中，不再重派或回退。于是 zombie target 永远停在 `starting`。

3. **launch slot reclaim 放在 status read-model 太弱，dispatch-critical path 也缺活性对账**: 父 `LAUNCHED_WORKER_PROMPTS` 一旦写入只在同 continuity 时被 `manager_worker_launch_state_reconcile_same_continuity_prompts`（6669）做名字去重，没有在 launch / dispatch-critical path 基于 target liveness 释放卡死 prompt 的对账。结果是 `ACTIVE_RUNNING_WORKER_COUNT=1` 被永久占用，父 manager `manager_continuity_has_unconsumed_launchable_worker_prompt` 一直返回 false（已记录），同时 4 分钟一次 `context_compacted` rotation 重写同名 prompt 假装在动；HEAD 不变。即使把释放逻辑只补到 `manager_worker_launch_state_refresh_for_status`，也仍可能在真正决定“还有没有可派 worker”时读到旧的 consumed/active snapshot。

实测证据（develop 树 daemon pid=87958 启动 ~80 分钟）：worker prompt 列表 20 份（`20260424-205811` … `20260424-223034` 同名 `runtime-lifecycle-receipt-guarded-replay`）；target `test-pre-merge-runtime-lifecycle-followthrough` workcell-state 永久 `supervisor=up ai=down exit_reason=starting role_hint=manager`，无 ai.pid；`feature/runtime-lifecycle-receipt-closeout-reconcile` worker 树 supervisor=down ai=down 留 4 个 dirty 文件；develop HEAD 无变。

## Decision

Materialize a bounded same-family followthrough owner that closes all three seams together, because they are all on the single "target supervisor cannot get onto the correct worker execution path before manager loses confidence" path:

1. introduce an effective runtime role decision that prefers a valid worker verification contract over branch-default role hint for delegated targets, and use that decision consistently in runtime control-plane call sites that choose manager vs worker behavior, not only in `cmd_daemon_run`;
2. add a narrow `starting`-stuck reconciliation path: when a delegated target stays in `LAST_EXIT_REASON=starting` beyond the existing startup lifecycle grace and still has no valid `ai.pid`, runtime should clean the zombie supervisor residue and let the parent reclaim the launch slot;
3. add target-liveness reconciliation in the dispatch-critical launch/continuity path, with `manager_worker_launch_state_refresh_for_status` 只做状态投影同步：dead/never-up target AI releases its `LAUNCHED_WORKER_PROMPTS` entry and decrements `ACTIVE_RUNNING_WORKER_COUNT`, so manager re-evaluates instead of looping on the same prompt name.

## Boundaries

- do not redesign the watchdog / exit-contract / `auth_change_wake_fans_out_running_projects` mechanisms — they are correct and already match the dogfooding architecture;
- do not widen this into a global agent/skill/prompt role redesign; the fix belongs in runtime control-plane role resolution, because manager prompt / verification contract are already the machine-readable delegation truth and the missing seam is runtime consumption of that truth;
- do not weaken the codex slot-switch lock — the cure is preventing target manager-mode launch on a worker contract, not letting two manager AIs share a slot;
- do not invent a brand-new reclaim timer unless existing startup lifecycle grace proves insufficient; first align the `starting`-stuck reclaim rule with the current bootstrap / launch-in-flight grace semantics;
- do not retroactively absolve already-merged-clean owner lanes; the launch state liveness pass must stay narrow to `target ai.pid never came up after startup grace`.

## Followthrough

The owner issue should land the three changes in `docs/system/workspace/scripts/runtime/freely` and the manager-watchdog.sh recover loop, with feature-local pre-tests that simulate (a) a delegated target with a valid worker contract electing worker behavior across the runtime control plane, not just one branch point, (b) a delegated target stuck at `starting` with live supervisor but no `ai.pid` being released after the existing startup grace boundary, and (c) a parent launch path / continuity check releasing a dead target's slot before deciding there is no launchable worker. After premerge-integration evidence is captured, replay through `test-pre-merge-runtime-target-worker-role-and-starting-stuck-recovery-20260424` into `develop`, retire both the feature and the test-pre-merge worktrees, then restart `freely daemon start --project /Users/zhaoyu/Downloads/code/my-freely/freely` from the freshly merged develop tree to prove autonomous loop continuation: select task -> finish task -> retire worktree -> continue to next task without manual intervention.
