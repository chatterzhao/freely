# Pre-Tests: I-* 终态平台取证与关闭对账
- issue_id: I-20261125T071429Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: I-* 终态判定不再只信本地 platform_state：adapter 提供只读副本枚举，wt-close 在门禁内取证，batch/pr-merge 不再吞错
- acceptance_target: raw-20261125T071429Z 期望 1-4 与非目标边界
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261125T071429Z-wt-close-platform-truth
- required_evidence: develop 基线 RED、工位 GREEN，逐断言 ok/FAIL 与 SUMMARY 日志
- evidence_level: integration
- artifact_ref: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261125T071429Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/tests/test-wt-close-platform-truth.py
- expected_output: SUMMARY: N ok, 0 failed
- expected_RED_output: SUMMARY: <N-M> ok, M failed — 基线无 find_open_replicas_by_local_id / wt-close 无 verify-local-id 调用 / batch 与 pr-merge 仍有 `|| true`
- actual_RED_output: "SUMMARY: 0 ok, 12 failed — develop 基线无 replica_truth 模块、wt-close 无 verify-local-id、batch/pr-merge 仍吞错（证据 acceptance-1-red.log）"
- actual_output: "SUMMARY: 18 ok, 0 failed；另 test-wt-close-children.py 17 ok/0 failed（含 B8 平台 OPEN 副本阻断）（证据 acceptance-1.log）"
- evidence_file: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261125T071429Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: 对 develop 源码跑同一 AT（--source-dir <develop>）；基线缺少只读枚举函数、门禁未取证、两处 `|| true` 存在，断言必然命中。
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: T1-T5
- case_design: 行为断言（过滤函数对 OPEN/CLOSED/跨 id/raw 标题的判定）+ 源码结构断言（门禁取证调用、无吞错写法、去重存在）

## Unit
- acceptance_target: 只读副本过滤逻辑与门禁接线
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: 每条 check 打印 ok/FAIL，SUMMARY 汇总
- blocker_taxonomy: execution_pending_or_failed
- test_tasks:
  1. `find_open_replicas_by_local_id` 对混合记录返回仅 OPEN 且标题含 local_id 的副本。
  2. 不把 `[RAW-...]` 标题、其他 I-* 标题计入。
  3. degraded 读失败时返回 ok=False（不得当成空列表）。
  4. `wt-close` Phase 2.5 含 `verify-local-id` 调用且失败即 exit 1。
  5. `cmd-batch.sh` 无 `cmd_close_linked "$local_id" || true`；`pr-merge-guarded` 无 `batch "$_raw_key" || true`。
  6. `_already_on_platform` 含平台侧判定。

## Integration
- acceptance_target: 关闭通道对账 + 合并门禁 fail-closed
- testing_layer: integration
- target_environment: test-pre-merge 工位
- required_evidence: `close_linked` 走 `close-local-id`；batch 汇总退出码；pr-merge 捕获 rc
- test_tasks:
  1. 断言 `raw_lifecycle_effects.close_linked` 调用 `close-local-id` 而非 `close-multi`。
  2. 断言 batch 在任一 close 失败时最终非零退出。
  3. 断言 pr-merge 在 batch 非零时打印中止信息并退出非零。

## End-to-End
- acceptance_target: 平台真实状态变为门禁判据
- testing_layer: end-to-end
- target_environment: test-pre-merge 工位（只读调用真实平台）
- required_evidence: `platform-adapter.py verify-local-id I-20261125T071429Z-A` 在实现前报未知命令、实现后返回 `{"ok": true, "replicas": {}}` 或明确 OPEN 列表
- test_tasks:
  1. 实现后执行只读取证命令，确认 JSON 结构与退出码。
  2. 确认取证过程无平台写（不产生新的 issue/comment）。
