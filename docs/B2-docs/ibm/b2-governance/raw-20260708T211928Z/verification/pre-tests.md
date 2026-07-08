# Pre-Tests: scan classify fix
- issue_id: I-20260708T211928Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: I-* issue正确读取phase_state并分类为i_non_terminal
- acceptance_target: 15个I-* issue不是raw_not_started而是i_non_terminal
- testing_layer: integration
- target_environment: test-pre-merge-20260708T211928Z-scan-classify-fix
- required_evidence: scan输出中i_non_terminal站有15个item,phase_state非空
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260708T211928Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/runtime/task-lifecycle-scan.py --project . 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); items=[i for i in d['items'] if i.get('station')=='i_non_terminal']; assert len(items)==15; assert all(i.get('phase_state','')!='' for i in items); print(f'i_non_terminal={len(items)} all_have_phase=TRUE PASS')"
- expected_output: i_non_terminal=15 all_have_phase=TRUE PASS
- expected_RED_output: i_non_terminal=0 or phase_state空
- actual_RED_output: (RED)
- actual_output: (GREEN)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: (失败时填写)
- red_how: fix — 修改前parse_frontmatter不读bullet, phase_state为空

### acceptance-2
- id: AT-002
- requirement: raw_not_started的next_action含--kind fix
- acceptance_target: 所有wt-create用--kind fix
- testing_layer: integration
- target_environment: test-pre-merge-20260708T211928Z-scan-classify-fix
- required_evidence: grep确认--kind fix出现
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260708T211928Z/verification/test-evidence/acceptance-2.log
- test_command: python3 docs/system/workspace/scripts/runtime/task-lifecycle-scan.py --project . 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); rns=[i for i in d['items'] if i.get('station')=='raw_not_started']; assert all('--kind fix' in i.get('next_action','') for i in rns); assert all('--skill' not in i.get('next_action','') for i in rns); print(f'all_raw_not_started_have_--kind_fix=TRUE PASS')"
- expected_output: all_raw_not_started_have_--kind_fix=TRUE PASS
- expected_RED_output: --skill存在
- actual_RED_output: (RED)
- actual_output: (GREEN)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: (失败时填写)
- red_how: fix — 修改前用--skill

### acceptance-3
- id: AT-003
- requirement: 无误扫(terminal不会分到非sync站)
- acceptance_target: phase_state=terminal的item只在sync_batch或merged_develop站
- testing_layer: integration
- target_environment: test-pre-merge-20260708T211928Z-scan-classify-fix
- required_evidence: 0个terminal误分
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260708T211928Z/verification/test-evidence/acceptance-3.log
- test_command: python3 docs/system/workspace/scripts/runtime/task-lifecycle-scan.py --project . 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); TERMINAL={'absorbed','dropped','completed'}; wrong=[i for i in d['items'] if i.get('phase_state','') in TERMINAL and i.get('station') not in ('platform_sync_batch','merged_develop')]; print(f'wrong_terminal={len(wrong)}'); assert len(wrong)==0; print('PASS')"
- expected_output: wrong_terminal=0 PASS
- expected_RED_output: wrong_terminal>0
- actual_RED_output: (RED)
- actual_output: (GREEN)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: (失败时填写)
- red_how: fix — 修改前I-* terminal可能误分为raw_created

## Unit
- acceptance_target: py_compile通过
- testing_layer: unit
- target_environment: fix/raw-20260708T211928Z-scan-classify-fix
- required_evidence: python3 -m py_compile 通过
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 编译检查在dev阶段确认
- replacement_evidence: python3 -m py_compile 通过

## Integration
- acceptance_target: scan正确分类所有275个原始items
- testing_layer: integration
- target_environment: test-pre-merge-20260708T211928Z-scan-classify-fix
- required_evidence: 4站覆盖所有items
- blocker_taxonomy: execution_pending_or_failed

## End-to-End
- acceptance_target: develop merge chain
- testing_layer: end-to-end
- target_environment: test-pre-merge → develop
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pass
- real_environment_reason: scan对develop运行, 分类验证通过
