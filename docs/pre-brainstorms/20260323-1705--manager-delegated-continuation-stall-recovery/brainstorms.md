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

## 建议承接位置

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/skills/watchdog-control-plane/SKILL.md`
- 相关 runtime script tests

## 生命周期判断

- 这不是单条 cleanup issue 的业务阻塞
- 这是 Freely 自举中暴露的通用 runtime orchestration gap
- 应先留在 pre-brainstorm / candidate 队列，再根据边界稳定度决定是否 materialize 为独立 issue
