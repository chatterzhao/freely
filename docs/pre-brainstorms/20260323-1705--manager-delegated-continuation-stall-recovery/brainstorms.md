# 预研头脑风暴：manager-delegated-continuation-stall-recovery

## 背景

这轮在 `develop` 上做 Freely 自举端到端 dogfood 时，主管已经收到 cleanup continuation，并把它吸收到当前 prompt：

- `freely chat` 成功写入 human interruption intake
- interruption manager 成功把它 claim / delegate 成 `handoff://cleanup`
- 最新 manager prompt 明确包含 `Delegated continuation handoff`

但随后 runtime 暴露出新的假活断点：

- manager AI 进程仍然存活
- cycle log 长时间不再更新
- 没有新的 manager continuity
- 没有新的 worker handoff / launch state
- cleanup followthrough 因此停在 prompt 内部，外层 control plane 看不到下一跳

## 问题定义

当前 runtime stall detection 只覆盖：

`pending intake` 比 `cycle log` 更新，且 manager AI 长时间无输出

这不足以覆盖更常见的 continuation 假活：

`delegated continuation already entered prompt -> manager emits no new continuity / handoff -> AI process still alive`

如果没有更硬的 runtime-owned stall contract，Freely 会把“进程还活着”误判成“自治还在推进”，无法完成从 worktree 创建、交接、cleanup 到 retirement 的闭环。

## 候选方向

1. 把 `delegated continuation already entered prompt` 视为可监督状态，而不是纯会话内部细节
2. 若 prompt 已含 delegated continuation，且超过阈值没有新的 manager continuity / worker handoff，runtime 应触发 recovery
3. 保留现有 `pending intake > cycle log` 检测，两条 stall contract 并存
4. 这条能力属于 runtime control plane，不应只留在一次性 dogfood 结论里

## 当前证据收敛

- `freely live-status` 已能稳定暴露：
  - `current_prompt_has_delegated_continuation=1`
  - `latest_manager_worker_prompts_generated=none`
  - `last_consumed_delegated_continuation_ids=none`
- `docs/system/workspace/scripts/runtime/freely` 已有专门的
  - `manager_ai_stalled_after_delegated_continuation_prompt`
  - `recover_stalled_manager_ai_if_needed`
- `docs/system/workspace/skills/watchdog-control-plane/SKILL.md` 已把这条 contract 写成 runtime watchdog 的职责边界
- `docs/system/workspace/scripts/tests/test-freely-manager-delegated-continuation-stall-recovery`
  与 `docs/system/workspace/scripts/tests/test-freely-manager-generated-handoff-stall-recovery`
  已覆盖：
  - prompt 已吸收 delegated continuation 但无新 continuity / handoff 的 recovery
  - prompt 之后已有新 continuity / worker prompt 但 launch-state 仍停旧锚点的 recovery

## continuity guard writeback

- 本轮由 `fresh_with_handoff` 重新进入，直接原因是上一轮 `codex` 会话命中 `context_compacted`
- 当前 worker 工位重新核对后，`live-status` 仍显示：
  - `role_hint: worker`
  - `last_rotation_reason: context_compacted`
  - `current_prompt_has_delegated_continuation: 1`
  - `pending_delegated_continuation_ids` 与 `last_consumed_delegated_continuation_ids` 对齐，说明 delegated continuation 已被吸收，但没有新的 canonical artifact 接管这条线
- 当前仓库扫描未发现 `docs/progress/**`、`docs/epics/**` 或其他 issue/progress/recovery 真源已经接管本候选；因此这轮 continuity 仍应写回 pre-brainstorm，而不是误切到 IBM、dev-loop 或 recovery
- 当前分支 `feature/manager-delegated-continuation-stall-materialization-20260323` 仍未被 `develop` 吸收；这说明 worktree cleanup 与 candidate materialization 仍应分开判断，不能因为已有 canonical writeback 提交就把该候选视为已关闭

## 与相邻 issue 的边界

- 不吸收到 `runtime-worker-launch-linkage-and-stall-recovery-governance`
  - 该 issue 冻结的是 `pending intake > cycle log` 的 stalled-AI recovery，与 manager prompt 已吸收 continuation 之后的假活不同
- 不吸收到 `latest-manager-continuity-worker-consumption-governance`
  - 该 issue 关注“已经生成了新的 continuity / prompt set，但 worker 仍消费旧轮次”
  - 当前候选关注的是“manager prompt 已吸收 delegated continuation，但没有继续产出新的 continuity / handoff”
- 不吸收到 `worker-active-reentry-for-manager-delegated-continuation-governance`
  - 该 issue 关注 worker 已活着时如何消费 delegated continuation，不覆盖 manager 侧 prompt absorption 后的 stalled manager AI

## 当前判断

- 这条 contract 已经从“模糊现象”收敛为“可描述、可测试、可观测”的 runtime gap
- 但本轮仍不直接 materialize：
  - 仓库里已有 runtime / skill / test 证据，但尚未形成 milestone-owned issue 真源
  - 仍需再做一轮真实 dogfood，确认该 contract 在 cleanup / retirement followthrough 上稳定，不会被吸收到更大的 manager recovery 家族
- 因此当前继续保留在 `pre-brainstorm`
  - route_kind: `pre_brainstorm`
  - target_skill: `workspace/skills/doc-pre-brainstorm-execution/SKILL.md`
  - next_recommended_route: `doc-pre-brainstorm-execution`

## 建议承接位置

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/skills/watchdog-control-plane/SKILL.md`
- 相关 runtime script tests

## 生命周期判断

- 这不是单条 cleanup issue 的业务阻塞
- 这是 Freely 自举中暴露的通用 runtime orchestration gap
- 应先留在 pre-brainstorm / candidate 队列，再根据边界稳定度决定是否 materialize 为独立 issue
- 下一次重判重点：
  - 真实 dogfood 是否再次命中相同假活
  - runtime patch 是否把 cleanup / retirement followthrough 稳定推进到可关闭
  - 是否出现一个更高层的 manager recovery issue 能自然吸收这条 contract，而不是事后硬并
