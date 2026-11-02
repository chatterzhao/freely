# Pre-Tests: 受控调用方显式标记
- issue_id: I-20261102T103216Z-A

## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: reference-transaction 在 FREELY_WT_CREATE=1 时放行受控分支创建，无标记时拦截
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: repo hooks, no ps
- required_evidence: hook 返回值
- evidence_level: mock
- artifact_ref: docs/system/workspace/scripts/tests/test-guarded-caller-markers
- test_command: bash docs/system/workspace/scripts/tests/test-guarded-caller-markers
- expected_output: AT-001 PASS（带标记 rc=0，无标记 rc!=0）
- expected_RED_output: 带标记仍 rc!=0，提示 Branch creation blocked
- actual_RED_output: AT-001 FAIL: rc=1, Branch creation blocked
- actual_output: AT-001 PASS: marker allows managed branch
- evidence_file: docs/B2-docs/git-worktree/wt-close/raw-20261102T103216Z/verification/test-evidence/test-guarded-caller-markers.log
- red-green-status: green
- status: passed
- blocker: execution_pending_or_failed

### acceptance-2
- id: AT-002
- requirement: pre-push 在 FREELY_ALLOW_REMOTE_BRANCH_DELETE=1 时不拦删除，无标记时拦截
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: repo hooks, no ps
- required_evidence: hook 返回值与 stderr
- evidence_level: mock
- artifact_ref: docs/system/workspace/scripts/tests/test-guarded-caller-markers
- test_command: bash docs/system/workspace/scripts/tests/test-guarded-caller-markers
- expected_output: AT-002 PASS（带标记无拦截文案，无标记拦截）
- expected_RED_output: 带标记仍出现远程分支删除被拦截
- actual_RED_output: AT-002 FAIL: still blocked
- actual_output: AT-002 PASS: marker allows remote delete
- evidence_file: docs/B2-docs/git-worktree/wt-close/raw-20261102T103216Z/verification/test-evidence/test-guarded-caller-markers.log
- red-green-status: green
- status: passed
- blocker: execution_pending_or_failed

### acceptance-3
- id: AT-003
- requirement: 真实 wt-create 在 ps 不可用环境能创建 fix 工位
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: integration
- target_environment: macOS sandbox without ps
- required_evidence: wt-create 成功日志
- evidence_level: integration
- artifact_ref: docs/B2-docs/git-worktree/wt-close/raw-20261102T103216Z/verification/test-evidence/wt-create-success.log
- test_command: 见 test-guarded-caller-markers AT-003 段（读取日志断言）
- expected_output: 日志含 Creating fix worktree 且无 Branch creation blocked
- expected_RED_output: 日志含 Branch creation blocked
- actual_RED_output: Branch creation blocked
- actual_output: Creating fix worktree, no Branch creation blocked
- evidence_file: docs/B2-docs/git-worktree/wt-close/raw-20261102T103216Z/verification/test-evidence/wt-create-success.log
- red-green-status: green
- status: passed
- blocker: execution_pending_or_failed

## Unit
- acceptance_target: 两个 hook 的标记分支
- testing_layer: unit
- target_environment: repo hooks
- required_evidence: AT-001 + AT-002
- blocker_taxonomy: execution_pending_or_failed
1. 运行 test-guarded-caller-markers，断言 AT-001/AT-002。

## Integration
- acceptance_target: 真实 wt-create 路径
- testing_layer: integration
- target_environment: 无 ps 的 macOS 沙箱
- required_evidence: AT-003
- blocker_taxonomy: execution_pending_or_failed
1. 运行测试脚本的 AT-003 段，断言 wt-create 成功日志。

## End-to-End
- acceptance_target: n/a
- testing_layer: end-to-end
- target_environment: n/a
- required_evidence: n/a
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 端到端需要真实双平台推送与删除，由 post-merge 的 wt-close 验证。
- replacement_evidence: AT-003 + 合并后 wt-close 远程删除

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 在真实仓库 hook 与真实沙箱下执行；wt-create 已实际建出本工位。
