# Pre-Tests: 门禁 fail-open 收敛为 fail-closed
- issue_id: I-20261103T132458Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 6 个 shim 无裸 `exit 0`、用 `-f`、缺真身 `exit 2`，`post-checkout` 逐字节不变；隔离仓库缺真身时 `git commit` 被拒，真身存在但丢 `+x` 时仍真实执行；`pre-commit.sh` hooksPath 不符/门禁真身缺失时非零且外部项目合法早退保留；`pr-create-guarded` 每处 not-found skipping 伴随非零退出而正常无 raw key 路径继续；`checkpoint-guard` 默认 required 非零；`check-file-size` 全量报出 `runtime/freely` 且增量接入不阻断历史；真实工位 `git commit` 成功
- acceptance_target: 环境异常与真实通过不再共用退出码 0，且不因修复自锁每轮 commit / wt-create
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 隔离 git 仓库（真实 git commit）+ 真实 dev 工位冒烟
- required_evidence: 新增回归测试 28 项全 GREEN + 真实 commit 冒烟 exit 0 + 14 个回归基线对比零新增失败
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-gate-fail-closed
- test_command: bash docs/system/workspace/scripts/tests/test-gate-fail-closed all
- expected_output: PASS: 28 checks, 0 failed
- expected_RED_output: FAIL: 26 of 28 checks failed
- actual_RED_output: 未修改 develop HEAD（`94587c5f3`）基线 RED 26 项失败 —— 6 个 shim 仍 `exit 0`/需执行位、pre-commit.sh 守卫恒通过、4 处 skipping 无退出码、checkpoint 默认 0、check-file-size 无调用点；CASE A 缺真身时 commit 被放行、CASE C checkpoint 返回 0；2 项既有能力保持 PASS（`post-checkout` 独立实现、正常无 raw key 路径）（AT-001-RED.log）
- actual_output: PASS: 28 checks, 0 failed；CASE A 缺真身 commit 被拒且诊断说明环境故障、CASE B sentinel 证明 `-x` 丢失仍执行真身、CASE C checkpoint 默认 rc=2；真实工位 `git commit` exit 0 / 1s（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/gate/governance/raw-20261103T132458Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5,T6,T7
- case_design: static 组用 Python 逐个检查 shim 的 `exit 0`/`-x`/`exit 2`、`post-checkout` 自包含逻辑、pre-commit.sh 前 14 行与守卫、pr-create-guarded 4 处 skipping 窗口内是否含非零退出且正常无 raw key 路径不含、checkpoint 默认赋值行、file-size 接线；behavior 组构造隔离 git 仓库（每个 shim 都配 pass 真身，只按用例移除 pre-commit 真身），真实执行 `git commit` 断言拒绝/执行/诊断，另构造 staged 12 个文件的临时项目验证 checkpoint 默认非零。
- red_how: fix RED — 用 `git show 94587c5f3:<file>` 把 10 个真源还原到未修改 develop 状态后运行同一断言组，确认环境异常被翻译成通过。

## Unit
- acceptance_target: shim / 真源守卫 / 退出码约定的静态契约
- testing_layer: unit
- target_environment: fix/raw-20261103T132458Z-gate-fail-closed
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-gate-fail-closed static

## Integration
- acceptance_target: R1..R7、Q1/Q2、commit 门禁链、四态/反查/恢复不退化
- testing_layer: integration
- target_environment: 未修改 develop HEAD 基线对比
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-wt-create-four-state-dir all
2. bash docs/system/workspace/scripts/tests/test-freely-package-output-guard
3. python3 docs/system/workspace/scripts/tests/test-open-list-read-degraded.py

## End-to-End
- acceptance_target: 隔离仓库真实 git commit + 真实工位冒烟
- testing_layer: end-to-end
- target_environment: 隔离 git 仓库 + 真实 dev 工位
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-gate-fail-closed behavior
2. 真实工位 `git commit` 冒烟（exit 0，记录于 AT-001-GREEN.log）

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 在真实 fix 工位以项目真源命令执行；R2 物化 H1 自举生效；全部新 fail-closed 门禁激活下真实 `git commit` 成功（exit 0 / 1s），确认不自锁；10 个真源还原到未修改 develop HEAD 做基线对比，14 个相关回归退出码逐一相同（4 个预存红测试输出逐字节一致）→ 0 新增失败；bin/check-epics-map 对齐通过；双平台 raw 副本用封装命令关闭、三份 fingerprint 一致。
