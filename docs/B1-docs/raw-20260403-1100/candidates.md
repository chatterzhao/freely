# Candidates - 20260403-1100--governance-chain-legacy-repair

## C-20260403-1100-A: legacy issue

- candidate_format_version: `v2`
- title: Governance chain legacy repair for develop push unblock
- status: promoted
- decision_reason: 当前真正缺的不是单个字段修补，而是一个能承接 legacy governance drift 与历史 child repair slices 的 canonical owner；该 owner 已完成真相修复并转入历史留痕。
- promoted_issue_path: `docs/B2-docs/gate/governance-chain-legacy-repair/issues/governance-chain-legacy-repair.md`
- promoted_issue_id: `I-20260403-1100-A`
- milestone: M-20260403-1100-A
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action: Keep `1100` only as historical traceability for the completed truth repair. Any future governance-chain backfill must start from current `develop` as a new owner instead of reactivating this candidate.
- revisit_trigger: 当新的 canonical drift 再次出现，或新一轮 gate 输出表明 parent truth 又与 artifact reality 脱节时，新开 candidate/issue，而不是恢复 `1100` 为 active owner。
- problem: `develop` 上暴露出的 legacy governance drift 已经裂成多条 repair slices，但这些切片此前没有合法 parent owner，导致 repair 自身也在制造新的 candidate / issue / progress 失真。
- why_now:
  - `governance-merge-gate` 已按当前 canonical 质量线暴露 legacy drift
  - `1200/1201/1202/1203` 当时曾并行存在，但都缺乏 lawful owner 归属，现已只保留为 historical child slices
  - 若此时继续只修字段而不修 owner chain，后续 review 仍无法证明哪条 lane 才是 canonical truth
- acceptance_criteria:
  - `I-20260403-1100-A` 的 completed/historical 语义在 milestone / issue / progress 三处保持一致
  - `1200/1201/1202/1203` 在 canonical docs 中明确为 historical child slices，且不再指向不存在的 issue
  - 当前 batch 的 route 明确禁止用 gate weakening 替代 truth repair
  - 当前批次完成后，后续 legacy artifact backfill 必须从新的 owner lifecycle 继续推进
- promotion_gate:
  - 不为了解除阻塞而放宽 `governance-merge-gate`
  - 不让 child slice relationship 只存在于 commit message 或口头说明
  - 不让 promoted candidate 指向不存在的 issue / progress
- open_questions:
  - 哪些 legacy repair classes 应 absorbed，哪些值得后续拆为独立 owner？
  - child slices 何时需要从 pre-brainstorm 升级为 issue-bound execution lane？
- acceptance_reviews:
  - reviewer: `codex-self-review`
    verdict: `supports`
    note: `1100` 已完成 canonical umbrella owner 职责；当前应把这层 authority 固化为历史 closeout 真相，而不是继续保留 active/current owner 语义。
- completion_note: 2026-04-04 truth-repair 恢复了缺失的 `1100` owner artifacts，清理了悬挂引用，并把该 owner 固化为已完成的历史留痕。
