---
issue_id: I-20260804T073054Z-A
issue_path: docs/B2-docs/skills/skill-yaml-frontmatter/raw-20260804T073054Z/issues/I-20260804T073054Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260804T073054Z-A
- issue_path: docs/B2-docs/skills/skill-yaml-frontmatter/raw-20260804T073054Z/issues/I-20260804T073054Z-A.md

## Implementation Decision Note

- decision: 修复 30 个 frontmatter 块标量语法，并在 deploy-skills 与 pre-commit 增加 YAML 校验
- why_this: 根因是语法错误 + 部署链无校验；双链路拦截才能防复发
- alternatives_considered: 仅批量 sed 修复（快但会复发，拒绝）；重写全部 skill frontmatter 为 flow 风格（改动面大且无必要）
- boundary_non_goals: 不改 skill 内容语义；不重排部署目录结构
- residual_risk: 部署目录存在旧非前缀 skill 与源目录并存，清理依赖 deploy-skills --force 覆盖；无法覆盖的独立目录需人工核对
