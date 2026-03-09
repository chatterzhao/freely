# Candidates - 20260309-1943--agent-skills-standard-compliance

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260309-1943
- title: Workspace Skill Governance and Agent Skills Compliance Alignment
- problem: Freely 当前 workspace skills 满足最小 `SKILL.md` 格式，但 skill 索引、目录自包含性、progressive disclosure 和“修改 skill 本身”的治理入口都还不完整。
- why_now: Freely 正在用 skill 体系治理自己；如果 skill 自身不可发现、不可移植、不可审计，后续所有 dogfooding 都会建立在半合规结构上。
- acceptance_hint: 1) 修正 skill 索引漂移；2) 明确 skill 变更治理入口并记录如何使用外部 `skill-creator`；3) 将核心 skill 的长说明拆到 `references/` 或 colocated resources；4) 统一相对路径引用策略。
- priority: P1
- status: proposed
- decision_reason: 问题已在本分支完成结构级整改：skill 索引已校正，核心 skills 已拆分 references，并补了专用 `workspace-skill-governance` 入口。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []
- remediation_done:
  - `docs/system/workspace/skills/README.md` 已修正失效的 `doc-loop-execution` 入口
  - `docs/system/workspace/skills/workspace-skill-governance/SKILL.md` 已新增
  - 核心编排 skills 已拆分为主文 + `references/`
  - examples / applicability references 已补到薄弱 skills
