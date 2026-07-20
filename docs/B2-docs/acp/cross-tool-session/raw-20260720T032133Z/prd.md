# PRD: Manager prompt 委派决策规则
- issue_id: I-20260720T032133Z-A

## Goal
Manager prompt明确引导AI在已委派raw_key上使用a2a_task.py prompt（session/prompt）而非a2a-exit --state submitted（session/new）。

## Implementation
- 文件: docs/system/workspace/scripts/runtime/freely
- 位置: _append_worker_fleet_status_if_needed内的Python代码
- 变更: 表格增加task_id列 + 决策规则文本

## Dev-Loop Handoff
- 改动: 仅prompt模板字符串
- 验证: merge后观察Manager是否正确使用prompt
