# Pre-Tests — task_mode=wait supervisor 前置门禁

- issue_id: I-20260506T1000Z-A

## Unit

- acceptance target: supervisor loop 新增 9 行前置门禁——不涉及可执行单元测试边界
- testing layer: unit
- target environment: feature worktree (local)
- required evidence: grep + diff verification of inserted lines
- blocker taxonomy: definition_missing
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 9 行 bash 条件判断，不涉及可执行单元测试
- replacement_evidence: code-reviews/20260506-task-mode-wait-prelaunch-gate.md

## Integration

- acceptance target: wait 模式启动 daemon，验证 supervisor 仅 polling 不发射 AI
- testing layer: integration
- target environment: test-pre-merge worktree with develop baseline
- required evidence: lifecycle-trace 仅显示 L220/L232，无 L020/L040
- blocker taxonomy: definition_missing
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 验证面是 runtime 行为，通过 live-status + lifecycle-trace 确认
- replacement_evidence: code-reviews/20260506-task-mode-wait-prelaunch-gate.md

## End-to-End

- acceptance target: 完整 merge 链路 feature→test-pre-merge→develop gate 全部通过
- testing layer: end_to_end
- target environment: test-pre-merge worktree
- required evidence: merge-guarded gate passed with governance docs validated
- blocker taxonomy: definition_missing
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 端到端验证面是 gate 链路本身
- replacement_evidence: merge-guarded gate pass log

## Real-Environment

- real_environment_status: pass
- real_environment_reason: 本次实现不需要真实环境测试。9 行 bash 条件判断，行为通过 test-pre-merge daemon 启动验证（live-status + lifecycle-trace），切换 auto 模式后正常发射 AI。

## Acceptance Items

### AI-1: wait 模式不发射 AI

- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- acceptance: daemon start 后 supervisor 仅 L220/L232 polling，无 L020 prompt_build / L040 ai_launch
- evidence: `lifecycle-trace.log` 持续 60s+ 仅 polling entries
- status: `pass`

### AI-2: 切 auto 后正常发射

- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- acceptance: `task-mode set --task-mode auto` 后，下一个 polling 周期检测到模式变化，正常 L020→L021→L040→ai_launch
- evidence: `lifecycle-trace.log` 显示 prompt_build_complete + ai_launch_begin
- status: `pass`

### AI-3: worker 不受影响

- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- acceptance: worker worktree role_hint=worker，前置门禁 role check 跳过，worker 正常执行
- evidence: code review verification (role_hint guard 逻辑审查)
- status: `pass`
