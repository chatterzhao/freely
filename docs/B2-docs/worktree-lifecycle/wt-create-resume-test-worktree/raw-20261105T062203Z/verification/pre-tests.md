# Pre-Tests: 恢复模式按 git 登记反查 dev 工位真实路径
- issue_id: I-20261105T062203Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 恢复模式的恢复摘要与 scan_state_worktree 必须指向真实存在的 dev 工位路径；反查不到时报错而不猜路径；test 工位补建、完整初始化与二次重跑幂等不受影响；正常创建与 legacy 补建的冲突避让语义不变
- acceptance_target: 消除恢复路径把带 hash 后缀的不存在路径写入运行时状态
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 隔离 git 仓库（不触网）
- required_evidence: 新增行为回归测试 8 项全 GREEN + 7 个相关回归零新增失败
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-wt-create-recovery-dev-path
- test_command: bash docs/system/workspace/scripts/tests/test-wt-create-recovery-dev-path all
- expected_output: PASS: 8 checks, 0 failed
- expected_RED_output: FAIL: 3 of 8 checks failed
- actual_RED_output: RED 3 项失败 —— 恢复摘要打印 `.../fix-raw-20261105T062300Z-recovery-path-300efa56`（不存在），scan_state_worktree 为同一错误路径，static 组缺反查契约；既有 5 项能力 PASS（AT-001-RED.log）
- actual_output: PASS: 8 checks, 0 failed；摘要与 scan state 均指向真实 dev 工位（`-d` 校验通过），test 工位完整初始化，二次重跑幂等（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261105T062203Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5
- case_design: 隔离 git 仓库放置真实 wt-create 与 worktree-common.sh，预置 dev 分支 + 真实 dev 工位、test 分支缺失，并构造含 raw key 的 manager-task-source-scan-latest.json；运行恢复模式后解析恢复摘要的 dev 路径、读取 scan_state_worktree、校验 test-gate.env、二次重跑断言幂等。static 组用 Python 精确提取恢复块，断言其中不再出现 `resolve_target_path "$dev_branch"`、含 `_wt_registered_dir` 与反查失败报错，同时断言正常创建仍保留冲突避让。
- red_how: fix RED — 在未修复的 develop 真源上运行同一断言组，确认带 hash 后缀的错误路径被打印并写入 scan state。

## Unit
- acceptance_target: 恢复块静态契约与正常新建路径冲突避让保留
- testing_layer: unit
- target_environment: fix/raw-20261105T062203Z-recovery-dev-path
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-wt-create-recovery-dev-path static

## Integration
- acceptance_target: R3 四态、Q1 恢复 + legacy、Q2 身份、R1/R2 能力不退化
- testing_layer: integration
- target_environment: 真实工位回归套件
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-wt-create-four-state-dir all
2. bash docs/system/workspace/scripts/tests/test-wt-create-resume-test-worktree all
3. bash docs/system/workspace/scripts/tests/test-raw-key-drift all

## End-to-End
- acceptance_target: 恢复摘要与 scan state 指向真实 dev 工位
- testing_layer: end-to-end
- target_environment: 隔离 git 仓库（不触网）
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-wt-create-recovery-dev-path behavior

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 在真实 fix 工位以项目真源命令执行；本轮 wt-create 物化自动带 H1（R2 自举验证）；隔离 git 仓库中恢复模式真实执行，摘要与 scan_state_worktree 均指向预建的真实 dev 工位；7 个相关回归测试（含 R1/R2/R3/Q1/Q2）全 PASS；bin/check-epics-map 对齐通过。
