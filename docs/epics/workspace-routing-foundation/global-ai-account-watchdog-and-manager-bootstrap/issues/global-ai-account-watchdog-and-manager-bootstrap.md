# Issue: global-ai-account-watchdog-and-manager-bootstrap

- issue_id: `I-20260318-1630`
- title: Global AI account watchdog and manager bootstrap
- phase_state: `in_ibm`
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
   - 先用可用账号启动监控/主管链
   - 监控链已运行后，故意切到不可用账号
   - 最终自动切回可用账号并恢复主管

## Acceptance

- 文档明确区分三类 AI powerless 场景及其 owner。
- 至少存在一个纯脚本入口，可在没有任何 AI 帮助时恢复账号并拉起主管。
- live 集成测试脚本能验证“切到坏账号后自动切回好账号”的真实链路。
- 主管恢复后继续只承担监督和委派，不接管全局账号切换。

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
  - live 测试是否能覆盖两个坏账号回切到一个好账号的真实链路

## Next

- 先保持 `in_ibm`，把正式职责、CLI 入口和 live 集成测试方案收敛清楚。
