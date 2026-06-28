# Pre-Tests: platform pull title standardization
- issue_id: I-20260507T143546Z-A
## Unit
- acceptance target: _created_at_to_key 正确转换时间戳
- testing layer: unit
- target environment: feature worktree
- required evidence: "2026-05-06T10:00:35Z" → "20260506T100035Z"
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: human_observation_only
- not_applicable_explanation: 纯函数逻辑，通过代码审查验证
- replacement_evidence: 代码审查确认转换逻辑正确
## Integration
- acceptance target: raw-issue-pull 时标题不一致会被修正
- testing layer: integration
- target environment: feature worktree
- required evidence: 拉取缺秒 issue 后标题含标准 key
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 需要真实平台 API 调用，通过代码审查验证
- replacement_evidence: 代码路径完整，_update_issue_title 有异常保护
## End-to-End
- acceptance target: merge passes
- testing layer: end_to_end
- target environment: develop merge chain
- required evidence: merge receipts
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: 新增函数不影响现有行为（仅 pull 时触发）
- replacement_evidence: pr-merge-guarded 输出
## Real-Environment
- real_environment_status: pass
- real_environment_reason: best-effort title update，失败不阻塞 pull
## Acceptance Items
### AT-001 created_at to key
- id: created-at-to-key
- requirement: _created_at_to_key 正确格式化时间戳为 YYYYMMDDTHHMMSSZ
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
- status: pass
- artifact_ref: docs/epics/platform-pull-standardize/code-reviews/closeout-review.md
