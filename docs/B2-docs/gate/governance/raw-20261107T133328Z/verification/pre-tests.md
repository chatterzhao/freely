# Pre-Tests: wt-close 复用单一评论扫描
- issue_id: I-20261107T133328Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: `wt-close` 不再自己数评论（无 `grep -c "^### comment-"`），改为调用 `quality/comment-resolution-scan.py` 并按其对**本 issue** 的判定阻塞；只有系统事件评论（`- source: system`）不阻塞；人类评论无 `#### resolution-` 阻塞、补后放行；`$((...))` 破损文案消失；两个门禁结论一致
- acceptance_target: 评论 resolution 规则只有一个实现，系统事件评论不再被当人类评论
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: integration
- target_environment: 隔离 B1 夹具目录 + 真实 `wt-close` 与真实 `comment-resolution-scan.py` + develop HEAD 基线快照对比
- required_evidence: 5 项静态断言 + 5 个行为场景全 GREEN；相关回归基线对比退出码一致
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-wt-close-comment-scan
- test_command: bash docs/system/workspace/scripts/tests/test-wt-close-comment-scan all
- expected_output: SUMMARY: 10 ok, 0 failed
- expected_RED_output: SUMMARY: 3 failed（静态 2：wt-close 仍在计数、无 `$((` 破损文案未消；行为 1：系统事件评论仍阻塞）
- actual_RED_output: develop `42fb5833a` 基线快照内放入最终版 AT-001 —— `SUMMARY: 7 ok, 3 failed`（AT-001-RED.log）
- actual_output: 工位同一断言 —— `SUMMARY: 10 ok, 0 failed`（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/gate/governance/raw-20261107T133328Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5
- case_design: 行为组构造 B1 夹具目录，按 `wt-close` 现在的判定方式（跑 scan、看本 issue 是否出现在输出里）复算结论；三种文档形态（无评论 / 仅系统评论 / 人类评论 ± resolution）逐一断言，并额外断言 scan 的 rc 与 wt-close 结论一致。
- red_how: fix RED — `git archive develop -- bin docs` 出基线快照，把最终版 AT-001 拷入后运行。

## Unit
- acceptance_target: 静态契约（无第二份实现、引用单一扫描、无破损文案、语法）
- testing_layer: unit
- target_environment: fix/raw-20261107T133328Z-wt-close-single-comment-scan
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-wt-close-comment-scan static

## Integration
- acceptance_target: wt-close 的其他 Phase 与相邻门禁不退化
- testing_layer: integration
- target_environment: 工位 + 未修改 develop 基线对比
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-issue-sync-promote-b2
2. bash docs/system/workspace/scripts/tests/test-issue-sync-close-terminal-first
3. bash docs/system/workspace/scripts/tests/test-test-gate-record
4. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-wt-close.py
5. python3 docs/system/workspace/scripts/tests/test-raw-reconciliation.py

## End-to-End
- acceptance_target: 两个门禁对同一文档结论一致
- testing_layer: end-to-end
- target_environment: 隔离 B1 夹具目录
- required_evidence: AT-001
- blocker_budget: 0
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-wt-close-comment-scan behavior

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 全链路使用真实 `wt-close` 与真实 scan；真实收口证据是本轮合并后用 `freely wt-close --raw-key 20261104T082556Z`（R13）与 `--raw-key 20261107T133328Z`（本轮）各跑一次，二者此前都因该判定失败。
