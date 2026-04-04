# Candidates - 20260403-1100--governance-chain-legacy-repair

## C-20260403-1100-A

- candidate_format_version: `v2`
- title: Governance chain legacy repair for develop push unblock
- status: promoted
- decision_reason: 当前真正缺的不是单个字段修补，而是一个能承接 legacy governance drift 和 active child repair slices 的 canonical owner。
- promoted_issue_path: `docs/epics/workspace-routing-foundation/governance-chain-legacy-repair/issues/governance-chain-legacy-repair.md`
- promoted_issue_id: `I-20260403-1100-A`
- milestone: M-20260306-workspace-routing-foundation
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action: Keep `1100` as the umbrella owner, normalize the child repair slices into lawful parent-linked pre-brainstorm truth, then continue the real legacy artifact backfill without weakening the gate.
- revisit_trigger: 当 child repair slices 再次出现伪 promoted 声明、或新一轮 gate 输出表明 canonical parent truth 又与 artifact reality 脱节时立即重审。
- problem: `develop` 上暴露出的 legacy governance drift 已经裂成多条 repair slices，但这些切片此前没有合法 parent owner，导致 repair 自身也在制造新的 candidate / issue / progress 失真。
- why_now:
  - `governance-merge-gate` 已按当前 canonical 质量线暴露 legacy drift
  - `1200/1201/1202/1203` 已经并行存在，但都缺乏 lawful owner 归属
  - 若此时继续只修字段而不修 owner chain，后续 review 仍无法证明哪条 lane 才是 canonical truth
- acceptance_criteria:
  - `I-20260403-1100-A` 在 milestone / issue / progress 三处保持一致
  - `1200/1201/1202/1203` 在 canonical docs 中明确为 parent-linked child slices，且不再指向不存在的 issue
  - 当前 batch 的 route 明确禁止用 gate weakening 替代 truth repair
  - 后续 legacy artifact backfill 可以以本 owner 为 authority 继续推进
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
    note: `1100` 应先成为 canonical umbrella owner，再决定具体 repair slices 的 absorbed / materialized 落位。
