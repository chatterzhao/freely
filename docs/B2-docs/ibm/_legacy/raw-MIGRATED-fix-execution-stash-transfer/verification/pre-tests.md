# Pre-Tests: fix-execution stash 工作流

## Acceptance Items

### Acceptance 1: fix-execution 无 cp 硬编码
- acceptance_target: SKILL.md 不出现 cp 修改转移方式
- testing_layer: unit
- test_command: grep -c "cp <test-pre-merge\|cp 修改\|cp 到可写" docs/system/workspace/skills/freely-fix-execution/SKILL.md
- expected_output: "0"
- actual_output: 
- evidence_file: 

### Acceptance 2: stash push --include-untracked 存在
- acceptance_target: 包含正确的 stash push 命令
- testing_layer: unit
- test_command: grep -c "stash push --include-untracked" docs/system/workspace/skills/freely-fix-execution/SKILL.md
- expected_output: "2"
- actual_output: 
- evidence_file: 

### Acceptance 3: stash apply + status + drop 存在
- acceptance_target: apply → check → drop 安全流程
- testing_layer: unit
- test_command: grep -c "stash apply.*stash drop" docs/system/workspace/skills/freely-fix-execution/SKILL.md
- expected_output: "1"
- actual_output: 
- evidence_file: 
