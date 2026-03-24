---
name: doc-pre-brainstorm-execution
description: 执行 pre-brainstorm 前置收敛环，负责把新问题收敛为 candidate，并与 milestone 保持原子同步。
---

# skill:doc-pre-brainstorm-execution

## 职责

- 接收原始发现源或仍未稳定的 candidate。
- 在合适的 dedicated worktree 中产出 `brainstorms.md` 与 `candidates.md`。
- 把 candidate 原子同步进 `docs/milestones.md`。
- 明确下一跳是继续 pre-brainstorm，还是进入 `doc-ibm-execution`。
- 三个 loop 下 doc-loop 的整体能力归宿与生命周期细节见 `docs/system/workspace/three-loop-capability-lifecycle.md`。

## 不负责

- 不直接产出正式 issue-bound `IBM` 文档。
- 不直接实现代码、测试或主回写 progress。

## 工作流

1. 写入前先读取 [entry-and-worktree-checks.md](references/entry-and-worktree-checks.md)。
2. 若是首次进入 pre-brainstorm，按 [candidate-recording.md](references/candidate-recording.md) 写 `brainstorms.md`、`candidates.md` 和 `docs/milestones.md`。
3. 若是继续研究 milestone 里的 `candidate_issues`，继续沿用同一 reference 补边界、依赖、下一动作和重启触发条件；若本轮仍不能收口，必须显式保留它的可见状态，而不是跳过。
4. future candidate 默认使用 `candidate_format_version: v2`，并补齐 candidate-level acceptance boundary：
   - `acceptance_criteria`
   - `promotion_gate`
   - `open_questions`
   - `acceptance_reviews`
5. 当 candidate 准备 promotion 时，优先做独立 acceptance review：
   - 至少一个 subagent / fresh process / peer worker pass
   - 若 candidate 会影响 loop placement / owner / canonical artifact / execution base / depends_on，优先多个独立 review pass
   - review 结果写回 `acceptance_reviews`
6. 当边界稳定且 promotion gate 满足后，按 [promotion-handoff.md](references/promotion-handoff.md) 把 candidate 提升到 IBM，并返回最小 issue 上下文包。

## 回流输出

- `status`
- `why`
- `updated_artifacts`
- `next_recommended_route`
- `recovery_context`
- `execution_base`
- `integration_target`
- `depends_on`

## 完成判定

- `brainstorms.md` 与 `candidates.md` 已更新。
- `v2` candidate 的 acceptance boundary 已写清。
- candidate 已同步到 milestone。
- 已明确它继续 pre-brainstorm，还是进入 IBM。
- 若本轮未进入 IBM，已显式标记 `needs_research` / `blocked` 等状态，并写清 `next_action` 与 `revisit_trigger`。
