# Candidates - 20260405-1130--project-level-agents-bootstrap-and-management

## C-20260405-1130-A

- candidate_format_version: `v2`
- title: Project-level AGENTS bootstrap and management contract
- status: `needs_research`
- source_brainstorm: `docs/pre-brainstorms/20260405-1130--project-level-agents-bootstrap-and-management/brainstorms.md`
- problem: Freely 已存在“为项目补最小 `AGENTS.md` 并优先读取它”的行为，但缺少稳定 capability contract 来定义模板来源、已有文件保留策略、runtime 组合顺序和 self-hosting 管理边界。
- why_now:
  - 当前 dogfooding 已经暴露“Freely 管理用户项目的 `AGENTS.md`”与“Freely 管理自己项目的 `AGENTS.md`”是同一条产品能力问题
  - 现有测试只证明缺失时会创建，还没有冻结已有 `AGENTS.md` 的保留语义
  - 当前窄 owner 已明确禁止把这条能力边界偷渡进 `AGENTS.md` 输出风格实验
- acceptance_criteria:
  - capability doc 明确项目级 `AGENTS.md` 的生成、读取、保留和升级边界
  - 回归测试覆盖“已有项目 `AGENTS.md` 不被意外覆盖”或其他被正式批准的 contract
  - 明确 generated default、项目自定义入口与 Freely 仓库自用 `AGENTS.md` 的层级关系
  - 明确 self-hosting 下 Freely 如何按同一规则管理自己的项目级 `AGENTS.md`
- promotion_gate:
  - 不把这条能力继续塞回当前 `agents-cli-output-style-experiment-governance` owner
  - 不在 contract 未冻结前直接修改 runtime 覆盖策略
  - materialize 前先确认该能力应挂接的 milestone / epic
- open_questions:
  - 默认模板应来自哪里，是否允许项目初始化时注入项目意图摘要
  - 已有 `AGENTS.md` 的保留/升级策略是否需要 diff、merge 或显式 break-glass
  - Freely 复用能力真源与项目 `AGENTS.md` 的优先级和拼接方式应如何 formalize
- decision_reason:
  - 这是已存在行为的 contract 缺口，不是凭空新增需求
  - 它已经影响用户项目治理入口和 Freely 自举治理入口两条主线
  - 但当前边界还不稳定，先停在 pre-brainstorm 更符合法律
- next_action: 保持在 pre-brainstorm，待确认 milestone/epic 归属后再 materialize 独立 capability owner，并补 preserve-existing-AGENTS 测试。
- revisit_trigger: 当需要把项目级 `AGENTS.md` 的生成/管理行为作为 Freely 对外长期消费能力冻结时。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
