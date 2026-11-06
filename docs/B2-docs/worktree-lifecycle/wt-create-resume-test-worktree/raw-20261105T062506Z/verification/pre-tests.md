# Pre-Tests: 补齐 seed 声明并建立 allowlist/seed 一致性检查
- issue_id: I-20261105T062506Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: wt-create 新建的工位无需人工复制即可跑通打包；打包白名单中位于 gitignored 路径的条目必须在 seed manifest 中有声明，新增未同步条目被一致性检查拦下；输出路径守卫及其顺序不变；新 seed 条目不得新增硬失败点（既有 agent-table required=true 行为不在范围）
- acceptance_target: 消除新工位打包测试的无关失败，并用机器约束防止清单漂移复发
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 隔离最小 seed 项目 + 真实打包命令（不触网）
- required_evidence: 新增回归测试 13 项全 GREEN + 7 个相关回归基线对比零新增失败
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-worktree-seed-package-parity
- test_command: bash docs/system/workspace/scripts/tests/test-worktree-seed-package-parity all
- expected_output: PASS: 13 checks, 0 failed
- expected_RED_output: FAIL: 11 of 13 checks failed
- actual_RED_output: RED 11 项失败 —— seeder 只 link agent-table、未声明 bootstrap；最小工位真实打包报 `[ERROR] missing file: .freely/tool-boundary-bootstrap.md` 并 abort；5 项 static 缺声明与 checker；2 项既有能力 PASS（AT-001-RED.log）
- actual_output: PASS: 13 checks, 0 failed；seeder 复制 bootstrap、parity 检查 `1 ignored / 0 undeclared`、新增未 seed 条目被点名拦下、最小 seed 项目真实打包成功且产物含 bootstrap（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261105T062506Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5,T6
- case_design: static 组校验 seed 声明（copy / required=false）、checker 存在、freely-package 调用位置在 rm -rf 之前、输出守卫保留、bash -n；behavior 组以最小无符号链接源项目应用真实 seeder，断言 bootstrap 落地；对真实项目跑 parity 检查；构造含新增未 seed gitignored 条目的临时 git 项目，断言 checker 点名并 exit 1；构造最小打包项目（allowlist 输入用占位文件，bootstrap 仅由 seeder 提供），真实执行 `freely-package` 并断言产物含 bootstrap。
- red_how: fix RED — 在未修复的 develop 真源上运行同一断言组，确认新工位打包因缺 bootstrap 失败。

## Unit
- acceptance_target: seed 声明、checker 契约与守卫顺序静态正确性
- testing_layer: unit
- target_environment: fix/raw-20261105T062506Z-seed-package-parity
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-worktree-seed-package-parity static

## Integration
- acceptance_target: 输出守卫、R1/R2/R3/R4/Q1/Q2 能力不退化
- testing_layer: integration
- target_environment: 未修改 develop HEAD 基线对比
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-freely-package-output-guard
2. bash docs/system/workspace/scripts/tests/test-wt-create-four-state-dir all
3. bash docs/system/workspace/scripts/tests/test-wt-create-recovery-dev-path all

## End-to-End
- acceptance_target: 最小 seed 项目真实打包、未声明条目被拦下
- testing_layer: end-to-end
- target_environment: 隔离最小项目（不触网）
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-worktree-seed-package-parity behavior

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 在真实 fix 工位以项目真源命令执行；R5 工位由 wt-create 创建时即复现缺 bootstrap；用封装 seeder 补齐后输出守卫测试 PASS；真实项目 parity 检查 `1 ignored / 0 undeclared`；最小 seed 项目真实打包成功；7 个相关回归以未修改 develop HEAD 做基线对比，退出码逐一相同（全 0）→ 0 新增失败；bin/check-epics-map 对齐通过。
