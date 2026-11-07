---
candidate_id: C-20261107T133328Z-A
status: promoted
source_raw: raw-20261107T133328Z
created_at: 2026-11-07
milestone: M-20261107T133328Z-A
---

# Candidates

被否决的替代方案（wt-close 再写一份判断、伪造 resolution、--force 绕过）见 brainstorms.md。

## C-20261107T133328Z-A: wt-close 复用单一评论扫描

- candidate_format_version: v2
- title: `wt-close` 删除自算的 comment/resolution 计数，改调 `quality/comment-resolution-scan.py`；系统事件评论不计入未解决
- status: promoted
- decision_reason: 同一规则两份实现必然漂移；当前 wt-close 的旧实现会把系统事件评论当人类评论，导致任何经过 promote 的 raw 都无法收口，只能 `--force`（禁止项）。
- next_action: 建 AT-001（5 静态 + 5 行为），改 `wt-close`。
- revisit_trigger: 若将来把评论判定搬进 runtime（例如 `freely comments` 子命令），wt-close 与 pr-create 都要改为调用该命令。
- acceptance_criteria:
  - `wt-close` 源码内不再有 `grep -c "^### comment-"`。
  - `wt-close` 引用 `comment-resolution-scan.py`，并用其输出决定是否阻塞。
  - 只有系统事件评论的文档不被阻塞；人类评论无 resolution 被阻塞；补 resolution 后放行。
  - 两个门禁对同一文档给出相同结论。
  - 破损的 `$((...))` 文案消失。
- promotion_gate: AT-001 RED → GREEN + 回归基线对比 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 真机复现 wt-close 阻塞与错误文案；核对两份实现的差异；证伪 #4183/#4151/#4075 覆盖范围。
  - verdict: pass
- promoted_issue_id: I-20261107T133328Z-A
- promoted_issue_path: docs/B2-docs/gate/governance/raw-20261107T133328Z/issues/I-20261107T133328Z-A.md
- milestone: M-20261107T133328Z-A
- session_refs: []
