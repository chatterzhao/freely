# Candidates - 20260326-1810--freely-layered-architecture-and-tooling-topology

## Context
- Source brainstorm: ./brainstorms.md
- Status: candidate

## Candidates

### C-20260326-1810-A
- candidate_format_version: v2
- title: Freely layered architecture and tooling topology
- problem: Freely 现在缺少一份更上位的系统拓扑真源。`three-loop-capability-lifecycle` 只适合表达 loop / route / lifecycle，不足以承担整栋系统拓扑；`tools.md` 虽然已经定义了 `codex`、`cc`、`cc-use-codex-cli` 等 AI tooling contract，却还没有被放进一张稳定的层级图里；`cli-first-entrypoint-and-observability-surface-unification` 与 `backend-service-contract-and-adapter-taxonomy` 也分别冻结了 front-door / status family / contract-vs-adapter 的局部边界，但尚未被一张总图统一吸收。这导致 `chat`、`status` family 与 `CLI/TUI/GUI` 容易被错误并列，也导致 external AI tooling、backend contract、adapter taxonomy 缺少清晰站位。
- why_now: 这是架构认知的上游问题。若不先收敛，后续 `three-loop`、`tools.md`、runtime/agent 文档和对外产品叙事都会继续混层。当前用户已经明确指出现有分层草图不成立，说明这不是可留到以后再慢慢补的细节问题。
- acceptance_criteria:
  - 候选明确区分 loop/lifecycle 真源 与 更上位的 architecture/topology 真源
  - 候选明确把交互语义、观测语义、产品宿主壳、外部 AI tooling layer、runtime/agent layer、backend contract/adapter layer、eval/harness layer 区分开
  - 候选明确 `codex cli`、`Claude Code` 等按当前 Freely 使用方式属于系统架构的哪一层
  - 候选明确 `chat` / `init` / `start` 与 `status` family 不是 `CLI/TUI/GUI` 的 peer，而是通过 host shell 暴露的 semantic surface
  - 候选明确记录项目当前哪些真源已经部分表达这些边界，哪些地方仍缺统一总图
  - 候选明确给出后续落点：是新增 topology 文档、修改 `three-loop`、还是两者结合
- promotion_gate:
  - 已确认这不是单纯润色现有 mermaid 图，而是需要稳定新的层级语义
  - 已确认 `three-loop` 不应被强行扩成整套 architecture map
  - 已给出 `tools.md` 与新 topology 真源的关系，而不是忽略 AI tooling layer
  - 已确认这里至少需要“纵向分层 + 横向语义面”两种表达，而不是只画单轴楼层图
- open_questions:
  - 新文档应放在 `docs/system/workspace/` 还是更上位的 `docs/system/architecture/`
  - 最终采用单轴楼层图加注释，还是直接采用两轴拓扑图
  - interaction / observability semantic 与 host shell / form factor 应如何命名最稳
- acceptance_reviews:
  - reviewer: `codex`
    mode: `fresh-process candidate acceptance review`
    summary: `The problem boundary is stable enough for pre-brainstorm: Freely needs a higher-level topology truth source above three-loop, and the user’s corrections plus existing repo evidence show that the missing abstraction is not only “more layers” but also “semantic surfaces versus host shells”. The remaining work is freezing the naming, deciding whether the final artifact is a single-axis or two-axis diagram, and choosing the canonical landing zone.`
    verdict: `needs_more_research`
- acceptance_hint:
  - `chat` / `start` / `init` 不再和 `CLI/TUI/GUI` 直接并列
  - `status` / `live-status` / `fleet-status` 也不再和 `CLI/TUI/GUI` 直接并列
  - `codex cli` / `Claude Code` / MCP 组合路径要有明确架构层归属
  - `three-loop` 继续只讲 loop/lifecycle，而不是被迫承载全部分层
  - `backend contract` / `adapter taxonomy` 要纳入总图，而不是停留在 control-surface 局部 issue 中
  - eval 与 harness 至少要被显式区分，不再只靠口头解释
- priority: P0
- status: needs_research
- decision_reason: 问题已经明确，而且项目里已有足够多局部正确真源可以证明总图缺口真实存在；但具体层命名、最终图形表达、以及 semantic surface 与 host shell 的正式术语还需要再收敛，先保持 pre-brainstorm。
- next_action: 继续 pre-brainstorm，把现有 `three-loop-capability-lifecycle`、`tools.md`、`cli-first-entrypoint-and-observability-surface-unification`、`backend-service-contract-and-adapter-taxonomy` 统一映射成一张最小拓扑草图，并明确项目当前已有实现/文档偏差点，再决定是否 materialize。
- revisit_trigger: 当最小拓扑草图、文档落点、语义面命名、以及各既有真源的引用关系都能冻结成独立 issue scope 时，重新进入 materialization 判断。
- promoted_issue_path: `pending://freely-layered-architecture-and-tooling-topology-materialization`
- milestone: `docs/milestones.md#m-20260306-workspace-routing-foundation`
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
