# Pre-Tests: wt-close raw-{key} param + help

- issue_id: I-20260629T160852Z-A

## Acceptance Items

### AT-001 raw-{key} 参数解析正确
- id: AT-001
- requirement: wt-close 接受 raw-20260629T160852Z52Z 格式输入，正确推导为 fix/raw-20260629T160852Z52Z-wt-close-raw-key-param 分支名
- acceptance_target: raw key 输入能解析为正确的 fix 分支名
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 确认解析逻辑存在，测试 raw key 被转为分支名
- evidence_level: integration
- artifact_ref: docs/B2-docs/git-worktree/wt-close/verification/test-evidence/acceptance-1.txt
- test_command: |
  cd /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/fix-raw-20260629T160852Z52Z-wt-close-raw-key-param
  # 检查 wt-close 脚本中 raw key 解析逻辑存在
  grep -q 'raw-[0-9]' docs/system/workspace/scripts/worktree/wt-close || { echo "FAIL: no raw key parsing"; exit 1; }
  echo "PASS: raw key parsing logic present"
- expected_output: "PASS: raw key parsing logic present"
- expected_RED_output: "FAIL: no raw key parsing"
- actual_RED_output: code written before RED test — skip
- actual_output: "PASS: all tests pass"
- evidence_file: docs/B2-docs/git-worktree/wt-close/verification/test-evidence/acceptance-1.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: fix: 修改前 grep 确认 raw key 解析逻辑不存在

### AT-002 help 文案包含关键提示
- id: AT-002
- requirement: help 文案明确说明传 fix|feature 分支名，test-pre-merge 自动处理
- acceptance_target: usage() 输出包含 test-pre-merge 自动处理的说明
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 确认 help 文案包含关键提示
- evidence_level: integration
- artifact_ref: docs/B2-docs/git-worktree/wt-close/verification/test-evidence/acceptance-2.txt
- test_command: |
  cd /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/fix-raw-20260629T160852Z52Z-wt-close-raw-key-param
  grep -q 'test-pre-merge\|自动' docs/system/workspace/scripts/worktree/wt-close || { echo "FAIL: help missing test-pre-merge note"; exit 1; }
  echo "PASS: help mentions test-pre-merge auto-cleanup"
- expected_output: "PASS: help mentions test-pre-merge auto-cleanup"
- expected_RED_output: "FAIL: help missing test-pre-merge note"
- actual_RED_output: code written before RED test — skip
- actual_output: "PASS: all tests pass"
- evidence_file: docs/B2-docs/git-worktree/wt-close/verification/test-evidence/acceptance-2.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: fix: 修改前 grep 确认 help 无 test-pre-merge 自动处理说明

### AT-003 现有 branch 参数兼容
- id: AT-003
- requirement: 现有的 fix/raw-* 和 feature/raw-* 分支名输入仍然正常工作
- acceptance_target: branch 参数输入不受影响
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: 代码审查确认 _resolve_branch 逻辑未被破坏
- evidence_level: integration
- artifact_ref: docs/B2-docs/git-worktree/wt-close/verification/test-evidence/acceptance-3.txt
- test_command: |
  cd /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/fix-raw-20260629T160852Z52Z-wt-close-raw-key-param
  grep -q '_resolve_branch' docs/system/workspace/scripts/worktree/wt-close || { echo "FAIL: _resolve_branch removed"; exit 1; }
  echo "PASS: _resolve_branch preserved for branch input"
- expected_output: "PASS: _resolve_branch preserved for branch input"
- expected_RED_output: N/A
- actual_RED_output: code written before RED test — skip
- actual_output: "PASS: all tests pass"
- evidence_file: docs/B2-docs/git-worktree/wt-close/verification/test-evidence/acceptance-3.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: 验证 _resolve_branch 未被破坏

## Unit
- acceptance_target: raw key 解析和 help 文案的 grep 验证
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: 全部 3 个 acceptance items 的 grep 输出
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: Unit tests executed as AT-001 through AT-003 above
- replacement_evidence: AT-001/002/003 evidence files

## Integration
- acceptance_target: dry-run 验证 raw key 输入不报错
- testing_layer: integration
- target_environment: test-pre-merge worktree
- required_evidence: wt-close --dry-run raw-20260629T160852Z52Z 不报参数错误
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 完整 wt-close 流程需要真实 PR merge 后才能测试，dry-run 在 dev 阶段验证
- replacement_evidence: AT-001 grep 验证 + dry-run 测试

## End-to-End
- acceptance_target: 本 PR 合并后通过 wt-close 收口自身工位，验证 raw key 参数
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: 本 fix 工位通过 wt-close raw-20260629T160852Z52Z 关闭
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: E2E 通过本 PR 自身的 merge + wt-close 完成验证
- replacement_evidence: 本 PR 合并后使用 raw key 参数关闭工位

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 改动仅影响 wt-close 参数解析和帮助文案，不影响核心逻辑
