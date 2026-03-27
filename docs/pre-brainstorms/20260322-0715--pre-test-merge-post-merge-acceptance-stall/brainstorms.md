# 预研头脑风暴：pre-test-merge-post-merge-acceptance-stall

## 兼容说明

- 本预研目录与历史候选名继续保留 `pre-test-merge` 命名，避免破坏既有留痕与引用。
- 当前 canonical 语义已经改成 `test-pre-merge-*` 测试批次前缀族；下文出现的 `pre-test-merge` 都按这个前缀族理解，而不是单例长期分支。

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

## 2026-03-24 followthrough narrowing

在 `develop` 上继续 dogfood `I-20260322-0445` 的 post-merge acceptance 后，又出现了相同形态的现场：

- delegated continuation 已进入 manager prompt
- `current_prompt_has_delegated_continuation=1`
- 最新 continuity 仍停在更早一轮
- 新 prompt 明确要求产出新的 manager continuity / worker prompt artifact

但这轮不能草率判成“runtime recovery 已失效”，因为现场时间点更细后显示：

- `prompt-20260324-030820.txt` mtime: `2026-03-24 03:08:26 PDT`
- `cycle-20260324-030820.log` mtime: `2026-03-24 03:09:45 PDT`
- 人工停止 root runtime 前仅到 `03:11` 出头

也就是说，这轮只走到了 watchdog `90s` stall threshold 的边缘，还不足以证明“超过阈值后 runtime 仍未恢复”。因此这次 followthrough 不能直接 materialize 为 runtime patch；先收窄 contract，再继续用真实 dogfood 验证。

## 问题定义

这不是 `0445` 的“latest continuity consumption”实现本身失效，而是新的 post-merge acceptance 断点：

`pre-test-merge manager receives delegated acceptance continuation -> prompt contains handoff -> manager never emits next continuity / decision`

## 候选方向

1. 明确 `pre-test-merge` 主管在 post-merge acceptance 中的完成阈值
- 不能无限停留在“继续读治理真源”。

2. 定义 delegated manager continuation 的 watchdog stall gate
- 若 prompt 已含 delegated continuation 且超过阈值仍无新 continuity，应触发 recovery / reroute。
- stall 判据必须看 manager 是否在 bounded time 内写出新的 continuity / decision；不能把“是否存在 launchable worker prompt”误当作必要条件。

3. 区分“AI 正在合理长跑”与“AI 已经进入 acceptance stall”
- 需要更硬的 evidence，而不是只看进程活着。

4. 区分“真实 stall”与“尚未超过 watchdog 阈值的慢轮次”
- 若 cycle log 仍在刷新，或距离最后 prompt / cycle 写入尚未超过阈值，不能提前把现场判成 runtime bug。

## 建议承接位置

- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- `docs/system/workspace/skills/multi-worktree-supervision/SKILL.md`
- `docs/system/workspace/scripts/runtime/freely`

## 生命周期判断

- 这不是历史 closeout
- 这是 `0445` post-merge acceptance 发现的新 runtime/acceptance gap
- 应进入新的 issue 生命周期，不应回写 `0445` 的已实现 scope

## 当前最小 contract

1. manager prompt 已含 delegated continuation
2. prompt / cycle log 都已超过 stall threshold
3. 在该阈值窗口内没有出现更晚的 manager continuity / decision artifact
4. 是否有 launchable worker prompt 不影响 stall 判定；那是派工库存判断，不是 manager 前进与否的判据

只有同时满足 1-3 时，才应把现场判成 delegated acceptance stall。

## Reroute decision

- The governance boundary part of this finding now depends on:
  - `pending://pre-test-merge-responsibility-usage-and-lifecycle-governance-materialization`
- That governance issue owns:
  - `pre-test-merge` role boundaries
  - stale/retire/rebuild semantics
  - promote vs replay rules
- This `0715` lifecycle remains independently active because its core gap is narrower and more runtime-specific:
  - delegated acceptance continuation has entered the manager prompt
  - but the manager does not emit the next continuity/decision in bounded time
- Therefore this worktree should not be retired or absorbed wholesale; it should continue as a rerouted, dependency-aware candidate.
