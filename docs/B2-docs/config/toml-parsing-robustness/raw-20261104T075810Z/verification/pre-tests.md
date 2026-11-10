# Pre-Tests: config schema + doctor 可观测类型校验
- issue_id: I-20261104T075810Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 配置契约覆盖全部 58 键；字符串 `allowed_paths`、未知键、必填缺失、bool/int/float 混淆必须报出 `文件:行号` 与期望类型；合法 list 配置与随附模板必须通过；schema 缺失必须 fail-closed
- acceptance_target: 配置写错不再静默降级，外部项目能验证自己的配置是否被正确理解
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 真实 `bin/freely doctor` 子进程 + 临时项目 `.freely/config.toml` + develop HEAD 基线快照（`git archive develop -- bin docs .githooks templates .gitee-ci.yml .github`）
- required_evidence: 12 静态/对照 + 8 行为共 20 项全 GREEN；基线 RED `2 ok / 18 failed`
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-config-schema-validation.py
- test_command: python3 docs/system/workspace/scripts/tests/test-config-schema-validation.py
- expected_output: SUMMARY: 20 ok, 0 failed
- expected_RED_output: SUMMARY: 2 ok, 18 failed（S11 模板已 list、S12 gate 静默分支存在两项对照组 PASS）
- actual_RED_output: develop `d02586ecb` 基线快照注入最终版 AT-001 → `2 ok, 18 failed`（AT-001-RED.log）
- actual_output: 工位同一断言 → `20 ok, 0 failed`（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/config/toml-parsing-robustness/raw-20261104T075810Z/verification/test-evidence/AT-001-RED.log,docs/B2-docs/config/toml-parsing-robustness/raw-20261104T075810Z/verification/test-evidence/AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5
- case_design: 静态组核对 schema 存在/stdlib 可解析/覆盖 58 键/`list[str]` 声明/必填/字段完整/doctor 单一接线/无第二份实现/随包；对照组确认模板已是 list 与 gate 静默分支真实存在（这两项在基线 PASS，证明断言未测错对象）。行为组构造 4 类坏配置（字符串 allowed_paths + 未知键、缺必填、类型混淆、模板合法配置）逐条核对 `file:line` 与 rc；另验 schema 缺失 rc=2 与真实 `bin/freely doctor` 输出携带诊断。
- red_how: fix RED — `git archive develop` 出 `/tmp/r23-base`，把最终版 AT-001 拷入快照 tests 目录，以 `--source-dir /tmp/r23-base` 运行。

## End-to-End
- acceptance_target: 真实 `freely doctor` 对坏配置给出带行号诊断
- testing_layer: end-to-end
- target_environment: 真实 `bin/freely` 子进程 + 临时项目
- required_evidence: AT-001（B8）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-config-schema-validation.py

## Unit
- acceptance_target: schema 结构与类型判定
- testing_layer: unit
- target_environment: fix/raw-20261104T075810Z-config-schema-validation
- required_evidence: AT-001（静态组 + B1–B7）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/quality/config_schema.py --project . --json

## Integration
- acceptance_target: 既有门禁与命令链不退化
- testing_layer: integration
- target_environment: 工位 + develop HEAD 基线快照
- required_evidence: AT-001 + 相关回归
- blocker_taxonomy: execution_pending_or_failed
1. bash -n docs/system/workspace/scripts/runtime/freely
2. ./bin/check-epics-map --project .
3. bin/test-all --ci

## Real-Environment
- real_environment_status: pass
- real_environment_exception: 临时项目不访问平台、不改仓库；主仓与本工位的 gitignored `.freely/config.toml` 现场修正为 list，属运行时状态修正，不进入 PR。
- real_environment_reason: 真实 `./bin/freely doctor --project <abs>` 在修正前输出 `config_schema: INVALID ...:60 ... got str`、修正后输出 `config_schema: ok`；`bash -n` 与 `check-epics-map`（16 epics / 206 stories aligned）通过；gate 文件 sha256 前后一致。
