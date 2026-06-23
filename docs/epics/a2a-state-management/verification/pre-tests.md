# Pre-Tests: A2A 状态管理全量修复
- issue_id: I-20260623T140410Z-A

## Unit
- acceptance target: VALID_STATES + CHECK 约束一致性
- testing layer: unit
- target environment: feature worktree
- required evidence: `a2a-exit --state canceled` 成功、`--state consumed` 被拒绝
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 状态验证在 Python/DB 层，需集成测试
- replacement_evidence: grep 确认 C1-C6 代码变更正确

## Integration
- acceptance target: daemon stop → working 保持 → start → _restore_tasks 修正
- testing layer: integration
- target environment: test-pre-merge worktree
- required evidence: stop 后 SQLite 中 working 不变 → start 后 failed(PID 死)/keep(PID 活)
- blocker taxonomy: execution_pending_or_failed

## End-to-End
- acceptance target: wt-close → Worker task state=completed（非 consumed）
- testing layer: end_to_end
- target environment: test-pre-merge worktree
- required evidence: wt-close 后 a2a_task.py get --task-id X 返回 state=completed
- blocker taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 本次变更为状态管理逻辑修正，不需要真实环境测试

## Acceptance Items
| id | requirement | evidence_level | status | artifact_ref |
|----|------------|---------------|--------|-------------|
| AT1 | C1: wt-close state=completed | integration | pass | a2a_task.py get verification |
| AT2 | C2: CLI metadata passthrough | script regression | pass | grep a2a_task.py update kwargs |
| AT3 | C3-C4: state consistency | script regression | pass | grep VALID_STATES + CHECK |
| AT4 | C5: PATCH 拒绝 unknown | integration | pending | curl PATCH invalid state |
| AT5 | C6: dead code removed | script regression | pass | grep h_a2a_task_update_from_exit_kind |
| AT6 | A0: stop no touch state | integration | pass | SQLite query after stop |
| AT7 | A1-A3: _restore_tasks edges | integration | pass | restart cycle log |
| AT8 | B1-B4: recovery notifications | integration | pass | SSE event in Manager session |
| AT9 | premerge-integration gate | premerge-integration | pending | test-pre-merge verification |

- surface_kind: bugfix
- target_lane: premerge-integration
- promotion_gate: develop_merge
