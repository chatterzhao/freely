# Candidates - 20260405-1000--cli-output-conciseness-and-token-efficiency

## Context
- Source brainstorm: ./brainstorms.md
- Status: resolved

## Candidates

### C-20260405-cli-output-style

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
- acceptance_reviews: []
- priority: P2
- status: dropped
- milestone: `M-20260326-freely-product-architecture`
- decision_reason: 本轮决定把产物收敛为 `AGENTS.md` 中的开发入口回复风格实验，只约束开发 Freely 过程中的人类可读输出；暂不把它继续推进为 Freely 能力或独立 issue。
- promoted_issue_path: `pending://issue-materialization`
- next_action: 保持 `AGENTS.md` 中的精炼白话文实验约束，观察其是否足以改善开发过程中的 CLI 输出质量；当前不进入 issue materialization。
- revisit_trigger: 当这条实验被证明不足、需要进入更高优先级真源，或需要作为 Freely 对外能力长期消费时重新唤起
- session_refs:
  - tool: iflow
    session_id: current
    jsonl_path: unavailable://session-in-progress
    role: worker
