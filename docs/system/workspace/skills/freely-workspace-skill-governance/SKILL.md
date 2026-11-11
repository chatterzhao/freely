---
name: freely-workspace-skill-governance
description: >-
  在 Freely 仓库内治理和修改 workspace skill。覆盖 skill 新增、拆分、
  重构、校准，以及 references、scripts 和 skill 索引的维护。

  Use when: 任务涉及修改 `docs/system/workspace/skills/**` 下的 skill。
  触发词："skill governance"、"修改 skill"、"新增 skill"、"重构 skill"。
loop: governance
owner: governance
supersedes: []
---

# skill:freely-workspace-skill-governance

## 职责

- 约束 Freely 仓库内 skill 改动的合法入口和同步范围。
- 确保 skill 改动先有 pre-brainstorm，再落实现与索引修正。
- 确保 `SKILL.md`、`references/`、运行时真源和 skill 索引保持一致。

## 不负责

- 不替代通用 `skill-creator`
- 不替代 `freely-doc-B1_IBM-execution` 或 `freely-doc-B2_IBM-execution`

## 工作流

1. 若 skill 改动边界尚未收敛，先进入 `freely-doc-B1_IBM-execution`。
2. 需要通用 skill 设计准则时，读取系统 skill `/home/devbox/.codex/skills/.system/skill-creator/SKILL.md`。
3. 修改 skill 时同时检查：
   - 当前 `SKILL.md`
   - 同目录 `references/`
   - `docs/system/workspace/skills/README.md`
   - 相关 `docs/system/workspace/scripts/**`
   - 相关 hooks / `bin/*`
   - `docs/CONSTITUTION.md`
   - `docs/LAWS.md`
4. 主 `SKILL.md` 只保留触发条件、职责、最短步骤和 reference 导航；长矩阵、模板、示例下沉到 `references/`。
5. 如果 skill 名称、入口或关键职责变化，必须同步修正索引和交叉引用。

## 完成

- skill 入口、主文、references 和相关真源已同步。
- skill 改动没有留下已知漂移。
