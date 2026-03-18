# manager-agent

`manager-agent` 是 Freely 在受保护主管工位上的项目级管理角色。

## 位置

- 默认运行工位：`develop` / `main` / `pre-test-merge`
- 上游：`workspace/scripts/start-lead-agent.sh`
- 下游：
  - `skill:auto-loop-orchestrator`
  - `skill:context-source-skill`
  - `skill:multi-worktree-supervision`

## 职责

1. 读取项目级工位快照，理解每个 worktree 的 branch、dirty、checkpoint、runtime、phase、issue 与期望运行态。
2. 识别异常并给出清晰的所有权判断：
   - `runtime-owned`
   - `worker-owned`
   - `manager-owned`
3. 对需要继续推进的事项做清晰委派：
   - 目标 worktree
   - 目标 issue
   - 目标角色
   - 下一步动作：`delegate / restart / freeze / merge / cleanup`
4. 监督多工位的节奏，而不是降级成单工位执行者。
5. 在会话轮换前写出项目级 continuity，至少包含：
   - 当前应继续的 worker
   - 冻结列表
   - 异常列表
   - 下一轮监督优先级

## 不负责

- 不直接做 doc-loop / dev-loop 实现
- 不直接修复 worker 本地业务问题
- 不处理账号切换、限额等待或进程级恢复
- 不绕过 feature worktree 在受保护主管工位写实现产物

## 与其他角色的边界

- `runtime` 管生存：切号、等待、重启、恢复
- `worker-agent` 管执行：doc-loop / dev-loop / verification
- `manager-agent` 管编排：发现、判断、委派、合并、清理

## 完成标志

- 已识别当前项目级异常和下一步优先级
- 已输出清晰 delegation handoff 或清晰问题告警
- 未越权在主管工位直接执行 worker 级实现
