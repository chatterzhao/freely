# Pre-Tests: pretests-gate 字段值解析统一化
- issue_id: I-20261104T082740Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 字段值含 Markdown 行内代码、冒号、美元符号时仍被完整解析，空值仍判缺失且不吸纳下一行，且 #3957 的四种引号写法不退化
- acceptance_target: 字段解析真源唯一，8 处调用点共用，内容字符不再被当作分隔符
- surface_kind: unit
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: fix/raw-20261104T082740Z-pretests-gate-backtick
- required_evidence: 新增回归测试全量 GREEN，含 17 条单元断言与隔离真实 git 仓库端到端门禁通过
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-pretests-gate-inline-code-fields
- test_command: bash docs/system/workspace/scripts/tests/test-pretests-gate-inline-code-fields all
- expected_output: PASS: inline-code field parsing contract holds
- expected_RED_output: RED: 7 assertion(s) failed
- actual_RED_output: RED: 7 assertion(s) failed — 行内反引号字段被判缺失、空值字段被误收录、单双引号写法不被支持、blocker_taxonomy 含反引号不计、14 个键全部解析失败（AT-001-RED.log）
- actual_output: PASS: inline-code field parsing contract holds，17/17 单元断言通过；隔离 git 仓库中门禁退出码 0；3 条端到端检查通过（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/gate/pretests-gate-field-parsing-compat/raw-20261104T082740Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3
- case_design: 从 pretests-gate 的 heredoc 中抽出内嵌 Python 定义区并直接调用 parse_fields、parse_scalar、has_blocker_taxonomy、parse_issue_binding，覆盖行内反引号、冒号、美元符号、空值、四种引号写法、14 个字段键、blocker_taxonomy 空行语义；再在 mktemp 隔离 git 仓库中构造含行内代码的 pre-tests.md 运行真实门禁，断言无字段缺失报错且退出码 0。
- red_how: fix RED — 在当前未修复的 gate 上运行同一断言组，确认 7 项失败并复现空值跨行错读。

## Unit
- acceptance_target: 字段解析真源与 8 处调用点的结构正确性
- testing_layer: unit
- target_environment: fix/raw-20261104T082740Z-pretests-gate-backtick
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-pretests-gate-inline-code-fields unit

## Integration
- acceptance_target: parse_issue_binding 与 parse_scalar 在四种引号写法下保持兼容，parse_fields 全部 14 个键可解析
- testing_layer: integration
- target_environment: fix/raw-20261104T082740Z-pretests-gate-backtick
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-pretests-gate-inline-code-fields unit

## End-to-End
- acceptance_target: 真实 git 仓库中门禁端到端接受含行内代码的治理文档
- testing_layer: end-to-end
- target_environment: 临时 git 仓库（隔离环境）
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-pretests-gate-inline-code-fields e2e

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 在真实项目工位执行修复后的门禁与回归测试，并在隔离 git 仓库中跑通端到端门禁；另以 develop HEAD 的未修改 gate 作基线逐项比对 10 个门禁相关测试，确认 9 个既有失败完全同因、本 PR 零回归。
