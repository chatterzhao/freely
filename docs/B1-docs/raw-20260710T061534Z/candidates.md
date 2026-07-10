---
candidate_id: C-20260710T061534Z-A
status: absorbed
source_raw: raw-20260710T061534Z
absorbed_into: I-20260710T061534Z-A
created_at: 2026-07-10
milestone: M-20260710T061534Z-A
---

## C-20260710T061534Z-A: Manager Agent 协作链路修复

- candidate_format_version: v2
- title: Manager Agent 协作链路修复 — 超时 + hygiene 移入 scan
- status: absorbed
- decision_reason: 实际观察确认 Manager cycle 被 hygiene 硬编码注入 + 180s 超时杀死，从未走到 a2a-exit 委派步骤。委派链路设计正确，只需修超时和 hygiene 架构。
- next_action: B2 设计实现
- revisit_trigger: N/A
- acceptance_criteria:
  - Manager cycle 可完整执行（不再被超时杀死）
  - Worktree 卫生以 scan items 形式呈现（非硬编码 prompt 注入）
  - Manager 可语义判断工位有用/无用
  - 委派链路（a2a-exit → Worker ACP session）保持正常工作
- promotion_gate: B1 预研完成，candidate 已收敛
- open_questions: []
- acceptance_reviews: []
- promoted_issue_id: I-20260710T061534Z-A
- promoted_issue_path: docs/B2-docs/runtime/scan/raw-20260710T061534Z/issues/I-20260710T061534Z-A.md
- milestone: M-20260710T061534Z-A
- session_refs: []

## 改动计划

### 1. acp-bridge.py: idle 判定逻辑修正
- `_idle_monitor_loop` 检查 `self.pending` 中是否有活跃 `session/prompt`
- 有 active prompt → 不触发 idle shutdown（AI 正在工作中）
- 只在真正空闲（无 session、无 in-flight prompt）时关机
- 不改变 timeout 数值（保留 180s）

### 2. task-lifecycle-scan.py: 新增 worktree_governance 检测
- 将 `manager_hygiene_alerts()` 的逻辑移入 scan
- 产出 `source_family=worktree_governance` 的 scan items
- 每个 item 包含: worktree_path, branch, dirty_entries, checkpoint_required, last_active
- next_action 模板: `[manager] 语义判断工位状态 → 继续 or wt-close`

### 3. freely: 移除硬编码 hygiene prompt 注入
- `build_prompt()` 中移除 `append_manager_hygiene_alert_if_needed` 调用
- 保留 `append_checkpoint_governance_if_needed`（checkpoint 是独立功能）
- Manager 从 scan 统一消费所有 actionable items

### 不在此次范围
- Manager prompt 巡逻流程重排
- agent-roles.toml 扩展

### 4. scan + manager-agent: 委派指令追加 workflow 引用
- 所有 scan next_action 的 `[worker]` 行追加："严格按照 skill:freely-workflow-guarded-execution 指导开展工作"
- manager-agent.md 委派示例追加同样指令
