# Pre-Tests: deploy-skills 默认部署到全部已安装 tool

- issue_id: I-20260624T004510Z-A

## Unit
- acceptance target: opencode* 通配符正确匹配 `opencode-apikey-*` tool 名
- testing layer: unit
- target environment: fix worktree
- required evidence: `bin/deploy-skills --tools opencode-apikey-ds-flash-auto --dry-run` 成功匹配 opencode*
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: ""
- replacement_evidence: `bin/deploy-skills --tools opencode-apikey-ds-flash-auto --dry-run` 返回 deployed > 0

## Integration
- acceptance target: 无 `--tools` 时默认从 registry 检测全部已安装 tool
- testing layer: integration
- target environment: fix worktree
- required evidence: `bin/deploy-skills --dry-run` 返回至少一个已安装 tool
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: ""
- replacement_evidence: `bin/deploy-skills --dry-run` 自动检测到 claude

## End-to-End
- acceptance target: fix→test-pre-merge→develop merge passes
- testing layer: end_to_end
- target environment: develop-bound guarded merge chain
- required evidence: guarded merge receipts
- blocker taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 手动测试通过：默认检测到 claude，--tools 显式指定 opencode-apikey-ds-flash-auto 也成功

## Acceptance Items
### AT-001 opencode 通配符修复
- id: AT-001
- requirement: `opencode-apikey-*` tool 名被 `opencode*)` 通配符匹配
- surface_kind: integration
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: integration
^- status: passed
- artifact_ref: (manual test output)

### AT-002 registry 驱动默认 tool
- id: AT-002
- requirement: 无 `--tools` 参数时，从 tool-registry.json5 检测所有已安装 tool
- surface_kind: integration
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: integration
^- status: passed
- artifact_ref: (manual test output: detected claude)

### AT-003 --tools 显式控制
- id: AT-003
- requirement: `--tools` 参数仍保持精确控制能力
- surface_kind: integration
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: integration
^- status: passed
- artifact_ref: (manual test output: claude,codex both deployed)
