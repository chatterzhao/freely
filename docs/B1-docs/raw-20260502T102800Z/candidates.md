# Candidates - 20260502-1028--stale-start-lock-cleanup

### C-20260502T102800Z-A: legacy issue

- title: `Clean stale start lock before daemon stop`
- status: `promoted`
- scope: 清理 force-kill 残留的 project-start.lock，确保 daemon stop 不被死锁阻塞
- priority: `P0`
- type: `fix`
- milestone: `M-20260306-workspace-routing-foundation`
- route_kind: `hotfix`
- phase_state: `done_pre_brainstorm`
- promoted_issue_path: `docs/B2-docs/runtime/stale-start-lock-cleanup/issues/I-20260502T102800Z-A.md`
- session_refs:
  - {tool: ccds, session_id: "20260502-stale-lock", jsonl_path: "unavailable://manual", role: "author"}
- acceptance_criteria:
  - daemon stop 前自动清理 stale project-start.lock
  - force-kill 后 daemon stop 不阻塞
- promotion_gate: `runtime-daemon-test`
- open_questions: []
- acceptance_reviews:
  - reviewer: `human`
  - status: `accepted`
- next_action: `Merge to develop, then release to main.`
