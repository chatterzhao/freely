### C-20260506T1000Z-A

- title: `task_mode=wait supervisor 前置门禁`
- status: `promoted`
- scope: supervisor 循环 `select_launch_kind` 前增加 manager 专属 wait 检查，阻止 build prompt + launch AI。仅新增 9 行 bash。
- priority: `P0`
- type: `fix`
- milestone: `M-20260306-workspace-routing-foundation`
- route_kind: `discovery`
- acceptance_criteria:
  - wait 模式启动 daemon：supervisor 仅 L220/L232 polling，无 L020 prompt_build / L040 ai_launch
  - 切到 auto 模式：前置门禁检测到模式变化，正常发射 AI
  - worker 不受影响
  - 与现有后置门禁（stop_ai handler）正交
- promotion_gate: `governance-merge-gate`
- open_questions: []
- acceptance_reviews:
  - reviewer: `human`
  - status: `verified`
- next_action: `进入 B2_IBM，materialize I-*，实施修复`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/I-20260506T1000Z-A-task-mode-wait-prelaunch-gate.md`

### 变更后的 INDEX 条目
- `20260506T1000Z--task-mode-wait-prelaunch-gate`: `candidates.md`（本文件）、`brainstorms.md`
