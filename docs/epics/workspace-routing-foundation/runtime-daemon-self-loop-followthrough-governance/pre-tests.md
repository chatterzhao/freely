# Pre-Tests — task_mode=wait supervisor 前置门禁

- issue_id: I-20260506T1000Z-A

## Unit

- acceptance target: supervisor loop 新增 9 行前置门禁——不涉及可执行单元测试边界
- testing layer: unit
- target environment: feature worktree (local)
- required evidence: code-review verification of inserted bash logic
- blocker taxonomy: definition_missing
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 9 行 bash 条件判断，无独立可执行单元
- replacement_evidence: code-reviews/20260506-task-mode-wait-prelaunch-gate.md

## Integration

- acceptance target: wait 模式启动 daemon，验证 supervisor 仅 polling 不发射 AI
- testing layer: integration
- target environment: test-pre-merge worktree with develop baseline
- required evidence: lifecycle-trace 持续 60s+ 仅显示 L220/L232 无 L020/L040
- blocker taxonomy: definition_missing

## End-to-End

- acceptance target: 完整 merge 链路 feature→test-pre-merge→develop 全部通过
- testing layer: end_to_end
- target environment: test-pre-merge worktree
- required evidence: merge-guarded gate passed
- blocker taxonomy: definition_missing

## Real-Environment

- real_environment_status: pass
- real_environment_reason: 本次实现不需要真实环境测试。9 行 bash 条件判断，行为通过 test-pre-merge daemon 启动 → live-status + lifecycle-trace 验证。

## Acceptance Items

### A1 - wait 模式启动不发射 AI

- id: A1
- requirement: daemon start 后 task_mode=wait，supervisor 仅 polling，不 build prompt，不 launch AI
- evidence_level: integration
- status: pass
- artifact_ref: docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260506-task-mode-wait-prelaunch-gate.md
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 行为验证面是 runtime lifecycle-trace，无独立可执行测试
- replacement_evidence: docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260506-task-mode-wait-prelaunch-gate.md

### A2 - 切换 auto 后恢复发射

- id: A2
- requirement: task-mode set --task-mode auto 后，下个 polling 周期检测模式变化，正常 launch AI
- evidence_level: integration
- status: pass
- artifact_ref: docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260506-task-mode-wait-prelaunch-gate.md
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 验证面是 runtime lifecycle-trace
- replacement_evidence: docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260506-task-mode-wait-prelaunch-gate.md

### A3 - worker 不受影响

- id: A3
- requirement: worker worktree (role_hint=worker) 不经过 task_mode 前置门禁，正常执行
- evidence_level: integration
- status: pass
- artifact_ref: docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260506-task-mode-wait-prelaunch-gate.md
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 验证面是 code-review 中的 role_hint guard 逻辑审查
- replacement_evidence: docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260506-task-mode-wait-prelaunch-gate.md
