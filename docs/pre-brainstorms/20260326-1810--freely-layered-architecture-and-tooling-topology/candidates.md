# Candidates - 20260326-1810--freely-layered-architecture-and-tooling-topology

## Context
- Source brainstorm: ./brainstorms.md
- Status: candidate

## Candidates

### C-20260326-1810-A
- candidate_format_version: v2
- title: Freely layered architecture and tooling topology
- problem: Freely 现在缺少一份更上位的系统分层真源。`three-loop-capability-lifecycle` 只适合表达 loop / route / lifecycle，不足以承担整栋系统拓扑；而 `tools.md` 虽然已经定义了 `codex`、`cc`、`cc-use-codex-cli` 等 AI tooling contract，却还没有被放进一张稳定的层级图里。这导致 `chat` 与 `CLI/TUI/GUI` 容易被错误并列，也导致外部 AI tool orchestration layer 缺少清晰站位。
- why_now: 这是架构认知的上游问题。若不先收敛，后续 `three-loop`、`tools.md`、runtime/agent 文档和对外产品叙事都会继续混层。当前用户已经明确指出现有分层草图不成立，说明这不是可留到以后再慢慢补的细节问题。
- acceptance_criteria:
  - 候选明确区分 loop/lifecycle 真源 与 更上位的 architecture/topology 真源
  - 候选明确把交互入口、产品表面载体、外部 AI tooling layer、runtime/agent layer、eval/harness layer 区分开
  - 候选明确 `codex cli`、`Claude Code` 等按当前 Freely 使用方式属于系统架构的哪一层
  - 候选明确给出后续落点：是新增 topology 文档、修改 `three-loop`、还是两者结合
- promotion_gate:
  - 已确认这不是单纯润色现有 mermaid 图，而是需要稳定新的层级语义
  - 已确认 `three-loop` 不应被强行扩成整套 architecture map
  - 已给出 `tools.md` 与新 topology 真源的关系，而不是忽略 AI tooling layer
- open_questions:
  - 新文档应放在 `docs/system/workspace/` 还是更上位的 `docs/system/architecture/`
  - interaction entry layer 与 product surface / host form factor 应如何命名最稳
- acceptance_reviews:
  - reviewer: `codex`
    mode: `fresh-process candidate acceptance review`
    summary: `The problem boundary is stable enough for pre-brainstorm: Freely needs a higher-level topology truth source above three-loop, and the user’s corrections make it clear that tool orchestration and interaction entry layering must be first-class parts of that topology. The remaining work is deciding naming and document landing zones, not whether the problem exists.`
    verdict: `needs_more_research`
- acceptance_hint:
  - `chat` / `start` / `init` 不再和 `CLI/TUI/GUI` 直接并列
  - `codex cli` / `Claude Code` / MCP 组合路径要有明确架构层归属
  - `three-loop` 继续只讲 loop/lifecycle，而不是被迫承载全部分层
  - eval 与 harness 至少要被显式区分，不再只靠口头解释
- priority: P0
- status: needs_research
- decision_reason: 问题已经明确，但具体层命名、文档落点、以及是否把 interaction entry 与 product surface 分成两层还需要再收敛，先保持 pre-brainstorm。
- next_action: 继续 pre-brainstorm，对现有 `three-loop-capability-lifecycle`、`tools.md`、front-door/runtime/status 真源做对照，收敛出最小楼层图与文档落点，然后再决定是否 materialize。
- revisit_trigger: 当分层命名、AI tooling 归属、interaction entry 与 host form factor 的边界，以及新旧文档分工都能冻结成独立 issue scope 时，重新进入 materialization 判断。
- promoted_issue_path: `pending://freely-layered-architecture-and-tooling-topology-materialization`
- milestone: `docs/milestones.md#m-20260306-workspace-routing-foundation`
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
