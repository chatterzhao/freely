# Tasks: Freely 打包与自举验证

## Task List

### T-001 package-allowlist.txt 定义
- description: 创建 `docs/system/workspace/package-allowlist.txt`，明确定义 Freely 产品交付的内容边界
- owner: I-20260502-0500-A
- status: completed
- artifact: docs/system/workspace/package-allowlist.txt
- evidence: 17 条路径定义，含 Owner 维护责任标注，已合并到 develop

### T-002 bin/freely-package 打包脚本
- description: 实现打包脚本，支持 --version/--output 参数，读取 allowlist 复制文件，写入 FREELY_VERSION，执行完整性验证
- owner: I-20260502-0500-A
- status: completed
- artifact: bin/freely-package
- evidence: version validate, allowlist copy, integrity verify, 非法版本号/missing 路径报错退出

### T-003 bin/test-pre-merge-selfhost 自举验证门禁
- description: 实现自举验证门禁脚本，执行打包 → install → doctor → daemon start → Manager cycle → daemon stop 全流程验证
- owner: I-20260502-0500-A
- status: completed
- artifact: bin/test-pre-merge-selfhost
- evidence: --timeout 参数, 6-step 流程, 独立退出码 1-7, supervisor 退出确认

### T-004 develop HEAD 打包验证
- description: 从 develop HEAD 执行一次完整打包和自举验证，修复发现的任何问题
- owner: I-20260502-0500-A
- status: completed
- artifact: 验证报告
- evidence: AT-001/002/003/006/007/008 PASS; AT-004/005/009 需要 test-pre-merge 批次环境

### T-005 治理和文档产物
- description: issue/PRD/pre-tests/tasks/code-review/milestones 治理产物维护
- owner: I-20260502-0500-A
- status: completed
- artifact: docs/epics/freely-packaging-selfhost/
