# Pre-Tests: 标题规范化前移到 scan 漏斗

- issue_id: I-20261116T050414Z-A

## Acceptance Items

### acceptance-1

- id: AT-001
- requirement: `freely task-source-scan` 在调用 scan 分析器前把平台 OPEN raw 的不规范标题改为 canonical，打印 from→to，且分析器/pre-scan 辅助脚本零平台写
- acceptance_target: 从平台拿到 raw 之后所有本地环节看到的都是 `[RAW-<key>] <human>`
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261116T050414Z-scan-title-normalize
- required_evidence: develop 基线 RED（标题不变、无 from→to）；修复后 GREEN（标题 canonical、打印 from→to、scan 输出含该 key）
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-raw-title-normalize.py
- test_command: python3 docs/system/workspace/scripts/tests/test-raw-title-normalize.py
- expected_output: SUMMARY with 0 failed, including scan-preflight E2E and read-only boundary assertions
- expected_RED_output: ImportError/AttributeError（normalize_open_raw_titles 不存在）或标题仍为旧值、无 from→to 输出
- actual_RED_output: (RED 阶段填写)
- actual_output: (GREEN 阶段填写)
- evidence_file: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261116T050414Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: pending
- status: pending
- blocker: ''
- task_refs: T1,T2
- case_design: 用 FakeHandler 注入两条平台 OPEN 记录（标题缺前缀但 body 含 `raw-<key>`、另一条已达标），断言只有前者触发写、标题变为 canonical、stdout 含 from→to、重复执行零写；另断言 task-lifecycle-scan.py 与 pre-scan-fix.sh 的调用记录无平台写。
- red_how: fix RED — 在 develop 基线上跑同一 AT，规范化模块不存在，端到端断言失败。

### acceptance-2

- id: AT-002
- requirement: gate 报 `non_canonical_title` 且含 observed/expected/suggested_command；pr-create preflight 调用规范化并重跑只读门禁；其余 fact 仍 fail-closed
- acceptance_target: 已 absorbed/CLOSED raw 的标题问题也能在提 PR 前自动修复并打印 from→to
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: integration
- target_environment: test-pre-merge-20261116T050414Z-scan-title-normalize
- required_evidence: 基线 RED 无该诊断；修复后诊断字段齐全、pr-create 场景 allow、content_diverged 场景仍 block
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-raw-title-normalize.py
- test_command: python3 docs/system/workspace/scripts/tests/test-raw-title-normalize.py
- expected_output: SUMMARY with 0 failed, including gate diagnostic and pr-create preflight cases
- expected_RED_output: receipt 无 `non_canonical_title` 诊断；pr-create 仍只打印「resolve explicitly」
- actual_RED_output: (RED 阶段填写)
- actual_output: (GREEN 阶段填写)
- evidence_file: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261116T050414Z/verification/test-evidence/AT-002-RED.log,AT-002-GREEN.log
- red-green-status: pending
- status: pending
- blocker: ''
- task_refs: T3,T4
- case_design: 构造带非达标标题的 replica 记录跑 `reconcile()`，断言诊断 code/字段；构造 pr-create Step 0b 的 preflight 分支，断言只调用一次规范化并重跑 gate；content_diverged/ambiguous 场景断言零平台写且 rc≠0。
- red_how: fix RED — develop 基线 `reconcile()` 不产出该诊断。

## Unit

- acceptance_target: `canonical_raw_title()` 与 `extract_raw_key()` 的组合在标题缺前缀时能由 body 定 key 并算出 expected_title
- testing_layer: unit
- target_environment: fix/raw-20261116T050414Z-scan-title-normalize
- required_evidence: AT-001 内的纯函数断言全部通过
- blocker_taxonomy: execution_pending_or_failed
1. 跑 AT-001 中的 key 提取与标题规范化纯函数断言。
2. 跑 `--dry-run` 零写断言。

## Integration

- acceptance_target: scan 命令 preflight 与 gate 诊断在同一测试脚本内协同验证
- testing_layer: integration
- target_environment: test-pre-merge-20261116T050414Z-scan-title-normalize
- required_evidence: AT-001/AT-002 的 FakeHandler 调用记录
- blocker_taxonomy: execution_pending_or_failed
1. 跑 AT-001 的 FakeHandler 平台写记录断言。
2. 跑 AT-002 的 gate 诊断与 pr-create preflight 断言。

## End-to-End

- acceptance_target: `freely task-source-scan` 全流程在测试工位跑通且 bin 投影一致
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261116T050414Z-scan-title-normalize
- required_evidence: `bin/test-all --ci` 全绿 + `projections verify` rc=0
- blocker_taxonomy: execution_pending_or_failed
1. 在测试工位同步 dev 提交后跑 `bin/test-all --ci`。
2. 跑 `./bin/projections verify --project <test-wt>`。

## Real-Environment

- real_environment_status: pass
- real_environment_reason: FakeHandler 端到端覆盖平台 OPEN 记录读取、标题改写、from→to 输出、幂等与只读边界；真实双平台写入由既有 adapter 测试与本次合并后门禁覆盖。
