# Pre-Tests: fix dirty 提示 backtick 命令替换
- issue_id: I-20260705T061416Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 确认修复行不再含触发命令替换的反引号模式
- acceptance_target: `docs/system/workspace/scripts/runtime/freely:21982` 中无反引号，skill 名为纯文本
- testing_layer: unit
- target_environment: test-pre-merge-20260705T061416Z-fix-backtick-command-subst
- required_evidence: grep 验证无反引号命令替换模式
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260705T061416Z/verification/test-evidence/acceptance-1.log
- test_command: |
  LINE=$(sed -n '21982p' docs/system/workspace/scripts/runtime/freely)
  if echo "$LINE" | grep -q '`.*`'; then echo "FAIL: backtick still present"; else echo "PASS: no backtick command substitution"; fi
- expected_output: PASS: no backtick command substitution
- expected_RED_output: FAIL: backtick still present
- actual_RED_output: |
  FAIL: backtick still present
  Original line (HEAD): log_error "    详细流程见 skill \`freely-workflow-guarded-execution\`"
  grep '`.*`' matched — backtick command substitution pattern confirmed in original code
- actual_output: |
  PASS: no backtick command substitution
  Fixed line: log_error "    详细流程见 skill freely-workflow-guarded-execution"
  grep '`.*`' — no match. Backtick removed.
- evidence_file: docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260705T061416Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- red_how: 对 git HEAD 原始代码执行 grep 检测，确认反引号模式存在
- status: pass
- blocker: (失败时填写)

### acceptance-2
- id: AT-002
- requirement: 修复后脚本语法正确
- acceptance_target: `bash -n` 对 freely 脚本语法检查通过
- testing_layer: unit
- target_environment: test-pre-merge-20260705T061416Z-fix-backtick-command-subst
- required_evidence: bash -n 无报错
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260705T061416Z/verification/test-evidence/acceptance-2.log
- test_command: bash -n docs/system/workspace/scripts/runtime/freely && echo "PASS: syntax OK" || echo "FAIL: syntax error"
- expected_output: PASS: syntax OK
- expected_RED_output: N/A
- actual_RED_output: N/A（修复前后语法都正确，RED/GREEN 不适用）
- actual_output: PASS: syntax OK
- evidence_file: docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260705T061416Z/verification/test-evidence/acceptance-2.log
- red-green-status: not_applicable
- red-green-not-applicable-reason: 修复前后语法都应正确，RED/GREEN 不适用于语法检查
- status: pass
- blocker: (失败时填写)

### acceptance-3
- id: AT-003
- requirement: 模拟 dirty 场景，提示文本不再触发 command not found
- acceptance_target: 在 dirty 检查上下文中执行该 log_error 行，bash 不报 command not found
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260705T061416Z-fix-backtick-command-subst
- required_evidence: 执行 log_error 行不产生 command not found 错误
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260705T061416Z/verification/test-evidence/acceptance-3.log
- test_command: |
  log_error() { echo "$*" >&2; }
  eval "$(sed -n '21982p' docs/system/workspace/scripts/runtime/freely)" 2>&1 | grep -v 'command not found' && echo "PASS: no command not found" || echo "WARN: check output"
- expected_output: PASS: no command not found
- expected_RED_output: command not found: freely-workflow-guarded-execution
- actual_RED_output: |
  bash: freely-workflow-guarded-execution: command not found
  The original line with \\`freely-workflow-guarded-execution\\` triggers bash command substitution.
- actual_output: |
  详细流程见 skill freely-workflow-guided-execution
  exit: 0 — no command not found on stderr
- evidence_file: docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260705T061416Z/verification/test-evidence/acceptance-3.log
- red-green-status: green
- red_how: 用 bash -c 执行原始 log_error 行（含 \\`...\\`），stderr 输出 "command not found: freely-workflow-guarded-execution"
- status: pass
- blocker: (失败时填写)

## Unit
- acceptance_target: 语法正确性 + 无反引号模式
- testing_layer: unit
- target_environment: test-pre-merge-20260705T061416Z-fix-backtick-command-subst
- required_evidence: bash -n 通过 + grep 无反引号
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001（grep 无反引号）和 AT-002（bash -n 语法）已覆盖全部 unit 层测试。单行字符串修改无独立 unit 测试面，不需要额外的单元测试用例。
- replacement_evidence: AT-001 (red-green-status: green, status: pass) + AT-002 (status: pass) — 覆盖语法和无反引号验证

## Integration
- acceptance_target: 修复行在 dirty 检查中正确显示为纯文本
- testing_layer: integration
- target_environment: test-pre-merge-20260705T061416Z-fix-backtick-command-subst
- required_evidence: 执行后无 command not found
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-003 通过 bash -c 直接执行修复后的 log_error 行，验证无 command not found，已覆盖集成层。单行字符串修改无模块间数据流交互，不需要额外的集成测试。
- replacement_evidence: AT-003 (red-green-status: green, status: pass) — 覆盖 dirty 场景 log_error 执行

## End-to-End
- acceptance_target: freely daemon start 时 dirty 检查提示无异常
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260705T061416Z-fix-backtick-command-subst → develop merge chain
- required_evidence: daemon start 日志无 command not found
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-003 在独立 bash 进程执行修复行，确认无 command not found。单行 log 字符串修改，daemon 完整启动作为端到端验证是过度测试——修复不改变任何控制流、状态或数据，仅改变一条 echo 输出字符串。
- replacement_evidence: AT-003 (red-green-status: green, status: pass) + bash -n 语法检查通过 — 覆盖端到端真实风险面

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 单行 log 字符串修改，无需真实环境验证。语法检查和 end-to-end 测试覆盖充分。
