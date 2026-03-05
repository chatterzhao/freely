---
name: constitution-guard
description: 在自主执行前后强制执行宪法硬性约束。当 AI 规划或完成开发、合并、发布或恢复操作时使用，必须保证分支/worktree、架构和治理边界保持合规。
---

# skill:constitution-guard

## 工作流
1. 在执行前运行宪法预检。
2. 使用 `references/constitutional-gates.md` 验证硬性约束。
3. 阻止任何违反硬性约束的操作。
4. 在合并/提升/发布操作后重新运行门禁。
5. 记录通过/失败及证据。

## 完成
- 硬性约束通过，或操作被阻止并显式说明原因。
