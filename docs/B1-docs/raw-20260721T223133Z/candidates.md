---
candidate_id: C-20260721T223133Z-A
status: promoted
source_raw: raw-20260721T223133Z
created_at: 2026-07-21
milestone: M-20260721T223133Z-A
---

# Candidates

## C-20260721T223133Z-A：统一生命周期命令的状态观测与受控迁移

- candidate_format_version: v2
- title: 统一已有 PR 更新与 raw metadata 状态合同
- status: promoted
- decision_reason: `pr-create-guarded` 和 `wt-create` 都在执行状态迁移前使用了错误前提；raw 元数据又缺少统一字段合同，导致 scan/gate 无法可靠判定。应以配置驱动平台观测和版本化扁平 schema 统一修复。
- next_action: 物化 I-20260721T223133Z-A，先编写 PR 更新、metadata 创建、wt-create 保持 proposed、scan/gate 非法组合的 RED 测试，再实现共享状态模块和消费者迁移。
- revisit_trigger: 若新 schema 无法在不批量改写历史 raw 的条件下兼容现有门禁，回到 B1 评估显式迁移；不得引入长期双写 schema。
- acceptance_criteria:
  - 已有 PR 的本地 head 领先远端时，`freely pr-create-guarded` 在 merge dry-run 前按所有配置平台分类，并由 adapter 完成受控 push 与 PR 复用/更新。
  - absent/behind/equal/ahead/diverged 五态有明确动作；ahead/diverged fail closed，恢复说明只引用 Freely/adapter 命令。
  - 新 raw issue 从 feedback 起具有固定字段全集、顺序和显式空值，后续命令只更新值。
  - `wt-create` 后 raw 保持 proposed；只有 canonical I-* 物化时原子写入 absorbed 三元组。
  - scan、gate、sync、PR、closeout 按字段值和跨字段组合判断；字段存在但值为空不能放行。
  - 旧 raw 文件不批量迁移，消费者保持读取兼容；新 schema 的非法组合 fail closed。
  - 测试覆盖多平台聚合、PR 已有更新、schema 稳定性、状态迁移、scan/gate 与旧格式兼容。
- promotion_gate: B2 文档定义唯一 schema 真源、状态转换表、消费者清单和可执行 RED/GREEN 测试矩阵；实现不得把新功能追加到超大 runtime 单体脚本。
- open_questions: []
- acceptance_reviews:
  - reviewer: cursor-explore-review
  - mode: subagent
  - summary: 盘点 751 份 raw 元数据、生产链和消费者后，确认 wt-create 是错误 absorbed 的直接写入点，且多个存在性消费者必须同步调整。
  - verdict: pass
- promoted_issue_id: I-20260721T223133Z-A
- promoted_issue_path: docs/B2-docs/runtime/command-lifecycle-state-contract/raw-20260721T223133Z/issues/I-20260721T223133Z-A.md
- milestone: M-20260721T223133Z-A
- session_refs: []
