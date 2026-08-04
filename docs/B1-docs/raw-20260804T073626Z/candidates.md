---
candidate_id: C-20260804T073626Z-A
status: absorbed
source_raw: raw-20260804T073626Z
created_at: 2026-08-04
milestone: M-20260804T073626Z-A
---

# Candidates

## C-20260804T073626Z-A: platform-adapter pull KeyError（已被 reconciliation 工位吸收）

- candidate_format_version: v2
- title: platform-adapter pull KeyError 阻塞 wt-create
- status: absorbed
- decision_reason: develop 已合并 I-20260725T030511Z-A（raw replica reconciliation），其实现覆盖本 issue 全部修复建议：needle 大小写、discover_raw_replicas 契约、残留消费点 .get() 防御；wt-create 对两个 raw issue 实测成功。
- next_action: 无（absorbed，不新开实现）
- revisit_trigger: 若未来平台 handler 恢复直接遍历 search 结果取 issue_number 且无防御，需重新评估。
- acceptance_criteria:
  - GitHub search_raw_issue 对大写 Z 的 raw key 可匹配
  - pull 不再抛 KeyError（统一 issue_id 契约）
  - 残留调用点无未防御的 issue_number 直接索引
  - wt-create --source platform 真实创建工位成功
- promotion_gate: 不适用（absorbed）
- open_questions: []
- acceptance_reviews:
  - reviewer: cli
  - mode: independent-readonly-review
  - summary: 逐项核对 develop 代码（L234/L426/L710/L917/L942）与 wt-create 实测，确认全部落地
  - verdict: pass
- absorbed_into: I-20260725T030511Z-A
- milestone: M-20260804T073626Z-A
- session_refs: []
