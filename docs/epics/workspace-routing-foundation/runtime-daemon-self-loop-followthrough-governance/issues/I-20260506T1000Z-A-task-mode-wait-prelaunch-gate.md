# I-20260506T1000Z-A: task_mode=wait supervisor 前置门禁

- issue_id: `I-20260506T1000Z-A`
- title: `task_mode=wait supervisor 前置门禁`
- status: `in_verification`
- priority: `P0`
- milestone: `M-20260306-workspace-routing-foundation`
- phase_state: `in_verification`
- source_candidate: `docs/pre-brainstorms/20260506T1000Z--task-mode-wait-prelaunch-gate/candidates.md#C-20260506T1000Z-A`
- source_candidates: `docs/pre-brainstorms/20260506T1000Z--task-mode-wait-prelaunch-gate/candidates.md#C-20260506T1000Z-A`
- promoted_from: `raw-20260506T1000Z`
- platform_ids:
  - github: 231
  - gitee: ""
- pre_tests_path: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/pre-tests.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews`

## Changes

`docs/system/workspace/scripts/runtime/freely` supervisor 循环 L18202：在 `select_launch_kind` 前增加 manager 专属 task_mode=wait 前置门禁（9 行 bash）。

## Implementation Decision Note

- decision: `Supervisor 循环 select_launch_kind 前增加 manager 专属 task_mode=wait 前置门禁`
- why_this: `两段式门禁：前置阻止发射，后置（已有）等待 AI 自然结束。最小侵入（9行），仅对 manager 生效。`
- alternatives_considered: `build_prompt 内部检查（浪费资源）、移除后置门禁改为纯前置（失去运行中切 wait 的优雅等待能力）`
- boundary_non_goals: `不修改后置门禁行为、不改变 worker 调度逻辑、不增加新配置项`
- residual_risk: `无。wait 模式下 supervisor 持续 polling task_mode_gate，用户切换模式后自动恢复。`

## Verification

- test-pre-merge 启动 daemon (task_mode=wait) → 无 prompt build / AI launch
- task-mode set --task-mode auto → 正常发射
- worker 不受影响（role_hint guard）
