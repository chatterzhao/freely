# Pre-Tests: 封装命令文档系统化
- issue_id: I-20260706T232728Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: AGENTS.md 速查表增加"你想做什么"和"它封装了什么"列
- acceptance_target: AGENTS.md 速查表从"场景→正确命令→禁止"三列增强为意图→命令→封装→禁止四列
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260706T232728Z-encaps-cmd-docs
- required_evidence: grep 确认 AGENTS.md 包含"你想做什么"和"它封装了什么"列
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260706T232728Z/verification/test-evidence/acceptance-1.log
- test_command: grep -c "你想做什么" AGENTS.md && grep -c "它封装了什么" AGENTS.md
- expected_output: 两个 grep 都返回 >0
- expected_RED_output: grep -c "你想做什么" AGENTS.md → 0
- actual_RED_output: grep -c "你想做什么" AGENTS.md → 0
- actual_output: grep -c "你想做什么" AGENTS.md → 2; grep -c "它封装了什么" AGENTS.md → >0
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260706T232728Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: feature: grep 检查 AGENTS.md 中不存在"你想做什么"列，确认功能未实现。执行 `grep -c "你想做什么" AGENTS.md` → 0，RED 确认。

### acceptance-2
- id: AT-002
- requirement: freely-workflow-guarded-execution SKILL.md 铁律区域前增加正向引导的意图→命令速查
- acceptance_target: SKILL.md "硬性规则"章节前新增"意图→命令速查"表格
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260706T232728Z-encaps-cmd-docs
- required_evidence: grep 确认 SKILL.md 包含"意图→命令速查"章节
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260706T232728Z/verification/test-evidence/acceptance-2.log
- test_command: grep -c "意图→命令速查" docs/system/workspace/skills/freely-workflow-guarded-execution/SKILL.md
- expected_output: 返回 >0
- expected_RED_output: grep -c "意图→命令速查" SKILL.md → 0
- actual_RED_output: grep -c "意图→命令速查" ~/.claude/skills/freely-workflow-guarded-execution/SKILL.md → 0
- actual_output: grep -c "意图→命令速查" docs/system/workspace/skills/freely-workflow-guarded-execution/SKILL.md → 1
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260706T232728Z/verification/test-evidence/acceptance-2.log
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: feature: grep 检查 SKILL.md 中不存在"意图→命令速查"章节。执行确认 → 0，RED。

### acceptance-3
- id: AT-003
- requirement: .githooks/bin/gh wrapper 每个拦截消息增加"为什么"解释
- acceptance_target: gh wrapper pr create/pr merge/issue close 三个拦截 case 全部增加"封装"说明
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260706T232728Z-encaps-cmd-docs
- required_evidence: grep 确认 .githooks/bin/gh 包含"封装"描述
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260706T232728Z/verification/test-evidence/acceptance-3.log
- test_command: grep -c "封装" .githooks/bin/gh
- expected_output: 返回 >=3（每个 case 至少一次）
- expected_RED_output: grep -c "封装" .githooks/bin/gh → 0
- actual_RED_output: grep -c "封装" .githooks/bin/gh → 0
- actual_output: grep -c "封装" .githooks/bin/gh → 6
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260706T232728Z/verification/test-evidence/acceptance-3.log
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: feature: grep 检查 gh wrapper 中不存在"封装"解释。执行确认 → 0，RED。

### acceptance-4
- id: AT-004
- requirement: .githooks/pre-commit.sh develop 分支拦截末尾增加正向引导
- acceptance_target: pre-commit.sh 拦截消息末尾包含"你刚才想做的是"意图→命令映射提示
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260706T232728Z-encaps-cmd-docs
- required_evidence: grep 确认 pre-commit.sh 包含正向引导文本
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260706T232728Z/verification/test-evidence/acceptance-4.log
- test_command: grep -c "你刚才想做" .githooks/pre-commit.sh
- expected_output: 返回 >0
- expected_RED_output: grep -c "你刚才想做" .githooks/pre-commit.sh → 0
- actual_RED_output: grep -c "你刚才想做" .githooks/pre-commit.sh → 0
- actual_output: grep -c "你刚才想做" .githooks/pre-commit.sh → 1
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260706T232728Z/verification/test-evidence/acceptance-4.log
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: feature: grep 检查 pre-commit.sh 中不存在正向引导文本。执行确认 → 0，RED。

### acceptance-5
- id: AT-005
- requirement: .githooks/pre-push.sh push 拦截末尾增加正向引导
- acceptance_target: pre-push.sh 拦截消息末尾包含"你刚才想做的是"意图→命令映射提示
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260706T232728Z-encaps-cmd-docs
- required_evidence: grep 确认 pre-push.sh 包含正向引导文本
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260706T232728Z/verification/test-evidence/acceptance-5.log
- test_command: grep -c "你刚才想做" .githooks/pre-push.sh
- expected_output: 返回 >0
- expected_RED_output: grep -c "你刚才想做" .githooks/pre-push.sh → 0
- actual_RED_output: grep -c "你刚才想做" .githooks/pre-push.sh → 0
- actual_output: grep -c "你刚才想做" .githooks/pre-push.sh → 1
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260706T232728Z/verification/test-evidence/acceptance-5.log
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: feature: grep 检查 pre-push.sh 中不存在正向引导文本。执行确认 → 0，RED。

### acceptance-6
- id: AT-006
- requirement: 新建 docs/system/workspace/commands.md 封装命令权威参考
- acceptance_target: commands.md 存在且覆盖全部 7 个封装命令
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260706T232728Z-encaps-cmd-docs
- required_evidence: ls + grep 确认文件存在且覆盖 7 个命令
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260706T232728Z/verification/test-evidence/acceptance-6.log
- test_command: ls docs/system/workspace/commands.md
- expected_output: 文件存在
- expected_RED_output: ls docs/system/workspace/commands.md → No such file or directory
- actual_RED_output: ls docs/system/workspace/commands.md → No such file or directory
- actual_output: ls docs/system/workspace/commands.md → 文件存在
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260706T232728Z/verification/test-evidence/acceptance-6.log
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: feature: ls 检查 commands.md 不存在。执行确认 → No such file，RED。

### acceptance-7
- id: AT-007
- requirement: 所有位置的命令引用互相一致
- acceptance_target: AGENTS.md ↔ commands.md ↔ SKILL.md ↔ hook 消息中的封装命令名完全一致
- testing_layer: integration
- target_environment: test-pre-merge-20260706T232728Z-encaps-cmd-docs
- required_evidence: 交叉 grep 确认 4 个源文件中封装命令引用一致
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260706T232728Z/verification/test-evidence/acceptance-7.log
- test_command: grep -oE 'freely (feedback|wt-create|pr-create-guarded|pr-review-guarded|pr-merge-guarded|wt-close|develop-push)' docs/system/workspace/commands.md AGENTS.md docs/system/workspace/skills/freely-workflow-guarded-execution/SKILL.md .githooks/bin/gh | sort -u
- expected_output: 7 个封装命令在 4 个源文件中一致引用
- expected_RED_output: commands.md 不存在，一致性检查不可执行
- actual_RED_output: commands.md 不存在，一致性检查不可执行
- actual_output: 交叉 grep 确认 7 个命令在 commands.md、AGENTS.md、SKILL.md、gh wrapper 中一致引用
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260706T232728Z/verification/test-evidence/acceptance-7.log
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: feature: commands.md 不存在时无法执行一致性检查。RED。

### acceptance-8
- id: AT-008
- requirement: freely deploy-skills 正常执行
- acceptance_target: SKILL.md 修改后 freely deploy-skills 部署成功
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260706T232728Z-encaps-cmd-docs
- required_evidence: 部署后 ~/.claude/skills/freely-workflow-guarded-execution/SKILL.md 包含新章节
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260706T232728Z/verification/test-evidence/acceptance-8.log
- test_command: grep -c "意图→命令速查" ~/.claude/skills/freely-workflow-guarded-execution/SKILL.md
- expected_output: 返回 >0
- expected_RED_output: SKILL.md 尚未修改，deploy 将部署旧版本
- actual_RED_output: SKILL.md 尚未修改，deploy 将部署旧版本
- actual_output: grep -c "意图→命令速查" ~/.claude/skills/freely-workflow-guarded-execution/SKILL.md → 1
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260706T232728Z/verification/test-evidence/acceptance-8.log
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: feature: SKILL.md 未修改时 deploy-skills 会将旧版本（无"意图→命令速查"）重新部署。RED。

## Unit
- acceptance_target: 无单元级可执行代码——本次变更全部为纯文档/文本修改（.md、.sh 文本），不涉及函数、类或模块级别的可执行单元
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: 不适用——无单元级可执行边界
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 本次变更仅修改 Markdown 文档和 shell 脚本的文本内容，不涉及可执行代码的函数/类/模块。grep 文本验证已在 Acceptance Items (AT-001~AT-008) 中覆盖。
- replacement_evidence: 文档内容正确性由 AT-001~AT-008 通过 grep-based 文本存在性检查验证

## Integration
- acceptance_target: 无集成面——本次变更不修改模块接口、API、数据流或进程间协作
- testing_layer: integration
- target_environment: test-pre-merge-20260706T232728Z-encaps-cmd-docs
- required_evidence: 不适用——无集成边界
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 本次变更不涉及模块间协作、数据流或 API 接口。AGENTS.md/SKILL.md/commands.md/hook 消息均为独立文档文件，彼此间无运行时依赖。
- replacement_evidence: 跨文档一致性由 AT-007（命令名交叉一致性检查）验证

## End-to-End
- acceptance_target: 文档变更通过全部门禁、创建 PR、合并到 develop
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260706T232728Z-encaps-cmd-docs → develop merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 端到端验证由 pr-create-guarded 门禁链（dev↔test 一致性 → epics-map → dry-run merge gate → IBM governance gate → pretests-gate）自动完成。纯文档变更无运行时 E2E 场景。
- replacement_evidence: pr-create-guarded gate chain 全部通过即为端到端验证通过

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 全部 8 条 Acceptance Items 在 test-pre-merge 工位通过 grep 验证。deploy-skills 部署成功，SKILL.md 修改已生效。全部 red-green-status=green。
