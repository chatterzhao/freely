# Tasks: 修复 chat help 错误信息 shell 引号嵌套
- issue_id: I-20260720T023136Z-A

## 任务分解

### T1: 修改 L6700 log_error 字符串
- [x] 将 `docs/system/workspace/scripts/runtime/freely` L6700 的外层双引号改为单引号，使 `<描述>`/`<详细描述>` 成为字面量
- 关联: AT-001

### T2: 语法与渲染验证
- [x] 运行 `bash -n docs/system/workspace/scripts/runtime/freely` 确认语法通过
- [x] 模拟执行 log_error 行确认输出完整文本且无 `No such file`（AT-002）
- [x] grep 确认 `fix|feat: <描述>`、`<详细描述>`、`--kind fix --body` 全部命中（AT-003）
- 关联: AT-001 / AT-002 / AT-003

### T3: 证据归档
- [x] 将 AT-001~AT-003 执行证据写入 `verification/test-evidence/`
- 关联: 全部 acceptance items
