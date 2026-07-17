---
candidate_id: C-20260717T103359Z-A
status: promoted
source_raw: raw-20260717T103359Z
created_at: 2026-07-17
milestone: M-20260717T103359Z-A
---

# Candidates

## C-20260717T103359Z-A: 工位所有权三道硬防线

- candidate_format_version: v2
- title: wt-close 未完成/异主拦截 + protected root 污染检测 + fallback prompt 铁律
- status: promoted
- decision_reason: 三种事故模式各配硬防线;prompt 层约束已被实证击穿。见 brainstorms
- next_action: B2 → RED → dev → GREEN → PR
- revisit_trigger: ACP init 超时若在新代码复现,另案根修 fallback 触发源
- acceptance_criteria:
  - AC1: 无 merge 证据的 key 默认 wt-close 被拦(要求 --force+reason);有 merge 证据的 key 通过该前置检查
  - AC2: FREELY_AGENT_RAW_KEY≠目标 key 时 wt-close 被拦;相等或未设时不受此检查影响
  - AC3: 运行中污染 develop 一个文件 → protected_root_dirty_detected 事件出现且同指纹去抖不重复
  - AC4: fallback 直启前 prompt 文件头部幂等注入边界铁律段(重复 prepend 不叠加)
- promotion_gate: 三次事故实证 + 插入点勘察完毕(bin/wt-close 前段/主循环/L13240 fallback 区)
- open_questions: []
- acceptance_reviews:
  - reviewer: inline-incident-analysis
  - mode: inline
  - summary: 三事故模式与防线一一映射;既有 --force+reason 语义复用不新增豁免面
  - verdict: pass
- promoted_issue_id: I-20260717T103359Z-A
- promoted_issue_path: docs/B2-docs/gate/governance/raw-20260717T103359Z/issues/I-20260717T103359Z-A.md
- milestone: M-20260717T103359Z-A
- session_refs: []
