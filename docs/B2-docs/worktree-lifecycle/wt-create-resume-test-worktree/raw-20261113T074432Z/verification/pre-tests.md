# Pre-Tests: test-pre-merge 沙箱的受控回收
- issue_id: I-20261113T074432Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: test-pre-merge-* 在 --force + --discard-unmerged 齐备时可被 wt-close 回收；缺任一 flag 拒绝；main/develop 仍一律拒绝；develop 基线同条件必须拒绝
- acceptance_target: 残留测试沙箱可用封装命令回收，且不降低受保护分支的门禁强度
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 抽取真实守卫块 + `_is_protected_branch` 在沙箱 bash 中执行（不触网、不动真工位）
- required_evidence: AT-001 静态 5 + 行为 7 + 基线控制 1 全 GREEN；unit 5 项 PASS；合并后真机回收成功
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-wt-close-test-premerge-guard.py
- test_command: python3 docs/system/workspace/scripts/tests/test-wt-close-test-premerge-guard.py
- expected_output: SUMMARY: 12 ok, 0 failed
- expected_RED_output: SUMMARY: 8 ok, 5 failed
- actual_RED_output: develop b0686c6fa 快照上 S2/S4/S5、B1/B2 全红（守卫无窄例外、基线确实拒绝 test-pre-merge）；基线控制 R1 通过（AT-001-RED.log）
- actual_output: SUMMARY: 12 ok, 0 failed；B1 两 flag 放行、B2 明确打印、B3 三种缺 flag 组合拒绝、B4 develop/main 拒绝（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261113T074432Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log,unit-t-wt-close-premerge-guard-01.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4
- case_design: 静态组断言守卫块要求两个 flag 且仍调用 `_is_protected_branch`；行为组抽取真实守卫块与 helper，在 bash 沙箱里跑 6 种 (branch, force, discard) 组合；基线控制对 develop 源码跑同条件并断言仍拒绝，防止「永远为真」的假绿。
- red_how: fix RED — git archive develop 导出基线树，用 --source-dir 与 --baseline 运行同一 AT。

## Unit
- acceptance_target: 守卫块的窄例外与 main/develop 保护
- testing_layer: unit
- target_environment: fix/raw-20261113T074432Z-wt-close-test-premerge-guard
- required_evidence: t-wt-close-premerge-guard-01.sh 5 项 PASS
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/unit/t-wt-close-premerge-guard-01.sh

## Integration
- acceptance_target: 既有 wt-close 收口路径与 CI 子集不退化
- testing_layer: integration
- target_environment: test-pre-merge 工位
- required_evidence: bin/test-all --ci 全绿；projections verify ok；三门禁 ok
- blocker_taxonomy: execution_pending_or_failed
1. bin/test-all --ci

## End-to-End
- acceptance_target: 合并后真机回收 R33.6 自证残留工位
- testing_layer: end-to-end
- target_environment: 主仓（合并后的 develop）
- required_evidence: wt-close --raw-key 20261112T040108Z 成功；git worktree list 只剩主工位
- blocker_taxonomy: execution_pending_or_failed
1. ./bin/freely wt-close --raw-key 20261112T040108Z --discard-unmerged --force --reason "<合规前缀+理由>"

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 缺陷在 R33.9 合并后真机复现（分支解析成功但保护守卫拒绝），修复后用同一命令真机回收。
