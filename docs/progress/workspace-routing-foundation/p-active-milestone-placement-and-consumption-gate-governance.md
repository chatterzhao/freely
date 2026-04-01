# Progress: active-milestone-placement-and-consumption-gate-governance

- issue_id: `I-20260331-2012-A`
- title: Active milestone placement and consumption gate governance
- phase_state: `completed`
- runtime_state: `stopped`
- branch: `feature/milestone-placement-merge-gate-followup-20260331`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260331-feature-milestone-placement-merge-gate-followup`
- issue_path: `docs/epics/workspace-routing-foundation/active-milestone-placement-and-consumption-gate-governance/issues/active-milestone-placement-and-consumption-gate-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "dev-loop-closeout"}

## Summary

- 这条 owner 已把 active milestone placement correctness 从隐含习惯提升为显式 gate：
  - `governance-check` 与 `governance-merge-gate` 现在都会拦 active candidate 的 `unassigned` / `pending://...`、错误 milestone、completed milestone unresolved placement，以及 promoted 但未 materialize 的假承接
  - `LAWS`、pre-brainstorm skill、milestone-planning skill 与 manager patrol guidance 已统一写明 `needs_research` 的 keep / cautious rehome / dropped 合同
  - 当前 backlog 中暴露出的 candidate placement drift 已一并对齐回 active milestone
- 当前批次已通过 focused tests 与 `./bin/governance-check`，保持 `in_verification`，等待 manager merge review / canonical absorption；如果后续要继续做更强的 milestone 排期或自动迁移，应另开 lifecycle。
- post-merge replay 又暴露一个窄 follow-up：`governance-merge-gate` 仍把 unresolved candidate 的 milestone metadata 修正误判成“必须同批携带该 candidate 自己的 I-* owner”。本 follow-up 收窄为两件事：
  - 允许 unresolved `proposed|needs_research|blocked` candidate 在已有治理 owner 的 develop merge 中一起修 placement metadata
  - 把 develop 中仍残留的 `C-20260330-2318-A`、`C-20260331-1837-A`、`C-20260331-1840-A` milestone 绑定补回 active milestone
- 当前分支继续承接这条 post-merge replay：第二阶段 develop absorption 会把 candidate binding writeback 与本 owner 的 issue/progress evidence 一起带入 merge diff，避免再次退化成 candidate-only develop merge。
- 第二阶段 replay 还补了一个同 scope 的 gate 归类修正：`docs/system/workspace/agents/**`、`skills/**`、`scripts/quality/**` 与 `test-governance-*` 属于 governance-only path，不应被 capability-phase 限制误判成产品实现改动。

- closure_status: `merged-and-verified`
- closure_evidence:
  - `merge_commits: 79f8bba, b279330, 8972f7c`
  - `tests: bash docs/system/workspace/scripts/tests/test-governance-check-candidate-v2 && bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
  - `governance: ./bin/governance-check`
  - `review: docs/epics/workspace-routing-foundation/active-milestone-placement-and-consumption-gate-governance/code-reviews/20260331-active-milestone-placement-gate-verification.md`
