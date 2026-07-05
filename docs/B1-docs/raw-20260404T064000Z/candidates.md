# Candidates - 20260404-0640--protected-branch-merge-receipt-gap-followthrough

## C-20260404T064000Z-A: legacy issue

- candidate_format_version: `v2`
- title: Protected-branch merge receipt gap followthrough
- problem: 最近的 protected-branch merge 复核发现 `908a6ad` 缺失 canonical Freely merge receipt trailer，但当前 `governance-check` 只审 HEAD protected merge 和 break-glass ledger，所以这种“普通 merge 的历史 receipt gap”不会被 ancestry audit 捕获，也没有专用 canonical backfill 面。
- why_now:
  - 这不是理论缺口，而是 `develop` ancestry 中已经存在的实际 receipt gap
  - 若不把普通 merge gap 的 backfill contract 收成真源，后续只能靠人工 review 发现同类问题
  - 旧的 protected-branch merge receipt hardening owner 已完成，必须以更窄 follow-on 处理，而不是 reopen 旧 owner
- acceptance_criteria:
  - 定义一个只承接普通 protected merge receipt gap 的 canonical backfill ledger
  - `governance-check` 能从 effective date 起回扫 protected branch merge history，并要求缺 trailer 的普通 merge 必须有 matching backfill entry
  - 已带 canonical trailer 的普通 merge 若仍声明 backfill，`governance-check` 必须拒绝
  - break-glass merge 继续由 break-glass ledger 审计，不与普通 merge gap ledger 混用
  - `908a6ad` 的 canonical backfill 条目、follow-on owner 和 evidence_refs 必须落盘
- promotion_gate:
  - 不 reopen `I-20260402T191200Z-A`
  - 不把普通 merge gap 收进 break-glass ledger
  - 不把 backfill ledger 当成未来正常 merge 缺 trailer 的放行方式
  - focused regression 必须覆盖 no-backfill fail / matching-backfill pass / trailer-bearing merge cannot use backfill
- open_questions:
  - 普通 merge gap ledger 是否需要单独的 mode 字段，还是固定就是 trailer-gap backfill
  - effective date 是否应绑定到这条 owner materialization 当天，而不是历史 break-glass audit 日期
- acceptance_reviews:
  - reviewer: `codex-self-review`
    verdict: `supports`
    note: 这是 ancestry audit 的 blind spot follow-on，不是旧 break-glass owner 的续写。
- decision_reason:
  - 当前 canonical tooling 已足够证明 receipt trailer contract 存在，缺的是“历史 gap 被继续审计”的 writeback 真源
  - 通过显式 backfill ledger + owner，可以在不改写历史的前提下恢复 auditability
- priority: `P1`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_id: `I-20260404T064000Z-A`
- promoted_issue_path: `docs/B2-docs/ibm/protected-branch-merge-receipt-gap-followthrough/issues/protected-branch-merge-receipt-gap-followthrough.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - materialize a narrow owner for ancestry receipt-gap backfill and audit
  - keep `908a6ad` as the first concrete backfill target
- revisit_trigger:
  - another protected-branch merge is discovered without canonical trailers
  - governance-check still accepts ancestry receipt gaps for ordinary protected merges
