# Candidates - 20260405-1000--cli-output-conciseness-and-token-efficiency

## Context
- Source brainstorm: ./brainstorms.md
- Status: resolved

## Candidates

### C-20260405T100000Z-A: legacy issue

- candidate_format_version: v2
- title: CLI Output Style Optimization
- problem: CLI 界面回复给人看的部分，是否可以通过风格约束来节省 token？文言文是否真的省 token？是否有更实用的精炼风格？
- why_now: 用户观察到网上有人说使用文言文可以省 token，特别是终端界面的陈述过程。这个假设需要验证，并确定是否应落地到 AGENTS.md。
- acceptance_criteria:
  - 确定 token 效率最优的风格约束
  - 确定约束范围（仅 CLI 或全场景）
  - 不牺牲编程任务的精确性
  - 用户接受度可接受
- promotion_gate:
  - Token 效率假设已验证（或决定不需要验证）
  - 用户接受度已评估
  - 约束文案已确定
- open_questions:
  - 文言文 vs 精炼白话文，哪种更省 token？
  - 约束范围如何界定？
  - 用户是否接受文言文风格？
  - 如何落地到 AGENTS.md？
- acceptance_reviews:
  - reviewer: `codex-self-review`
    verdict: `supports`
    note: 当前范围已被明确收窄为 `AGENTS.md` 开发入口实验；为了合法 merge 到 `develop`，以 narrow owner materialize 是更稳的路径，但这不等于 capability promotion。
- priority: P2
- status: promoted
- milestone: `M-20260326-freely-product-architecture`
- decision_reason: 本轮仍把产物限定为 `AGENTS.md` 中的开发入口回复风格实验，不把它升级成新的 Freely 能力；但讨论同时确认了一条既有能力真相：Freely 已会为项目生成最小 `AGENTS.md` 并优先读取它。为了合法 merge 到 `develop`，需要以一个 narrow issue owner 承接 `AGENTS.md`、pre-brainstorm、milestone writeback 与这条项目级入口事实的文档对齐。
- promoted_issue_id: `I-20260405-cli-output-style-A`
- promoted_issue_path: `docs/B2-docs/config/packaging/issues/agents-cli-output-style-experiment-governance.md`
- next_action: 以 narrow owner `I-20260405-cli-output-style-A` 完成 `AGENTS.md` 实验与“项目级 AGENTS 先生成再读取”的现有能力事实的 issue/progress/review writeback，并 replay 到 `develop`。
- revisit_trigger: 当这条实验被证明不足、需要进入更高优先级真源，或需要作为 Freely 对外能力长期消费时重新唤起
- session_refs:
  - tool: iflow
    session_id: current
    jsonl_path: unavailable://session-in-progress
    role: worker
