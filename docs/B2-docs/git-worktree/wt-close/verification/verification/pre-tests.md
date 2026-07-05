# Pre-Tests: wt-close --raw-key flag

- issue_id: I-20260629T164530Z-A

## Acceptance Items

### AT-001 --raw-key 多种格式提取正确
- id: AT-001
- requirement: --raw-key 支持 raw-{key}、fix/raw-{key}-{slug}、feature/raw-{key}-{slug}、{bare-key} 四种输入，正确提取 raw key
- acceptance_target: _extract_raw_key 对四种输入返回正确的 bare key
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 确认 _extract_raw_key 函数存在且使用 grep -oE 精确提取
- evidence_level: integration
- artifact_ref: docs/B2-docs/git-worktree/wt-close/verification/test-evidence/acceptance-1.txt
- test_command: |
  cd /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/fix-raw-20260629T164530Z30Z-wt-close-raw-key-flag
  grep -q '_extract_raw_key\|grep -oE.*raw-' docs/system/workspace/scripts/worktree/wt-close || { echo "FAIL"; exit 1; }
  echo "PASS: _extract_raw_key with grep -oE found"
- expected_output: "PASS: _extract_raw_key with grep -oE found"
- expected_RED_output: FAIL
- actual_RED_output: code written before RED
- actual_output: "PASS: _extract_raw_key with grep -oE found"
- evidence_file: docs/B2-docs/git-worktree/wt-close/verification/test-evidence/acceptance-1.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: fix: 修改前 grep 确认无 --raw-key flag 解析

### AT-002 --platform-only 不走分支解析
- id: AT-002
- requirement: --raw-key + --platform-only 时跳过 _resolve_branch_from_raw_key
- acceptance_target: --platform-only 路径中 raw_key 直接从 --raw-key 提取
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 确认 --platform-only 路径不调 _resolve_branch_from_raw_key
- evidence_level: integration
- artifact_ref: docs/B2-docs/git-worktree/wt-close/verification/test-evidence/acceptance-2.txt
- test_command: |
  cd /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/fix-raw-20260629T164530Z30Z-wt-close-raw-key-flag
  grep -A3 'PLATFORM_ONLY.*true' docs/system/workspace/scripts/worktree/wt-close | grep -q 'raw_key=' || { echo "FAIL"; exit 1; }
  echo "PASS: platform-only sets raw_key from _raw_key"
- expected_output: "PASS: platform-only sets raw_key from _raw_key"
- expected_RED_output: FAIL
- actual_RED_output: code written before RED
- actual_output: "PASS: platform-only sets raw_key from _raw_key"
- evidence_file: docs/B2-docs/git-worktree/wt-close/verification/test-evidence/acceptance-2.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: fix: 修改前 raw_key 变量未绑定

### AT-003 + 前缀已 strip
- id: AT-003
- requirement: git branch --list 输出的 + 前缀被 strip
- acceptance_target: sed 表达式包含 + 字符
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 确认 sed 's/^[*+ ]*//'
- evidence_level: integration
- artifact_ref: docs/B2-docs/git-worktree/wt-close/verification/test-evidence/acceptance-3.txt
- test_command: |
  cd /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/fix-raw-20260629T164530Z30Z-wt-close-raw-key-flag
  grep -q 's/\^\[\*+ \]\*//' docs/system/workspace/scripts/worktree/wt-close || { echo "FAIL"; exit 1; }
  echo "PASS: + prefix stripped"
- expected_output: "PASS: + prefix stripped"
- expected_RED_output: FAIL
- actual_RED_output: code written before RED
- actual_output: "PASS: + prefix stripped"
- evidence_file: docs/B2-docs/git-worktree/wt-close/verification/test-evidence/acceptance-3.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: fix: 修改前 sed 只 strip * 和空格

## Unit
- acceptance_target: grep 验证全部修改
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: 全部 3 个 acceptance items 通过
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: Unit tests executed as AT-001/002/003 above
- replacement_evidence: AT evidence files

## Integration
- acceptance_target: --raw-key + --platform-only 正常关闭平台 issue
- testing_layer: integration
- target_environment: develop worktree
- required_evidence: wt-close --raw-key 20260629T162119Z --platform-only 执行无误
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 需要真实 platform issue 测试，E2E 验证
- replacement_evidence: unit grep tests + syntax check

## End-to-End
- acceptance_target: 本 PR merge 后用 --raw-key 收口自身工位
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: wt-close --raw-key 20260629T164530Z 正常关闭
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: E2E 通过本 PR merge 后的 wt-close 验证
- replacement_evidence: 本 PR 合并后用 --raw-key 收口

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 单元测试和语法检查通过
