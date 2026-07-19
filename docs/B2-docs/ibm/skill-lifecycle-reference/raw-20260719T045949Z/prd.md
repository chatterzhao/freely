# PRD: B1/B2 skill 补充三环能力生命周期交叉引用
- issue_id: I-20260719T045949Z-A
- epic: ibm
- story: skill-lifecycle-reference

## Goal
两个核心 IBM skill 末尾新增三环能力生命周期交叉引用，让读者明确自己在 doc-loop 中的位置。

## 实现方案
- B1 skill（freely-doc-B1_IBM-execution）：末尾新增"能力生命周期参考"，说明 B1 是 doc-loop 第一阶段
- B2 skill（freely-doc-B2_IBM-execution）：末尾新增"关键参考"，聚合 PRD 质量门槛、设计派生约束、三环生命周期引用

改动范围：2 个 SKILL.md 文件，纯文档，无代码逻辑变更。
