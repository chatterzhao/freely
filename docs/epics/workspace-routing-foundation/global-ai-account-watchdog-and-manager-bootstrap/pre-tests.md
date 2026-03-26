# Pre-tests: global-ai-account-watchdog-and-manager-bootstrap

## Acceptance target

1. Freely 对 Codex 恢复的 canonical contract 以 `.ai-auth/<slot>` 为唯一调度身份，不再用 account 或 cooldown ledger 充当主恢复真相。
2. 当前 slot 遇到 `rate limit`、`deactivated_workspace`、auth failure / invalid auth file、slot probe failure 时，runtime/watchdog 会统一进入 failure-driven full slot sweep。
3. 只有真实 probe 证明某个 slot 当前可用后，watchdog 才允许把该 slot 的授权文件切进真实 Codex 工作位并继续 manager / worker 恢复。
4. 当所有保存 slot 都不可用时，恢复链会进入低频真实 reprobe；`earliest reset` 最多作为 debug evidence 或排序提示，不再主导恢复决策。
5. 这条恢复 contract 由纯脚本 watchdog / runtime 完成，不依赖 manager AI 或 worker AI 的语义判断。
6. `whoami`/`switch`/`status`/`save`/`login` 的对外契约必须以 slot 为唯一身份，auth email 仅作为 `auth_email` 元数据暴露。
7. manager 因 `auth_failure` 退出后，detached `ensure-manager --watch` 与 interruption dispatcher 仍必须留在控制面继续恢复和消化 intake，不能一起掉光。

## Testing layers

1. Doc-loop gate
   - `issues/`, `tasks.md`, `progress`, `milestones.md`, `watchdog-control-plane` skill、`runtime/freely`、`ai-cli` 的能力说明，对 slot-sweep-first contract 保持一致。
2. Script regression gate
   - focused tests 必须覆盖 failure taxonomy 到 full slot sweep 的统一路由，而不是只验证 cooldown 写回。
3. Runtime integration gate
   - `freely ensure-manager` 与 `freely ai switch codex` 必须共享同一套 slot probe / switch 主路径。
   - `freely start` 在 manager 触发 `auth_failure` 后，控制面进程仍需存活并可被 `freely stop` 清理。
4. Real-environment gate
   - live 验收必须证明：当前活跃 slot 失效后，watchdog 能扫到另一个真实可用 slot 并恢复监督；若所有 slot 都不可用，也不会因为旧 cooldown 账本而错误睡死或错误判可用。

## Target environments

1. dedicated feature worktree 中的 focused shell regressions
2. 临时 project sandbox 中的 `freely ensure-manager` / `freely start` 最小集成验证
3. canonical develop 环境中的 live replay / dogfood evidence

## Required evidence

1. 至少一条 focused regression 明确锁住 `rate limit -> full slot sweep`。
2. 至少一条 focused regression 明确锁住 `deactivated_workspace -> full slot sweep`。
3. 至少一条 focused regression 明确锁住 `auth failure / invalid auth file -> full slot sweep`。
4. 至少一条 focused regression 明确锁住 `all slots unavailable -> low-frequency reprobe`，并证明 `earliest reset` 不是主恢复 gate。
5. `watchdog-control-plane`、`runtime/freely`、`ai-cli` 的真源说明不再把 cooldown 描述为 canonical recovery owner。
6. live evidence 能说明真实 `.ai-auth/<slot>` inventory 与实际 probe/switch 行为一致。
7. 至少一条 focused regression 明确锁住 “slot 标签与 auth email 不一致时，CLI 仍以 slot 为身份、仅把 email 作为 metadata”。
8. 至少一条 focused regression 明确锁住 “manager `auth_failure` 后 watchdog control-plane 仍存活并继续接管恢复”。

## Blocker taxonomy

1. `definition_missing`
   - story 真源仍混用 account/cooldown 与 slot/sweep 两套恢复 contract。
2. `commands_only`
   - 只有命令清单，没有写清 acceptance target、failure taxonomy、目标环境和 required evidence。
3. `evidence_plan_missing`
   - 缺少对 `deactivated_workspace`、auth failure、all-slots-unavailable 任一关键 failure path 的明确验收面。
4. `execution_pending_or_failed`
   - pre-tests 定义已齐，但 focused regression、integration、或 live evidence 尚未执行或未通过。

## Non-goals

1. 不要求本 issue 删除所有 cooldown 相关 artifact；允许保留 debug / observability 输出。
2. 不要求本 issue 改变 `.ai-auth/<slot>` 的 login 命名约定；该 contract 已由 slot-only 语义承接。
3. 不要求 manager AI 参与 slot 可用性判定；恢复 owner 仍是脚本 watchdog / runtime。
