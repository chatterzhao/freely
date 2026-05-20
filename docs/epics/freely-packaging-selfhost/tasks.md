# Tasks: Freely 打包与自举验证

## Task List

### T-001 package-allowlist.txt 定义
- description: 创建 `docs/system/workspace/package-allowlist.txt`，明确定义 Freely 产品交付的内容边界
- owner: I-20260502-0500-A
- status: pending
- artifact: docs/system/workspace/package-allowlist.txt

### T-002 bin/freely-package 打包脚本
- description: 实现打包脚本，支持 --version/--output 参数，读取 allowlist 复制文件，写入 FREELY_VERSION，执行完整性验证
- owner: I-20260502-0500-A
- status: pending
- artifact: bin/freely-package

### T-003 bin/test-pre-merge-selfhost 自举验证门禁
- description: 实现自举验证门禁脚本，执行打包 → install → doctor → daemon start → Manager cycle → daemon stop 全流程验证
- owner: I-20260502-0500-A
- status: pending
- artifact: bin/test-pre-merge-selfhost

### T-004 develop HEAD 打包验证
- description: 从 develop HEAD 执行一次完整打包和自举验证，修复发现的任何问题
- owner: I-20260502-0500-A
- status: pending
- artifact: 验证报告

### T-005 治理和文档产物
- description: issue/PRD/pre-tests/tasks/code-review/milestones 治理产物维护
- owner: I-20260502-0500-A
- status: completed
- artifact: docs/epics/freely-packaging-selfhost/
