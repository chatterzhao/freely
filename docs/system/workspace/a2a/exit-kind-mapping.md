# A2A Task 状态

> Google A2A 标准状态机: submitted → working → input-required → completed / failed / canceled
> Freely 使用标准状态名。`a2a-exit --state <value>` 直接写入 A2A Task.state。
> 旧 `exit_kind` 已废弃（worker_blocked, worker_done 等）。

## A2A 标准状态

| A2A Task state | 含义 | Freely 使用场景 |
|---------------|------|----------------|
| `submitted` | 任务已提交，等待处理 | Manager 创建 worker/reviewer 任务 |
| `working` | Agent 正在执行 | Worker 执行 phase |
| `input-required` | Agent 需要外部输入才能继续 | Worker 完成 phase，等 reviewer GO/FIX |
| `completed` | 任务成功完成 | wt-close 后 |
| `failed` | 任务失败（崩溃/超时） | Worker 崩溃、超时 |
| `canceled` | 任务被取消 | Manager 主动放弃 |

## 状态转换

```
submitted → working → input-required → working → ... → completed
                    ↘ failed                        ↘ canceled
```

### 场景 1: 正常 fix|feature 流程

```
1. submitted  Manager 创建 worker 任务
2. working    Worker 执行 B1
3. input-required  Worker 完成 B1，等 reviewer
4. working    Reviewer GO，Worker 执行 B2
...循环...
N. completed  Manager wt-close
```

### 场景 2: 阻塞恢复

```
1. working    Worker 执行中
2. input-required  Worker 遇到问题，需要 Manager 澄清
3. working    Manager 回复后继续
```

### 场景 3: 主动取消

```
1. working    Worker 执行中
2. canceled   Manager 决定放弃此 raw issue
```

## 历史映射（已废弃，仅用于理解旧代码）

旧 `exit_kind` → 新 `--state`：

| 旧 exit_kind | 新 --state |
|-------------|-----------|
| worker_blocked | input-required |
| worker_done | completed |
| worker_working | working |
| worker_handoff_needed | input-required |
| stop_ai | failed |
| manager_working | submitted |
| delegate_workers | submitted |
| resume_manager | completed |
