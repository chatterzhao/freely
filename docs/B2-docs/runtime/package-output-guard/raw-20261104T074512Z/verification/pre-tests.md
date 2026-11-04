# Pre-Tests: freely-package 输出路径安全守卫
- issue_id: I-20261104T074512Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: --output 指向 /、$HOME、.. 或白名单外目录时，必须在 rm -rf 之前拒绝
- acceptance_target: `refuse_dangerous_output()` 存在且在删除前执行
- surface_kind: unit
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: fix/raw-20261104T074512Z-package-output-guard
- required_evidence: 单测 RED→GREEN
- evidence_level: mock
- artifact_ref: docs/system/workspace/scripts/tests/test-freely-package-output-guard
- test_command: bash docs/system/workspace/scripts/tests/test-freely-package-output-guard
- expected_output: PASS: output guard holds
- expected_RED_output: RED: output guard missing or misplaced
- actual_RED_output: RED: output guard missing or misplaced（守卫缺失、危险模式未覆盖、无拒绝文案）
- actual_output: PASS: output guard holds（guard at 66 < rm at 98；安全路径打包成功）
- evidence_file: docs/B2-docs/runtime/package-output-guard/raw-20261104T074512Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2
- case_design: 静态断言守卫函数存在且行号早于 `rm -rf "$OUTPUT"`；覆盖 `/`、`$HOME`、`..` 三类字面；再用临时目录实跑安全路径，确认未误伤。

## Unit
- acceptance_target: 守卫存在性、执行顺序、危险模式覆盖、拒绝文案
- testing_layer: unit
- target_environment: fix/raw-20261104T074512Z-package-output-guard
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. `bash docs/system/workspace/scripts/tests/test-freely-package-output-guard`

## Integration
- acceptance_target: 安全路径在真实打包流程中仍可完成
- testing_layer: integration
- target_environment: test-pre-merge
- required_evidence: AT-001 + 打包产物清单
- blocker_taxonomy: covered_by_more_realistic_required_surface
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 本修复只作用于删除前的拒绝分支；安全路径的打包行为由同一测试在临时目录真实执行覆盖，无需额外集成环境。
- replacement_evidence: AT-001 的 safe target 分支。

## End-to-End
- acceptance_target: 下一次正式发布打包不受影响
- testing_layer: end-to-end
- target_environment: release packaging
- required_evidence: 打包产物与 .freely_version
- blocker_taxonomy: covered_by_more_realistic_required_surface
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 发布打包为低频人工流程，本次以安全路径实跑替代；下次 nightly 打包作为回归观察点。
- replacement_evidence: AT-001 + 下次 nightly 产物。

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 单测在真实脚本与真实 allowlist 上执行；危险目标用静态断言避免真实删除。
