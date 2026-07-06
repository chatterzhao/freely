# Tasks: A2A 状态管理全量修复

## C 组：审计 bug（优先——运行时缺陷）

- [x] C1: wt-close:683 `--state consumed` → `--state completed`
- [x] C2: a2a_task.py:869 `update` CLI 补传 `--reason/--completion-summary/--next-action` 到服务器
- [x] C3: a2a_task.py:640 `VALID_STATES` 加 `canceled`
- [x] C4: freely_db_manager.py:224 CHECK 约束加 `pending-input`
- [x] C5: a2a_server.py:538 PATCH `sm` dict 拒绝未知状态（去掉 fallback `body["state"]`）
- [x] C6: freely_db_manager.py:1105 删除死代码 `h_a2a_task_update_from_exit_kind`

## A 组：架构修正

- [x] A0: freely:20273 删除 `working→input-required` —— stop 只杀进程不动 A2A state

## A 组：重启状态修正（_restore_tasks）

- [x] A1: `working` + `worker_pid` 为空 → `input-required`
- [x] A2: `submitted`(Manager) 只检查活跃 Worker（过滤 `completed/failed/canceled`）
- [x] A3: `input-required` + worktree 路径不存在 → `failed`

## B 组：重启环境恢复（_restore_tasks 后通知 Manager）

- [x] B1: working+PID存活+worktree在 → `a2a_task.py prompt --task-id X --message "resume"`
- [x] B2: 状态修正为 `failed` → SSE 注入 "Worker X died: {reason}"
- [x] B3: `input-required`+worktree在 → SSE 注入 "Worker X needs input: {reason}"
- [x] B4: `submitted`(Manager)+活跃Worker → SSE 注入 "Restored: Worker X still running"
