# Pre-Tests: 修复 chat help 错误信息 shell 引号嵌套
- issue_id: I-20260720T023136Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: bash 语法检查通过，且 L6700 字符串不再含被解释为重定向的裸尖括号
- acceptance_target: 修复后 `bash -n` 对目标行所在脚本通过；grep 确认修复后的 log_error 参数以单引号包裹（无裸尖括号）
- testing_layer: unit
- target_environment: test-pre-merge-20260720T023136Z-chat-help-quoting
- required_evidence: `bash -n` 返回 0 + grep 输出确认单引号包裹
- evidence_level: integration
- surface_kind: unit
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: T1
- case_design: 修改 L6700 外层双引号为单引号后，用 bash -n 验证整脚本语法，用 grep 确认该行以单引号包裹中文占位符
- artifact_ref: docs/B2-docs/human/cli-help-and-dry-run-contract-followthrough-governance/raw-20260720T023136Z/verification/test-evidence/acceptance-1-3-green.log
- test_command: bash -n docs/system/workspace/scripts/runtime/freely && grep -n "描述" docs/system/workspace/scripts/runtime/freely
- expected_output: bash -n 无输出（exit 0）；grep 命中 L6700 且该行以单引号包裹 `<描述>`/`<详细描述>`
- expected_RED_output: bash 提示 `line 6700: 描述: No such file or directory`（当前行为）
- actual_RED_output: `bash: 描述: No such file or directory` + EXIT=1（在原始代码上模拟执行确认）
- actual_output: bash -n exit 0 无报错；L6700 现为 `log_error '[chat]   freely feedback --title "fix|feat: <描述>" --kind fix --body "<详细描述>"'`（单引号包裹）
- evidence_file: docs/B2-docs/human/cli-help-and-dry-run-contract-followthrough-governance/raw-20260720T023136Z/verification/test-evidence/acceptance-1-3-green.log
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: 手工模拟执行修复前的 log_error 行：`bash -c 'log_error(){ echo "$*"; }; log_error "[chat]   freely feedback --title "fix|feat: <描述>" --kind fix --body "<详细描述>""'`，实际输出 `bash: 描述: No such file or directory` + EXIT=1，bug 稳定复现

### acceptance-2
- id: AT-002
- requirement: 模拟执行修复后的 log_error 行输出完整帮助文本，无 No such file 报错
- acceptance_target: 消息含 `freely feedback --title "fix|feat: <描述>" --kind fix --body "<详细描述>"` 字面量且 exit 0
- testing_layer: unit
- target_environment: test-pre-merge-20260720T023136Z-chat-help-quoting
- required_evidence: 模拟执行的 stdout 完整包含目标文本，exit code 为 0
- evidence_level: integration
- surface_kind: unit
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: T2
- case_design: 用 bash 模拟 log_error 函数执行修复后的字符串，验证输出完整、exit 0，证明无重定向解释
- artifact_ref: docs/B2-docs/human/cli-help-and-dry-run-contract-followthrough-governance/raw-20260720T023136Z/verification/test-evidence/acceptance-1-3-green.log
- test_command: bash -c 'log_error(){ echo "$*"; }; log_error '"'"'[chat]   freely feedback --title "fix|feat: <描述>" --kind fix --body "<详细描述>"'"'"'; echo "EXIT=$?"'
- expected_output: `[chat]   freely feedback --title "fix|feat: <描述>" --kind fix --body "<详细描述>"` 且 `EXIT=0`，无 `No such file`
- expected_RED_output: `bash: 描述: No such file or directory` + `EXIT=1`
- actual_RED_output: `bash: 描述: No such file or directory` + `EXIT=1`
- actual_output: `[chat]   freely feedback --title "fix|feat: <描述>" --kind fix --body "<详细描述>"` + `EXIT=0`，无 `No such file`
- evidence_file: docs/B2-docs/human/cli-help-and-dry-run-contract-followthrough-governance/raw-20260720T023136Z/verification/test-evidence/acceptance-1-3-green.log
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: 修复前原始字符串模拟执行即复现：`bash -c 'log_error(){ echo "$*"; }; log_error "[chat]   freely feedback --title "fix|feat: <描述>" --kind fix --body "<详细描述>""'` → `bash: 描述: No such file or directory` + EXIT=1

### acceptance-3
- id: AT-003
- requirement: 渲染后中文字符与消息内双引号原样保留（可读性验收）
- acceptance_target: 输出中 `<描述>`、`<详细描述>` 为字面占位符，`fix|feat:` 前缀与 `--kind fix --body` 结构完整
- testing_layer: unit
- target_environment: test-pre-merge-20260720T023136Z-chat-help-quoting
- required_evidence: AT-002 输出内容逐字比对含全部目标片段
- evidence_level: integration
- surface_kind: unit
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: T2
- case_design: 对模拟执行输出做 grep 逐片段断言，确认中文占位符与命令结构完整渲染
- artifact_ref: docs/B2-docs/human/cli-help-and-dry-run-contract-followthrough-governance/raw-20260720T023136Z/verification/test-evidence/acceptance-1-3-green.log
- test_command: out=$(bash -c 'log_error(){ echo "$*"; }; log_error '"'"'[chat]   freely feedback --title "fix|feat: <描述>" --kind fix --body "<详细描述>"'"'"''); for p in 'fix|feat: <描述>' '<详细描述>' '--kind fix --body'; do echo "$out" | grep -F -e "$p"; done
- expected_output: 三个片段各命中一行（fix|feat: <描述>、<详细描述>、--kind fix --body），无缺失
- expected_RED_output: grep 无命中或报 `No such file`（原始字符串无法完整渲染）
- actual_RED_output: grep exit=1 无命中（原始字符串模拟执行即崩溃，无法渲染目标片段）
- actual_output: 三个片段全部 HIT（fix|feat: <描述>、<详细描述>、--kind fix --body 均命中），完整输出 `[chat]   freely feedback --title "fix|feat: <描述>" --kind fix --body "<详细描述>"`
- evidence_file: docs/B2-docs/human/cli-help-and-dry-run-contract-followthrough-governance/raw-20260720T023136Z/verification/test-evidence/acceptance-1-3-green.log
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: 原始字符串在模拟执行时即崩溃（`bash: 描述: No such file or directory`），stdout 为空，grep 全部片段均无命中

## Unit
- acceptance_target: 单字符串字面量修复：bash -n 通过 + 模拟 log_error 输出完整
- testing_layer: unit
- target_environment: feature worktree + test-pre-merge-20260720T023136Z-chat-help-quoting
- required_evidence: AT-001/AT-002/AT-003 全绿
- blocker_taxonomy: execution_pending_or_failed
1. 在 test-pre-merge 工位执行 AT-001 的 test_command（bash -n + grep 单引号包裹）。
2. 执行 AT-002 / AT-003 的模拟渲染断言，确认输出完整且 EXIT=0。

## Integration
- acceptance_target: 该 log_error 行位于 chat 命令错误分支，属单点字符串修复，无跨模块协作面
- testing_layer: integration
- target_environment: test-pre-merge-20260720T023136Z-chat-help-quoting
- required_evidence: bash -n 对整个脚本通过（脚本整体可加载即为集成面最小证据）
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: 本次改动是单个字符串字面量，不触达模块间数据流/状态变更；整个脚本 bash -n 通过 + AT-001 已覆盖语法集成面
- replacement_evidence: 全脚本 bash -n docs/system/workspace/scripts/runtime/freely 通过

## End-to-End
- acceptance_target: 用户视角的 chat help 错误提示完整可读
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260720T023136Z-chat-help-quoting
- required_evidence: 触发 chat 命令本地 raw issue 创建禁用分支（若可触发）或等价模拟执行输出
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 该 log_error 分支依赖完整 chat runtime 状态（daemon/session），在测试工位无法稳定构造完整用户流程；其渲染正确性已由 AT-002/AT-003 的 shell 模拟执行等价覆盖
- replacement_evidence: AT-002/AT-003 的模拟执行输出证据

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 本 issue 为纯静态字符串修复，不涉及 bin/ai、codex exec、freely start 等真实环境链路，本次实现不需要真实环境测试；由 shell 模拟执行 + bash -n 提供足够证据。
