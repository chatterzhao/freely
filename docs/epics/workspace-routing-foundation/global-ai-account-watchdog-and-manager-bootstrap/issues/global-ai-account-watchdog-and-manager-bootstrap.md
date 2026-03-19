# Issue: global-ai-account-watchdog-and-manager-bootstrap

- issue_id: `I-20260318-1630`
- title: Global AI account watchdog and manager bootstrap
- phase_state: `in_verification`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `global-ai-account-watchdog-and-manager-bootstrap`
- issue-name: `global-ai-account-watchdog-and-manager-bootstrap`
- source_candidate: `docs/pre-brainstorms/20260318-1630--global-ai-account-watchdog/candidates.md#c-20260318-a`
- source_brainstorm: `docs/pre-brainstorms/20260318-1630--global-ai-account-watchdog/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `docs/epics/workspace-routing-foundation/manager-self-supervision-and-autonomous-recovery/issues/manager-self-supervision-and-autonomous-recovery.md`
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}]

## Why

Freely 现在已经开始区分 manager、worker 和 runtime，但还缺最上层的全局恢复链：

- 当当前全局 Codex 账号不可用时，任何新的 AI 进程都起不来
- 这类恢复不应依赖 manager AI 或 worker AI
- Freely 需要纯脚本先切号，再拉起主管；主管恢复后再监督所有工位

## Scope

1. 物化 `global watchdog` 的正式职责边界。
2. 提供 CLI-first 的主管拉起入口，例如 `freely ensure-manager`。
3. 把全局账号恢复与主管拉起从 manager/worker 职责中剥离出来。
4. 提供一条 live 集成测试脚本，验证：
   - 先由脚本自己探测当前可用账号并启动监控/主管链
   - 监控链已运行后，故意切到不可用账号
   - 当前 AI 进程结束后，由 watchdog 负责恢复；不要把恢复动作交给 AI
   - 每次切号后都由脚本重新拉起新的 Codex 进程，并优先 `resume` 恢复会话
   - 最终自动切回脚本真实探测出的可用账号并恢复主管；若所有账号都不可用，则切到最早恢复账号并等待唤醒
5. 在 watchdog 拉起主管前，写入结构化 handoff，说明：
   - 哪个账号触发了 limit/不可用
   - 当前切到了哪个账号
   - 这次是立即恢复还是等待最早 reset 后恢复
   - 主管起来后优先检查哪些工位、该先判定 resume 还是 fresh_with_handoff

## Acceptance

- 文档明确区分三类 AI powerless 场景及其 owner。
- 至少存在一个纯脚本入口，可在没有任何 AI 帮助时恢复账号并拉起主管。
- live 集成测试脚本能验证“切到坏账号后自动切回好账号”的真实链路。
- live 集成测试脚本在未显式给出好账号时，也能通过真实 probe 发现当前可用账号。
- live 集成测试脚本能验证“切号 -> 新 Codex 进程启动 -> resume/续接 -> 继续监督”的真实链路。
- 主管恢复后继续只承担监督和委派，不接管全局账号切换。
- watchdog 在拉起主管前会写结构化恢复交接，而不是让主管盲启动。

## Completion

- `docs/pre-brainstorms/20260318-1630--global-ai-account-watchdog/*`
- `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
- `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/tasks.md`
- `docs/system/workspace/scripts/tests/test-freely-global-account-watchdog-live`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/runtime/ai-cli`

## Verification

- 当前验证重点：
  - `freely ensure-manager` 是否是纯脚本，不依赖 AI
  - 当当前账号不可用时，是否能自动切到可用账号并拉起主管
  - 当 cooldown 账本过时或错误时，是否会真实 probe 所有已保存账号，而不是盲信旧账本
  - live 测试是否能覆盖两个坏账号回切到一个好账号的真实链路
- 最新验证事实：
  - 官方帮助中心与 rate-limit 文档没有提供“多个本地保存 Codex 账号当前可用性查询”的直接接口，因此 Freely 采用脚本真实 probe 方案
  - `test-ai-cli-switch-default-tool` 已覆盖默认 `codex` 切号 UX 与切后真实账号校验
  - `test-freely-ensure-manager` 已覆盖“先选可用账号再拉主管”的脚本回归
  - `freely ensure-manager` 当前在 watchdog 拉起主管前，会写 manager bootstrap handoff，告知 limit/切号/恢复原因及主管优先检查面
  - `test-freely-global-account-watchdog-live` 已真实通过：
    - `worahe3972@outlook.com -> worahe3971@outlook.com`
    - `worahe3973@outlook.com -> worahe3971@outlook.com`
  - live 测试口径已收紧为：监控脚本先启动，切到坏账号后等待当前 AI 进程结束，再验证 watchdog 是否切回脚本真实探测出的可用账号并拉起新 Codex

## Next

- 进入 completion verification，准备与 manager 自治主线一起评审，并决定是否并回 `develop`。
