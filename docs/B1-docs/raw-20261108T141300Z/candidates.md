---
candidate_id: C-20261108T141300Z-A
status: promoted
source_raw: raw-20261108T141300Z
created_at: 2026-11-10
milestone: M-20261108T141300Z-A
---

# Candidates

被否决方案见 brainstorms.md。

## C-20261108T141300Z-A: 物化时把平台 severity 标签写回本地 frontmatter

- candidate_format_version: v2
- title: `pull_raw_issue` 从双平台 `severity/*` 标签解析优先级（冲突 fail-closed）写入可选第 22 字段；恢复 `canonical_projection` 对 severity/* 的比较；无标签历史 raw 零改写
- status: promoted
- decision_reason: `feedback --severity` 创建的 P0/P1 在 `wt-create` 物化后丢失，本地读视图按默认 P2 分诊，而平台标签仍是 P0/P1；R16.5 为了放行只能把 severity/* 从副本比较中排除，属权宜。
- next_action: 建 AT-001（2 静态 + 7 行为，含真实 `pull_raw_issue`）→ 接线 → 恢复比较 → 回归。
- revisit_trigger: 若将来 severity 改为「平台标签之外」的权威来源（如 SQLite chats 表），需重述解析优先级。
- acceptance_criteria:
  - RED：带 `severity/P0` 标签的双平台副本物化后 frontmatter 无 severity；`canonical_projection` 排除 severity。
  - GREEN：AT-001 `9 ok / 0 failed`；`parse_issue_text` + `resolve_severity` 读回 P0。
  - GREEN：双平台显式冲突抛 ValueError；一方缺标签只告警不阻塞；无标签 raw 保持 21 字段零改写。
  - GREEN：`canonical_projection` 能区分 P0 与 P1。
  - 回归：materialization / raw-metadata / feedback-severity / raw-reconciliation / replica-degraded / `test-all --ci` 与 develop 基线一致。
- promotion_gate: AT-001 RED → GREEN + 回归 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 逐条复核 issue 证据在 develop 仍成立；确认契约已支持可选第 22 字段、缺口只在物化接线；验证 `readable[plat]["labels"]` 可用；评估恢复比较对历史 raw 的影响（第二指纹机制 + 6 个测试实跑）。
  - verdict: pass
- promoted_issue_id: I-20261108T141300Z-A
- promoted_issue_path: docs/B2-docs/platform/issue-parity/raw-20261108T141300Z/issues/I-20261108T141300Z-A.md
- milestone: M-20261108T141300Z-A
- session_refs: []
