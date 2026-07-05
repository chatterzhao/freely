---
owner_issue: I-20260514T103532Z-A
kind: verification
phase_state: completed
---

- issue_id: I-20260514T103532Z-A

# Pre-Test Results: Agent Handoff Protocol v2 Closeout

**Date**: 2026-05-15T17:49:19Z
**Branch**: test-pre-merge-20260515T1758Z-agent-handoff-protocol-v2
**Suite**: 77/77 passed

## Summary

| Metric | Value |
|--------|-------|
| Total Checks | 77 |
| Passed | 77 |
| Failed | 0 |
| Verdict | **PASS** — All pre-tests green |

## Detailed Results

| ✅ | **AI-1: column 'handoff_id' exists** |  |
| ✅ | **AI-1: column 'role' exists** |  |
| ✅ | **AI-1: column 'raw_key' exists** |  |
| ✅ | **AI-1: column 'worktree' exists** |  |
| ✅ | **AI-1: column 'branch' exists** |  |
| ✅ | **AI-1: column 'prompt_file' exists** |  |
| ✅ | **AI-1: column 'parent_handoff_id' exists** |  |
| ✅ | **AI-1: column 'previous_worker_handoff_id' exists** |  |
| ✅ | **AI-1: column 'intent_kind' exists** |  |
| ✅ | **AI-1: column 'status' exists** |  |
| ✅ | **AI-1: column 'exit_kind' exists** |  |
| ✅ | **AI-1: column 'reason' exists** |  |
| ✅ | **AI-1: column 'restart_point' exists** |  |
| ✅ | **AI-1: column 'next_action' exists** |  |
| ✅ | **AI-1: column 'completion_summary' exists** |  |
| ✅ | **AI-1: column 'evidence_paths' exists** |  |
| ✅ | **AI-1: column 'worker_prompts_csv' exists** |  |
| ✅ | **AI-1: column 'repair_target_role' exists** |  |
| ✅ | **AI-1: column 'repair_target_handoff_id' exists** |  |
| ✅ | **AI-1: column 'validation_errors_json' exists** |  |
| ✅ | **AI-1: column 'session_id' exists** |  |
| ✅ | **AI-1: column 'created_by' exists** |  |
| ✅ | **AI-1: column 'consumed_by' exists** |  |
| ✅ | **AI-1: column 'launched_at' exists** |  |
| ✅ | **AI-1: column 'last_activity_at' exists** |  |
| ✅ | **AI-1: column 'completed_at' exists** |  |
| ✅ | **AI-1: column 'created_at' exists** |  |
| ✅ | **AI-1: column 'updated_at' exists** |  |
| ✅ | **AI-1: total columns >= 25** | got 29 columns |
| ✅ | **AI-1: status CHECK includes 'consumed'** |  |
| ✅ | **AI-2a: delegate_workers parses successfully** | action=delegate_workers |
| ✅ | **AI-2b: worker_done parses successfully** | action=worker_done |
| ✅ | **AI-2c: missing required field triggers repair** | action=repair |
| ✅ | **AI-2d: invalid exit_kind triggers repair** | action=repair |
| ✅ | **AI-2e: no handoff block triggers repair** |  |
| ✅ | **AI-2f: resume_manager parses successfully** |  |
| ✅ | **AI-2g: stop_ai parses successfully** |  |
| ✅ | **AI-2h: worker_blocked parses successfully** |  |
| ✅ | **AI-2i: worker_handoff_needed parses successfully** |  |
| ✅ | **AI-3: delegate_workers JSON has no Runtime fields** | clean |
| ✅ | **AI-3: resume_manager JSON has no Runtime fields** | clean |
| ✅ | **AI-3: stop_ai JSON has no Runtime fields** | clean |
| ✅ | **AI-4: worker_done has all required fields** | all present |
| ✅ | **AI-4: worker_blocked has all required fields** | all present |
| ✅ | **AI-4: worker_handoff_needed has all required fields** | all present |
| ✅ | **AI-5: mark_stale affects 0 after consume** | affected=0 |
| ✅ | **AI-5: update from completed with expected=launched affects 0** | affected=0 |
| ✅ | **AI-6: 3 unconsumed workers before auto-consume** | count=3 |
| ✅ | **AI-6: auto-consume affected 3** | affected=3 |
| ✅ | **AI-6: all 3 now consumed** | consumed count=3 |
| ✅ | **AI-7: inactive worker marked stale (blocked)** | affected=1 |
| ✅ | **AI-7: status changed to blocked** | status=blocked |
| ✅ | **AI-7: exit_kind set to worker_blocked** |  |
| ✅ | **AI-7: reason mentions inactivity** |  |
| ✅ | **AI-8: repair created** |  |
| ✅ | **AI-8: repair_target_role=manager** | got=manager |
| ✅ | **AI-8: repair_target_handoff_id=target-123** | got=target-123 |
| ✅ | **AI-8: validation_errors_json is valid JSON array** | got=[{"field": "worker_prompts_csv", "error": "required for delegate_workers, got ''"}] |
| ✅ | **AI-8: exit_kind=resume_manager** | got=resume_manager |
| ✅ | **AI-8: status=pending** | got=pending |
| ✅ | **AI-8: validation_errors contains worker_prompts_csv error** |  |
| ✅ | **AI-9: has_active_worker_for_worktree(wt9) returns True** |  |
| ✅ | **AI-9: active_workers_for_worktree(wt9) returns 1 record** | count=1 |
| ✅ | **AI-9: has_active_worker_for_worktree(nonexistent) returns False** |  |
| ✅ | **AI-10: freely script references HANDOFF_INJECT** |  |
| ✅ | **AI-10: start-lead-agent delegates to freely runtime** | references freely runtime |
| ✅ | **AI-10: handoff.py has extract_handoff_block function** | function exists |
| ✅ | **AI-11a: manager parses delegate_workers** | action=delegate_workers |
| ✅ | **AI-11b: worker1 completes** | action=worker_done |
| ✅ | **AI-11c: worker2 completes** | action=worker_done |
| ✅ | **AI-11d: 1 manager record** | count=1 |
| ✅ | **AI-11e: 2 worker records** | count=2 |
| ✅ | **AI-11f: manager auto-completed** | status=completed |
| ✅ | **AI-11g: manager exit_kind=delegate_workers** |  |
| ✅ | **AI-11h: worker 20260515 raw_key=test-ai11** |  |
| ✅ | **AI-11h: worker 20260515 raw_key=test-ai11** |  |
| ✅ | **AI-11i: no workers consumed yet (no auto-consume called)** |  |


## Coverage

| Area | Items | Status |
|------|-------|--------|
| Schema | AI-1 | ✅ |
| JSON Parse | AI-2a–AI-2i | ✅ |
| Manager JSON spec | AI-3 | ✅ |
| Worker JSON spec | AI-4 | ✅ |
| Optimistic locking | AI-5 | ✅ |
| Auto-consume | AI-6 | ✅ |
| Inactivity detection | AI-7 | ✅ |
| Structured repair | AI-8 | ✅ |
| Scan filtering | AI-9 | ✅ |
| HANDOFF_INJECT fork-only | AI-10 | ✅ |
| E2E regression | AI-11a–AI-11i | ✅ |

## Implementation Decision Note

- **decision**: 将 handoff protocol v2 合并到 develop
- **why_this**: 全部 11 项验收标准 (AI-1 至 AI-11) 通过，77/77 检查点全部绿色，验证了 schema 结构、JSON 解析、管理/Worker 输出规范、乐观锁、auto-consume、不活跃检测、结构化修复、scan 过滤、HANDOFF_INJECT fork-only 注入和端到端回归
- **alternatives_considered**: 无 — 本次 closeout 不涉及架构重新决策，仅执行预测试验收
- **boundary_non_goals**: 不修改 ACP bridge、fleet supervision、wt-close 生命周期，不与 GitHub Actions 或 #343 的 ACP 修复耦合
- **residual_risk**: 低 — #343 的四个 bug 在新协议下不复存在，全流程 delegate_workers → worker_done → manager 消费已通过 AI-11 端到端回归验证

## Evidence

- Test database: `/var/folders/4y/s0ffqqjx6y392zmmp6rpm5_c0000gn/T/tmprfwsv0vh.db` (cleaned up after closeout)
- Test script: `/tmp/handoff_pre_tests.py`
- All test definitions from `docs/B2-docs/agent-handoff-protocol/verification/pre-tests.md`
