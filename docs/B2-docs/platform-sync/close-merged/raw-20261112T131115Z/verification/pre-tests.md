# Pre-Tests: issue-sync close 支持 kind=linked
- issue_id: I-20261112T131115Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: issue-sync close 对 kind=linked 可完成双平台关单并回写 status: closed，body 与 linked 专属字段逐字保留；部分失败可重试且文档不变；close-linked 拒绝 raw；close-platforms 对 linked 仍拒绝（raw 契约未放宽）
- acceptance_target: linked 残留可以真正收口，且 raw 的严格语义不变
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 本地 fixture 树 + stub platform-adapter（不触网）
- required_evidence: AT-001 静态 6 + 行为 9 全 GREEN；负向控制（partial / kind=raw / close-platforms on linked）均按预期失败
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-issue-sync-close-linked.py
- test_command: python3 docs/system/workspace/scripts/tests/test-issue-sync-close-linked.py
- expected_output: SUMMARY: 15 ok, 0 failed
- expected_RED_output: SUMMARY: 7 ok, 8 failed
- actual_RED_output: develop e4d5f76fd 快照上 S1/S2/S4/S5/S6 全红（没有 close-linked、cmd-close 不分派），B1/B2/B8 红（linked 文档无法关闭 / 也没有 kind 守卫）（AT-001-RED.log）
- actual_output: SUMMARY: 15 ok, 0 failed；B1 rc=0、B2 status: closed、B3 phase_state 保留、B4 body 逐字、B5 linked 字段保留、B6 rc=3、B7 文档字节不变、B8/B9 双守卫（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/platform-sync/close-merged/raw-20261112T131115Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log,unit-t-linked-close-01.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4
- case_design: 静态组检查分派与函数存在性；行为组用 fixture linked/raw 文档 + stub adapter 三次运行真实 effects 入口：全绿（断言回写与保真）、partial（断言 rc!=0 且字节不变）、kind 混淆（断言双向拒绝）。
- red_how: fix RED — git archive develop 导出基线树，用 --source-dir 运行同一 AT。

## Unit
- acceptance_target: cmd-close 分派与 close_linked 的 kind 守卫
- testing_layer: unit
- target_environment: fix/raw-20261112T131115Z-issue-sync-close-linked
- required_evidence: t-linked-close-01.sh 6 项 PASS
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/unit/t-linked-close-01.sh

## Integration
- acceptance_target: raw 关单路径与 CI 子集不退化
- testing_layer: integration
- target_environment: test-pre-merge 工位
- required_evidence: bin/test-all --ci 全绿；projections verify ok；三门禁 ok
- blocker_taxonomy: execution_pending_or_failed
1. bin/test-all --ci

## End-to-End
- acceptance_target: 修复后能真正关掉现存 linked 残留
- testing_layer: end-to-end
- target_environment: 合并后的主仓
- required_evidence: issue-sync close 逐条成功、平台状态 CLOSED、本地 status: closed
- blocker_taxonomy: execution_pending_or_failed
1. ./bin/freely issue-sync --project <工位> close <I-id>（#4318 / #4311 / #4312 / #4308 / #4305）

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 缺陷在 R33.6 收尾时真机复现（close 恒失败、linked 残留无法收口），修复后逐一关掉现存残留即真机验收。
