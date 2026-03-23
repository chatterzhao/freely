# 预研头脑风暴：pre-test-merge-post-merge-acceptance-stall

## 背景

在 `feature/completed-worktree-closeout-merge-prep-20260322` 吸收 `I-20260322-0445` 后，专门创建了 `pre-test-merge` 经理工位做真实 post-merge acceptance：

- `freely start` 成功
- `freely chat` 成功把 `I-20260322-0445` 的验收请求写入 intake
- interruption resolution 成功将其委派为 `continuation`
- 下一轮 prompt 也已包含 delegated continuation handoff

但随后出现新的断点：

- manager AI 进程长时间保持 active
- `manager_continuity_file` 仍未生成
- `last_consumed_delegated_continuation_ids` 仍为空
- 没有进一步产出 acceptance 结论、worker delegation 或新的 lifecycle decision

## 观察证据

- worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/pre-test-merge`
- intake:
  - `20260322-065827-i-20260322-0445-post-merge-accep`
- `live-status` 关键状态：
  - `pending_delegated_continuation_ids=20260322-065827-i-20260322-0445-post-merge-accep`
  - `current_prompt_has_delegated_continuation=1`
  - `manager_continuity_file: none`
  - `latest_manager_continuity_generated: unavailable`
- Codex session evidence:
  - `rollout-2026-03-22T06-58-16-019d15d6-df83-7872-9733-31414c5e2431.jsonl`
  - 最后稳定输出停在读取 `PROJECT_INTENT/CONSTITUTION/milestones/live-status`，之后没有新的治理结论

## 问题定义

这不是 `0445` 的“latest continuity consumption”实现本身失效，而是新的 post-merge acceptance 断点：

`pre-test-merge manager receives delegated acceptance continuation -> prompt contains handoff -> manager never emits next continuity / decision`

## 候选方向

1. 明确 `pre-test-merge` 主管在 post-merge acceptance 中的完成阈值
- 不能无限停留在“继续读治理真源”。

2. 定义 delegated manager continuation 的 watchdog stall gate
- 若 prompt 已含 delegated continuation 且超过阈值仍无新 continuity，应触发 recovery / reroute。

3. 区分“AI 正在合理长跑”与“AI 已经进入 acceptance stall”
- 需要更硬的 evidence，而不是只看进程活着。

## 建议承接位置

- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- `docs/system/workspace/skills/multi-worktree-supervision/SKILL.md`
- `docs/system/workspace/scripts/runtime/freely`

## 生命周期判断

- 这不是历史 closeout
- 这是 `0445` post-merge acceptance 发现的新 runtime/acceptance gap
- 应进入新的 issue 生命周期，不应回写 `0445` 的已实现 scope

## Reroute decision

- The governance boundary part of this finding now depends on:
  - `docs/epics/workspace-routing-foundation/pre-test-merge-responsibility-usage-and-lifecycle-governance/issues/pre-test-merge-responsibility-usage-and-lifecycle-governance.md`
- That governance issue owns:
  - `pre-test-merge` role boundaries
  - stale/retire/rebuild semantics
  - promote vs replay rules
- This `0715` lifecycle remains independently active because its core gap is narrower and more runtime-specific:
  - delegated acceptance continuation has entered the manager prompt
  - but the manager does not emit the next continuity/decision in bounded time
- Therefore this worktree should not be retired or absorbed wholesale; it should continue as a rerouted, dependency-aware candidate.
