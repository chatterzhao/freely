# PRD: active-milestone-placement-and-consumption-gate-governance

## Problem

Freely 已经要求 unresolved candidate 必须持续可见，也已经要求 develop merge 具备 `C/M/I` traceability，但中间还缺一层 placement correctness。只要 candidate 出现在“某个 milestone 队列”里，过去的 gates 就可能放行，即使它仍然是 `unassigned`、落在错误 milestone，或者挂进已经 completed 的 lane。

## Product Decision

第一刀只做最小治理闭环：

1. active candidate 必须绑定一个明确 active milestone
2. unresolved candidate 只能留在 active milestone 的 `candidate_issues`
3. candidate 声明的 `milestone:` 要与 `docs/milestones.md` 的真实承接一致
4. completed milestone 默认拒绝新的 unresolved candidate
5. `needs_research` 必须显式三分：继续留当前 milestone、谨慎后移到更合适的 active milestone、或直接 dropped

## User / Runtime Outcome

- 预研 candidate 不会再因为 `unassigned` / `pending://...` 伪装成已排期
- active milestone 会继续扫描当前真正需要消费的 unresolved candidate
- merge gate 能更早发现“形式可见、实际上不会被消费”的错误放置
- skill/agent 巡检会明确提示 `needs_research` 的 keep / rehome / drop 决策，而不是无限期挂起

## Proof

- gate enforcement in `docs/system/workspace/scripts/quality/governance-check`
- merge-path enforcement in `docs/system/workspace/scripts/quality/governance-merge-gate`
- focused regressions in `docs/system/workspace/scripts/tests/test-governance-check-candidate-v2` and `docs/system/workspace/scripts/tests/test-governance-merge-gate`
- truth-source writeback in `docs/LAWS.md`, milestone-planning / pre-brainstorm skills, and manager patrol guidance
