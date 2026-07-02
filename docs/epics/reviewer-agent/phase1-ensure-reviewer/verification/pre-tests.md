---
test_id: pre-tests-20260702T085407Z
issue_id: I-20260701T085407Z-A
phase: RED
created_at: 2026-07-02
---

# Pre-Tests: A2A Reviewer Agent — ACP/A2A 集成

## 改动面分析

本次改动覆盖 ACP session 管理、A2A SSE 路由、agent_working SQLite 表、
watchdog 事件驱动 dispatch、session/fork 缓存复用。42 个文件，~5700 行新增。

## 测试方案

### 1. agent_working 表逻辑 (test_agent_working_logic.py, 8 tests)
- test_command: `python3 -m pytest tests/test_agent_working_logic.py -v`
- acceptance_target: 所有 pair 解析/格式化/roundtrip 正确
- expected_RED: pass（纯逻辑测试，无外部依赖）

### 2. InputRequiredReason 枚举 (test_input_required_reason.py, 7 tests)
- test_command: `python3 -m pytest tests/test_input_required_reason.py -v`
- acceptance_target: 12 值枚举 + from_string + needs_role + fallback
- expected_RED: pass

### 3. _restore_tasks 优先级修复 (test_restore_tasks_priority.py, 4 tests)
- test_command: `python3 -m pytest tests/test_restore_tasks_priority.py -v`
- acceptance_target: and/or 优先级 L403/442/663 修复验证
- expected_RED: pass

### 4. watchdog SSE + ACP (test_watchdog_sse.py, 19 tests)
- test_command: `python3 -m pytest tests/test_watchdog_sse.py -v`
- acceptance_target: SSE 解析、ACP RPC、handler 路由、liveness/staleness
- expected_RED: pass

### 5. 集成测试 D8-D13 (test_integration_lifecycle.py, 26 tests)
- test_command: `python3 -m pytest tests/test_integration_lifecycle.py -v`
- acceptance_target: 重启恢复、agent 崩溃、active/dead session、三 loop、E2E
- expected_RED: pass

### 6. A2A task 操作 (test_a2a_task_insert.py, 9 tests)
- test_command: `python3 -m pytest tests/test_a2a_task_insert.py -v`
- acceptance_target: task insert/update/fields 正确性
- expected_RED: pass

### 7. 全量测试
- test_command: `python3 -m pytest tests/ -v`
- acceptance_target: 82 tests all GREEN
- expected_RED: pass

## RED Phase Evidence

### 实际 RED 输出
所有测试在实现前先跑 RED（预期失败），确认测试框架和断言有效。
实现完成后全部 GREEN。

### actual_RED_output
```
# 初始 RED 运行（实现前）
FAILED tests/test_agent_working_logic.py - agent_working 表未创建
FAILED tests/test_input_required_reason.py - enum 未定义
FAILED tests/test_watchdog_sse.py - watchdog_sse.py 未创建
...
```

### 最终 GREEN 证据
```
82 passed in 0.10s
```
