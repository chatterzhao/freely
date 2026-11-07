---
candidate_id: C-20261105T122053Z-A
status: promoted
source_raw: raw-20261105T122053Z
created_at: 2026-11-05
milestone: M-20261105T122053Z-A
---

# Candidates

被否决的替代方案（改 scan 真源、改变健康路径返回结构、删除 REST 回退、让聚合层抛异常中断所有调用方、把失败标记为普通 issue 记录）属退化或越界，记录见 brainstorms.md，不作为 candidate 立项。

## C-20261105T122053Z-A: 读失败显式标记，健康路径零变化

- candidate_format_version: v2
- title: handler 记录 read_health，聚合层在读失败时产出 __degraded__，parity 降级跳过
- status: promoted
- decision_reason: 根因是读失败被压成空字典且无平台级健康标记。scan 已有 `__degraded__` 消费逻辑，聚合层只需在失败时产出该标记即可复用既有降级语义，无需改 scan 或任何调用方；健康路径必须保持 107 条纯字典不变。
- next_action: 写 AT-001 RED（mock 读失败 / 异常 / 全失败 / parity 假差异），给 handler 加 read_health、改聚合层与 parity，跑 GREEN 与 12 个回归基线对比，并用真实双平台读取验证健康路径无标记。
- revisit_trigger: 若未来把清单改为分页流式返回，另开 issue 调整降级标记的传递方式；本 PR 以 dict 中的 `__degraded__` 保留键为契约。
- acceptance_criteria:
  - 两平台健康时返回 107 条纯字典，结构/记录字段与修复前一致，无额外键。
  - 单平台或全部平台读失败时结果含 `__degraded__`，点名平台与错误，且保留可读平台的部分记录。
  - handler 抛异常时不产生 `github:status` / `github:error` 假记录或 TypeError。
  - scan 的 `get_platform_open_issues()` 能产出 `__degraded__` 且既有降级消费者仍工作（scan 真源不改）。
  - parity 在降级时 SKIP + 重试提示，不报假差异；健康时仍正常比较。
  - REST 回退保留；`pull_raw_issue()` / 写通道 / `_discover_one` 语义不动。
  - 12 个相关回归以未修改 develop HEAD 做基线对比，零新增失败。
- promotion_gate: AT-001 RED → GREEN + 12 个回归基线对比 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 逐行核对 _open_issue_records_via_rest / GitHub / Gitee 三处读通道、_safe 的错误对象、模块级聚合层、scan 既有 `__degraded__` 消费者与 parity 差异计算；用真实双平台读取验证健康路径 102 条无标记；2 个真源还原到未修改 develop HEAD 做 RED 与 12 个回归基线对比。
  - verdict: pass
- promoted_issue_id: I-20261105T122053Z-A
- promoted_issue_path: docs/B2-docs/platform/issue-parity/raw-20261105T122053Z/issues/I-20261105T122053Z-A.md
- milestone: M-20261105T122053Z-A
- session_refs: []
