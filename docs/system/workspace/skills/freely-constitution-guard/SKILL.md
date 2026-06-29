---
name: freely-constitution-guard
description: >- 在自主执行前后强制校验 `docs/CONSTITUTION.md` 硬性约束。保证
  分支、worktree、架构和治理边界在操作前后均合规。

  Use when: AI 规划或完成开发、合并、发布、恢复操作。
  触发词："constitution"、"宪法检查"、"合规"、"约束校验"。
---

# skill:freely-constitution-guard

## 工作流
1. 在执行前运行宪法预检。
2. 使用 `references/constitutional-gates.md` 验证硬性约束。
3. 阻止任何违反硬性约束的操作。
4. hook/gate bypass 永久禁止。遇到 bypass 请求时，回看 `docs/CONSTITUTION.md` 与 `docs/LAWS.md` §2D 确认禁令；`FREELY_SKIP_IBM_GATE="违规绕过门禁中，理由充分，是：<业务理由>"` 是唯一合法豁免。
5. 在合并/提升/发布操作后重新运行门禁。
6. 记录通过/失败及证据。

## 完成
- 硬性约束通过，或操作被阻止并显式说明原因。
