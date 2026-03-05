---
name: dev-loop-execution
description: 执行 D:dev-loop(DDD) 工作流，包含文档阅读、实现、测试和文档更新闭环。当 AI 在治理的 issue/story 上下文中执行代码变更时使用。
---

# skill:dev-loop-execution

## 工作流
1. 阅读治理文档和 issue 上下文。
2. 实现前，定义当前周期的语义范围，避免在单次提交中混合不相关关注点。
3. 在正确的功能 worktree 中实现变更。
4. 如果代码和文档不一致，优先代码/测试修正路径。
5. 开发和评审期间，持续根据实现和发现的缺陷添加/调整测试用例。
6. push/merge 前，执行语义提交边界复查；如仍有混合关注点则拆分提交。
7. 运行必需的测试，包括集成验收测试，将 `TEST` 结果作为合并/提升证据。
8. 用测试证据更新进度/issue 状态文档。
9. 用 `skill:laws-enforcer` 和 `skill:constitution-guard` 验证闭环。

## 完成
- 代码、测试和文档状态更新已对齐且可验证。
