- candidate_id: C-20260616T143914Z-A
- title: 在每个关键文档头部加入规范流程位置标记，AGENTS.md.example 新增完整流程章节
- status: promoted
- milestone: M-20260616T143914Z-A
- promoted_issue_path: docs/issues/I-20260616T143914Z-A/issue.md
- decision_reason: 方案 A — 每个文档自包含位置标记，AGENTS.md 集中写完整链，skill SKILL.md 内联标记
- next_action: Materialize I-* issue in B2_IBM
---

# Candidate: 规范流程文档治理 — 位置标记 + AGENTS.md 完整化

## Problem
完整规范流程只在一处完整描述，其余文档各说各的，读者（人或 AI）不知道自己处于流程的哪一步。

## Solution
1. **AGENTS.md.example** 新增 "规范流程" 章节（feat/fix/doc-only 三种变体 + 每一步对应的命令/skill + loop 归属）
2. **5 个 skill SKILL.md** 头部加位置标记
3. **CONSTITUTION.md** 分支规范处补完整链路引用
4. **three-loop-capability-lifecycle.md** 加指向 AGENTS.md 的交叉引用

## Acceptance Criteria
- [ ] AGENTS.md.example 有完整规范流程章节（三种变体 + 命令/skill + loop）
- [ ] freely-feat-execution/SKILL.md 描述 + 位置标记
- [ ] freely-fix-execution/SKILL.md 位置标记
- [ ] freely-doc-B1_IBM-execution/SKILL.md 位置标记
- [ ] freely-doc-B2_IBM-execution/SKILL.md 位置标记
- [ ] freely-dev-loop-execution/SKILL.md 位置标记
- [ ] CONSTITUTION.md 分支规范处完整链路引用
- [ ] three-loop-capability-lifecycle.md AGENTS.md 交叉引用

## Revisit trigger
If canonical workflow steps are added/removed/reordered.
