# Pre-Tests: raw-issue-pull interception guard
- issue_id: I-20260507T143544Z-A

## Unit
- acceptance target: develop 分支拒绝 raw-issue-pull
- testing layer: unit
- target environment: feature worktree
- required evidence: stderr 含"不能在受保护分支"且 exit 1
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: human_observation_only
- not_applicable_explanation: Shell 脚本通过直接执行验证，执行结果即证据
- replacement_evidence: 从 develop 执行 raw-issue-pull 返回 exit 1 且输出预期错误信息

## Integration
- acceptance target: CLI dispatch 正确路由 raw-issue-pull
- testing layer: integration
- target environment: feature worktree
- required evidence: bin/freely raw-issue-pull 调用成功返回 JSON
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: human_observation_only
- not_applicable_explanation: CLI 路由通过直接执行验证
- replacement_evidence: bin/freely raw-issue-pull --raw-key xxx 返回正确 JSON

## End-to-End
- acceptance target: feature→test-pre-merge→develop merge passes
- testing layer: end_to_end
- target environment: develop-bound guarded merge chain
- required evidence: guarded merge receipts
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: Shell 脚本修改，合并即端到端验证
- replacement_evidence: pr-merge-guarded 成功输出
- blocker taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 从匹配工位可正常 pull issue，从不匹配分支被正确拒绝

## Acceptance Items
### AT-001 develop block
- id: develop-block
- requirement: raw-issue-pull 在 develop/main 分支拒绝执行
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
^- status: passed
- artifact_ref: docs/epics/raw-issue-pull-intercept/code-reviews/review.md

### AT-002 branch mismatch
- id: branch-mismatch
- requirement: 当前分支不包含 raw-key 时拒绝
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
^- status: passed
- artifact_ref: docs/epics/raw-issue-pull-intercept/code-reviews/review.md

### AT-003 cli dispatch
- id: cli-dispatch
- requirement: bin/freely raw-issue-pull 路由到 cmd_raw_issue_pull
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
^- status: passed
- artifact_ref: docs/epics/raw-issue-pull-intercept/code-reviews/review.md
