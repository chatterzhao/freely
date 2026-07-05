# Candidates - 20260405-1235--tool-authorization-bootstrap-and-post-consent-materialization

## C-20260405T123500Z-A: legacy issue

- candidate_format_version: `v2`
- title: Tool authorization bootstrap and post-consent materialization contract
- status: `promoted`
- source_brainstorm: `docs/B1-docs/raw-20260405T123500Z/brainstorms.md`
- problem: Freely 已具备 activation consent、tool policy materialization、worktree boundary bootstrap 与 adapter axis，但仍没有单独 contract 定义用户显式同意后如何为各外部工具完成 project authorization/bootstrap、哪些能力能自动 materialize、哪些仍需手工 trust，以及在未同意/未完成时系统应如何解释退化行为。
- why_now:
  - 当前 dogfooding 已明确要求 `freely init` 只能由用户主动触发，不能静默 auto-trust 项目
  - Freely 已经在自动写 `.codex/config.toml`、wrapper、`--add-dir`、launch-time permission posture；缺少对“这算哪一层授权”的统一解释
  - `direct` / `acp` / `cc-use-codex-cli` / `kiro-cli` 的配置面差异已经足够大，不先收敛 matrix 就容易把某个工具的特例误当产品总规则
- acceptance_criteria:
  - 冻结一份 per-tool authorization/bootstrap matrix，明确 project-local config、launch-time injection、home-level manual requirement 和 unsupported surface
  - 明确 activation consent、project authorization bootstrap、tool trust、adapter policy 各自边界
  - 明确 `freely init` 与 future settings mutation 在“用户拒绝/未完成授权”时必须提示的退化结果
  - 明确 Freely 何时可以调用工具官方非交互配置入口，何时只能输出手工步骤
- promotion_gate:
  - 不把 ACP、default autonomy、tool policy materialization 混写成一个模糊超级 owner
  - materialize 前先确认至少 `codex`、`cc/cc-use-codex-cli`、`iflow`、`kiro-cli` 四类工具的边界都有证据支撑
  - 不在 contract 未冻结前越权修改用户 home 级配置
- priority: `P1`
- open_questions:
  - 是否需要把 “project authorization bootstrap accepted” 单独落盘，而不是只复用 activation consent
  - Claude Code 是否存在足够稳定的 project-local settings path，可被 Freely 版本化管理
  - 对不支持 project-local config 的工具，Freely 是否应优先调用官方 CLI 子命令而非长期依赖 wrapper
  - UI/CLI 对后续授权变更是否需要增设显式 `authorize-tool` / `repair-tooling` 类入口
- decision_reason:
  - 当前缺口跨越产品治理、runtime、tool adapter 和 manual followthrough，已经超出单个已有 owner 的窄 followthrough 范围
  - 本地代码和测试已证明 Freely 具备“部分自动 materialization”能力，因此现在最需要的是边界合同，而不是再堆实现
  - 用户已明确要求这一步先充分研究，不急于直接编码 capability
- milestone: `M-20260326-freely-product-architecture`
- promoted_issue_path: `docs/B2-docs/config/packaging/issues/tool-authorization-bootstrap-and-post-consent-materialization-governance.md`
- promoted_issue_id: `I-20260405T123500Z-A`
- next_action: This candidate is now materialized as `I-20260405T123500Z-A`. Keep the owner documentation-first: freeze the authorization/bootstrap matrix, post-consent degradation semantics, CLI-first backend contract, and runtime refactor seam before opening narrower implementation follow-ons.
- revisit_trigger: 当 per-tool matrix 已稳定，或某个工具新增了可验证的 project-local config/trust surface，或 Freely 开始提供 UI/CLI 授权修改入口时。
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
