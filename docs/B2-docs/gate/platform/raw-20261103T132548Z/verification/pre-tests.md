# Pre-Tests: 测试证据链可验证并替换 CI 桩
- issue_id: I-20261103T132548Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 手写三行 `test-gate.env` 被真实 `pretests-retirement-gate` 拒绝；`test-gate run` 真实执行且失败运行被拒、成功运行放行；证据篡改与 HEAD 漂移被 hash/HEAD 校验拒绝；`bin/test-all --ci` 退出 0 且列 known-broken；两个 CI 有真实执行步骤；`freely evidence add` 记录 sha256
- acceptance_target: 「测试跑过」由真实进程退出码 + 不可篡改证据证明，CI 真的执行测试
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 隔离 git 夹具（真实 `pretests-retirement-gate`、真实 `test-evidence.py`、真实 `bin/test-all`）+ develop HEAD 基线快照对比；真机由本轮收口的 `freely test-gate run` 验证
- required_evidence: 12 静态 + 8 行为共 20 项全 GREEN；17 个相关回归 worktree/baseline 退出码对比
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-test-evidence-chain.py
- test_command: python3 docs/system/workspace/scripts/tests/test-test-evidence-chain.py all
- expected_output: SUMMARY: 20 ok, 0 failed
- expected_RED_output: SUMMARY: 16 failed（静态 8：无 evidence helper、门禁无校验、无 test-gate run / evidence add / test-all、CI 桩未替换；行为 8：手写三行 env 被真实门禁放行、失败运行未拒、成功运行未证、篡改未拒、HEAD 漂移未拒、真门禁未接、runner 缺失、manifest 缺失）
- actual_RED_output: develop `3906ac56c` 基线快照（`git archive develop -- bin docs .gitee-ci.yml .github`）放入**最终版** AT-001 —— `SUMMARY: 4 ok, 16 failed`（AT-001-RED.log）。4 项 PASS 是既有能力守卫（gate / writer / 两个 CI 文件存在），证明夹具可跑通；行为组第 1 项实测真实门禁 `rc=0` 放行手写 env，即缺陷本体。
- actual_output: 工位同一断言 —— `SUMMARY: 20 ok, 0 failed`（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/gate/platform/raw-20261103T132548Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log,AT-001-REGRESSION-BASELINE.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5,T6,T7,T8
- case_design: 静态组断言 6 个真源/CI 接线 + 4 条既有能力守卫；行为组构造隔离 git 夹具（含 stub `bin/pretests-gate`、手写 `test-gate.env`、证据文件），真实 `bash pretests-retirement-gate --project --worktree-path` 驱动门禁，再逐项调用真实 `test-evidence.py write/validate/manifest-add` 与 `bin/test-all --ci`。真实项目 `.freely/run` 零写入。
- red_how: fix RED — `git archive develop -- bin docs .gitee-ci.yml .github` 出基线快照，把最终版 AT-001 拷入后以 `--source-dir /tmp/r17-base` 运行，基线文件一个不改。

## Unit
- acceptance_target: 证据链接线契约
- testing_layer: unit
- target_environment: feature/raw-20261103T132548Z-test-evidence-verifiable
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-test-evidence-chain.py static

## Integration
- acceptance_target: test-gate / 写通道 / 生命周期 / 契约 / 门禁等既有能力不退化
- testing_layer: integration
- target_environment: 工位 + 未修改 develop HEAD 基线快照
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-test-gate-record
2. bash docs/system/workspace/scripts/tests/test-platform-write-channel
3. bash docs/system/workspace/scripts/tests/test-issue-sync-close-terminal-first
4. bash docs/system/workspace/scripts/tests/test-issue-sync-promote-b2
5. bash docs/system/workspace/scripts/tests/test-wt-close-comment-scan
6. python3 docs/system/workspace/scripts/tests/test-raw-reconciliation.py
7. python3 docs/system/workspace/scripts/tests/test-raw-replica-degraded.py
8. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-raw-metadata.py
9. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-materialization.py
10. python3 docs/system/workspace/scripts/tests/test-feedback-severity.py all
11. python3 docs/system/workspace/scripts/tests/test-install-state.py all
12. python3 docs/system/workspace/scripts/tests/test-github-label-autocreate.py all
13. python3 docs/system/workspace/scripts/tests/test-platform-handler-probe.py
14. python3 docs/system/workspace/scripts/tests/test-scan-frontmatter-nested.py
15. python3 docs/system/workspace/scripts/tests/test-platform-open-parity.py
16. bash docs/system/workspace/scripts/tests/test-governance-gate-batch-read
17. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-wt-close.py

## End-to-End
- acceptance_target: 手写 env 拒绝 / runner 证据放行 / 篡改与漂移拒绝 / runner 聚合
- testing_layer: end-to-end
- target_environment: 隔离 git 夹具 + 真实门禁
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-test-evidence-chain.py behavior

## Real-Environment
- real_environment_status: pass
- real_environment_exception: 行为测试用隔离 git 夹具，不改真实 `.freely/run/test-gate.env`；真实证据由本轮收口时在 test-pre-merge 工位执行 `freely test-gate run --worktree <test wt> --command '<tests>'` 产生，门禁据此放行 `pr-create-guarded`。
- real_environment_reason: 17 个回归中 16 项 MATCH；`test-platform-open-parity.py` 的 1 项 DIFF 是活跃平台状态差异（基线快照非 git 工位 → 空集合假 OK；真实工位检出 `20261108T134701Z` 仅 Gitee），非代码退化，已排进 v4 队列 R59，详见回归日志 NOTE。`test-command-lifecycle-wt-close.py` 为预存红，两边同值。
