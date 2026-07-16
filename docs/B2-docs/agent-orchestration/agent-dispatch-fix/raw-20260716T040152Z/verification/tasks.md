# Tasks: Agent 编排链路缺陷修复

- issue_id: I-20260716T040152Z-A
- owner: zhaoquan

## Phase 1: 紧急修复 Bug 1 + 测试

- [ ] **Task 1.1**: `a2a_task.py` a2a-exit argparse 添加 `--reason` 参数
  - 文件: `docs/system/workspace/scripts/runtime/a2a_task.py`
  - 在 p_exit.add_argument 中添加 `--reason` (约 line 829)
  - 参考: `update` 子命令的 `--reason` 定义 (line 725)

- [ ] **Task 1.2**: `a2a_task.py` a2a-exit handler 传递 `reason` 到 A2A client
  - 文件: `docs/system/workspace/scripts/runtime/a2a_task.py`
  - 在 `c.create()` 和 `c.update()` 调用中添加 `reason=getattr(args, 'reason', '') or ""`

- [ ] **Task 1.3**: 创建 `tests/test_a2a_exit_reason.py` 单元测试
  - 测试 a2a-exit --reason 参数解析
  - 测试 reason 正确传递到 A2A client create/update

- [ ] **Task 1.4**: 创建 `tests/test_agent_orchestration_e2e.py` 端到端测试
  - 测试 a2a-exit → A2A task → reason 字段完整链路
  - 测试 watchdog_sse 收到 reason 后的路由决策

## Phase 2: 修复竞态和静默失败

- [ ] **Task 2.1**: `freely-cycle` 移除 reviewer 分配逻辑
  - 文件: `bin/freely-cycle`
  - 移除 lines 86-117 中的内联 Python reviewer 分配代码
  - 保留状态查询和 poll 功能

- [ ] **Task 2.2**: `agent_working.py` update_only 失败时输出错误日志
  - 文件: `docs/system/workspace/scripts/runtime/agent_working.py`
  - 在 agent_assign 的 upsert_only 路径添加 stderr 日志

- [ ] **Task 2.3**: 更新 `tests/test_agent_working_logic.py` 添加 update_only 错误处理测试

## Phase 3: 修复入口一致性和参数不一致

- [ ] **Task 3.1**: 创建 `bin/a2a-exit` wrapper
  - 调用 `python3 $ROOT_DIR/docs/system/workspace/scripts/runtime/a2a_task.py a2a-exit "$@"`

- [ ] **Task 3.2**: 统一 `--status`/`--state` 参数兼容
  - 文件: `a2a_task.py` list 子命令
  - 添加 `--status` → `--state` 映射（如未完成）

- [ ] **Task 3.3**: 更新 agent 文档 (manager-agent.md, worker-agent.md)
  - 统一 a2a-exit 调用方式
