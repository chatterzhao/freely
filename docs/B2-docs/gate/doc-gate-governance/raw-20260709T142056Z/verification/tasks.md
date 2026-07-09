# Tasks: doc gate 移除 3 个非 agent 注入文件检查
- issue_id: I-20260709T142056Z-A

- [x] 从 `check_doc_gate_or_fail` 移除 3 个 B1-docs 文件 + pre-brainstorms 目录检查
- [x] RED 验证：AT-001 确认修复前 B1-docs 引用存在
- [x] dev 实现：删除 4 行
- [x] GREEN 验证：AT-001 确认修复后 B1-docs 引用消失
- [x] AT-002 验证 daemon 可启动
