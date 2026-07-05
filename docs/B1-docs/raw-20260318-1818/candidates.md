# Candidates - 20260318-1818--ai-cli-availability-manager

## Context
- Source brainstorm: ./brainstorms.md
- Status: done_research

## Candidates

### C-20260318-1818-A: legacy issue
- title: AI CLI 工具环境变量支持确认
- problem: 需要确认 codex、kiro-cli、iflow 是否支持通过环境变量切换配置目录，这是整个方案可行性的前提。
- why_now: 如果工具不支持环境变量模式，需要采用更复杂的凭证管理方案，设计复杂度会显著增加。
- acceptance_hint: 
  - 确认每个工具是否支持 `{TOOL}_CONFIG_DIR` 或类似环境变量
  - 对于不支持的工具，确定替代方案（如软链接、配置文件路径参数）
  - 产出 `references/tool-config-matrix.md`
- priority: P0
- status: absorbed
- adoption_type: supporting_evidence
- decision_reason: 工具配置矩阵已作为 `ai-cli-availability-manager` 的 supporting evidence 被 `I-20260318-1630` 吸收，不再单独 materialize 平行 issue。
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260318-1818-A/issue.md
- milestone: M-20260318-1818-A
- session_refs: []
- sequencing_rank: 1
- resolution: |
    - codex: 支持 CODEX_HOME 环境变量切换配置目录
    - iflow: 支持 IFLOW_* 环境变量覆盖配置项，不支持目录切换
    - kiro: 未安装待确认
    - 已产出 references/tool-config-matrix.md

### C-20260318-1818-A: legacy issue
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
- status: absorbed
- adoption_type: supporting_evidence
- decision_reason: skill 与 references 已作为 `I-20260318-1630` 的 canonical completion surface 落盘，这条 pre-brainstorm 只保留 supporting provenance。
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260318-1818-A/issue.md
- milestone: M-20260318-1818-A
- session_refs: []
- sequencing_rank: 2
- depends_on:
  - C-20260318-A
- resolution: |
    - 已创建 SKILL.md 定义核心流程
    - 已创建 references/tool-config-matrix.md
    - 已创建 references/limit-patterns.md
    - 已创建 references/profile-management.md

### C-20260318-1818-A: legacy issue
- title: Profile 配置格式设计
- problem: 需要设计 Freely 如何知道用户有哪些 profile 可用，以及当前使用哪个。
- why_now: 这是 skill 运行时需要的数据结构，必须在实现前确定。
- acceptance_hint:
  - 确定配置文件位置（`~/.config/freely/ai-cli-profiles.yaml` 或项目级 `.env/`）
  - 定义配置格式（profile 名称、config_dir 路径、active 标记）
  - 考虑多项目场景下的配置共享与隔离
- priority: P0
- status: absorbed
- adoption_type: supporting_evidence
- decision_reason: profile 配置格式已作为 `ai-cli-availability-manager` 的 supporting contract 被当前 canonical owner 吸收。
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260318-1818-A/issue.md
- milestone: M-20260318-1818-A
- session_refs: []
- sequencing_rank: 2
- depends_on:
  - C-20260318-A
- resolution: |
    - 已在 references/profile-management.md 中定义配置格式
    - 全局配置：~/.config/freely/ai-cli-profiles.yaml
    - 项目级覆盖：.env/ai-cli-profiles.yaml
    - 支持环境变量引用避免明文存储敏感信息

### C-20260318-1818-A: legacy issue
- title: 限流检测与自动切换逻辑
- problem: 需要检测 AI CLI 输出中的限流信号，并决定切换策略。
- why_now: 这是可用性管理的核心功能，决定了 Freely 能否在限流时自动恢复。
- acceptance_hint:
  - 定义各工具的限流检测正则模式
  - 确定切换策略：静默自动切换 / 记录后通知用户 / 等待用户确认
  - 定义 profile 耗尽时的兜底行为（暂停循环 / 报警 / 等待冷却）
  - 与 recovery-subagent-governance 集成
- priority: P1
- status: absorbed
- adoption_type: supporting_evidence
- decision_reason: 限流检测、双限额归因与切换验证现已属于 `I-20260318-1630` 的 canonical verification surface，不再单开 follow-on issue。
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260318-1818-A/issue.md
- milestone: M-20260318-1818-A
- session_refs: []
- sequencing_rank: 3
- depends_on:
  - C-20260318-B
  - C-20260318-C
- resolution: |
    - 已在 references/limit-patterns.md 中定义限流检测模式
    - 已在 SKILL.md 中定义切换流程
    - 默认策略：静默自动切换，记录事件到 recovery
    - 兜底行为：全部 profile 失效时暂停循环，通知用户
    - 2026-03-18 当前轮补充验证到 Codex 结构化限额至少分为 `primary` 与 `secondary` 两档
    - `runtime/freely` 已补充双限额解析、统一 reason 归因与 `reset_at` 选择
    - 已新增测试覆盖：
      - `primary_rate_limit_exhausted`
      - `secondary_rate_limit_exhausted`
    - 验证证据：
      - `docs/system/workspace/scripts/tests/test-freely-ai-account-switch`
      - `docs/system/workspace/scripts/runtime/freely`

### C-20260318-1818-A: legacy issue
- title: CLI First 原则写入宪法
- problem: Freely 需要明确 CLI 优先的架构原则，确保所有功能都有 CLI 接口。
- why_now: 在设计 ai-cli 命令时发现需要明确这一原则，避免后续开发走偏。
- acceptance_hint:
  - 宪法中添加 CLI First 章节
  - 定义 CLI 接口设计规范
- priority: P0
- status: dropped
- adoption_type: superseded
- decision_reason: `CLI First` 已直接进入宪法真源，作为架构原则独立成立，不再保留为这组 availability manager 子候选的 active owner。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- superseded_by:
  - docs/CONSTITUTION.md
- session_refs: []
- sequencing_rank: 1
- resolution: |
    - 已写入 CONSTITUTION.md 第 10.1 章
    - 架构优先级：CLI (核心) → API (可选) → UI (可选)

### C-20260318-1818-A: legacy issue
- title: 统一登录命令设计
- problem: 用户需要两步操作（codex login + freely save），体验不连贯。
- why_now: 用户反馈操作繁琐，需要简化。
- acceptance_hint:
  - `freely ai login codex` 一键完成登录和保存
  - 自动检测账号并保存授权文件
- priority: P0
- status: absorbed
- adoption_type: supporting_evidence
- decision_reason: `freely ai login codex` 已进入 `runtime/ai-cli` 与 `I-20260318-1630` 的 canonical completion，不再需要单独 owner。
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260318-1818-A/issue.md
- milestone: M-20260318-1818-A
- session_refs: []
- sequencing_rank: 4
- depends_on:
  - C-20260318-B
- resolution: |
    - 已实现 bin/ai 脚本
    - login 命令：调用 codex login 后自动保存
    - 自动从 JWT 提取 email 作为账号名

### C-20260318-1818-A: legacy issue
- title: 目录命名规则
- problem: 邮箱中包含 `.` 可能导致某些文件系统问题。
- why_now: 实现时发现需要明确目录命名规则。
- acceptance_hint:
  - 确定哪些字符需要替换
  - 保持可读性
- priority: P1
- status: absorbed
- adoption_type: supporting_evidence
- decision_reason: 实现细节，但影响用户体验。
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260318-1818-A/issue.md
- milestone: M-20260318-1818-A
- resolution: |
    - 测试确认 macOS/Linux 支持 `@`
    - 只替换 `.` 为 `-`
    - 示例：worahe3973@outlook.com → codex-worahe3973@outlook-com
