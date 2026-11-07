---
candidate_id: C-20261104T082549Z-A
status: promoted
source_raw: raw-20261104T082549Z
created_at: 2026-11-04
milestone: M-20261104T082549Z-A
---

# Candidates

被否决的替代方案（新建独立 sync-debt 账本、把事实判定搬进 pull、让部分成功返回 1 由调用方猜、把写通道一起改、stdout 里塞警告）属重复造轮子或越界，记录见 brainstorms.md，不作为 candidate 立项。

## C-20261104T082549Z-A: pull 按可用平台回退并复用 sync-debt 记账

- candidate_format_version: v2
- title: raw-issue-pull/wt-create 支持 --platform/--source-platform，单平台不可读时从可读副本物化并记账，部分成功退出码 3
- status: promoted
- decision_reason: 根因是「任一平台不可读即全停」与「platform_ids/assignee/title 三个循环假定全部副本有 issue_id」。sync-debt 与 allow-degraded 判定已存在，只需复用并把三个循环收窄到可读副本；同时必须让 wt-create 把 3 当成继续，否则修复无效。
- next_action: 写 AT-001 RED（隔离 fake adapter + 基线还原），改 3 个真源，跑 GREEN 与 11 个既有回归基线对比，端到端验证 CLI 退出码 3 / stdout 单一 JSON / sync-debt 落账。
- revisit_trigger: 若 #4149 改进平台写通道后需要统一退出码语义，另开 issue 对齐；本 PR 的 3 只描述 pull 路径的部分成功。
- acceptance_criteria:
  - 屏蔽 github 后仍能从 gitee 物化成功，不再是 FATAL。
  - `--platform gitee` 明确从 gitee 读取并写回 `primary_platform` / `platform_ids`。
  - 不可读平台记入既有 `sync-debt list`，不阻断工位创建。
  - 部分成功退出码为 3 而非 1；全部不可读仍 FATAL；显式指定不可读平台失败而不静默回退。
  - 双平台都 ok 时 primary 与 platform_ids 与修复前完全一致；R2 H1 / Q2 兼容分支不退化。
  - stdout 恰好一个 JSON 文档；11 个既有回归基线对比零新增失败。
- promotion_gate: AT-001 RED → GREEN + 11 个回归基线对比 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 逐行核对 _discover_one 的 unknown/missing/ambiguous/ok 语义、raw_reconciliation 的 allow_degraded 决策、既有 sync-debt.py API、wt-create 的 JSON stdout 契约与 _fill_platform_ids 容错；隔离 git 项目端到端验证退出码 3 与账本落账；3 个真源还原到未修改 develop HEAD 做 RED 与 11 个回归基线对比。
  - verdict: pass
- promoted_issue_id: I-20261104T082549Z-A
- promoted_issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261104T082549Z/issues/I-20261104T082549Z-A.md
- milestone: M-20261104T082549Z-A
- session_refs: []
