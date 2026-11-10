# Pre-Tests: 状态键白名单由自动扫描 lint 守护
- issue_id: I-20261110T084522Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 白名单不再宣称未经验证的扫描且指向 lint；lint 存在、missing=0、stale=0；扫描器覆盖 6 类写入形态且不误抓局部变量；65 个新键 legacy 与 TAB+JSON 逐字节往返；恶意值不执行；未知键仍拒绝；issue 复现的 mixed legacy 文件可读
- acceptance_target: 「状态键」从人工清单变成由可执行扫描器守护的契约，消除兼容读取时静默丢状态
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 真实 `state_file.py` + 真实 `bin/check-state-file-keys`（含 `--project` 驱动的独立夹具项目）+ 临时状态文件；develop HEAD 基线快照对比
- required_evidence: 4 静态 + 7 扫描器 + 5 行为共 16 项全 GREEN；基线 RED `1 ok / 15 failed`
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-state-key-whitelist.py
- test_command: python3 docs/system/workspace/scripts/tests/test-state-key-whitelist.py
- expected_output: SUMMARY: 16 ok, 0 failed
- expected_RED_output: SUMMARY: 1 ok / 15 failed（lint 不存在、白名单 77 键、65 键 legacy/TAB+JSON 全失败、issue 复现抛错；唯一 PASS 是「伪造未知键仍拒绝」——防止把护栏一起放宽）
- actual_RED_output: develop `6b927cae1` 基线快照注入最终版 AT-001 → `SUMMARY: 1 ok, 15 failed`（AT-001-RED.log）。关键：`all 65 newly registered keys are in ALLOWED_KEYS (missing 65)`、`verdict-compatible legacy file with mixed keys reads` FAIL —— 正是 issue 的原始复现。
- actual_output: 工位同一断言 → `SUMMARY: 16 ok, 0 failed`（AT-001-GREEN.log）；`lint reports zero missing keys (got 0, rc=0)`、`lint reports zero stale keys (got 0)`。
- evidence_file: docs/B2-docs/runtime/daemon/raw-20261110T084522Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5
- case_design: 静态组断言模块注释、lint 存在、lint `--json` 的 missing/stale 皆空。扫描器组构造**独立临时项目**（复制 `state_file.py`，写一份含 6 类写入形态的假 `freely`），以 `--project` 驱动 lint 并断言每个形态的键都被抽到、且 `accumulated`/`now_epoch` 等局部变量未泄漏。行为组对 65 个键逐一验证 legacy `KEY="value"` 读回、TAB+JSON 写读逐字节（值含 `"`/`$()`/反引号，marker 不创建）、伪造键仍抛错、issue 复现的 mixed legacy 文件读到正确值。
- red_how: fix RED — `git archive develop -- bin docs .githooks templates .gitee-ci.yml .github contracts` 出 `/tmp/r23e-base`，**只**拷最终版 AT-001，以 `--source-dir /tmp/r23e-base` 运行。

## End-to-End
- acceptance_target: 真实扫描器 + 真实协议读写
- testing_layer: end-to-end
- target_environment: 真实 lint（--project 夹具）+ 真实模块
- required_evidence: AT-001（扫描器 7 项 + 行为 5 项）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-state-key-whitelist.py

## Unit
- acceptance_target: 白名单契约与 lint 静态结果
- testing_layer: unit
- target_environment: fix/raw-20261110T084522Z-state-key-whitelist
- required_evidence: AT-001（静态 4 项）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-state-key-whitelist.py

## Integration
- acceptance_target: 协议三族、runtime 与既有测试不退化
- testing_layer: integration
- target_environment: 工位 + develop HEAD 基线快照
- required_evidence: AT-001 + 相关回归
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-state-file-protocol.py
2. python3 docs/system/workspace/scripts/tests/test-state-family-cooldown.py
3. python3 docs/system/workspace/scripts/tests/test-state-family-execution-network.py
4. bash docs/system/workspace/scripts/tests/test-freely-execution-network-failure-classification
5. python3 docs/system/workspace/scripts/tests/test-source-safe-library.py
6. python3 docs/system/workspace/scripts/tests/test-concurrency-singletons.py
7. python3 docs/system/workspace/scripts/tests/test-severity-materialization.py
8. python3 docs/system/workspace/scripts/tests/test-raw-reconciliation.py
9. python3 docs/system/workspace/scripts/tests/test-db-single-writer.py
10. python3 docs/system/workspace/scripts/tests/test-frontmatter-ownership.py
11. bash docs/system/workspace/scripts/tests/test-wt-close-comment-scan
12. bash docs/system/workspace/scripts/tests/test-issue-sync-promote-b2
13. bash docs/system/workspace/scripts/tests/test-test-gate-record
14. python3 bin/check-state-file-sources
15. python3 bin/check-state-file-keys
16. bin/test-all --ci

## Real-Environment
- real_environment_status: pass
- real_environment_exception: 所有状态文件操作在临时目录进行；扫描器夹具是独立临时项目，不触碰主仓 `runtime/freely`；PoC 的 `touch` 只作用于临时目录。
- real_environment_reason: 缺陷只在「真实模块读真实格式的存量文件」时暴露；16 项回归 + `test-all --ci` + 两个 lint 全绿，确认白名单补齐未影响任何既有能力。
