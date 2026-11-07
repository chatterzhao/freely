# Pre-Tests: 补齐打包 allowlist 运行时必需文件并建立防复发检查
- issue_id: I-20261106T100938Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 打包产物必须含 5 个运行时必需的 workspace 顶层文件且 sha256 与真源一致；安装态可自举打包并 `integrity: verified`；安装态 seeder 读 manifest 而非 builtin；安装态 R5 parity 通过；新增被运行时引用的 tracked 顶层文件若未声明则被一致性检查拦下；3 个纯文档不随包；显式白名单机制、输出守卫与 R5 hook 顺序不变
- acceptance_target: 消除安装态产物不自洽，并用机器约束防止清单漏配复发
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 真实工位打包产物 + 隔离 git 项目（不触网）
- required_evidence: 新增回归测试全 GREEN（static 14 + behavior 8）+ 10 个回归全 PASS + 9 个基线对比零新增失败
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-package-runtime-allowlist-parity
- test_command: bash docs/system/workspace/scripts/tests/test-package-runtime-allowlist-parity all
- expected_output: PASS: 8 checks, 0 failed（static 14 项全部 ok）
- expected_RED_output: FAIL: 6 of 8 checks failed（static 10 项 FAIL）
- actual_RED_output: RED 精确复现 —— 真实打包产物缺 5 个运行时文件；安装态 `freely-package` 报 `[ERROR] allowlist not found` exit 1；安装态 seeder `source=builtin entries=1`（真源 `manifest entries=3`）；安装态 R5 parity exit 2；checker 与 5 条 allowlist 声明均缺失。既有能力 6 项保持 PASS（doc-only 未打包、R5 checker 存在、危险输出守卫、R5 hook、bash -n、真实打包 integrity）（AT-001-RED.log）
- actual_output: PASS: 8 checks, 0 failed；static 14 项全 ok；安装态自举 `integrity: verified`、seeder `source=manifest entries=3`、R5 parity `undeclared=[]`、防复发拦截点名 `new-runtime-contract.txt`（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/gate/governance/raw-20261106T100938Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5,T6
- case_design: static 组用 Python 精确校验 allowlist 的 5 条声明、3 个纯文档未被无条件打包、checker 存在、`freely-package` 调用顺序（守卫在最前 → R5 seed parity → 新 runtime parity → rm -rf）与 bash -n；behavior 组真实执行打包到安全临时目录，对产物做 sha256 parity、在产物内真实执行 `freely-package` 自举打包、在产物内调用 seeder 与 R5 parity checker、并构造一个含新增未声明 runtime 文件的隔离 git 项目验证 checker 点名拦截。
- red_how: fix RED — 在未修复的 develop 真源上运行同一断言组，确认安装态自举打包与 seeder 降级。

## Unit
- acceptance_target: allowlist 声明、checker 契约、守卫与 hook 顺序静态正确性
- testing_layer: unit
- target_environment: fix/raw-20261106T100938Z-package-allowlist-gaps
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-package-runtime-allowlist-parity static

## Integration
- acceptance_target: R1..R5、Q2、输出守卫等能力不退化
- testing_layer: integration
- target_environment: 未修改 develop HEAD 基线对比
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-worktree-seed-package-parity all
2. bash docs/system/workspace/scripts/tests/test-freely-package-output-guard
3. bash docs/system/workspace/scripts/tests/test-wt-create-four-state-dir all

## End-to-End
- acceptance_target: 真实打包产物、安装态自举、防复发拦截
- testing_layer: end-to-end
- target_environment: 真实工位打包产物 + 隔离 git 项目（不触网）
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-package-runtime-allowlist-parity behavior

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 在真实 fix 工位以项目真源命令执行；R2 物化 H1 自举生效；真实打包产物与安装态自举打包均 `integrity: verified`；9 个相关回归以未修改 develop HEAD 做基线对比，退出码逐一相同（全 0），输出差异仅 `rm -rf` 行号 112→126、随机临时目录名与计时数字 → 0 新增失败；bin/check-epics-map 对齐通过；双平台 raw 副本用封装命令关闭、三份 fingerprint 一致。
