---
candidate_id: C-20261103T055554Z-A
status: promoted
source_raw: raw-20261103T055554Z
created_at: 2026-11-03
milestone: M-20261103T055554Z-A
---

# Candidates

## C-20261103T055554Z-A: raw replica 身份解析优先 [RAW-key] 标题前缀

- candidate_format_version: v2
- title: 修复 raw replica 身份解析被 body 交叉引用污染
- status: promoted
- decision_reason: raw issue 的身份是 `[RAW-{key}]` 标题前缀；body 里的引用不是身份声明。当前 search_raw_issue 把 title/body 子串都当身份，导致多匹配 ambiguous 并 block PR。把身份解析收敛为"标题前缀优先 + 单条兜底 + 多真实身份仍 ambiguous"最小且可单测。
- next_action: B2 物化 I-20261103T055554Z-A；先写 RED 单测（标题优先/多身份 ambiguous/兜底单条），再改 platform-adapter 解析层；随后用真实 key 跑 discover_raw_replicas 验证。
- revisit_trigger: 若出现"同一 raw key 确实对应多个 canonical issue"的合法场景，需要重新定义多副本身份模型。
- acceptance_criteria:
  - `search_raw_issue` 的调用方通过统一解析得到"标题前缀唯一命中"，body 交叉引用不产生额外身份。
  - 多个标题前缀命中仍返回 ambiguous（不静默选一个）。
  - 标题无命中时保留单条 body 命中兜底；多条仍 ambiguous。
  - 对 raw-20260807T114900Z 真机 discover 返回两个平台 ok，不再 ambiguous。
- promotion_gate: 单测 RED→GREEN + 真机 discover 证据 + governance-merge-gate 通过
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research
  - summary: 读 platform-adapter search_raw_issue/_discover_one/_unique_raw_issue 与 raw_reconciliation；确认 ambiguous 由 #4108 body 证据路径触发
  - verdict: pass
- promoted_issue_id: I-20261103T055554Z-A
- promoted_issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261103T055554Z/issues/I-20261103T055554Z-A.md
- milestone: M-20261103T055554Z-A
- session_refs: []
