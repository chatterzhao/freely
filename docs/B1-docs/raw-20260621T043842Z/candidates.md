## C-20260621T043842Z-A

<!-- 使用 bullet 格式: `- key: value`，不要用 YAML `---` 分隔符 -->

- candidate_format_version: v2
- status: promoted
- promoted_issue_path: docs/issues/I-20260621T043842Z-A/issue.md
- milestone: M-20260621T043842Z-A
- decision_reason: 方案A (最小改动，直接修复 bug)
- promoted_at: 2026-06-21T04:40:00Z
- acceptance_criteria: |
    1. Worker fork session 能通过 SESSION_PARENT_PROJECT 找到正确的 A2A socket
    2. worktree_has_active_worker 在已有 worker 时返回 true
    3. manager_exit_contract_kind 仅在真正有 pending worker 时返回 delegate_workers
    4. Scan 不再对已有 submitted/launched worker 的 raw_key 重复出项
- promotion_gate: |
    修改仅涉及 bug fix（JSON 解析错误 + 环境变量缺失 + 状态检查不完整），
    无 API 变更，无新增依赖，所有改动向后兼容。
- acceptance_reviews: |
    启动 freely daemon 观察 worker 分配行为，确认无重复 worker。
- session_refs: |
    GitHub #3200, #3201, #3202
    raw-20260621T043836Z, raw-20260621T043842Z, raw-20260621T043850Z
