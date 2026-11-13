# Pre-Tests: linked 平台状态投影与收口判据单一化
- issue_id: I-20261113T130925Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: batch 能处理 linked 并在首次同步关闭 completed+未关闭者；wt-close 只读检查（未就绪拒绝、零平台写入）；两条入口判据一致；基线红
- acceptance_target: 本地终态与平台状态可幂等对齐，且只有一条收口判据
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 抽取真实 cmd_batch / Phase 2.5 + stub 依赖，sandbox project
- required_evidence: batch AT 8/0（基线 R1 红）；wt-close AT 16/0（基线 R1/R2 红）
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-issue-sync-batch-closeout.py
- test_command: python3 docs/system/workspace/scripts/tests/test-issue-sync-batch-closeout.py
- expected_output: SUMMARY: 8 ok, 0 failed
- expected_RED_output: SUMMARY: 6 ok, 2 failed
- actual_RED_output: develop c042c3c7a 上 cmd_batch 用 basename(dirname)=issues 过滤掉全部 linked（0 处理），且 close 被 hash 门禁包裹；AT 两条红（AT-001-batch-RED.log）
- actual_output: SUMMARY: 8 ok, 0 failed；B1 首次同步关闭、B2 in_dev 不关、B3 已关不重复、B4 变更时 update+close（AT-001-batch-GREEN.log）
- evidence_file: docs/B2-docs/platform-sync/close-merged/raw-20261113T130925Z/verification/test-evidence/AT-001-batch-RED.log,AT-001-batch-GREEN.log,AT-001-wtclose-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3
- case_design: batch AT 抽取真实 cmd_batch，stub create/update/comment/close 并记录调用，覆盖四种状态组合；wt-close AT 改为检查语义，覆盖 completed/closed、in_dev、未关闭、缺失、skip-platform、dry-run。
- red_how: fix RED — git archive develop 导出基线树。

## Unit
- acceptance_target: batch 的 linked 识别与关闭判据
- testing_layer: unit
- target_environment: fix/raw-20261113T130925Z-issue-closeout-contract
- required_evidence: 两个 AT 的静态组
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-issue-sync-batch-closeout.py

## Integration
- acceptance_target: 既有收口路径与 CI 不退化
- testing_layer: integration
- target_environment: test-pre-merge 工位
- required_evidence: bin/test-all --ci 全绿
- blocker_taxonomy: execution_pending_or_failed
1. bin/test-all --ci

## End-to-End
- acceptance_target: 合并后真实对齐历史 linked
- testing_layer: end-to-end
- target_environment: 主仓 + 工位
- required_evidence: batch 关闭 #4330/#4332/#4334/#4340 等，platform_state 落盘
- blocker_taxonomy: execution_pending_or_failed
1. ./bin/freely issue-sync --project <工位> batch

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 缺陷由用户要求对齐时真机复现（batch 0 关闭、8 条静默跳过）；根因是 local_id 与 hash 双门禁。
