# Pre-Tests: 物化时保留 severity 优先级
- issue_id: I-20261108T141300Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 带 `severity/P0` 标签的双平台副本物化后，本地 frontmatter 有 `severity: P0` 且单一所有者解析读回 P0；双平台显式冲突 fail-closed；无标签历史 raw 零改写；副本比较恢复对 severity/* 的区分
- acceptance_target: P0/P1 不在 `wt-create` 那一刻退回 P2，本地读视图与平台标签一致
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 真实 `platform-adapter.pull_raw_issue`（仅 mock 平台读取/assignee/title 更新）+ 真实 `raw_reconciliation.canonical_projection` + 临时目录物化；develop HEAD 基线快照对比
- required_evidence: 2 静态 + 7 行为共 9 项全 GREEN；基线 RED `1 ok / 8 failed`
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-severity-materialization.py
- test_command: python3 docs/system/workspace/scripts/tests/test-severity-materialization.py
- expected_output: SUMMARY: 9 ok, 0 failed
- expected_RED_output: SUMMARY: 1 ok / 8 failed（物化无 severity、projection 排除 severity、解析器返回 P2、无 fail-closed、无冲突检测；1 项 PASS 是「legacy 零改写」守卫——基线同样不写）
- actual_RED_output: develop `ed4a9ffea` 基线快照注入最终版 AT-001 → `SUMMARY: 1 ok, 8 failed`（AT-001-RED.log）。关键：`P0 survives materialization (found=False)`。
- actual_output: 工位同一断言 → `SUMMARY: 9 ok, 0 failed`（AT-001-GREEN.log）；`single-owner parser reads severity P0 (got P0)`。
- evidence_file: docs/B2-docs/platform/issue-parity/raw-20261108T141300Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4
- case_design: 静态组断言物化真源写入 `fm["severity"]` 且 `canonical_projection` 不再排除 severity。行为组：①双平台一致标签（含大小写 `severity/p0`）解析为 P0 ②P0 vs P1 抛 ValueError ③无标签返回 None + 告警 ④**真实 `pull_raw_issue`**（mock `discover_raw_replicas`/`check_and_claim_assignee`/`_update_issue_title`）物化出 `issue.md` 并 grep `severity: P0` ⑤`parse_issue_text` + `resolve_severity` 读回 P0 ⑥无标签物化不写 severity 行 ⑦`canonical_projection` 对 P0/P1 产生不同指纹。
- red_how: fix RED — `git archive develop -- bin docs .githooks templates .gitee-ci.yml .github contracts` 出 `/tmp/r23-base`，把最终版 AT-001 拷入快照 tests 目录，以 `--source-dir /tmp/r23-base` 运行。

## End-to-End
- acceptance_target: 真实物化链路与副本比较
- testing_layer: end-to-end
- target_environment: 真实 `pull_raw_issue` + 临时目录 + 真实 `canonical_projection`
- required_evidence: AT-001（行为 7 项）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-severity-materialization.py

## Unit
- acceptance_target: 标签解析规则与静态接线
- testing_layer: unit
- target_environment: fix/raw-20261108T141300Z-severity-on-materialize
- required_evidence: AT-001（静态 2 项 + 解析 3 项）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-severity-materialization.py

## Integration
- acceptance_target: 物化 / 契约 / 对账 / severity 能力不退化
- testing_layer: integration
- target_environment: 工位 + develop HEAD 基线快照
- required_evidence: AT-001 + 相关回归
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-materialization.py
2. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-raw-metadata.py
3. python3 docs/system/workspace/scripts/tests/test-feedback-severity.py
4. python3 docs/system/workspace/scripts/tests/test-raw-reconciliation.py
5. python3 docs/system/workspace/scripts/tests/test-raw-replica-degraded.py
6. bin/test-all --ci

## Real-Environment
- real_environment_status: pass
- real_environment_exception: 端到端物化只 mock 平台读取，不访问 GitHub/Gitee、不改真实 `.freely`、不写真实 B1 文档；物化目标为临时目录。
- real_environment_reason: 该缺陷只在 `wt-create → raw-issue-pull → pull_raw_issue` 链路中暴露，必须用真实物化函数验证；6 个相关测试与 `bin/test-all --ci` 全绿，证明恢复 severity 比较未引入历史 divergence。
