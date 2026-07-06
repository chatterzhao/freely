---
local_id: I-20260622T000649Z-A
kind: I
phase_state: completed
source_candidate: docs/B1-docs/raw-20260622T000649Z49Z/candidates.md#C-20260622T000649Z-A
verification_artifact_dir: docs/B2-docs/I-20260622T000649Z-A/code-reviews
raw_refs:
  - raw-20260622T000649Z49Z
candidate_refs:
  - C-20260622T000649Z-A
created_at: '2026-06-22T09:00:00Z'
updated_at: '2026-06-22T09:00:00Z'
---

# I-20260622T000649Z-A: --reason Gate for All CLI Bypass Mechanisms

## Summary

所有 CLI bypass 机制（--force, --skip, --discard, --verdict）必须提供 --reason，
格式为: --reason "违规绕过门禁中，理由充分，是：<业务理由>"

- **freely init --force**: 新增 --reason 参数和 GATE 拦截
- **freely start --force**: 新增 --reason 参数和 GATE 拦截
- **freely daemon start --force**: 新增 --reason 参数和 GATE 拦截
- **freely task-mode set --force**: 新增 --reason 参数和 GATE 拦截
- **pr-review-guarded --verdict**: 转为命名参数 --verdict/--reviewer/--reason，覆盖失败维度时需 --reason
- **wt-close**: 更新 GATE 消息为统一"先按要求完成"模式，修正示例

## Design
- GATE 统一模式: 先提示按要求完成 → 再说明合理业务理由 → 格式 → 示例
- auto storm recovery (cmd_daemon_start) 不受 GATE 影响：GATE 在 auto-force 逻辑之前检查
- pr-review-guarded 只在 --verdict pass 覆盖失败维度时才触发 GATE（智能检测）

## Acceptance Criteria
- [x] freely init --force 缺少 --reason 时被拦截
- [x] freely start --force 缺少 --reason 时被拦截
- [x] freely daemon start --force 缺少 --reason 时被拦截
- [x] freely task-mode set --force 缺少 --reason 时被拦截
- [x] pr-review-guarded --verdict pass 覆盖失败维度时缺少 --reason 被拦截
- [x] wt-close GATE 消息符合统一模式
- [x] 所有 GATE 示例使用正确的业务理由（非技术症状）
