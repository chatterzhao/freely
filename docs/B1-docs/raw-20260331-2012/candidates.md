# 候选：active-milestone-placement-and-consumption-gate

- id: `C-20260331-2012-A`
- candidate_format_version: `v2`
- title: Enforce active milestone placement correctness for unresolved candidates
- source_brainstorm: `docs/pre-brainstorms/20260331-2012--active-milestone-placement-and-consumption-gate/brainstorms.md`
- problem: Freely's current governance already requires active candidates to remain visible in `docs/milestones.md`, and the merge gate already checks candidate visibility plus `C/M/I` traceability. But the current contract still treats "present in some milestone queue" as sufficient, without proving that the candidate is attached to the correct and still-active milestone. This allows important current research to remain effectively unconsumed via `milestone: unassigned`, placement in the wrong milestone, or placement in a completed milestone that will never schedule it.
- why_now:
  - 当前仓库已经把 unresolved research persistence 与 develop merge `C/M/I` gate 都写成 canonical rule，但两者中间仍缺“milestone 放置正确性”这一层。
  - 真实 active candidate 已出现 `milestone: unassigned` 且未进入 milestone queue 的情况，说明现有 gate 仍允许“研究存在但不被当前里程碑消费”。
  - 如果不先冻结 placement correctness，后续继续补 candidate visibility 或 owner traceability 仍会留下“形式合规、实际悬空”的治理漏口。
- acceptance_criteria:
  - define a canonical rule that active `needs_research`, `proposed`, and `blocked` candidates must bind to one explicit active milestone rather than `unassigned`
  - define how candidate-declared `milestone:` must match the actual `M-*` section that carries the candidate in `docs/milestones.md`
  - define whether completed milestones may ever accept new unresolved candidates, and freeze the default deny behavior
  - define when a `needs_research` candidate should stay in the current milestone, when it may be rehomed to a later active milestone, and when it should be dropped instead of kept indefinitely
  - define how milestone placement correctness propagates through `C-*`, `M-*`, and `I-*` identities without losing the shared issue-id key
  - freeze the minimum merge-gate and governance-check assertions required to reject wrong-milestone, completed-milestone, and unassigned placement for active candidates
- promotion_gate:
  - keep the first materialized issue focused on merge-gate and milestone-truth enforcement, not a full milestone scheduling redesign
  - prove the active-versus-completed milestone boundary before adding finer-grained sequencing such as sub-milestone numbering
  - treat existing candidate visibility and `C/M/I` checks as dependencies to refine, not as reasons to skip the new owner
- open_questions:
  - should active candidate placement be enforced only in `governance-merge-gate`, or also in `governance-check`
  - should `candidate` legacy status be normalized into the same active-placement rule as `needs_research` and `proposed`
  - how should explicitly rehomed candidates record milestone moves without looking like placement drift
  - what minimum evidence proves that a later milestone will consume a rehomed `needs_research` candidate soon enough to avoid silent long-term parking
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The placement gap was real, and this slice is now narrow enough to materialize: the minimum active-milestone contract is frozen, written back to truth sources, and enforced in both governance gates plus focused tests.`
    verdict: `promote`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/active-milestone-placement-and-consumption-gate-governance/issues/active-milestone-placement-and-consumption-gate-governance.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- expected_outcome:
  - freeze a canonical rule that active unresolved candidates cannot remain `milestone: unassigned`
  - freeze milestone placement correctness as a distinct governance requirement beyond mere milestone visibility
  - freeze a cautious rehome-or-drop rule for `needs_research` candidates that the current milestone has already decided not to consume
  - define how active, completed, and rehomed milestone placement states should be represented without breaking `C/M/I` traceability
  - prepare a narrow owner lane to implement milestone-placement enforcement in the quality gates
- likely_truth_sources:
  - `docs/LAWS.md`
  - `docs/milestones.md`
  - `docs/system/workspace/scripts/quality/governance-check`
  - `docs/system/workspace/scripts/quality/governance-merge-gate`
  - `docs/pre-brainstorms/20260320-0908--research-candidate-persistence-governance/candidates.md`
  - `docs/pre-brainstorms/20260321-1835--lifecycle-complete-before-merge-governance/brainstorms.md`
  - `docs/pre-brainstorms/20260327-1003--prebrainstorm-materialization-audit/brainstorms.md`
- decision_reason:
  - 现有治理已经证明“candidate 必须可见”和“develop merge 需要 `C/M/I` owner 链”都成立，但还不足以防止 candidate 被挂进错误或不会消费的 milestone。
  - 另一个真实缺口是：`needs_research` 即使没有丢失，也可能长期挂在当前不会消费它的 milestone 中；因此 placement correctness 必须连同 rehome-or-drop contract 一起冻结。
  - 当前更大的问题不是排期算法不够精细，而是 active candidate placement 还没有成为硬 gate。
  - 本轮已经把最小 contract 写回 `LAWS`、skills、manager patrol，并落到 `governance-check` / `governance-merge-gate` 与 focused tests，同时纠正了现存 backlog 的真实 placement drift。
  - 因此这条 candidate 不再停留在 `needs_research`，而是提升为独立的 milestone-owned gate owner，继续通过 formal issue 做 verification 与 canonical absorption。
- next_action:
  - keep the promoted owner in `in_verification` until manager merge review absorbs the gate into canonical `develop`
  - verify that candidate, milestone, issue, and progress artifacts now all point to the same active milestone without duplicate candidate placement
  - leave broader scheduling, priority, or automatic rehome mechanics to a later lifecycle if new evidence appears
- revisit_trigger:
  - 当 merge review 发现 placement wording 与其他 truth sources 仍有冲突，或 completed milestone deny / rehome boundary 需要继续扩写时，回到 issue-bound doc-loop；否则在 canonical absorption 后关闭该 owner
