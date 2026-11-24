# Pre-Tests: issue-sync update 失败传播
- issue_id: I-20261124T054217Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 双平台写结果汇总，任一失败非零退出
- acceptance_target: cmd-update 失败传播行为
- testing_layer: integration
- target_environment: test-pre-merge-20261124T054217Z-issue-sync-gitee-failure
- required_evidence: AT 在 develop 基线 RED、工位 GREEN
- evidence_level: integration
- artifact_ref: docs/B2-docs/gate/platform/raw-20261124T054217Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/tests/test-issue-sync-write-result.py
- expected_output: SUMMARY: N ok, 0 failed
- expected_RED_output: SUMMARY: <N-M> ok, M failed（基线吞 Gitee/GitHub 失败、无汇总输出）
- actual_RED_output: "SUMMARY: 2 ok, 3 failed — 基线吞 GitHub/Gitee 失败、无结果汇总"
- actual_output: "SUMMARY: 5 ok, 0 failed；cmd-update 成功路径含 update complete + result overall=success"
- evidence_file: docs/B2-docs/gate/platform/raw-20261124T054217Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: fix 复现——develop 基线源码把 Gitee 失败仅 echo 后返回 0，AT 静态与行为断言必然失败。

## Unit
- acceptance_target: 源码检查每平台返回值
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: AT 静态断言
- blocker_taxonomy: execution_pending_or_failed
- test_tasks:
  1. 断言 cmd-update.sh 对 _gh_update 与 _gitee_update 都检查返回值（非 `|| echo` 吞掉）。
  2. 断言存在 overall 汇总与非零退出路径。

## Integration
- acceptance_target: mock 平台失败时命令非零退出
- testing_layer: integration
- target_environment: test-pre-merge-20261124T054217Z-issue-sync-gitee-failure
- required_evidence: mock 两平台分别失败的行为测试
- blocker_taxonomy: execution_pending_or_failed
- test_tasks:
  1. mock Gitee 失败 → 汇总含 gitee=failure、overall=partial_failure、非零退出。
  2. mock GitHub 失败 → 同样非零。
  3. 双成功 → 含 update complete、零退出。

## End-to-End
- acceptance_target: 回归不破坏 issue-sync 生命周期
- testing_layer: end-to-end
- target_environment: test-pre-merge → develop merge chain
- required_evidence: `bash bin/test-all --ci` 全绿 + 既有 issue-sync AT 通过
- blocker_taxonomy: execution_pending_or_failed
- test_tasks:
  1. 跑 test-all --ci 确认全绿。
  2. 确认 update 成功路径输出与既有 gate 兼容。

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 本轮改动是脚本内结果传播逻辑，fix/test 工位 mock 平台行为测试即为真实环境验证；不对平台做实际写。
