---
name: dev-loop-execution
description: 执行 `DDD` 开发环，负责在已完成 docs 收敛的 issue/story 上下文中实现、测试，并把状态回写给 auto-loop。
---

# skill:dev-loop-execution

## 适用边界

- 当前 issue 已有完整或足够完整的 `doc-loop` 产物。
- 当前回合主要工作是实现、测试、评审修复和状态回写。

## 输入产物

- `docs/epics/{epic}/{story}/issues/{issue-name}.md`
- `docs/epics/{epic}/{story}/prd.md`
- `docs/epics/{epic}/{story}/pre-tests.md`
- `docs/epics/{epic}/{story}/tasks.md`
- `docs/milestones.md`
- 按需读取：
  - `docs/progress/{epic}/p-{issue}.md`
  - recovery 记录
  - review / test 结果

## 工作流
1. 阅读治理文档和 issue 上下文。
2. 实现前，定义当前周期的语义范围，避免在单次提交中混合不相关关注点。
3. 在正确的功能 worktree 中实现变更。
4. 如果代码和文档不一致，优先代码/测试修正路径。
5. 开发和评审期间，持续根据实现和发现的缺陷添加/调整测试用例。
6. push/merge 前，执行语义提交边界复查；如仍有混合关注点则拆分提交。
7. 运行必需的测试，包括集成验收测试，将 `TEST` 结果作为合并/提升证据。
8. 用测试证据更新：
   - `docs/progress/{epic}/p-{issue}.md`
   - `docs/milestones.md`
   - 对应 issue 状态文档
9. 用 `skill:laws-enforcer` 和 `skill:constitution-guard` 验证闭环。

## 状态交换

- 向 `auto-loop` 回流的最小结果应包括：
  - 当前实现状态：`in_progress | blocked | completed`
  - 关键 `TEST` 结果
  - progress / milestone / issue 回写结果
  - 若需要补文档或重回 `doc-loop`，明确给出原因
  - 若崩溃或阻塞，提供恢复所需最小上下文

## 完成
- 代码、测试和文档状态更新已对齐且可验证。
