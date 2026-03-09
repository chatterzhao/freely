# Candidates - 20260309-2003--document-skill-boundary-planning

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260309-2003-A
- title: Documentation Layer Boundary Realignment
- problem: `PROJECT_INTENT`、`CONSTITUTION`、`LAWS`、`AGENTS.md`、`README.md` 与 workspace skills 之间的职责边界还未被显式固定，导致部分内容重复、越层或漂移。
- why_now: Freely 把 skill 当作产品能力接口，如果上层文档和 skill 边界不稳，后续能力设计会持续混层。
- acceptance_hint: 明确六层信息架构；压缩 `README` 与 `AGENTS` 到入口职责；把 How 层内容回收到 skills/references；保持 `LAWS` 作为规则语义唯一事实源。
- priority: P0
- status: proposed
- decision_reason: 这是后续 skill 重构与治理入口设计的前提。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []
- sequencing_rank: 1

### C-20260309-2003-B
- title: Workspace Skill Architecture Restructure
- problem: 当前 skills 还未完全按产品能力接口来设计，核心编排 skill 的主文过胖，而“修改 skill 本身”的治理入口缺失。
- why_now: 不先重组 skill 架构，Freely 的能力暴露面就会继续停留在“项目流程文档”而不是“产品能力包”。
- acceptance_hint: 按 `guard/capability/governance` 三类整理；为核心 skill 增加 references 拆分；新增 `workspace-skill-governance` 或等效治理入口。
- priority: P0
- status: proposed
- decision_reason: 直接影响 Freely 如何通过 skill 暴露、组织和治理自身能力。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []
- sequencing_rank: 2
- depends_on:
  - C-20260309-2003-A

### C-20260309-2003-C
- title: Review Alignment Recovery and Loop Boundary Governance
- problem: Freely 还未把“评审发现不对齐时是直接修补还是 git 撤销重做”“每个循环何时应提交”“继续用旧 worktree 还是新建”收敛成显式治理能力。
- why_now: 如果这些前置规则缺失，文档重构和代码实现都会更容易跨边界补丁化，增加 token 消耗，并提高语义丢失和结构污染风险。
- acceptance_hint: 明确评审分流规则；定义直接修补 vs git 撤销重做的判断标准；定义循环提交粒度与 worktree 续用/新建规则；确保 Freely 自己先按这些规则运行。
- priority: P0
- status: proposed
- decision_reason: 这是控制重构与实现边界、避免“不断修改掉进地狱”的前置治理能力。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []
- capability_class: governance
- rollout_mode:
  - current-governance-for-this-planning
  - target-freely-capability
- sequencing_rank: 3
- depends_on:
  - C-20260309-2003-A
  - C-20260309-2003-B
