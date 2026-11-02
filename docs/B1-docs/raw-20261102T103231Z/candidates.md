---
candidate_id: C-20261102T103231Z-A
status: promoted
source_raw: raw-20261102T103231Z
created_at: 2026-11-02
milestone: M-20261102T103231Z-A
---

# Candidates

## C-20261102T103231Z-A: owner lane 显式认领 manager 身份

- candidate_format_version: v2
- title: daemon 在无 agent_working 行时按唯一 manager 认领本工位，不猜、不覆盖
- status: promoted
- decision_reason: `_resolve_current_agent_id` 只认 `agent_working`，而 owner 自建的工位没有该行，daemon 启动必然 fail-closed；身份只用于解析工具 slot，不承担权限边界。正确做法是补上缺的那一行，而不是让解析器静默回退。
- next_action: B2 物化 `I-20261102T103231Z-A`；先写 RED（无行时 claim 返回 None），再实现 `owner_lane.py` 并接入 `_resolve_current_agent_id`。
- revisit_trigger: 若连续两个里程碑内出现“worker 工位被认领为 manager”的日志，回退本 candidate 并改为显式 `freely claim-owner` 子命令。
- acceptance_criteria:
  - 零行工位：`claim` 写入一条 `manager_id` 行并返回该 id；日志明确标注 owner-lane
  - 已有行：原样返回，不覆盖、不新增（`created=false`）
  - 项目配置多个 manager：claim 失败，保持 fail-closed
  - 路径不是本项目 worktree：claim 失败
  - 写库失败：向上抛错，不吞
  - worker / reviewer 角色没有自动认领通道
- promotion_gate: RED→GREEN + 既有 `test-freely-*` 身份相关测试全绿 + `governance-merge-gate --range develop..HEAD` 通过
- open_questions:
  - raw_key 从分支名提取失败时（例如手工命名的分支）是否应拒绝认领而不是用目录名兜底
  - 认领是否需要 TTL/回收（目前行会一直留到 wt-close）
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research
  - summary: 读 `runtime/freely:339-368`（单一解析路径 + fail-closed 注释）、`agent_working.py:94-116`（agent_assign 写库入口）、`agent_working` 表（15 行，worktree 行只有 worker_id；`__manager__` 行 manager_id 为空）
  - verdict: pass
- promoted_issue_id: I-20261102T103231Z-A
- promoted_issue_path: docs/B2-docs/worktree-lifecycle/owner-lane/raw-20261102T103231Z/issues/I-20261102T103231Z-A.md
- milestone: M-20261102T103231Z-A
- session_refs: []

## C-20261102T103231Z-B: 身份一致性巡检

- candidate_format_version: v2
- title: scan 巡检“有 worktree 无 agent_working 行”与“有行无 worktree”的双向漂移
- status: needs_research
- decision_reason: 本轮只解决“零行可自举”，没有解决“行与工位长期不一致”。`wt-close` 删工位时若未清行，会留下幽灵绑定，后续 claim 会误判“已有行”。
- next_action: C-A 合并后单独立 raw；先定义巡检查询与处置动作（清理幽灵行 / 补建缺失行）。
- revisit_trigger: `agent_working` 中 worktree 路径不存在的行数 > 0
- acceptance_criteria:
  - 巡检输出双向漂移清单，只读
  - 处置动作需要显式命令，不在 scan 中自动删行
- promotion_gate: 独立 B2 + RED/GREEN
- open_questions:
  - 幽灵行是删还是标记 `stale` 保留审计
- acceptance_reviews: []
- promoted_issue_id: ''
- promoted_issue_path: ''
- milestone: M-20261102T103231Z-A
- session_refs: []
