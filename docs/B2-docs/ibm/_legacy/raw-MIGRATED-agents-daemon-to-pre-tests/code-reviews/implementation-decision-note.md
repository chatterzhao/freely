---
issue_id: I-20260624T104233Z-A
issue_path: docs/issues/I-20260624T104233Z-A/issue.md
phase_state: done_b2_ibm
---

- issue_id: I-20260624T104233Z-A
- issue_path: docs/issues/I-20260624T104233Z-A/issue.md

## Implementation Decision Note

- decision: AGENTS.md 中 hardcoded numbered steps（pre-init-runtime、freely-package、start daemon、verify Manager cycle、merge/fix）替换为指向 pre-tests.md 的委托语句
- why_this: Freely 面向任意类型项目，测试方式应由 pre-tests.md 定义，不能由 AGENTS.md 或 skill 文档硬编码 daemon 步骤。之前的修复（#3411）已改 skill 文件，但 AGENTS.md 的 numbered list 仍残留硬编码。本次彻底替换。
- alternatives_considered:
  1. 保留 numbered steps 但加标注 — 与 "验证方式由 pre-tests.md 决定" 原则矛盾
  2. 完全删除自举示例 — 丢失 Freely 自举上下文，不必要
  3. 当前方案：保持 pre-tests.md 委托 + 保留自举上下文 + 标注 daemon 型项目参考
- boundary_non_goals:
  - 不修改三个 skill 文件（已在 #3411 修复）
  - 不修改 bin/test-pre-merge-selfhost（自举实现脚本，非测试指令）
  - 不修改 docs/system/ 中关于 daemon 能力本身的文档
- residual_risk:
  - 后续新增 skill 或文档可能再次引入 daemon 硬编码，需 code-review 留意
  - pre-tests.md 模板和编写规范由 B2_IBM 维护，需保持一致性
