# Candidates - 20260318-ai-cli-availability-manager

## Context
- Source brainstorm: ./brainstorms.md
- Status: in_research

## Candidates

### C-20260318-A
- title: AI CLI 工具环境变量支持确认
- problem: 需要确认 codex、kiro-cli、iflow 是否支持通过环境变量切换配置目录，这是整个方案可行性的前提。
- why_now: 如果工具不支持环境变量模式，需要采用更复杂的凭证管理方案，设计复杂度会显著增加。
- acceptance_hint: 
  - 确认每个工具是否支持 `{TOOL}_CONFIG_DIR` 或类似环境变量
  - 对于不支持的工具，确定替代方案（如软链接、配置文件路径参数）
  - 产出 `references/tool-config-matrix.md`
- priority: P0
- status: proposed
- decision_reason: 这一步决定了 skill 的实现路径。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []
- sequencing_rank: 1

### C-20260318-B
- title: AI CLI Availability Manager Skill 实现
- problem: Freely 缺少管理 AI CLI 可用性的 skill，无法在限流时保持循环持续运行。
- why_now: 这是 Freely 自主运行的核心能力，没有它 Freely 无法真正实现无人值守。
- acceptance_hint:
  - `SKILL.md` 定义触发条件、核心流程、输入输出、下一跳
  - `references/tool-config-matrix.md` 记录各工具配置模式
  - `references/limit-patterns.md` 记录限流检测模式
  - `references/profile-management.md` 记录 profile 配置规范
  - 与 constitution-guard、laws-enforcer、recovery-subagent-governance 集成
- priority: P0
- status: proposed
- decision_reason: 这是核心功能，必须实现。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []
- sequencing_rank: 2
- depends_on:
  - C-20260318-A

### C-20260318-C
- title: Profile 配置格式设计
- problem: 需要设计 Freely 如何知道用户有哪些 profile 可用，以及当前使用哪个。
- why_now: 这是 skill 运行时需要的数据结构，必须在实现前确定。
- acceptance_hint:
  - 确定配置文件位置（`~/.config/freely/ai-cli-profiles.yaml` 或项目级 `.env/`）
  - 定义配置格式（profile 名称、config_dir 路径、active 标记）
  - 考虑多项目场景下的配置共享与隔离
- priority: P0
- status: proposed
- decision_reason: 配置格式影响 skill 的输入接口设计。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []
- sequencing_rank: 2
- depends_on:
  - C-20260318-A

### C-20260318-D
- title: 限流检测与自动切换逻辑
- problem: 需要检测 AI CLI 输出中的限流信号，并决定切换策略。
- why_now: 这是可用性管理的核心功能，决定了 Freely 能否在限流时自动恢复。
- acceptance_hint:
  - 定义各工具的限流检测正则模式
  - 确定切换策略：静默自动切换 / 记录后通知用户 / 等待用户确认
  - 定义 profile 耗尽时的兜底行为（暂停循环 / 报警 / 等待冷却）
  - 与 recovery-subagent-governance 集成
- priority: P1
- status: proposed
- decision_reason: 可以先实现手动切换验证框架，再逐步完善自动化。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []
- sequencing_rank: 3
- depends_on:
  - C-20260318-B
  - C-20260318-C
