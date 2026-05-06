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
