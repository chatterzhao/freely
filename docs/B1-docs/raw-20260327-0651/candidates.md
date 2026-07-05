# Candidates - 20260327-0651--pretests-gate-and-network-proxy-config

## Context
- Source brainstorm: ./brainstorms.md
- Status: candidate

## Candidates

### C-20260327-0651-A: legacy issue
- candidate_format_version: v2
- title: Materialize issue-bound pre-tests evidence gate and retirement enforcement
- problem: 现有 Freely 真源已经要求 `pre-tests.md` 具备质量线与真实环境验收面，但 closeout、merge、worktree retirement 仍没有稳定消费这些定义。系统知道“应该测”，却还不知道“当前 issue 的哪些 acceptance 已经由哪类证据满足”，所以 `pre-tests.md` 仍可能沦为摆设。
- why_now: OAuth sweep 真实环境 dogfood 已经证明 mock/integration 不能替代全部验收，而且当前 closeout 流程仍可能在没有 real-env artifact 的情况下被误判完成。这已不是单条 issue aftercare，而是 completion contract 缺少 machine-readable binding。
- acceptance_criteria:
  - 候选明确 issue 与自身 `pre-tests.md` 的单一绑定关系，不依赖全仓扫描
  - 候选明确 gate 至少覆盖 `phase_state=completed` 与 worktree retirement 两个关键出口
  - 候选明确 acceptance item 需要 machine-readable 字段与 artifact 落点，能区分 `mock`、`integration`、`real_env`、`post_merge_dogfood`
  - 候选明确未满足所需 evidence level 时，系统必须拒绝 completion / retirement
- promotion_gate:
  - 已确认这不是 `story-level-pre-tests-quality-gate-governance` 的简单 wording continuation，而是 machine-readable enforcement follow-on
  - 已确认本条能力可以落到 Freely runtime / hooks / retirement gate，而不是停留在 IBM 描述层
  - 已确认不会要求 gate 去扫描全仓；路径以当前 issue owner 为入口
- open_questions:
  - machine-readable acceptance item 应继续嵌在 `pre-tests.md`，还是引出独立 verification manifest
  - 最小强制入口是 git hook、runtime gate，还是两者并存
- acceptance_reviews:
  - reviewer: `codex`
    mode: `initial candidate acceptance review`
    summary: `The gap is no longer about wording quality alone. Freely needs an issue-bound evidence gate so completion and retirement can reject missing real-env proof without scanning the whole repo.`
    verdict: `ready_for_pre_brainstorm`
- priority: P0
- status: `promoted`
- decision_reason: 问题已 materialize 为 dedicated follow-on issue `I-20260327-0701`，实现聚焦第一阶段 completed gate，由 standalone `pretests-gate` 与 `pre-commit` 共享同一 verdict。
- next_action: 继续把这条 gate 合入 `develop`，然后由 closeout lane 把 issue 从 `in_verification` 推到 `completed`，再让其他 active worktree 吸收新的 completed gate 后进入 closeout。
- revisit_trigger: 当 merged worktree cleanup / retirement 仍可能绕过 issue-bound acceptance evidence 时，再以 follow-on 扩到 retirement gate。
- promoted_issue_id: `I-20260327-0701`
- promoted_issue_path: `docs/B2-docs/ibm/pre-tests-evidence-binding-and-completion-gate-governance/issues/pre-tests-evidence-binding-and-completion-gate-governance.md`
- legacy_id_mapping: I-20260327-0701  # 历史遗留的 issue id
- milestone: `M-20260306-workspace-routing-foundation`
- session_refs:
  - tool: codex
    session_id: current-thread
    jsonl_path: unavailable://codex-thread-only
    role: author

### C-20260327-0651-A: legacy issue
- candidate_format_version: v2
- title: Add project-scoped network proxy configuration for Freely runtime and tooling
- problem: 现在 Freely 的网络出口没有统一能力面。`codex exec` 路径在 watchdog 里仍写死 `127.0.0.1:7890`，而 `curl`/OAuth sweep 等路径又靠环境继承，导致真实环境下不同工具看到不同代理语义，前端未来也无从配置统一网络策略。
- why_now: OAuth sweep 刚成为 canonical inventory path 候选，真实环境已经证明网络配置不是边角问题。若继续让 `codex`、`curl`、watchdog 各自处理代理，后续 status/switch/manager 都会带着不一致的网络行为前进。
- acceptance_criteria:
  - 候选明确项目级代理配置真源应落在 Freely 可管理配置面，而不是脚本硬编码
  - 候选明确同一 resolver 要服务 `codex exec`、`curl`、watchdog、status、switch 与 future tooling launcher
  - 候选明确支持 `inherit`、`explicit`、`disabled` 等策略，而不强绑某个地址或端口
  - 候选明确未来前端可通过编辑 Freely 配置来驱动网络策略，无需知道脚本内部细节
- promotion_gate:
  - 已确认这是 Freely 产品能力，不是单条 OAuth issue 的临时实现补丁
  - 已确认 `.freely/config.env` 已是项目级 runtime 配置真源，可作为最小落点
  - 已确认默认方向是不在代码里继续硬编码代理地址
- open_questions:
  - 是否继续使用 `.freely/config.env` 作为唯一用户编辑面，还是增加结构化网络配置文件
  - 非 Codex tooling 的网络策略是否需要允许工具级覆盖，还是先冻结项目级全局策略
- acceptance_reviews:
  - reviewer: `codex`
    mode: `initial candidate acceptance review`
    summary: `This is a Freely product capability, not an OAuth one-off patch. Project-scoped proxy resolution should be centralized before more launchers and frontend surfaces depend on divergent env behavior.`
    verdict: `ready_for_pre_brainstorm`
- priority: P0
- status: `promoted`
- decision_reason: 问题已 materialize 为 dedicated follow-on issue `I-20260327-0651`，当前 lane 负责 shared resolver、launcher inheritance、OAuth inheritance 与 project-scoped config defaults。
- next_action: 继续在当前 lane 完成 closeout evidence、吸收新的 completed gate，并在验证后合入 `develop`。
- revisit_trigger: 当前端配置面或非 Codex tooling 需要更细粒度覆盖时，再扩展更结构化的 proxy config surface。
- promoted_issue_id: `I-20260327-0651`
- promoted_issue_path: `docs/B2-docs/ibm/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance/issues/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance.md`
- legacy_id_mapping: I-20260327-0651  # 历史遗留的 issue id
- milestone: `M-20260306-workspace-routing-foundation`
- session_refs:
  - tool: codex
    session_id: current-thread
    jsonl_path: unavailable://codex-thread-only
    role: author
