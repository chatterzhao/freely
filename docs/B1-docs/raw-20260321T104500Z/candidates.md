# Candidates

- id: C-20260321T104500Z-001
  title: Extend `worktree-maintenance-governance` with stacked merge-chain and merge-prep gates
  status: promoted
  why_now:
    - 当前实际 dogfooding 已经证明，复杂 worktree 不是“单棵树 ready 就 merge”，而是需要 `child -> parent -> merge-prep-from-develop -> develop` 的逐层治理。
    - 这类规则目前还在人工经验里，没有沉淀成 Freely 可复用的 skill 能力。
  promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260321T104500Z-A/issue.md
  legacy_id_mapping: I-20260321T104500Z  # 历史遗留的 issue id
  milestone: M-20260321T104500Z-A
  session_refs:
    - tool: cc-use-codex-cli
      session_id: 11111111-2222-4333-8444-555555555555
      jsonl_path: /Users/zhaoyu/.claude/projects/-private-tmp-freely-cc-codex-real-ed64yw-project/11111111-2222-4333-8444-555555555555.jsonl
      role: integration-smoke
    - tool: codex-cli
      session_id: 019d0f86-7c2e-7f50-999f-10cf4935e7ba
      jsonl_path: /Users/zhaoyu/.codex/sessions/2026/03/21/rollout-2026-03-21T01-27-02-019d0f86-7c2e-7f50-999f-10cf4935e7ba.jsonl
      role: integration-smoke
  acceptance_hint:
    - `skill:worktree-maintenance-governance` 新增 stacked merge-chain 规则或模式
    - skill 必须能显式识别 parent branch、上游 integration target 与 merge-prep necessity
    - skill 必须把 parent dirty / uncommitted changes 视为上游 gate，而不是只审当前 child
    - skill 必须能把 merge-prep 新发现的问题归因到 develop integration，而不是误判为 child branch 未完成
    - 最终输出必须是逐层 checklist，而不是一句笼统的 merge-ready / not-ready
