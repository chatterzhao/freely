# Pre-Tests: 四态判定校验工位目录与初始化标记
- issue_id: I-20261105T061812Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: wt-create 幂等判定必须同时校验分支、git 实际登记的工位目录与 test-gate.env 初始化标记；分支在但目录不在、或 test 工位半初始化时必须补齐；dev 缺 / test 在仍拒绝；双工位齐全仍幂等 no-op 且不产生重复工位
- acceptance_target: 中断恢复可自愈，且不退化既有 recovery / legacy / no-op 语义
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 多个隔离 git 仓库（不触网）
- required_evidence: 新增行为回归测试四态全 GREEN（13 项检查）+ 4 个既有 wt-create 回归基线对比零新增失败
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-wt-create-four-state-dir
- test_command: bash docs/system/workspace/scripts/tests/test-wt-create-four-state-dir all
- expected_output: PASS: 13 checks, 0 failed
- expected_RED_output: FAIL: 6 of 13 checks failed
- actual_RED_output: RED 6 项失败 —— CASE A「两分支在、两工位目录被删」与 CASE B「test 目录在但缺 test-gate.env」均被旧实现误判为 no-op exit 0（git worktree list 中目录为空）；3 项 static 缺判定 helper（AT-001-RED.log）
- actual_output: PASS: 13 checks, 0 failed；CASE A 补建双工位且 test 完全初始化，CASE B 补齐标记后第二次重跑为 no-op，CASE C 仍拒绝，CASE D 幂等无重复（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261105T061812Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5,T6
- case_design: 在隔离 git 仓库放置真实 wt-create、worktree-common.sh 与最小 replica gate stub；CASE A 只建两个分支不建工位目录；CASE B 建 dev/test 工位但删除 test-gate.env；CASE C 只建 test 分支与工位；CASE D 预置完整双工位与标记。每组用同一 wt-create 命令重跑，断言退出码、git worktree list 登记目录、test-gate.env 内容与工位数量。static 组校验两个 helper 与单一真源。
- red_how: fix RED — 在未修复的 develop 真源上运行同一断言组，确认两种残留被误判 no-op。

## Unit
- acceptance_target: 判定 helper 与既有能力静态结构
- testing_layer: unit
- target_environment: fix/raw-20261105T061812Z-four-state-dir-check
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-wt-create-four-state-dir static

## Integration
- acceptance_target: no-op / 不一致拒绝 / legacy 补建 / Q1 恢复语义不退化
- testing_layer: integration
- target_environment: 未修改 develop HEAD 基线对比
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-wt-create-resume-test-worktree all
2. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-wt-create.py

## End-to-End
- acceptance_target: 四种残留态真实执行并补齐
- testing_layer: end-to-end
- target_environment: 隔离 git 仓库（不触网）
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-wt-create-four-state-dir behavior

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 在真实 fix 工位以项目真源命令执行；本轮 wt-create 物化自动带 H1（R2 修复自举验证通过）；四种残留态在隔离 git 仓库真实执行全 GREEN；4 个既有 wt-create 回归以未修改 develop HEAD 复跑，2 PASS/2 FAIL 退出码逐一相同、输出差异仅时间戳，零新增失败；bin/check-epics-map 对齐通过。
