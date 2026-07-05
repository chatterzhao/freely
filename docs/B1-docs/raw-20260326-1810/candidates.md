# Candidates - 20260326-1810--freely-layered-architecture-and-tooling-topology

## Context
- Source brainstorm: ./brainstorms.md
- Status: promoted

## Candidates

### C-20260326-1810-A: legacy issue
- candidate_format_version: v2
- title: Freely layered architecture and tooling topology
- problem: Freely 现在缺少一份更上位的系统拓扑收敛。`three-loop-capability-lifecycle` 只适合表达 loop / route / lifecycle，不足以承担整栋系统拓扑；`tools.md` 虽然已经定义了 `codex`、`cc`、`cc-use-codex-cli` 等 external AI tooling contract，却还没有被放进一张稳定的层级图里；`cli-first-entrypoint-and-observability-surface-unification` 与 `backend-service-contract-and-adapter-taxonomy` 也分别冻结了 command family / status family / contract-vs-adapter 的局部边界，但尚未被一张总图统一吸收。这导致 `chat`、`status` family 与 `CLI shell / TUI shell / GUI app` 容易被错误并列，也导致 external AI tooling、service contract、adapter taxonomy 缺少清晰站位。
- why_now: 这是架构认知的上游问题。若不先收敛，后续 `three-loop`、`tools.md`、runtime/agent 文档和对外产品叙事都会继续混层。当前用户已经明确指出现有分层草图不成立，说明这不是可留到以后再慢慢补的细节问题。
- acceptance_criteria:
  - 候选明确首个正式产物应先回写 `PROJECT_INTENT / CONSTITUTION / LAWS`；`AGENTS.md` 只作为紧随其后的开发入口对齐，而不是并列架构真源
  - 候选明确冻结首轮文档职责分工：`PROJECT_INTENT` 讲高层拓扑，`CONSTITUTION` 讲硬边界，`LAWS` 讲判定与对齐，`AGENTS.md` 只讲开发入口思考顺序
  - 候选明确区分 loop/lifecycle 真源 与 更上位的 architecture/topology 真源
  - 候选明确区分 “Freely 自身产品架构收敛” 与 “未来可能独立抽象出的产品形态能力”，不得把前者直接当成后者
  - 候选明确把 command family、观测语义、host shell / form factor、external AI tooling layer、runtime/agent layer、service contract layer、adapter layer、autonomy evals / acceptance、evaluation harness 区分开
  - 候选明确 `codex cli`、`Claude Code` 等按当前 Freely 使用方式属于系统架构的哪一层
  - 候选明确 `chat` / `init` / `start` 是 command family，不与 `CLI shell / TUI shell / GUI app` 并列；`status` family 是 observability semantic，也不与这些 host shell 并列
  - 候选明确记录项目当前哪些真源已经部分表达这些边界，哪些地方仍缺统一总图
  - 候选明确给出后续落点：先改 `PROJECT_INTENT / CONSTITUTION / LAWS`，再判断 repo 其余文档需要怎样跟随对齐
- promotion_gate:
  - 已确认这不是单纯润色现有 mermaid 图，而是需要稳定新的层级语义
  - 已确认 `three-loop` 不应被强行扩成整套 architecture map
  - 已给出 `tools.md` 与新 topology 真源的关系，而不是忽略 AI tooling layer
  - 已确认这里至少需要“纵向分层 + 横向语义面”两种表达，而不是只画单轴楼层图
  - 已确认这轮讨论的是 Freely 自身产品/系统架构，不是 `docs/system/workspace/**` 能力目录扩写
  - 已确认即使未来值得泛化“产品形态方法”，也应另开独立 scope，不把 Freely 自己的壳组合直接泛化
  - 已确认 `AGENTS.md` 需要作为开发 Freely 的入口指引跟随对齐，但不替代核心架构真源
  - 已冻结 `PROJECT_INTENT / CONSTITUTION / LAWS / AGENTS.md` 的首轮职责分工
- open_questions:
  - 最终采用单轴楼层图加注释，还是直接采用两轴拓扑图
  - command family / observability semantic 与 host shell / form factor 应如何命名最稳
  - `PROJECT_INTENT / CONSTITUTION / LAWS / AGENTS.md` 之外，repo 对齐应覆盖到哪些局部 issue / epic / system 引用文档
  - “产品形态抽象方法”是否值得独立预研，而不是继续绑在当前 Freely 自身架构 scope 中
- acceptance_reviews:
  - reviewer: `codex`
    mode: `fresh-process candidate acceptance review`
    summary: `The boundary is now stable enough to materialize: this is Freely’s own product/system architecture convergence, the first formal outputs belong in PROJECT_INTENT/CONSTITUTION/LAWS with AGENTS.md aligned as development-entry guidance, and the scope explicitly excludes direct expansion into docs/system/** or automatic generalization into reusable capability.`
    verdict: `pass`
- acceptance_hint:
  - `chat` / `start` / `init` 不再和 `CLI shell`、`TUI shell`、`GUI app` 直接并列
  - `status` / `live-status` / `fleet-status` 也不再和 `CLI shell`、`TUI shell`、`GUI app` 直接并列
  - `codex cli` / `Claude Code` / MCP 组合路径要有明确架构层归属
  - `three-loop` 继续只讲 loop/lifecycle，而不是被迫承载全部分层
  - `backend contract` / `adapter taxonomy` 要纳入总图，而不是停留在 control-surface 局部 issue 中
  - eval 与 harness 至少要被显式区分，不再只靠口头解释
  - 首个正式产物先修改 `PROJECT_INTENT / CONSTITUTION / LAWS`，并同步更新 `AGENTS.md` 的开发入口思考顺序，之后再做 repo 对齐
  - Freely 自身的产品形态选择不得直接被写成通用能力；若要泛化，需另开独立 scope
- priority: P0
- status: promoted
- decision_reason: 问题边界、首轮文档职责分工与正式落点已经稳定，因此本候选已提升为独立 issue；后续只在 issue lifecycle 中继续做文档改写与 verification，不再停留在 pre-brainstorm。
- next_action: 按已冻结的职责分工回写 `PROJECT_INTENT / CONSTITUTION / LAWS / AGENTS.md`，并完成 milestone、issue 与 verification evidence 收口。若过程中持续出现“通用产品形态方法”需求，再单独判断是否新开预研。
- revisit_trigger: 若后续再次出现需要把 Freely 当前产品形态泛化成通用方法的需求，开新 pre-brainstorm，而不是回退本条已提升 issue。
- promoted_issue_path: `docs/B2-docs/config/packaging/issues/freely-layered-architecture-and-tooling-topology.md`
- legacy_id_mapping: I-20260326-1810  # 历史遗留的 issue id
- milestone: `docs/milestones.md#m-20260326-freely-product-architecture`
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
