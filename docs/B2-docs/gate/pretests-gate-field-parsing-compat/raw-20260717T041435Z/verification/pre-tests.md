# Pre-Tests: 门禁字段解析引号可选化
- issue_id: I-20260717T041435Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: pretests-gate extract 四格式解析（AC1）
- acceptance_target: 裸值/'单'/"双"/`反` 均解析出纯路径且过 VERIFICATION_DIR_RE
- testing_layer: integration
- target_environment: fix/raw-20260717T041435Z-gate-parser-quote-compat
- required_evidence: python 行为测试输出 4/4
- evidence_level: integration
- artifact_ref: docs/B2-docs/gate/pretests-gate-field-parsing-compat/raw-20260717T041435Z/verification/test-evidence/acceptance-1.log
- test_command: bash docs/B2-docs/gate/pretests-gate-field-parsing-compat/raw-20260717T041435Z/verification/harness/at001-gate-extract.sh
- expected_output: "AT-001 PASS: 4/4 格式解析通过"
- expected_RED_output: "AT-001 FAIL: quoted 格式解析失败"
- actual_RED_output: single/double 引号格式解析失败 → AT-001 FAIL (2/4)
- actual_output: AT-001 PASS: 4/4 格式解析通过
- evidence_file: docs/B2-docs/gate/pretests-gate-field-parsing-compat/raw-20260717T041435Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: pass
- blocker:
- red_how: fix — 现 extract 只剥反引号，单/双引号格式必失配 RE

### acceptance-2
- id: AT-002
- requirement: pr-review-guarded 取值四格式兼容（AC2）
- acceptance_target: 同四格式行经取值逻辑均得纯路径
- testing_layer: integration
- target_environment: fix/raw-20260717T041435Z-gate-parser-quote-compat
- required_evidence: bash 行为测试输出 4/4
- evidence_level: integration
- artifact_ref: docs/B2-docs/gate/pretests-gate-field-parsing-compat/raw-20260717T041435Z/verification/test-evidence/acceptance-2.log
- test_command: bash docs/B2-docs/gate/pretests-gate-field-parsing-compat/raw-20260717T041435Z/verification/harness/at002-review-extract.sh
- expected_output: "AT-002 PASS: 4/4 格式解析通过"
- expected_RED_output: "AT-002 FAIL: 裸值格式解析出整行"
- actual_RED_output: bare/double/backtick 解析出整行 → AT-002 FAIL (1/4)
- actual_output: AT-002 PASS: 4/4 格式解析通过
- evidence_file: docs/B2-docs/gate/pretests-gate-field-parsing-compat/raw-20260717T041435Z/verification/test-evidence/acceptance-2.log
- red-green-status: green
- status: pass
- blocker:
- red_how: fix — 现 sed 只认单引号包裹，裸值必返回整行

### acceptance-3
- id: AT-003
- requirement: 存量 I-* 双向回归（AC3）
- acceptance_target: 引号版（raw-20260717T004620Z）与双行版（raw-20260717T004721Z）的 I-* 经两解析器均得合法路径
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260717T041435Z-gate-parser-quote-compat
- required_evidence: 对 develop 已合并真实文件的解析输出
- evidence_level: real_env
- artifact_ref: docs/B2-docs/gate/pretests-gate-field-parsing-compat/raw-20260717T041435Z/verification/test-evidence/acceptance-3.log
- test_command: bash docs/B2-docs/gate/pretests-gate-field-parsing-compat/raw-20260717T041435Z/verification/harness/at003-legacy-regression.sh
- expected_output: "AT-003 PASS: 存量双格式全通过"
- expected_RED_output: "AT-003 FAIL（引号版被 gate 解析失配 或 无引号 bullet 被 review 解析成整行）"
- actual_RED_output: gate 解析失配: I-20260717T004620Z-A.md got='...'(带引号) → AT-003 FAIL
- actual_output: AT-003 PASS: 存量双格式全通过（引号版 I-20260717T004620Z-A + 双行版 I-20260717T004721Z-A 双解析器重放）
- evidence_file: docs/B2-docs/gate/pretests-gate-field-parsing-compat/raw-20260717T041435Z/verification/test-evidence/acceptance-3.log
- red-green-status: green
- status: pass
- blocker:
- red_how: fix — 今日 lane A/C 双向拦截即实证；对已合并真实文件重放解析即复现

## Unit
- acceptance_target: 解析行为最小面
- testing_layer: unit
- target_environment: fix/raw-20260717T041435Z-gate-parser-quote-compat
- required_evidence: AT-001/002 内含单格式子断言
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 解析器无独立单元边界（gate 为脚本级 python 函数、review 为内联 sed），行为面已由 AT-001/002 的四格式矩阵覆盖
- replacement_evidence: AT-001/AT-002 的 4/4 矩阵输出

## Integration
- acceptance_target: 两解析器四格式矩阵
- testing_layer: integration
- target_environment: fix/raw-20260717T041435Z-gate-parser-quote-compat
- required_evidence: AT-001/AT-002 PASS
- blocker_taxonomy: execution_pending_or_failed
1. AT-001
2. AT-002

## End-to-End
- acceptance_target: 存量真实文件双向回归
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260717T041435Z-gate-parser-quote-compat → develop merge chain
- required_evidence: AT-003 PASS + guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
1. AT-003

## Real-Environment
- real_environment_status: pass
- real_environment_reason: AT-003 对 develop 已合并真实 I-* 文件（引号版+双行版）双解析器重放全通过
