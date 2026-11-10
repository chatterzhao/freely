# Pre-Tests: raw H1 判定改为代码块感知
- issue_id: I-20261110T093145Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 单一契约导出代码块感知的标题查找器，物化 / 副本 gate / H1 backfill 三处复用；gate 无真实 H1 时报 `missing_local_title`；helper 对 ``` 与 ~~~ 围栏均正确；真实 `pull_raw_issue` 注入 H1 且保留正文；真实 `_local_record` 不借注释当 title 且保留正文；backfill 能修复这类文档；既有 H1 套件不退化
- acceptance_target: 副本一致性检查不再因 body 里的代码注释误判标题，健康 raw 的首个 PR 不被误挡
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 真实 `raw_title_contract` / `platform-adapter.pull_raw_issue`（只 stub 平台读取）/ `raw-reconciliation-gate._local_record` / `raw-issue-backfill-h1`（独立临时项目）；develop HEAD 基线快照对比
- required_evidence: 6 静态 + 4 单元 + 4 行为共 14 项全 GREEN；基线 RED `2 ok / 12 failed`
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-raw-title-codeblock.py
- test_command: python3 docs/system/workspace/scripts/tests/test-raw-title-codeblock.py
- expected_output: SUMMARY: 14 ok, 0 failed
- expected_RED_output: SUMMARY: 2 ok / 12 failed（helper 不存在、三处裸正则仍在、无显式诊断、物化不注入 H1、gate 借注释当 title、backfill 跳过修复；2 项 PASS 是守卫：既有 H1 套件仍绿、物化保留正文）
- actual_RED_output: develop `34d80fe18` 基线快照注入最终版 AT-001 → `SUMMARY: 2 ok, 12 failed`（AT-001-RED.log）。关键证据：`local record does not borrow a code comment as title (got '-> StateFileError: not a title')`。
- actual_output: 工位同一断言 → `SUMMARY: 14 ok, 0 failed`（AT-001-GREEN.log）；`materialization injects a real H1 ahead of the code comment`、`local record does not borrow a code comment as title (got '')`。
- evidence_file: docs/B2-docs/platform/issue-parity/raw-20261110T093145Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5
- case_design: 静态组断言契约含 `find_local_heading`/`_FENCE`、三处复用、gate 含 `missing_local_title`，并实跑既有 `test-materialize-h1 all` 与「backfill 修复含代码注释文档」的真实命令。单元组验证 helper：无 H1 + 代码块注释返回 None、真实 H1 优先、`~~~` 围栏同样忽略。行为组用真实 `pull_raw_issue`（stub `discover_raw_replicas`/assignee/title 更新）物化含 python 注释的 body，断言 H1 注入在注释之前且正文完整；再用真实 `_local_record` 断言 title 为空、body 完整。
- red_how: fix RED — `git archive develop -- bin docs .githooks templates .gitee-ci.yml .github contracts` 出 `/tmp/r23f-base`，**只**拷最终版 AT-001，以 `--source-dir /tmp/r23f-base` 运行。

## End-to-End
- acceptance_target: 真实物化 / 真实 gate / 真实 backfill 的联动行为
- testing_layer: end-to-end
- target_environment: 真实模块 + 临时项目目录
- required_evidence: AT-001（行为 4 项 + backfill 命令）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-raw-title-codeblock.py

## Unit
- acceptance_target: 代码块感知查找器与静态契约
- testing_layer: unit
- target_environment: fix/raw-20261110T093145Z-raw-title-parse
- required_evidence: AT-001（静态 6 项 + 单元 4 项）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-raw-title-codeblock.py

## Integration
- acceptance_target: 既有物化 / 契约 / 副本 / 状态能力不退化
- testing_layer: integration
- target_environment: 工位 + develop HEAD 基线快照
- required_evidence: AT-001 + 相关回归
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-materialize-h1 all
2. python3 docs/system/workspace/scripts/tests/test-raw-reconciliation.py
3. python3 docs/system/workspace/scripts/tests/test-raw-replica-degraded.py
4. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-materialization.py
5. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-raw-metadata.py
6. python3 docs/system/workspace/scripts/tests/test-severity-materialization.py
7. python3 docs/system/workspace/scripts/tests/test-feedback-severity.py
8. python3 docs/system/workspace/scripts/tests/test-state-key-whitelist.py
9. python3 docs/system/workspace/scripts/tests/test-state-file-protocol.py
10. bin/test-all --ci

## Real-Environment
- real_environment_status: pass
- real_environment_exception: 物化 / 回填都在临时目录的独立项目进行，只 stub 平台读取，不访问 GitHub/Gitee、不写主仓 B1 文档。真实只读核对：`raw-reconciliation-gate --require-local` 对当前工位 raw 返回 allow。
- real_environment_reason: 缺陷位于「平台 body → 本地文档 → 副本一致性」链路，必须用真实物化函数与真实 gate 验证；10 项回归 + `test-all --ci` 全绿，确认既有契约语义未变。
