# Pre-Tests: 测试证据有显式写入命令，守护进程不再冒充测试结果
- issue_id: I-20261107T120208Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: `freely test-gate record` 在 test 工位写入 `TEST_STATUS`/`LAST_TESTED_AT`/`LAST_TESTED_COMMIT` 并退出 0；非 `test-pre-merge-*` 工位、非法 `--status`、不存在的 `--commit` 全部 rc=2 且不改文件；`started` 不写 commit；写入原子且无残留；`cmd_start`/`cmd_stop` 不再写 test-gate.env 且 `_update_test_gate` 被删除；`_test_gate_write` 为唯一写入点（调用点恰好 1 处）
- acceptance_target: 让「测试在当前 HEAD 跑过」这一事实只能由一条可校验的命令产生，守护进程启停不再产生测试结论
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 隔离 git 夹具（真实 `git init` + `test-pre-merge-*` 分支）+ 真实 `runtime/freely` 子进程 + develop HEAD 基线快照对比
- required_evidence: 6 项静态断言 + 14 个行为场景全 GREEN；7 个相关回归基线对比退出码全 MATCH；真实自举（本命令给本轮 test 工位记录结果并过门禁）
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-test-gate-record
- test_command: bash docs/system/workspace/scripts/tests/test-test-gate-record all
- expected_output: SUMMARY: 20 ok, 0 failed
- expected_RED_output: SUMMARY: 15 failed（静态 4：`_update_test_gate` 仍在、`test-gate.env` 路径不在单一 helper 内（`_test_gate_file` 不存在）、`_test_gate_write` 调用点 0、`test-gate record` 未接入 dispatcher；usage 无此命令；行为 10：record 子命令不存在 → 写入/拒绝/校验/原子性场景全失败）
- actual_RED_output: develop HEAD `04afa025d` 基线快照（`git archive develop -- bin docs`）内放入**最终版** AT-001 运行 —— `SUMMARY: 5 ok, 15 failed`（AT-001-RED.log）：`runtime still has the daemon-owned _update_test_gate writer`、`test-gate.env path appears outside the single helper (NO_FILE_HELPER)`、`_test_gate_write call sites = 0`、`test-gate record is not dispatched`、`usage does not document test-gate record`，以及 10 条 record 行为用例全失败（`[ERROR] unknown command: test-gate`，rc=1 而非期望的 0/2）
- actual_output: 工位运行同一份断言 —— 静态 6 项全 ok、行为 14 项全 ok，`SUMMARY: 20 ok, 0 failed`（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/gate/governance/raw-20261107T120208Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log,AT-001-REGRESSION-BASELINE.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5,T6
- case_design: 每个行为用例新建隔离 git 仓库并把分支切到 `test-pre-merge-20260101T000000Z-probe`，通过**子进程**调用真实 `runtime/freely test-gate record`（不是 source 后直接调函数），断言退出码 + `.freely/run/test-gate.env` 实际字段；拒绝类用例额外断言文件**不存在**或**未被改写**；原子性用 `find .test-gate.*` 计数。
- red_how: fix RED — `git archive develop -- bin docs` 出基线快照，把最终版 AT-001 拷入后运行，基线文件一个不改。

## Unit
- acceptance_target: 静态契约（单一写入点、daemon 不写证据、dispatcher/usage、语法）
- testing_layer: unit
- target_environment: fix/raw-20261107T120208Z-test-gate-record-command
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-test-gate-record static

## Integration
- acceptance_target: wt-create 三条、写通道、raw 生命周期、wt-close、reconciliation 既有能力不退化
- testing_layer: integration
- target_environment: 工位 + 未修改 develop HEAD 基线对比
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-wt-create-resume-test-worktree
2. bash docs/system/workspace/scripts/tests/test-wt-create-four-state-dir
3. bash docs/system/workspace/scripts/tests/test-wt-create-recovery-dev-path
4. bash docs/system/workspace/scripts/tests/test-platform-write-channel
5. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-raw-metadata.py
6. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-wt-close.py
7. python3 docs/system/workspace/scripts/tests/test-raw-reconciliation.py

## End-to-End
- acceptance_target: 真实子进程写入/拒绝/校验/原子替换
- testing_layer: end-to-end
- target_environment: 隔离 git 夹具
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-test-gate-record behavior

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 行为用例全程使用真实 `git` 与真实 `runtime/freely` 子进程，只有夹具仓库是新建的；7 个相关回归 worktree/baseline 退出码全 MATCH（`test-command-lifecycle-wt-close.py` 的 1 项失败为预存红，基线同用例同断言）。真实自举：本轮用该命令给自己所在的 test 工位记录 `completed`，随后 `pr-create-guarded` 的门禁从 `pretests_not_tested` 变为通过 —— 命令解决了它自己被提出的那个阻塞。
