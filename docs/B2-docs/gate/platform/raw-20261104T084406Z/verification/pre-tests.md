# Pre-Tests: severity 从校验值变成可追溯的一等数据
- issue_id: I-20261104T084406Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: `--severity P0` 创建后 frontmatter 含 `severity: P0`；默认路径显式写 `P2`；平台 issue 带 `severity/Pn` label 且真实 adapter 转发给双平台 handler、旧 2 参 handler 不退化；`scan` 按 P0→P1→P2 排序且存量文档按 P2 参与；`validate()` 接受 21/22 两种合法形状并拒绝非法值；`normalize()`/`_labels()` 读视图回填 P2
- acceptance_target: 优先级从「校验后丢弃的参数」变成 frontmatter、平台标签、扫描报告三处一致可读的一等数据，且零历史文件改写
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 隔离 fixture（stub platform-adapter / freely_config，真实 `runtime/freely`、`bin/issue-sync`、`raw_metadata_contract.py` 作为库加载）+ develop HEAD 基线快照对比
- required_evidence: 6 静态 + 14 单元 + 10 行为共 30 项全 GREEN；14 个相关回归 worktree/baseline 退出码全 MATCH
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-feedback-severity.py
- test_command: python3 docs/system/workspace/scripts/tests/test-feedback-severity.py all
- expected_output: SUMMARY: 30 ok, 0 failed
- expected_RED_output: SUMMARY: 14 failed（静态 4：契约无 severity、feedback 不传参、issue-sync 无标签、normalize 无默认值；单元 1：无 VALID_SEVERITIES；行为 8：P0/P2 frontmatter 与 label 全缺、`_labels` 无 severity、scan 无排序、adapter 无 labels 参数）
- actual_RED_output: develop `444985f50` 基线快照（`git archive develop -- bin docs`）放入**最终版** AT-001 —— `SUMMARY: 3 ok, 14 failed`（AT-001-RED.log）：`--severity P0 -> frontmatter missing severity`、`create-issue labels missing severity/P0`、`_labels missing severity/P0`、`adapter create_issue has no labels parameter (RED): create_issue() takes 3 positional arguments but 4 were given` 等
- actual_output: 工位同一断言 —— `SUMMARY: 30 ok, 0 failed`（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/gate/platform/raw-20261104T084406Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log,AT-001-REGRESSION-BASELINE.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5,T6,T7
- case_design: 静态组断言四处真源都有 severity 接线；单元组直接用 importlib 加载真实契约模块，覆盖 21 字段不退化、22 字段追加、非法值拒绝、`normalize` 回填；行为组用隔离 fixture 驱动真实 `cmd_feedback`（stub 只替换平台边界与 config），断言 create-issue argv 的 body 与 labels，再用真实 `issue-sync` 的 `_labels`/`cmd_scan` 断言标签与排序，最后用真实 adapter 模块的 Probe/Legacy 双 handler 断言标签转发与 2 参兼容。
- red_how: fix RED — `git archive develop -- bin docs` 出基线快照，把最终版 AT-001 拷入后以 `--source-dir /tmp/r15-base` 运行，基线文件一个不改。

## Unit
- acceptance_target: 契约语义（21 字段兼容、22 字段追加、非法值拒绝、读视图回填）
- testing_layer: unit
- target_environment: fix/raw-20261104T084406Z-feedback-severity-persist
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-feedback-severity.py static
2. python3 docs/system/workspace/scripts/tests/test-feedback-severity.py unit

## Integration
- acceptance_target: 写通道、关闭路径、promote、test-gate、wt-close、契约、reconciliation、governance 等既有能力不退化
- testing_layer: integration
- target_environment: 工位 + 未修改 develop HEAD 基线对比
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-platform-write-channel
2. bash docs/system/workspace/scripts/tests/test-issue-sync-close-terminal-first
3. bash docs/system/workspace/scripts/tests/test-issue-sync-promote-b2
4. bash docs/system/workspace/scripts/tests/test-test-gate-record
5. bash docs/system/workspace/scripts/tests/test-wt-close-comment-scan
6. python3 docs/system/workspace/scripts/tests/test-raw-reconciliation.py
7. python3 docs/system/workspace/scripts/tests/test-raw-replica-degraded.py
8. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-raw-metadata.py
9. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-materialization.py
10. python3 docs/system/workspace/scripts/tests/test-platform-handler-probe.py
11. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-wt-close.py
12. python3 docs/system/workspace/scripts/tests/test-scan-frontmatter-nested.py
13. python3 docs/system/workspace/scripts/tests/test-platform-open-parity.py
14. bash docs/system/workspace/scripts/tests/test-governance-gate-batch-read

## End-to-End
- acceptance_target: feedback 真实运行 → frontmatter/label → scan 排序 → adapter 双平台转发
- testing_layer: end-to-end
- target_environment: 隔离 fixture（stub 仅替换平台边界）
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-feedback-severity.py behavior

## Real-Environment
- real_environment_status: pass
- real_environment_exception: 平台侧建单在测试中用 stub 覆盖，避免在真实仓库制造新 issue；真实转发路径由 adapter 模块的 Probe/Legacy 行为用例守护。
- real_environment_reason: 链路中只有平台 CLI 与 config 被 stub 替换，`runtime/freely`、`bin/issue-sync`、`raw_metadata_contract.py`、`platform-adapter.py` 都是真实文件真实执行；14 个相关回归 worktree/baseline 退出码全 MATCH（`test-command-lifecycle-wt-close.py` 的 1 项失败为预存红，基线同用例同断言）。
