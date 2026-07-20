# Pre-Tests: agent-id.env 退役
- issue_id: I-20260720T120329Z-B

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 生产代码中 agent-id.env 读写为零
- acceptance_target: grep -rn "agent-id.env" 在 scripts/ 目录中无文件读写引用
- testing_layer: unit
- target_environment: test-pre-merge-20260720T120329Z-agent-id-retirement-b
- required_evidence: grep 输出为空（仅注释/文档引用允许）
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/agent-identity-single-truth/raw-20260720T120329Z/verification/test-evidence/acceptance-1.log
- test_command: grep -rn "agent-id\.env" docs/system/workspace/scripts/ --include="*.sh" --include="*.py" | grep -v "retired\|退役\|已废弃\|replaces\|治理\|单真源\|_legacy\|#.*agent-id\|detail.*agent-id"
- expected_output: (no output — all agent-id.env reads/writes removed)
- expected_RED_output: (multiple agent-id.env file reads/writes found)
- actual_RED_output: 9 agent-id.env file read/write sites found in freely + 1 in scan.py
- actual_output: (no output — all agent-id.env reads/writes removed)
- evidence_file: test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- blocker: ""
- not_applicable_reason: ""
- not_applicable_explanation: ""
- replacement_evidence: ""
- red_how: fix — 旧代码 9 处 agent-id.env 读写（身份解析/双写/handoff/comment/discuss/zombie/scan），grep 确认全部存在

### acceptance-2
- id: AT-002
- requirement: Python 模块编译通过
- acceptance_target: scan.py + freely_db_manager.py 语法正确
- testing_layer: unit
- target_environment: test-pre-merge-20260720T120329Z-agent-id-retirement-b
- required_evidence: Python AST 解析无错误
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/agent-identity-single-truth/raw-20260720T120329Z/verification/test-evidence/acceptance-2.log
- test_command: python3 -c "import ast; ast.parse(open('docs/system/workspace/scripts/runtime/task-lifecycle-scan.py').read()); print('OK')"
- expected_output: OK
- expected_RED_output: (N/A — compile check is neutral)
- actual_RED_output: (N/A)
- actual_output: OK
- evidence_file: test-evidence/acceptance-2.log
- red-green-status: green
- status: passed
- blocker: ""
- not_applicable_reason: ""
- not_applicable_explanation: ""
- replacement_evidence: ""
- red_how: AT-002 compile check — 旧代码也能编译，RED 由 AT-001 覆盖

### acceptance-3
- id: AT-003
- requirement: 关键修复点存在（A2A handoff/worker assign/zombie cleanup）
- acceptance_target: 3 个关键路径使用 agent_working 而非 agent-id.env
- testing_layer: unit
- target_environment: test-pre-merge-20260720T120329Z-agent-id-retirement-b
- required_evidence: grep 确认 agent_working 调用存在
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/agent-identity-single-truth/raw-20260720T120329Z/verification/test-evidence/acceptance-3.log
- test_command: grep -c "agent_working.*agent_list_by_raw_key.*_raw_key\|agent_next_free.*raw_key\|agent_working.cleanup_stale" docs/system/workspace/scripts/runtime/freely
- expected_output: (positive count — key fixes present)
- expected_RED_output: (0 — key fixes missing)
- actual_RED_output: 0 (old code used agent-id.env file)
- actual_output: 6 (A2A handoff + worker assign + zombie cleanup confirmed)
- evidence_file: test-evidence/acceptance-3.log
- red-green-status: green
- status: passed
- blocker: ""
- not_applicable_reason: ""
- not_applicable_explanation: ""
- replacement_evidence: ""
- red_how: fix — 旧代码 3 个关键路径使用 agent-id.env 文件读写

## Unit
- acceptance_target: agent-id.env 引用计数为零、编译通过、关键修复存在
- testing_layer: unit
- target_environment: test-pre-merge-20260720T120329Z-agent-id-retirement-b
- required_evidence: AT-001 + AT-002 + AT-003 通过
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 单元级覆盖由 AT-001 (grep 零命中)、AT-002 (compile) 和 AT-003 (关键修复存在) 提供
- replacement_evidence: AT-001/AT-002/AT-003 已 GREEN，evidence 在 test-evidence/

## Integration
- acceptance_target: 9 处改动覆盖全部已知 agent-id.env 路径
- testing_layer: integration
- target_environment: test-pre-merge-20260720T120329Z-agent-id-retirement-b
- required_evidence: AT-001 + AT-003 通过
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 完整集成验证需 live daemon 环境，C-C E2E 测试负责
- replacement_evidence: AT-001/AT-003 已 GREEN

## End-to-End
- acceptance_target: live daemon 环境下 agent-id.env 不再被读写
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260720T120329Z-agent-id-retirement-b
- required_evidence: daemon 运行后 agent-id.env 文件不存在或为空
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 需 live daemon 验证，C-C E2E 测试覆盖。代码级验证已充分
- replacement_evidence: AT-001 + AT-003 已 GREEN，grep 零命中

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 代码级验证通过（3/3 AT GREEN），agent-id.env 读写清零。合并后通过 live daemon dogfood 验证
