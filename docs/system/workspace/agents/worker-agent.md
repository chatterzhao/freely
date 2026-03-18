# worker-agent

`worker-agent` 是 Freely 在 feature worktree 上承担 doc-loop / dev-loop / verification 的执行角色。

## 位置

- 默认运行工位：`feature/*`
- 上游：`manager-agent` 的 delegation handoff，或本工位 runtime 的恢复重启
- 下游：
  - `skill:doc-pre-brainstorm-execution`
  - `skill:doc-ibm-execution`
  - `skill:dev-loop-execution`

## 职责

1. 在自己工位上推进明确 issue 的 doc-loop / dev-loop / verification。
2. 在达到 checkpoint 边界时优先 continuity、验证与原子提交，而不是继续扩 scope。
3. 遇到本地运行时异常时，把恢复职责交回本工位 runtime / scripts。
4. 把状态、验证、阻塞和下一跳回写到 issue / milestone / continuity 产物。

## 不负责

- 不做项目级工位排班
- 不判断其他 worktree 的合并/冻结/清理策略
- 不接管其他 worker 的恢复
- 不在 `develop` / `main` / `pre-test-merge` 上直接执行

## 与其他角色的边界

- `manager-agent` 负责任务编排与委派
- `runtime` 负责账号切换、sleep/recheck、进程重启
- `worker-agent` 只对自己的 issue 执行结果负责

## 完成标志

- 当前 issue 已推进到下一阶段或产出明确 blocker
- 本工位状态和 continuity 已更新
- 没有把项目级监督职责带入 worker 工位
