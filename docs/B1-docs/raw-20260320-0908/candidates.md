# Candidates - 20260320-0908--research-candidate-persistence-governance

## Context
- Source brainstorm: `./brainstorms.md`
- Status: active

## Candidates

### C-20260320-0908-A: legacy issue
- title: 未收口研究项的持续可见性与重启条件治理
- problem: Freely 现在已经会记录 candidate，但对“本轮还不能收口的研究项”缺少强制可见性规则，导致主管扫描容易只盯活跃实现，忽略已经识别但尚未闭环的能力缺口。
- why_now: 当前正在逐个 worktree 清查预研和未合并能力；如果不把 unresolved research 的挂起/重启规则补上，后续还是会重复出现“知道它存在，但扫描时被跳过”的情况。
- acceptance_hint: `three-loop`、`doc-pre-brainstorm`、`docs/milestones.md` 和首跳 prompt 必须共同要求 unresolved candidate 保持在可扫描队列中，并写清 `next_action` 与 `revisit_trigger`。
- priority: P0
- status: needs_research
- decision_reason: 方向已经明确，但还需要验证最小治理是否只靠文档/提示词/测试就够，还是后续要 materialize 为更强的 issue-bound control-plane。
- next_action: unresolved candidate persistence 规则已写入 lifecycle、skill reference、lead prompt、milestone policy 与 prompt test；下一步观察是否还需要 materialize 为独立治理 issue，并继续补 queue-level `revisit_trigger` 一致性。
- revisit_trigger: 下一轮 worktree 审查再次发现“已研究但本轮未推进”的能力项无法在 `candidate_issues` 或 issue-bound artifact 中被看到。
- promoted_issue_path: pending://issue-materialization
- milestone: M-20260320-0908-A
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
