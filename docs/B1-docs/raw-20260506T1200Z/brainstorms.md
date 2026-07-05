# Brainstorms — IBM Skill Rename

## Discovery

### Source
- Raw issue: `docs/issues/raw-20260506T1200Z/issue.md`
- GitHub: https://github.com/chatterzhao/freely/issues/285
- Created: 2026-05-06, author: zhaoquan
- 原始问题：`doc-pre-brainstorm-execution` / `doc-ibm-execution` 命名未体现 B1_IBM/B2_IBM，I→B→M 骨架未被下层 skill 强制消费。

### 修复项
1. 改名 `doc-B1_IBM-execution` / `doc-B2_IBM-execution`，全局替换
2. 两个 SKILL.md 加入 I→B→M 骨架
3. ibm-framework.md 术语统一

### 当前状态调查

检查发现以下事实：

- **Skill 文件**：`freely-doc-B1_IBM-execution/SKILL.md` 和 `freely-doc-B2_IBM-execution/SKILL.md` 已存在，均包含 I→B→M 骨架章节
- **ibm-framework.md**：术语已统一使用 B1_IBM/B2_IBM/candidate/milestone/issue，旧称对照表已包含（ibm-framework.md 行 229-235）
- **旧 skill 文件**：`doc-pre-brainstorm-execution` / `doc-ibm-execution` 已不存在（已被全局替换吸收）

三项修复内容均已在并发工作中完成。

### 边界检查
- CONSTITUTION.md：分支/工作树策略与 skill 命名无冲突
- LAWS.md：无涉及 skill 命名的约束
- PROJECT_INTENT.md：未限制 skill 命名格式

## Convergence

该 raw issue 的全部修复内容已被其他并发工作吸收完成。当前代码库状态已经满足原始需求，无需额外操作。

## Decision

- **结论**: absorbed
- **理由**: 三项修复均已在并发工作中完成。`freely-doc-B1_IBM-execution` / `freely-doc-B2_IBM-execution` 已就位，I→B→M 骨架已嵌入，ibm-framework.md 术语已统一
- **证据**: 
  - `docs/system/workspace/skills/freely-doc-B1_IBM-execution/SKILL.md` — 存在且含 I→B→M 骨架
  - `docs/system/workspace/skills/freely-doc-B2_IBM-execution/SKILL.md` — 存在且含 I→B→M 骨架
  - `docs/system/workspace/ibm-framework.md` — 术语已统一
