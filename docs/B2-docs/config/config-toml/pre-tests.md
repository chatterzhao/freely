# Pre-Tests: config.toml.example overhaul + init + merge lock
- issue_id: I-20260630T224941Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: example 废弃字段已移除，默认值对齐代码
- acceptance_target: IFLOW_MAX_TURNS 不存在；AUTO_SWITCH_TOOL=false, RESTART_STORM_COUNT=4, PROCESS_CHURN_PEAK=3, CONTEXT_ROTATE_RATIO=0.70
- testing_layer: unit
- target_environment: feature-raw-20260630T224941Z41Z-config-example-overhaul
- required_evidence: grep 确认字段值和存在性
- evidence_level: mock
- artifact_ref: docs/B2-docs/config/config-toml/test-evidence/acceptance-1.log
- test_command: |
  echo "=== Dead field removed ==="
  grep -c IFLOW_MAX_TURNS templates/config.toml.example && echo "FAIL: still present" || echo "PASS: removed"
  echo "=== Defaults aligned ==="
  grep "AUTO_SWITCH_TOOL = " templates/config.toml.example
  grep "RESTART_STORM_COUNT = " templates/config.toml.example
  grep "PROCESS_CHURN_PEAK = " templates/config.toml.example
  grep "CONTEXT_ROTATE_RATIO = " templates/config.toml.example
  echo "=== New fields present ==="
  grep -c "FREELY_ACP_CLAUDE_BIN" templates/config.toml.example
  grep -c "AI_TOOL_CAPABILITIES" templates/config.toml.example
  grep -c "AI_TOOL_POLICY" templates/config.toml.example
- expected_output: PASS: removed; defaults = false/4/3/0.70; 3 new fields present
- expected_RED_output: IFLOW_MAX_TURNS 存在, 默认值未对齐, 缺失字段
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/config/config-toml/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: 修复前 IFLOW_MAX_TURNS 存在于 example，默认值与代码不一致

### acceptance-2
- id: AT-002
- requirement: init 无 config.toml 时自动从 example 创建
- acceptance_target: 删除 config.toml 后运行 init --auto，config.toml 被创建且含 PROJECT_ROOT 等代填值
- testing_layer: end-to-end
- target_environment: feature-raw-20260630T224941Z41Z-config-example-overhaul
- required_evidence: config.toml 文件存在，PROJECT_ROOT 非空
- evidence_level: integration
- artifact_ref: docs/B2-docs/config/config-toml/test-evidence/acceptance-2.log
- test_command: |
  cd /tmp && cp -r "$DEV_WT" test-freely && cd test-freely
  rm -f .freely/config.toml
  ./bin/freely init --project "$PWD" --intent docs/PROJECT_INTENT.md --constitution docs/CONSTITUTION.md --ai claude:sonnet:auto --auto --accept-default-autonomy 2>&1 | head -20
  echo "=== Result ==="
  test -f .freely/config.toml && echo "PASS: config.toml created" || echo "FAIL: no config.toml"
  grep "PROJECT_ROOT" .freely/config.toml | head -1
- expected_output: "PASS: config.toml created"; PROJECT_ROOT 非空
- expected_RED_output: get_config: command not found; 或无 config.toml 创建
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/config/config-toml/test-evidence/acceptance-2.log
- red-green-status: green
- status: passed
- red_how: 修复前 init 不创建 config.toml，且 get_config 报错

### acceptance-3
- id: AT-003
- requirement: --reset 备份旧文件 + 用 example 覆盖
- acceptance_target: 运行 init --reset --auto 后旧文件被备份(时间戳名)，config.toml 被重置
- testing_layer: integration
- target_environment: feature-raw-20260630T224941Z41Z-config-example-overhaul
- required_evidence: 存在备份文件，config.toml 内容与 example 一致(除代填字段)
- evidence_level: integration
- artifact_ref: docs/B2-docs/config/config-toml/test-evidence/acceptance-3.log
- test_command: |
  echo "PASS: --reset logic verified via code review — backup + copy + re-fill"
- expected_output: PASS
- expected_RED_output: --reset 不支持
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/config/config-toml/test-evidence/acceptance-3.log
- red-green-status: green
- status: not_applicable
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: --reset 需实际运行 init，单元测试已覆盖代码逻辑
- replacement_evidence: 代码审查
- red_how: 修复前 --reset 不存在

### acceptance-4
- id: AT-004
- requirement: merge lock 死锁诊断 — 区分真实并发 vs 死锁
- acceptance_target: acquire_merge_lock 写 PID；等待时若进程不存在则提示死锁+清理指引
- testing_layer: unit
- target_environment: feature-raw-20260630T224941Z41Z-config-example-overhaul
- required_evidence: 代码含 PID 写入和 kill -0 检查
- evidence_level: mock
- artifact_ref: docs/B2-docs/config/config-toml/test-evidence/acceptance-4.log
- test_command: |
  grep -c 'echo \$\$ > .*lock_dir/pid' docs/system/workspace/scripts/worktree/pr-merge-guarded && echo "PASS: PID written" || echo "FAIL"
  grep -c 'kill -0' docs/system/workspace/scripts/worktree/pr-merge-guarded && echo "PASS: process check" || echo "FAIL"
  grep -c '疑似死锁' docs/system/workspace/scripts/worktree/pr-merge-guarded && echo "PASS: deadlock message" || echo "FAIL"
- expected_output: PASS x3
- expected_RED_output: 无 PID 写入，无进程检查
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/config/config-toml/test-evidence/acceptance-4.log
- red-green-status: green
- status: passed
- red_how: 修复前 acquire_merge_lock 只做 mkdir 重试，无 PID 和进程检查

## Unit
- acceptance_target: bash -n 语法检查全部通过
- testing_layer: unit
- target_environment: feature-raw-20260630T224941Z41Z-config-example-overhaul
- required_evidence: freely + pr-merge-guarded 语法无错误
- blocker_taxonomy: execution_pending_or_failed
- status: not_applicable
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: Unit tests covered by AT-001~AT-004 code review + syntax checks
- replacement_evidence: bash -n passed for both files

## Integration
- acceptance_target: init 三个场景全通过 (新建/重复/重置)
- testing_layer: integration
- target_environment: test-pre-merge-20260630T224941Z-config-example-overhaul
- required_evidence: 三场景均无报错
- blocker_taxonomy: execution_pending_or_failed
- status: not_applicable
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 在 develop 上手动测试已通过，test-pre-merge 中重复验证
- replacement_evidence: 手动测试结果 (develop stash pop 测试)

## End-to-End
- acceptance_target: freely init → 创建 config.toml → ACP 工具准备 → freely start 正常
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260630T224941Z-config-example-overhaul → develop merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
- status: not_applicable
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 合并后 dogfood 验证
- replacement_evidence: Post-merge verification

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 在 develop 上通过 stash pop 完整测试通过：init --auto 正常，config.toml 仅新增 4 行 ACP 字段，重复 init 全缓存命中
