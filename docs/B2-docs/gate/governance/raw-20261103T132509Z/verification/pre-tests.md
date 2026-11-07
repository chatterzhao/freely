# Pre-Tests: 接线 commit-msg 提交期阻断
- issue_id: I-20261103T132509Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: `.githooks/commit-msg` shim 存在、用 `-f`、缺真身 `exit 2`；真身校验受控 handshake 且 receipt 分支只含 develop/main；develop merge 缺 trailer 被拒并打印原因；自填合法 trailer 但无受控 handshake 被拒；合法 guarded merge 通过；test-pre-merge sync merge 通过不自锁；普通 commit 与通用 message 规范保持；README 三层表述与实现一致；`post-checkout` 不变
- acceptance_target: 补齐 README 宣称三层治理的第一层，使手工 merge 伪造 receipt 在提交期被拦
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 隔离 git 仓库（真实 git merge / merge --continue / commit）
- required_evidence: 新增回归测试 14 项全 GREEN + 13 个回归基线对比零新增失败 + 真实工位链路冒烟
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-commit-msg-wireup
- test_command: bash docs/system/workspace/scripts/tests/test-commit-msg-wireup all
- expected_output: PASS: 14 checks, 0 failed
- expected_RED_output: FAIL: 9 of 14 checks failed
- actual_RED_output: 未修改 develop HEAD（`ba1a1ece8`）孤儿态 RED 9 项失败 —— shim 不存在、无 handshake 校验、trailer 分支仍含 test-pre-merge、README 无 commit-msg 说明；CASE A 缺 trailer merge 通过、CASE B 自填 trailer 通过、CASE F 通用规范不生效；5 项既有能力保持 PASS（post-checkout 不变、真身语法、合法 guarded merge、test 沙箱 merge、普通 commit）（AT-001-RED.log）
- actual_output: PASS: 14 checks, 0 failed；CASE A 拒绝且含 `Commit blocked` 原因、CASE B 拒绝且含 `handshake`、CASE C/D/E 通过、CASE F 通用规范生效（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/gate/governance/raw-20261103T132509Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5,T6
- case_design: static 组检查 shim 的 `-f`/`exit 2`、真身 handshake 与 case 模式、README、`post-checkout` 不变、bash -n；behavior 组在隔离 git 仓库中复制真实 shim + 真身，逐个构造 6 个场景：develop merge 无 trailer、develop merge 自填 trailer 无 handshake、develop merge 完整 trailer + handshake、test-pre-merge sync merge、普通 commit、超长 subject。用 `git merge --no-commit --no-ff` + 覆写 MERGE_MSG + `git merge --continue` 复现受控流程。
- red_how: fix RED — 用 `git show ba1a1ece8:<file>` 还原 2 个真源并删除 shim（回到孤儿态）后运行同一断言组，确认提交期无阻断。

## Unit
- acceptance_target: shim 契约、handshake 校验、分支范围、文档一致性
- testing_layer: unit
- target_environment: fix/raw-20261103T132509Z-commit-msg-wireup
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-commit-msg-wireup static

## Integration
- acceptance_target: R1..R8、Q1/Q2、门禁链、四态/反查/恢复不退化
- testing_layer: integration
- target_environment: 未修改 develop HEAD 基线对比
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-gate-fail-closed all
2. bash docs/system/workspace/scripts/tests/test-wt-create-four-state-dir all
3. python3 docs/system/workspace/scripts/tests/test-open-list-read-degraded.py

## End-to-End
- acceptance_target: 隔离仓库真实 merge/commit 与真实工位链路
- testing_layer: end-to-end
- target_environment: 隔离 git 仓库 + 真实 dev 工位
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-commit-msg-wireup behavior
2. 真实工位 `git commit` / `pr-create-guarded` / `pr-merge-guarded` 冒烟（记录在 R9 进展）

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 在真实 fix 工位以项目真源命令执行；R2 物化 H1 自举生效；真实历史 25 条 commit 逐条验证通用规范 0 违规、guarded merge 均带完整 trailer；探针实证 `git merge --continue` 触发 commit-msg hook 且受控状态可见；3 个真源还原到未修改 develop HEAD 做基线对比，13 个相关回归退出码逐一相同（5 个预存红测试输出逐字节一致）→ 0 新增失败；bin/check-epics-map 对齐通过；双平台 raw 副本用封装命令关闭、三份 fingerprint 一致。
