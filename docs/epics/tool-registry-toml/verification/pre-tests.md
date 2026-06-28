# Pre-Tests: tool-registry TOML 配置驱动（Phase 1+2）
- issue_id: I-20260624T013737Z-A

## Unit
- acceptance target: TOML registry 文件 schema 正确，query tool 可读取所有字段
- testing layer: unit
- target environment: feature worktree
- required evidence: `_tool_registry_get claude config_schema.fields.permission_bypass.path` → "permissionMode"
- blocker taxonomy: execution_pending_or_failed

## Integration
- acceptance target: monitor-ai-acp.sh + tool-launchers.sh 权限读取改为 registry 驱动
- testing layer: integration
- target environment: feature worktree
- required evidence: daemon start 不再硬编码 permissionMode/approval_policy
- blocker taxonomy: execution_pending_or_failed

## End-to-End
- acceptance target: feature→develop merge passes
- testing layer: end_to_end
- target environment: develop-bound guarded merge chain
- required evidence: guarded merge receipts
- blocker taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pending
- real_environment_reason: 需要 daemon start 验证 ACP bridge 权限读取正常

## Acceptance Items
### AT-001 TOML registry 可查询
- id: AT-001
- requirement: tool-registry.toml 存在，query tool 支持 TOML + 合并
- surface_kind: integration
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: integration
- status: pass

### AT-002 权限字段不再硬编码
- id: AT-002
- requirement: monitor-ai-acp.sh 用 config_schema 替代硬编码 permissionMode
- surface_kind: integration
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: integration
- status: pass

### AT-003 向后兼容
- id: AT-003
- requirement: deploy-skills（已改为 registry 驱动）在 TOML 下继续工作
- surface_kind: integration
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: integration
- status: pass
