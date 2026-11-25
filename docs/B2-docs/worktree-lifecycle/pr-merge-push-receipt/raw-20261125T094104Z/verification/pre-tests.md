# Pre-Tests: pr-merge issue-sync 源分支 push 回执 fail-closed
- issue_id: I-20261125T094104Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: issue-sync 自动 commit 后逐 configured platform push 源分支，汇总失败，无虚假成功回执
- acceptance_target: raw-20261125T094104Z 目标 1-3 与非目标边界
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261125T094104Z-pr-merge-push-receipt
- required_evidence: develop 基线 RED、工位 GREEN，逐断言 ok/FAIL 与 SUMMARY 日志
- evidence_level: integration
- artifact_ref: docs/B2-docs/worktree-lifecycle/pr-merge-push-receipt/raw-20261125T094104Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/tests/test-pr-merge-push-receipt.py
- expected_output: SUMMARY: N ok, 0 failed
- expected_RED_output: SUMMARY: <N-M> ok, M failed — 基线 push all + || true + 无条件 pushed 回执
- actual_RED_output: "SUMMARY: 5 ok, 9 failed（develop 基线：helper 缺失、push all || true、无条件回执）"
- actual_output: "SUMMARY: 14 ok, 0 failed；bash -n rc=0（证据 acceptance-1.log）"
- evidence_file: docs/B2-docs/worktree-lifecycle/pr-merge-push-receipt/raw-20261125T094104Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: 对 develop 源码跑同一 AT（--source-dir <develop>）；基线含 push all || true 与无条件回执，行为断言必然命中。
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: T1-T3
- case_design: 源码结构断言（无 push all || true、无条件 pushed）+ 行为断言（mock git push 注入失败 → 非零 + failed_remotes）+ 成功路径逐 remote 回执

## Unit
- acceptance_target: push 汇总逻辑
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: 每条 check 打印 ok/FAIL，SUMMARY 汇总
- blocker_taxonomy: execution_pending_or_failed
- test_tasks:
  1. `_sync_issues_changed_in_merge` 的 push 块不出现 `push all ... || true`。
  2. push 块不出现紧跟 commit 的无条件 `[MERGE-GUARD] issue-sync committed + pushed`。
  3. push 块遍历 configured remotes（跳过 all），逐一校验结果。
  4. 失败时汇总 failed_remotes 并非零退出。
  5. 失败回执含可操作重试命令。

## Integration
- acceptance_target: 双平台 push 失败可见
- testing_layer: integration
- target_environment: test-pre-merge 工位
- required_evidence: mock git push 一平台失败 → 非零 + 失败清单；两平台成功 → 逐 remote ok 回执
- test_tasks:
  1. 注入 github push 失败 → 汇总起非零、回执含 github。
  2. 注入 gitee push 失败 → 汇总起非零、回执含 gitee。
  3. 两平台成功 → 回执逐 remote 列 ok，无 "pushed" 无条件字样。

## End-to-End
- acceptance_target: 真实 pr-merge 场景源分支 push 回执可信
- testing_layer: end-to-end
- target_environment: test-pre-merge 工位
- required_evidence: 本 lane 合并后源分支 remote 与本地 HEAD 一致，回执逐平台可核对
- test_tasks:
  1. 合并后核对 github/origin 源分支 tracking ref 与 fix HEAD 一致。
  2. 确认回执无无条件 "pushed"，而是逐 remote 状态。
