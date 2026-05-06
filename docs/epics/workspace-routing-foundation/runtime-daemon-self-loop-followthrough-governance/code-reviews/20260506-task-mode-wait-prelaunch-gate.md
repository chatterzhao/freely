# Code Review: task-mode wait pre-launch gate

- issue_id: `I-20260506T1000Z-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/I-20260506T1000Z-A-task-mode-wait-prelaunch-gate.md`
- review_date: `2026-05-06`
- reviewer: `human`
- status: `verified`
- source_branch: `feature/raw-20260506T1000Z-task-mode-wait-prelaunch-gate`
- source_candidate: `docs/pre-brainstorms/20260506T1000Z--task-mode-wait-prelaunch-gate/candidates.md#C-20260506T1000Z-A`

## Implementation Decision Note

- decision: `Supervisor 循环 select_launch_kind 前增加 manager 专属 task_mode=wait 前置门禁`
- why_this: `两段式门禁：前置阻止发射，后置（已有）等待 AI 自然结束。最小侵入（9行），与现有代码正交。仅对 manager 生效，worker 不受 task_mode 约束。`
- alternatives_considered: `build_prompt 内部检查（浪费资源）、移除后置门禁改为纯前置（失去运行中切 wait 的优雅等待能力）`
- boundary_non_goals: `不修改后置门禁行为、不改变 worker 调度逻辑、不增加新配置项`
- residual_risk: `无。wait 模式下 supervisor 持续 polling task_mode_gate，用户切换模式后自动恢复。`

## Test Results

- wait 模式启动：supervisor L220/L232 polling 60s+，无 L020/L040 - PASS
- 切到 auto：L021 prompt_build → L040 ai_launch - PASS
- worker 不受影响（role_hint guard）- PASS
