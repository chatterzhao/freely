# Brainstorms - 20260426-0003--ibm-framework-docs

## Problem
Freely 的 issue 治理术语不一致。"预研头脑风暴"和"IBM 头脑风暴"是两个阶段但没有统一框架命名。B1 和 B2 的 I-B-M 结构隐式存在于 three-loop 和 LAWS 中，但从未显式文档化。

## Context
- three-loop 已有 pre-brainstorm 和 IBM 两个 doc-loop 子阶段
- LAWS.md §2 已定义完整链：candidate → milestone → issue → progress
- 缺少一份能力级的 canonical 文档把这些串联起来

## Decision
创建 `docs/system/workspace/ibm-framework.md` 作为 Freely 能力真源。统一术语：B1（Input→Brainstorm→Milestone）和 B2（Input→Brainstorm→Map）。AGENTS.md 和 PROJECT_INTENT.md 引用之。
