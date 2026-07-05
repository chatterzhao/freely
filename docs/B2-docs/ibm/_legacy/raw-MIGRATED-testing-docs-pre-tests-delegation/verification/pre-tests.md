# Pre-Tests: 测试文档 daemon 假设修复

## Acceptance Items

### Acceptance 1: fix-execution 无 daemon 硬编码
- acceptance_target: fix-execution SKILL.md 不出现 "stop/start daemon" 作为测试方式
- testing_layer: unit
- target_environment: test-pre-merge worktree
- required_evidence: grep 无匹配
- test_command: grep -c "stop.*start.*daemon\|stop/start daemon" docs/system/workspace/skills/freely-fix-execution/SKILL.md
- expected_output: "0"
- actual_output: 
- evidence_file: 

### Acceptance 2: test-execution 无 daemon 硬编码
- acceptance_target: test-execution SKILL.md 不出现 "启动 daemon" 或 "stop daemon"
- testing_layer: unit
- target_environment: test-pre-merge worktree
- required_evidence: grep 无匹配
- test_command: grep -c "启动 daemon\|stop daemon" docs/system/workspace/skills/freely-test-execution/SKILL.md
- expected_output: "0"
- actual_output: 
- evidence_file: 

### Acceptance 3: AGENTS.md 标注 Freely 自举示例
- acceptance_target: AGENTS.md test-pre-merge 段明确指出是 Freely 自举示例
- testing_layer: unit
- target_environment: test-pre-merge worktree
- required_evidence: grep 匹配
- test_command: grep -c "自举\|pre-tests.md.*B2_IBM\|daemon 型项目参考" AGENTS.md
- expected_output: "2"
- actual_output: 
- evidence_file: 
