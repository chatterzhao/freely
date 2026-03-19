# Candidates

## Candidate A
- Title: Watchdog umbrella term and sub-control-plane taxonomy
- Problem: `watchdog` 目前在 Freely 中同时指代“账号切换器”和“外层监督恢复控制面”，命名覆盖面与实现边界不稳定。
- Expected outcome: 正式把 `watchdog` 定义为 umbrella term，并拆清 `availability / runtime / continuity watchdog` 三类 owner、职责与非职责。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}]

## Candidate B
- Title: Skill-first watchdog capability extraction
- Problem: 账号探测、切号、等待恢复等可复用逻辑容易继续堆进 `runtime/freely`，导致 Freely 内部和未来独立全局脚本无法共享同一真源。
- Expected outcome: 明确哪些 watchdog 脚本和策略应下沉到 skill，哪些 Freely 专有 orchestration 应保留在 `runtime/freely`。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}]

## Candidate C
- Title: Historical watchdog productization worktree retirement handoff
- Problem: `feature/independent-ai-watchdog-productization-20260318` 的实现主线已进入 `develop`，但其独有治理结论仍未正式承接，不能直接退休。
- Expected outcome: 形成明确 disposition：`materialize_then_retire`，并记录 handoff target、retirement precondition 和 cleanup 留痕要求。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}]
