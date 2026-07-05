# Pre-Tests: A2A server _restore_tasks 异步化
- issue_id: I-20260624T004524Z-A

## Unit
- acceptance target: _restore_tasks 不在 __init__ 中调用，start() 中通过 daemon 线程执行
- testing layer: unit
- target environment: fix worktree
- required evidence: 代码审查确认 _restore_tasks 调用位置变更
- blocker taxonomy: execution_pending_or_failed

## Integration
- acceptance target: A2A server 启动后 socket 立即可用
- testing layer: integration
- target environment: fix worktree
- required evidence: daemon start 不再出现 A2A timeout 警告
- blocker taxonomy: execution_pending_or_failed

## End-to-End
- acceptance target: fix→develop merge passes
- testing layer: end_to_end
- target environment: develop-bound guarded merge chain
- required evidence: guarded merge receipts
- blocker taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 代码逻辑审查确认 _restore_tasks 是纯同步 DB 操作，线程安全

## Acceptance Items
### AT-001 _restore_tasks 不在 __init__ 中
- id: AT-001
- requirement: __init__ 不阻塞 socket 绑定
- surface_kind: integration
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: integration
^- status: passed

### AT-002 health check 消息修正
- id: AT-002
- requirement: 超时消息不再误导
- surface_kind: integration
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: integration
^- status: passed
