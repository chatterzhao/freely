# PRD: AGENTS.md daemon test refs → pre-tests.md

- issue_id: I-20260624T104233Z-A

## Goal
全项目搜索硬编码的 daemon 测试指令（stop/start daemon、启动 daemon、daemon start 等测试模式），替换为指向 pre-tests.md 的委托。确保所有测试方式由 pre-tests.md 定义，而非 AGENTS.md 或 skill 文档硬编码。

## Dev-Loop Handoff
- 修改范围：仅 AGENTS.md
- 修改方式：删除 hardcoded numbered steps（pre-init-runtime、freely-package、start daemon、verify Manager cycle、merge/fix），替换为 pre-tests.md 委托
- 保留：Freely 自举上下文（标注为 "daemon 型项目参考"）、`./bin/test-pre-merge-selfhost` 引用
- 验证方式：grep 全项目无 "stop/start daemon"、"启动 daemon"、"daemon start" 等测试硬编码模式
- 修复已提交：194080e42
