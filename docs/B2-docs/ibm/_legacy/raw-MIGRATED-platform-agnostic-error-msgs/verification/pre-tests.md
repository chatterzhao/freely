# Pre-Tests: 平台硬编码报错修复
## Acceptance Items
### A1: wt-create 无 GitHub
- test_command: grep -c "GitHub\|github" docs/system/workspace/scripts/worktree/wt-create
- expected_output: "0"
- actual_output: 
- evidence_file: 
### A2: hook 无硬编码参数
- test_command: grep -c "\-\-repo.*\-\-title.*\-\-body" .githooks/reference-transaction.sh
- expected_output: "0"
- actual_output: 
- evidence_file: 
### A3: freely feedback help 无 GitHub
- test_command: grep -c "GitHub repository" docs/system/workspace/scripts/runtime/freely
- expected_output: "0"
- actual_output: 
- evidence_file: 
