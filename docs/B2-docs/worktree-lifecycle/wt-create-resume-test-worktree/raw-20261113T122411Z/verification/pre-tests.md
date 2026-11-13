# Pre-Tests: children 报告的空字段不再折叠 TSV 列
- issue_id: I-20261113T122411Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 缺失 platform_state 时仍能定位并关闭 2 个 children；基线必须失败
- acceptance_target: 消除 TSV 空列折叠导致的收口失败
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 抽取真实 Phase 2.5 块 + helper，sandbox project + 记录调用的 adapter
- required_evidence: AT-001 GREEN 16/0；基线 18/1（B8 红）
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-wt-close-children.py
- test_command: python3 docs/system/workspace/scripts/tests/test-wt-close-children.py
- expected_output: SUMMARY: 16 ok, 0 failed
- expected_RED_output: SUMMARY: 18 ok, 1 failed
- actual_RED_output: develop 651214f27 上 R1/R2/R3 通过（已有 Phase 2.5、无占位、缺失 platform_state 时关闭失败），B8 红（AT-001-RED.log）
- actual_output: SUMMARY: 16 ok, 0 failed；B8 两 child 均缺 platform_state 仍关闭 2 次（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261113T122411Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2
- case_design: fixture 支持「字段缺失」（不写该行）；B8 用两个缺失 platform_state 的 child；基线断言改为结构（有 Phase 2.5、无占位）+ 行为（缺失时关闭失败）。
- red_how: fix RED — git archive develop 导出基线树。

## Unit
- acceptance_target: 占位输出
- testing_layer: unit
- target_environment: fix/raw-20261113T122411Z-wt-close-tsv-empty-field
- required_evidence: AT-001 静态 8 项
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-wt-close-children.py

## Integration
- acceptance_target: 既有收口路径与 CI 不退化
- testing_layer: integration
- target_environment: test-pre-merge 工位
- required_evidence: bin/test-all --ci 全绿
- blocker_taxonomy: execution_pending_or_failed
1. bin/test-all --ci

## End-to-End
- acceptance_target: 合并后收口 R33.15 残留工位
- testing_layer: end-to-end
- target_environment: 主仓
- required_evidence: wt-close --raw-key 20261113T115957Z 成功
- blocker_taxonomy: execution_pending_or_failed
1. ./bin/freely wt-close --raw-key 20261113T115957Z --discard-unmerged --force --reason "<合规前缀+理由>"

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 缺陷在 R33.15 真机收口时复现（no platform_ids），修复后用于收口该工位。
