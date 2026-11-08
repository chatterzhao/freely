# Pre-Tests: GitHub handler 自动补齐缺失标签
- issue_id: I-20261108T134853Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: label-not-found 时补齐每个缺失标签并重试一次返回 created；标签齐备时零额外调用；auth 等非 label 错误不重试不建标签；重试有界；`labels=""` 旧路径不变；真机 feedback 双平台 created
- acceptance_target: 任意 GitHub 仓库上的 feedback 建单不再因缺标签整单失败，且不掩盖真实错误
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: `unittest.mock` 替换 `subprocess.run` 驱动真实 `GitHubHandler` + develop HEAD 基线快照对比；真机由本条 issue 自身的创建过程验证
- required_evidence: 7 静态 + 12 行为共 19 项全 GREEN；16 个相关回归对比；真机双平台 created
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-github-label-autocreate.py
- test_command: python3 docs/system/workspace/scripts/tests/test-github-label-autocreate.py all
- expected_output: SUMMARY: 19 ok, 0 failed
- expected_RED_output: SUMMARY: 12 failed（静态 3：无 label create 字面量、无 ensure helper、create_issue 函数体无补齐/重试；行为 5：缺标签直接 error、无重试、无 label create、标签去重断言空集、二次失败无界）
- actual_RED_output: develop `c2a55934e` 基线快照（`git archive develop -- bin docs`）放入**最终版** AT-001 —— `SUMMARY: 7 ok, 12 failed`（AT-001-RED.log）。6 项 PASS 是既有能力守卫（GitHubHandler 存在、create_issue 已支持 labels、健康路径、非 label 错误不吞、无 labels 路径），证明夹具可跑通。
- actual_output: 工位同一断言 —— `SUMMARY: 19 ok, 0 failed`（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/gate/platform/raw-20261108T134853Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log,AT-001-REGRESSION-BASELINE.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5
- case_design: 静态组绑定标签补齐契约与 `create_issue` 函数体（不靠全文关键词，避免假通过）；行为组 mock `subprocess.run` 记录完整调用序列，覆盖缺标签补救、每标签一次、健康快路径、auth 失败不重试、无 labels 旧路径、二次失败有界。真实 gh 零调用。
- red_how: fix RED — `git archive develop -- bin docs` 出基线快照，把最终版 AT-001 拷入后以 `--source-dir /tmp/r165-base` 运行，基线文件一个不改。

## Unit
- acceptance_target: 标签补齐接线契约
- testing_layer: unit
- target_environment: fix/raw-20261108T134853Z-github-label-autocreate
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-github-label-autocreate.py static

## Integration
- acceptance_target: severity / 写通道 / parity / handler-probe / promote / close / install-state / 契约 / 门禁不退化
- testing_layer: integration
- target_environment: 工位 + 未修改 develop HEAD 基线快照
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-feedback-severity.py all
2. bash docs/system/workspace/scripts/tests/test-platform-write-channel
3. python3 docs/system/workspace/scripts/tests/test-platform-open-parity.py
4. python3 docs/system/workspace/scripts/tests/test-platform-handler-probe.py
5. bash docs/system/workspace/scripts/tests/test-issue-sync-promote-b2
6. bash docs/system/workspace/scripts/tests/test-issue-sync-close-terminal-first
7. python3 docs/system/workspace/scripts/tests/test-install-state.py all
8. python3 docs/system/workspace/scripts/tests/test-raw-reconciliation.py
9. python3 docs/system/workspace/scripts/tests/test-raw-replica-degraded.py
10. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-raw-metadata.py
11. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-materialization.py
12. bash docs/system/workspace/scripts/tests/test-wt-close-comment-scan
13. bash docs/system/workspace/scripts/tests/test-test-gate-record
14. bash docs/system/workspace/scripts/tests/test-governance-gate-batch-read
15. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-wt-close.py
16. python3 docs/system/workspace/scripts/tests/test-scan-frontmatter-nested.py

## End-to-End
- acceptance_target: fake gh 下的完整建单调用序列
- testing_layer: end-to-end
- target_environment: 隔离 mock，真实 GitHubHandler
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-github-label-autocreate.py behavior

## Real-Environment
- real_environment_status: pass
- real_environment_exception: 行为测试不调用真实 gh（会造 issue）；真机证据是本条 issue 自身的创建：补齐 `severity/P0|P1|P2` 标签后 `./bin/freely feedback create --severity P0` 返回 GitHub #4230 / Gitee IKTSSM 双双 created。
- real_environment_reason: 16 个回归中 15 项 MATCH；`test-platform-open-parity.py` 的 1 项 DIFF 为**活跃平台状态差异**而非代码退化：基线快照不是带 remote 的 git 工位，取到空集合假 OK；真实工位正确检出 `20261108T134701Z` 只在 Gitee（本缺陷修复前 PARTIAL 留下的单）。该测试全仓无门禁引用，不阻塞 PR；补建 GitHub 副本需 `raw-issue-pull` 在「分支名含该 raw-key」的工位内执行，已排进 v4 队列 R59，按用户「本轮后暂停」不另开工位。详见回归日志 NOTE。预存红 `test-command-lifecycle-wt-close.py` 两边同值。
