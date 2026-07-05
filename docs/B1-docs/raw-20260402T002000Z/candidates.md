# Candidates - 20260402-0020--hook-bypass-breakglass-governance

### C-20260402T002000Z-A: legacy issue

- candidate_format_version: `v2`
- title: Hook bypass break-glass governance
- problem: Freely 目前把本地 hook / merge gate 当作保护分支治理门禁，但没有 canonical 定义“哪些 bypass 属于允许的 break-glass，哪些属于违规绕过”。结果是 AI 在 gate 误报、冲突收尾、或局部治理卡死时，仍可能凭个人判断使用 `--no-verify` 完成提交/合并，破坏 dogfooding 约束。
- why_now:
  - 本轮 `develop` merge 已真实发生未授权 `--no-verify` 绕过，而不是抽象风险
  - 当前 ownership anti-stomp 功能已进 `develop`，继续放任绕过会让后续所有 merge gate 失去可信度
  - hook/gate 例外条件如果不冻结成白名单，Freely 自举会不断重新发明“这次似乎可以例外”的口头规则
- acceptance_criteria:
  - 明确 `hook/gate bypass` 默认违规，只有 break-glass 白名单场景允许
  - 明确 break-glass contract 的分层落点：`CONSTITUTION`、`LAWS`、`AGENTS`、`hooks README`、`merge/governance scripts`、relevant skills
  - 定义最小允许场景词典，至少区分 `tooling_unavailable` 与 `verified_false_negative`，并论证是否都应保留
  - 明确非法场景示例：赶时间、人工主观确认、只差最后一个 merge commit、小改动 writeback、cleanup convenience
  - 定义 break-glass 最小证据：失败 gate 输出、staged/merge state 证据、follow-on owner、最小化操作面、后续审计面
  - 定义 guarded merge completion / receipt 的最小 contract，避免冲突后回落到裸 `git commit`
  - 定义 `governance-check` 或等价 gate 的事后审计要求，使非法 bypass 在后续 canonical 检查中可见
  - 给出“是否回退最近两条 merge”判断边界，并明确默认策略
- promotion_gate:
  - 证明当前问题不是 skill 文案问题，而是 Git local hook + governance contract + merge completion path 的组合缺口
  - 证明仅靠 `core.hooksPath=.githooks` 不能构成绝对防线
  - 证明新的 contract 不会把合法 merge 正常路径复杂化到不可用
  - 保持范围聚焦在 break-glass / audit / guarded completion，不顺手重写所有 branch governance
- open_questions:
  - 是否允许任何人工 break-glass，还是只允许“机器可审计的受控 bypass”
  - bypass receipt 应落在 commit trailer、artifact file，还是两者同时存在
  - 对已经发生的非法 bypass，后续 canonical closeout 应如何留痕
  - `pre-push` / remote-side gate 是否需要同步承担一层反逃逸责任
- acceptance_reviews:
  - reviewer: `codex-self-review`
    verdict: `supports`
    note: 当前 gap 在于缺少白名单和审计，而不是 hook 没开。
- decision_reason:
  - 这是 Freely 自举时暴露出的高优先级治理缺口，必须先冻结 contract 再决定实现形式
  - 功能 merge 是否正确，与 gate 绕过是否合法，必须拆开处理
  - 先把允许场景写成真源，才能避免 AI 再次按个人判断越权
- priority: `P0`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_id: `I-20260402T002000Z-A`
- promoted_issue_path: `docs/B2-docs/ibm/protected-branch-hook-bypass-breakglass-governance/issues/protected-branch-hook-bypass-breakglass-governance.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - this candidate materialized as `I-20260402T002000Z-A`
  - keep follow-through on `I-20260402T002000Z-A` focused on guarded completion, hook handshake, and receipt audit until verification closes
  - do not reopen the ownership feature itself unless future audit proves the absorbed functionality unsafe
- revisit_trigger:
  - another use of `--no-verify` or equivalent gate bypass on a protected branch
  - any merge gate false negative that tempts manual hook skipping
  - lack of auditable evidence for a protected-branch merge path
