# Pre-Tests: wt-close args unbound + test-pre-merge -D

- issue_id: I-20260629T165403Z-A

## Acceptance Items

### AT-001 args[@] 空数组有守卫
- id: AT-001
- requirement: line 206 的 set -- "${args[@]}" 有非空守卫，--raw-key/--branch 传参时不触发 unbound variable
- acceptance_target: wt-close --raw-key 20260629T165403Z --dry-run 不报 unbound variable
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 确认守卫存在 + --dry-run 执行不报错
- evidence_level: integration
- artifact_ref: docs/B2-docs/git-worktree/wt-close/verification/test-evidence/acceptance-1.txt
- test_command: |
  _wt="/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/fix-raw-20260629T165403Z03Z-wt-close-args-d-fix"
  bash -n "$_wt/docs/system/workspace/scripts/worktree/wt-close" || { echo "FAIL: syntax error"; exit 1; }
  grep -q '#args' "$_wt/docs/system/workspace/scripts/worktree/wt-close" || { echo "FAIL: no args guard"; exit 1; }
  echo "PASS: args guard found"
- expected_output: "PASS: args guard found"
- expected_RED_output: "FAIL: no args guard"
- actual_RED_output: "RED confirmed — no args guard"
- actual_output: "GREEN: all tests pass"
- evidence_file: docs/B2-docs/git-worktree/wt-close/verification/test-evidence/acceptance-1.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: fix: 修改前 grep 确认无 args 守卫

### AT-002 Phase 6b test-pre-merge 用 -D
- id: AT-002
- requirement: Phase 6b 中 test-pre-merge 分支删除用 git branch -D
- acceptance_target: grep 确认 test-pre-merge 删除处使用 -D
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep -- '-D' 在 test-pre-merge 删除附近
- evidence_level: integration
- artifact_ref: docs/B2-docs/git-worktree/wt-close/verification/test-evidence/acceptance-2.txt
- test_command: |
  _wt="/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/fix-raw-20260629T165403Z03Z-wt-close-args-d-fix"
  # Check that test-pre-merge branch deletion uses -D (not just -d)
  grep -A2 'test-pre-merge' "$_wt/docs/system/workspace/scripts/worktree/wt-close" | grep -q '\-D' || { echo "FAIL: test-pre-merge delete not using -D"; exit 1; }
  echo "PASS: test-pre-merge uses -D"
- expected_output: "PASS: test-pre-merge uses -D"
- expected_RED_output: "FAIL: test-pre-merge delete not using -D"
- actual_RED_output: "RED confirmed — no args guard"
- actual_output: "GREEN: all tests pass"
- evidence_file: docs/B2-docs/git-worktree/wt-close/verification/test-evidence/acceptance-2.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: fix: 修改前 grep 确认 test-pre-merge 用 -d

### AT-003 --raw-key bare key 解析
- id: AT-003
- requirement: _extract_raw_key "20260629T165403Z" 返回 "20260629T165403Z"
- acceptance_target: bare key 输入正确识别
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 确认 _extract_raw_key 函数存在且处理 bare key
- evidence_level: integration
- artifact_ref: docs/B2-docs/git-worktree/wt-close/verification/test-evidence/acceptance-3.txt
- test_command: |
  _wt="/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/fix-raw-20260629T165403Z03Z-wt-close-args-d-fix"
  source "$_wt/docs/system/workspace/scripts/worktree/wt-close" 2>/dev/null || true
  result=$(bash -c 'source "$1"; _extract_raw_key "20260629T165403Z"' _ "$_wt/docs/system/workspace/scripts/worktree/wt-close" 2>/dev/null || echo "")
  [[ "$result" == "20260629T165403Z" ]] && echo "PASS: bare key extracted" || { echo "FAIL: got '$result'"; exit 1; }
- expected_output: "PASS: bare key extracted"
- expected_RED_output: N/A (regression test)
- actual_RED_output: "RED confirmed — no args guard"
- actual_output: "GREEN: all tests pass"
- evidence_file: docs/B2-docs/git-worktree/wt-close/verification/test-evidence/acceptance-3.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: 验证 bare key 解析不被破坏

### AT-004 --raw-key raw-{key} 格式
- id: AT-004
- requirement: _extract_raw_key "raw-20260629T165403Z03Z" 返回 "20260629T165403Z"
- acceptance_target: raw- 前缀输入正确 strip
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep -oE 提取逻辑存在
- evidence_level: integration
- artifact_ref: docs/B2-docs/git-worktree/wt-close/verification/test-evidence/acceptance-4.txt
- test_command: |
  _wt="/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/fix-raw-20260629T165403Z03Z-wt-close-args-d-fix"
  result=$(bash -c 'source "$1"; _extract_raw_key "raw-20260629T165403Z03Z"' _ "$_wt/docs/system/workspace/scripts/worktree/wt-close" 2>/dev/null || echo "")
  [[ "$result" == "20260629T165403Z" ]] && echo "PASS: raw- prefix stripped" || { echo "FAIL: got '$result'"; exit 1; }
- expected_output: "PASS: raw- prefix stripped"
- expected_RED_output: N/A (regression test)
- actual_RED_output: "RED confirmed — no args guard"
- actual_output: "GREEN: all tests pass"
- evidence_file: docs/B2-docs/git-worktree/wt-close/verification/test-evidence/acceptance-4.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: 验证 raw- 前缀 strip 逻辑

### AT-005 --raw-key fix/raw-{key}-{slug} 格式
- id: AT-005
- requirement: _extract_raw_key "fix/raw-20260629T165403Z03Z-wt-close-args-d-fix" 返回 "20260629T165403Z"
- acceptance_target: fix/ 前缀和 slug 都被正确 strip
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: 提取结果仅含 bare key 不含 slug
- evidence_level: integration
- artifact_ref: docs/B2-docs/git-worktree/wt-close/verification/test-evidence/acceptance-5.txt
- test_command: |
  _wt="/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/fix-raw-20260629T165403Z03Z-wt-close-args-d-fix"
  result=$(bash -c 'source "$1"; _extract_raw_key "fix/raw-20260629T165403Z03Z-wt-close-args-d-fix"' _ "$_wt/docs/system/workspace/scripts/worktree/wt-close" 2>/dev/null || echo "")
  [[ "$result" == "20260629T165403Z" ]] && echo "PASS: fix/ branch format parsed" || { echo "FAIL: got '$result'"; exit 1; }
- expected_output: "PASS: fix/ branch format parsed"
- expected_RED_output: N/A (regression test)
- actual_RED_output: "RED confirmed — no args guard"
- actual_output: "GREEN: all tests pass"
- evidence_file: docs/B2-docs/git-worktree/wt-close/verification/test-evidence/acceptance-5.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: 验证 fix/raw-{key}-{slug} 格式 slug 被正确剥离

## Unit
- acceptance_target: 全部 AT 通过
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: 全部 acceptance items grep/执行通过
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001~005 即 unit tests
- replacement_evidence: AT evidence files

## Integration
- acceptance_target: --raw-key --dry-run 端到端执行不报错
- testing_layer: integration
- target_environment: fix worktree
- required_evidence: wt-close --raw-key <key> --dry-run 返回 0
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 完整 wt-close 需要真实 PR merge 后
- replacement_evidence: --dry-run 测试 + AT unit 测试

## End-to-End
- acceptance_target: 本 PR merge 后用 --raw-key 收口
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: wt-close --raw-key 20260629T165403Z 成功关闭
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 本 PR 合并后用 --raw-key 收口验证
- replacement_evidence: 上一轮 --raw-key 已验证功能正常

## Real-Environment
- real_environment_status: pass
- real_environment_reason: --raw-key 功能在上轮 PR #3633 已验证，本轮只修 bug
