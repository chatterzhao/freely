# Pre-tests: global-ai-account-watchdog-and-manager-bootstrap

## Acceptance target

1. Freely 对 Codex 恢复的 canonical contract 以 `.ai-auth/<slot>` 与实时 probe 为唯一恢复真相；`cooldown` 不再用于任何恢复逻辑。
2. 当前 slot 遇到 `rate limit`、`deactivated_workspace`、auth failure / invalid auth file、slot probe failure 时，runtime/watchdog 会统一进入 failure-driven full slot sweep。
3. 一旦进入 slot sweep / reprobe 窗口，所有 manager / worker / AI launch 都必须被阻塞，直到 watchdog 明确找到可用 slot。
4. 只有真实 probe 证明某个 slot 当前可用后，watchdog 才允许把该 slot 的授权文件切进真实 Codex 工作位并继续 manager / worker 恢复。
5. 当所有保存 slot 都不可用时，恢复链会进入 all-unavailable hold：watchdog 保持存活与可观察，但 manager / worker 持续保持 down；恢复仅由低频真实 probe 或 inventory 变化命中 usable slot 后触发。
6. 恢复发生时必须先写结构化 handoff，再唤醒主管；handoff 需说明 blocked reason、wake trigger、previous slot 和 active slot。
7. 这条恢复 contract 由纯脚本 watchdog / runtime 完成，不依赖 manager AI 或 worker AI 的语义判断。
8. `whoami` / `switch` / `status` / `save` / `login` 的 CLI contract 必须以 slot 为唯一 identity；邮箱等内容只允许作为 `auth_email` 元数据出现，不能再冒充当前身份。

## Testing layers

1. Doc-loop gate
   - `issues/`, `tasks.md`, `progress`, `milestones.md`, `watchdog-control-plane` skill、`runtime/freely`、`ai-cli` 的能力说明，对 slot-sweep-first contract 保持一致。
2. Script regression gate
   - focused tests 必须覆盖 failure taxonomy 到 full slot sweep 的统一路由，并锁住 probe 窗口内的 no-launch gate。
3. Runtime integration gate
   - `freely ensure-manager` 与 `freely ai switch codex` 必须共享同一套 slot probe / switch 主路径，并共享同一套 no-launch gating truth。
4. Real-environment gate
   - live 验收必须证明：当前活跃 slot 失效后，watchdog 能扫到另一个真实可用 slot 并恢复监督；若所有 slot 都不可用，仍保持 no-launch hold，并在 inventory 变化或后续真实 probe 命中 usable slot 后再恢复。

## Target environments

1. dedicated feature worktree 中的 focused shell regressions
2. 临时 project sandbox 中的 `freely ensure-manager` / `freely start` 最小集成验证
3. canonical develop 环境中的 live replay / dogfood evidence

## Required evidence

1. 至少一条 focused regression 明确锁住 `rate limit -> full slot sweep -> no-launch until usable slot`。
2. 至少一条 focused regression 明确锁住 `deactivated_workspace -> full slot sweep -> no-launch until usable slot`。
3. 至少一条 focused regression 明确锁住 `auth failure / invalid auth file -> full slot sweep -> no-launch until usable slot`。
4. 至少一条 focused regression 明确锁住 `all slots unavailable -> watchdog alive + manager down + low-frequency reprobe`。
5. 至少一条 focused regression 或最小集成验证明确锁住 `.ai-auth` inventory 变化会触发重新检查，并在恢复前写 handoff。
6. `watchdog-control-plane`、`runtime/freely`、`ai-cli` 的真源说明不再把 cooldown 描述为任何恢复逻辑 owner。
7. 至少一条 focused regression 明确锁住 `whoami` / `switch` 的输出以 slot 为 identity，并允许 `auth_email` 与 slot 名不一致而不被误解释为当前身份漂移。
8. live evidence 能说明真实 `.ai-auth/<slot>` inventory 与实际 probe/switch/no-launch 行为一致。
9. 至少一条 focused regression 明确锁住 “manager `auth_failure` 后 watchdog control-plane 仍存活并继续接管恢复”。
10. 至少一条 focused regression 明确锁住 “interruption dispatcher 未 ready 时 `freely start` 会 fail fast”。
11. 至少一条 focused regression 明确锁住 “watchdog + dispatcher 仍存活时，`live-status` 不会误报 `stalled_without_runtime`”。
12. 至少一条 focused regression 明确锁住 “slot probe timeout 会把 partial probe output 落到 `.freely/run` 可追踪 artifact”，便于区分网络慢、CLI 卡死、还是 `402 deactivated_workspace` 已经返回但被 timeout 截断。
13. 至少一条 focused regression 明确锁住 “全局 slot switch lock 活跃时，新的 Codex launch / ensure-manager bootstrap 会等待，不会穿透 no-launch gate 抢跑”。
14. 至少一条 focused regression 明确锁住 “warning / debug wording 不会污染 machine-readable slot fields”，避免 `whoami` / `status` 的 slot identity 被文本提示覆盖。
15. 至少一条 focused regression、最小集成验证或 live replay 证明 “第一个恢复后的新 Codex launch 使用的是 watchdog 刚刚 probe 成功的 usable slot”，不会命中旧 `402` / 旧 auth。
16. 至少一条 focused regression 明确锁住 “`deactivated_workspace` 一旦在 probe 输出中尽早出现，就会优先被识别并进入 full slot sweep”，而不是继续等到 generic timeout 或下一轮恢复。

## Latest focused verification

1. `test-ai-cli-whoami-prefers-slot-identity` pass，锁住 slot-first identity 与 `auth_email` 元数据分离。
2. `test-freely-ai-account-switch` pass，锁住 auto-probe、usable-slot 切换与 `all_unavailable` no-launch gate。
3. `test-freely-ensure-manager` pass，锁住 manager bootstrap 前的真实 probe 和 handoff 写回。
4. `test-freely-ensure-manager-earliest-reset-wait-revive` pass，锁住 all-unavailable hold、低频 reprobe、以及后续 wake。
5. `test-freely-ensure-manager-inventory-change-wakes-watchdog` pass，锁住 `.ai-auth` inventory 变化 wake contract。
6. `test-freely-auth-failure-keeps-control-plane-alive` pass，锁住 manager `auth_failure` 后 detached watchdog / dispatcher 继续存活。
7. `test-freely-live-status-watchdog-survival` 与 `test-freely-live-status` pass，锁住 watchdog-only control-plane 不再误报 `stalled_without_runtime`。
8. `test-freely-start-requires-interruption-dispatcher-ready` pass，锁住 dispatcher 未 ready 时的 fail-fast gate。
9. `test-freely-codex-probe-timeout-artifact` pass，锁住 timeout / deactivated workspace probe output artifact 写回。

## Blocker taxonomy

1. `definition_missing`
   - story 真源仍混用 account/cooldown 与 slot/probe/no-launch 两套恢复 contract。
2. `commands_only`
   - 只有命令清单，没有写清 acceptance target、failure taxonomy、目标环境和 required evidence。
3. `evidence_plan_missing`
   - 缺少对 `deactivated_workspace`、auth failure、all-slots-unavailable、inventory-change wake 任一关键 path 的明确验收面。
4. `execution_pending_or_failed`
   - pre-tests 定义已齐，但 focused regression、integration、或 live evidence 尚未执行或未通过。

## Non-goals

1. 不要求本 issue 删除所有 cooldown 相关 artifact；允许保留 debug / observability 输出，但不得参与恢复逻辑。
2. 不要求本 issue 改变 `.ai-auth/<slot>` 的 login 命名约定；该 contract 已由 slot-only 语义承接。
3. 不要求 manager AI 参与 slot 可用性判定；恢复 owner 仍是脚本 watchdog / runtime。
