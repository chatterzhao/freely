---
candidate_id: C-20261104T082603Z-A
status: promoted
source_raw: raw-20261104T082603Z
created_at: 2026-11-07
milestone: M-20261104T082603Z-A
---

# Candidates

被否决的替代方案（bash 侧重复实现终态判断、伪回滚已关闭平台、非终态允许关闭、夹带 update/comment 通道收口）见 brainstorms.md。

## C-20261104T082603Z-A: 关闭路径先校验后执行，部分成功独立退出码

- candidate_format_version: v2
- title: `close_platforms` 用纯 transition 预演做前置校验、平台全关才回写 `platform_closed`、adapter 关闭统一 0/3/1、非严格路径不再无条件自证 `platform_state=closed`
- status: promoted
- decision_reason: 关闭是不可逆的平台写；先写平台后校验本地契约，会让「平台已关、本地未关」成为常态结果，而调用方只看到 rc=1。部分成功与全失败同码则让重试策略无从下手。
- next_action: 建 AT-001（静态断言四段式顺序 + 隔离 stub adapter 行为 + issue-sync 端到端 rc），改 `raw_lifecycle_effects.py`、`platform-adapter.py` 的关闭记账、`bin/issue-sync` 的严格/非严格两条路径。
- revisit_trigger: 若引入第三平台或把关闭整体迁到 adapter 入口层（#4166），需重新对齐退出码与记账口径。
- acceptance_criteria:
  - 非终态 raw 执行关闭：退出非零、平台一次都不调用（stub 未被触发）、frontmatter 不变、错误信息含当前 phase。
  - 终态 raw + 全平台成功：`platform_state=closed` 落盘、退出 0。
  - 终态 raw + 部分成功：退出 3、`platform_state` 保持原值、逐平台 status 可见、重跑幂等可自愈。
  - 终态 raw + 全失败：退出 1、`platform_state` 保持原值。
  - 非严格路径（I-*）：任一平台失败不写 `platform_state=closed`，部分成功 rc 3、全失败 rc 1。
  - adapter `close-multi` / `close-raw` 与 `create-issue` 同口径 0/3/1。
- promotion_gate: AT-001 RED → GREEN + 回归基线对比 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 逐行核对 5 处代码位置（adapter 先于 transition、终态约束、严格路径压码、非严格路径无条件写 closed、adapter 同码）；复现 issue 原文的「平台已关 + rc=1」；证伪 #4149/#4136/#4137/#4166 覆盖范围；确认关闭操作幂等，先校验后执行不破坏重跑。
  - verdict: pass
- promoted_issue_id: I-20261104T082603Z-A
- promoted_issue_path: docs/B2-docs/gate/platform/raw-20261104T082603Z/issues/I-20261104T082603Z-A.md
- milestone: M-20261104T082603Z-A
- session_refs: []
