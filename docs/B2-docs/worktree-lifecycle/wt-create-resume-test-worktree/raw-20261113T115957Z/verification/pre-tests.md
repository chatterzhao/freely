# Pre-Tests: wt-close 收口全部 I-* children
- issue_id: I-20261113T115957Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 遍历 promoted_children、B2 路径定位、非终态拒绝且零平台写入、终态逐个关闭、dry-run/skip-platform 正确、已关闭不重复；基线三条红
- acceptance_target: 删工位前保证 children 终态并完成平台收口
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 抽取真实 Phase 2.5 块 + 真实 _fm_get/_close_platform_ids_readonly，在 sandbox project 中运行（adapter 记录调用）
- required_evidence: AT-001 静态 8 + 行为 7 + 基线 3 全 GREEN
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-wt-close-children.py
- test_command: python3 docs/system/workspace/scripts/tests/test-wt-close-children.py
- expected_output: SUMMARY: 15 ok, 0 failed
- expected_RED_output: SUMMARY: 4 ok, 14 failed
- actual_RED_output: develop 7697cae64 无 Phase 2.5、B1 路径、只读 absorbed_into 三条红全部成立（R1–R3）（AT-001-RED.log）
- actual_output: SUMMARY: 15 ok, 0 failed；B1 两个 completed 关闭 2 次、B3 in_dev 拒绝且零写入、B5 dry-run 零写入、B6 skip-platform、B7 已关闭不重复（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261113T115957Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3
- case_design: 从源码抽取真实 Phase 2.5 块与两个 helper，在临时项目里放 B1 raw（children A/B）+ B2 I-* 文档 + 记录调用的 stub adapter，跑 7 种组合；基线只做结构断言（无 Phase 2.5 / B1 路径 / 不读 promoted_children），因为基线没有可执行块。
- red_how: fix RED — git archive develop 导出基线树，用 --source-dir 与 --baseline 运行同一 AT。

## Unit
- acceptance_target: Phase 2.5 结构
- testing_layer: unit
- target_environment: fix/raw-20261113T115957Z-wt-close-children-closeout
- required_evidence: AT-001 静态 8 项
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-wt-close-children.py

## Integration
- acceptance_target: 既有 wt-close 路径与 CI 子集不退化
- testing_layer: integration
- target_environment: test-pre-merge 工位
- required_evidence: bin/test-all --ci 全绿；projections verify ok；三门禁 ok
- blocker_taxonomy: execution_pending_or_failed
1. bin/test-all --ci

## End-to-End
- acceptance_target: 本轮 wt-close 自身收口 I-20261113T115957Z-A
- testing_layer: end-to-end
- target_environment: 本 issue 的收口链路
- required_evidence: wt-close 输出 closing I-* issue 且平台 closed
- blocker_taxonomy: execution_pending_or_failed
1. ./bin/freely wt-close --raw-key 20261113T115957Z

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 缺陷由历史 linked 残留（phase_state completed 却 OPEN）长期暴露；本轮 E2E 即用新逻辑收口自身 child。
