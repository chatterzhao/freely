# exit_kind → A2A Task 状态映射

> 本文档定义 Freely exit_kind 与 A2A Task 状态的完整映射关系。

## 映射表

| Freely exit_kind | A2A Task state | HTTP Status | 说明 |
|------------------|----------------|-------------|------|
| `manager_working` | `submitted` | 202 | Manager 已提交任务，等待 Worker 接收 |
| `worker_working` | `working` | 200 | Worker 正在执行任务 |
| `worker_done` | `completed` | 200 | 任务成功完成 |
| `worker_blocked` | `input-required` | 200 | Worker 阻塞，需要 Manager 提供输入 |
| `worker_handoff_needed` | `pending-input` | 200 | Worker 需要 Manager 介入决策 |
| `delegate_workers` | `submitted` | 202 | Manager 委派新 Worker，子任务已提交 |
| `resume_manager` | `completed` | 200 | Worker 完成任务，返回 Manager |
| `stop_ai` | `failed` | 500 | AI 停止/失败 |

## A2A Task 状态机

```
                    ┌──────────────┐
                    │   submitted   │◄── manager_working
                    └──────┬───────┘    delegate_workers
                           │
              ┌────────────▼────────────┐
              │          working        │◄── worker_working
              └────────────┬────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
  ┌───────────┐    ┌─────────────┐    ┌──────────┐
  │completed  │    │input-required│    │  failed   │
  └───────────┘    └─────────────┘    └──────────┘
        │                  ▲                  │
        │                  │                  │
  resume_manager    worker_blocked      stop_ai
        │                  │
        │        ┌─────────┴─────────┐
        │        │  pending-input   │
        │        └──────────────────┘
        │                ▲
        │                │
        └─────worker_handoff_needed
```

## 详细映射说明

### 1. manager_working → submitted

```yaml
freely_exit_kind: manager_working
a2a_task_state: submitted
http_status: 202 Accepted
语义: Manager 已创建任务，等待 Worker 接收和处理
示例: |
  Manager scan 发现新 issue，创建 Task，等待 Worker 执行
```

### 2. worker_working → working

```yaml
freely_exit_kind: worker_working
a2a_task_state: working
http_status: 200 OK
语义: Worker 正在积极执行任务
示例: |
  Worker 正在执行 freely-fix-execution 或 freely-feat-execution
  - progress: "已修复 XXX 问题，进入 YYY 阶段"
  - next_action: "继续执行 ZZZ"
```

### 3. worker_done → completed

```yaml
freely_exit_kind: worker_done
a2a_task_state: completed
http_status: 200 OK
语义: 任务成功完成，Worker 返回结果
示例: |
  Worker 完成修复/功能开发
  - completion_summary: "修复了 XXX 问题"
  - evidence_paths: ["docs/progress/xxx/evidence.md"]
  - next_action: "提交 PR"
```

### 4. worker_blocked → input-required

```yaml
freely_exit_kind: worker_blocked
a2a_task_state: input-required
http_status: 200 OK
语义: Worker 阻塞，需要 Manager 提供必要输入才能继续
示例: |
  Worker 需要以下输入才能继续:
  - 需要确认需求细节
  - 需要访问某个资源
  - 需要决策技术方案
```

### 5. worker_handoff_needed → pending-input

```yaml
freely_exit_kind: worker_handoff_needed
a2a_task_state: pending-input
http_status: 200 OK
语义: Worker 需要 Manager 介入决策，不能自己继续
示例: |
  Worker 遇到以下情况需要 Manager 决策:
  - 发现超出当前 issue scope 的问题
  - 遇到技术方案争议
  - 需要人类确认
```

### 6. delegate_workers → submitted

```yaml
freely_exit_kind: delegate_workers
a2a_task_state: submitted
http_status: 202 Accepted
语义: Manager 委派新 Worker 创建子任务
示例: |
  Manager 委派多个 Worker 并行执行子任务
  - worker_prompts_csv: "worker1.csv,worker2.csv"
  - next_action: "等待子任务完成"
```

### 7. resume_manager → completed

```yaml
freely_exit_kind: resume_manager
a2a_task_state: completed
http_status: 200 OK
语义: Worker 完成任务，返回 Manager 继续编排
示例: |
  Worker 完成子任务，返回 Manager
  - completion_summary: "子任务完成"
  - next_action: "等待 Manager 后续指令"
```

### 8. stop_ai → failed

```yaml
freely_exit_kind: stop_ai
a2a_task_state: failed
http_status: 500 Internal Server Error
语义: AI 停止/失败，需要人工干预
示例: |
  AI 遇到无法恢复的错误:
  - 工具崩溃
  - 认证失败
  - 超出资源限制
```

## 逆向映射 (A2A Task state → exit_kind)

| A2A Task state | 可能的 exit_kind | 说明 |
|----------------|------------------|------|
| `submitted` | `manager_working`, `delegate_workers` | 需要上下文判断 |
| `working` | `worker_working` | 唯一 |
| `completed` | `worker_done`, `resume_manager` | 需要 context 判断 |
| `failed` | `stop_ai` | 唯一 |
| `input-required` | `worker_blocked` | 唯一 |
| `pending-input` | `worker_handoff_needed` | 唯一 |

## 状态转换示例

### 场景 1: Bug 修复

```
1. manager_working → submitted
   Manager scan 发现 bug，创建 Task

2. worker_working → working
   Worker 接收任务，开始修复

3. worker_done → completed
   Worker 完成修复，返回结果
```

### 场景 2: 阻塞恢复

```
1. manager_working → submitted
   Manager 委派任务

2. worker_working → working
   Worker 开始执行

3. worker_blocked → input-required
   Worker 遇到问题，需要输入

4. manager 提供输入后
   input-required → working
   Worker 继续执行

5. worker_done → completed
   Worker 完成
```

### 场景 3: 委派子任务

```
1. manager_working → submitted
   Manager 创建父任务

2. delegate_workers → submitted
   Manager 委派子任务

3. 子任务 worker_working → working

4. 子任务 worker_done → completed

5. resume_manager → completed
   父任务完成，返回 Manager
```

## 实现注意事项

1. **状态转换必须原子**: Task 状态转换必须保证原子性
2. **历史记录**: 记录完整的状态转换历史
3. **超时处理**: `working` 状态超时后转换到 `failed`
4. **错误恢复**: `failed` 状态可重试或人工干预

## 参考

- [A2A Task State Machine](https://github.com/A2A-Specification/A2A)
- [Freely Handoff 机制](./handoff.md)