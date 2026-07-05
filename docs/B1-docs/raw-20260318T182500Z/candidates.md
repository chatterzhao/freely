# Candidate Issues

### C-20260318T182500Z-A: legacy issue
- status: promoted
- legacy_id_mapping: I-20260318T182500Z
- Title: worktree hygiene supervision control plane
- Problem: Freely 缺少针对 dirty-budget / checkpoint drift 的自治监督控制面，manager 只能观察，不能稳定推动 worker 收口。
- Expected outcome: 明确 manager/worker/runtime/hook 的 hygiene 分工，并新增可执行能力与测试。
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260318T182500Z-A/issue.md
- milestone: M-20260318T182500Z-A
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}]

## Candidate B
- Title: dedicated hygiene worker delegation flow
- Problem: 项目级 dirty/checkpoint 问题没有清晰的 delegated owner，导致 worker 在实现中越滚越脏。
- Expected outcome: manager 能在合适时委派 hygiene worker，对指定 worktree 做 review/checkpoint/cleanup 收口。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []
