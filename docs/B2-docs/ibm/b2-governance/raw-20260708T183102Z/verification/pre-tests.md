# Pre-Tests: pr-merge path + wt-close + worktree resolution
- issue_id: I-20260708T183102Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: pr-merge-guarded _sync_issues_changed_in_merge 从 worktree 读 issue.md
- acceptance_target: 第 459 行 issues_dir 指向 worktree 而非 develop
- testing_layer: integration
- target_environment: test-pre-merge-20260708T183102Z-pr-merge-wtclose-fix
- required_evidence: grep 确认代码路径
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260708T183102Z/verification/test-evidence/acceptance-1.log
- test_command: grep -n 'issues_dir=' docs/system/workspace/scripts/worktree/pr-merge-guarded
- expected_output: 含 _wt_path/docs/B1-docs
- expected_RED_output: 含 $PWD/docs/B1-docs
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: green
- status: passed
- blocker: (失败时填写)
- red_how: fix — 当前 L459 为 $PWD/docs/B1-docs

### acceptance-2
- id: AT-002
- requirement: pr-merge-guarded worktree 解析用 raw_key
- acceptance_target: 不再使用 awk index + head -1
- testing_layer: integration
- target_environment: test-pre-merge-20260708T183102Z-pr-merge-wtclose-fix
- required_evidence: grep 确认解析逻辑含 raw_key
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260708T183102Z/verification/test-evidence/acceptance-2.log
- test_command: grep -c 'raw_key\|_raw_key' docs/system/workspace/scripts/worktree/pr-merge-guarded
- expected_output: 计数 >= 2（原来至少 1 处，新增 at least 1 处）
- expected_RED_output: 计数为 1（只有 auto-sync test worktree 那一处）
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: green
- status: passed
- blocker: (失败时填写)
- red_how: fix — 当前 worktree 解析不用 raw_key

### acceptance-3
- id: AT-003
- requirement: wt-close 检测 platform_state: closed → 跳过 issue-sync
- acceptance_target: Phase 2 有 platform_state 检测逻辑
- testing_layer: integration
- target_environment: test-pre-merge-20260708T183102Z-pr-merge-wtclose-fix
- required_evidence: grep 确认 platform_state 检测
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260708T183102Z/verification/test-evidence/acceptance-3.log
- test_command: grep -n 'platform_state.*closed\|platform_state.*!=.*closed' docs/system/workspace/scripts/worktree/wt-close
- expected_output: 含有跳过逻辑
- expected_RED_output: 无 platform_state: closed 检测
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: green
- status: passed
- blocker: (失败时填写)
- red_how: fix — 当前无条件执行 issue-sync close

### acceptance-4
- id: AT-004
- requirement: wt-close 无 updated_at 时间戳写入
- acceptance_target: 第 752 行不再写 updated_at
- testing_layer: integration
- target_environment: test-pre-merge-20260708T183102Z-pr-merge-wtclose-fix
- required_evidence: grep 确认无 updated_at 写入
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260708T183102Z/verification/test-evidence/acceptance-4.log
- test_command: grep -c '_fm_set_str.*updated_at.*date' docs/system/workspace/scripts/worktree/wt-close || echo "0"
- expected_output: 0
- expected_RED_output: 1（第 752 行）
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: green
- status: passed
- blocker: (失败时填写)
- red_how: fix — 当前第 752 行写 updated_at

### acceptance-5
- id: AT-005
- requirement: wt-close 吸收 I-* 路径不写 develop
- acceptance_target: _wt_i_file 路径使用 worktree 而非 PROJECT_ROOT
- testing_layer: integration
- target_environment: test-pre-merge-20260708T183102Z-pr-merge-wtclose-fix
- required_evidence: grep 确认路径逻辑
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260708T183102Z/verification/test-evidence/acceptance-5.log
- test_command: grep -n '_wt_i_file=' docs/system/workspace/scripts/worktree/wt-close
- expected_output: 含 wt_path 而非 PROJECT_ROOT
- expected_RED_output: 含 PROJECT_ROOT
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: green
- status: passed
- blocker: (失败时填写)
- red_how: fix — 当前 L743 用 PROJECT_ROOT

## Unit
- acceptance_target: 每处修改语法正确
- testing_layer: unit
- target_environment: fix/raw-20260708T183102Z-pr-merge-wtclose-fix
- required_evidence: bash -n 语法检查通过
- blocker_taxonomy: execution_pending_or_failed

## Integration
- acceptance_target: 修改后 pr-merge-guarded 能正确找到并 sync issue
- testing_layer: integration
- target_environment: test-pre-merge-20260708T183102Z-pr-merge-wtclose-fix
- required_evidence: dry-run 输出显示 synced N issue(s)
- blocker_taxonomy: execution_pending_or_failed

## End-to-End
- acceptance_target: 完整 fix → PR → merge → wt-close 链路无 diff 阻塞
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260708T183102Z-pr-merge-wtclose-fix → develop merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 同类型 bug (platform_state + updated_at) 已在 PR #3817/#3823 修复验证
