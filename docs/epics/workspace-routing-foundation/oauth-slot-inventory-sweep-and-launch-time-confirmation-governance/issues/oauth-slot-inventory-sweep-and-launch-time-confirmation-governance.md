# Issue: oauth-slot-inventory-sweep-and-launch-time-confirmation-governance

- issue_id: `I-20260327-1115`
- title: OAuth slot inventory sweep and launch-time confirmation governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `oauth-slot-inventory-sweep-and-launch-time-confirmation-governance`
- issue-name: `oauth-slot-inventory-sweep-and-launch-time-confirmation-governance`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance/code-reviews`
- priority: P0
- source_candidate: `docs/pre-brainstorms/20260327-1115--oauth-api-usage-query-refactor/candidates.md#c-20260327-1115-a`
- source_brainstorm: `docs/pre-brainstorms/20260327-1115--oauth-api-usage-query-refactor/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`

## Why

`I-20260318-1630` 已完成的 canonical contract 建立了：

- failure-driven slot sweep
- no-launch gate
- all-unavailable hold
- slot-first identity

但它同时也把“真实 probe 才是 inventory truth、cooldown 不参与恢复逻辑”冻结成已完成边界。

本轮新证据已经证明，OpenAI 的 `wham/usage` OAuth query 能直接基于 `.ai-auth/codex-*/auth.json` 中的 token 并行扫描 slot inventory：

- 不消耗 token
- 不需要复制授权文件到 `~/.codex/auth.json`
- 能在约 3.7 秒内扫完本机 25 个 slot
- 不只返回 quota，还能直接暴露 `deactivated_workspace`

这不是给旧 watchdog issue 加一条 supporting evidence，而是要把 inventory truth / cooldown ledger / launch-time confirmation 的职责重新分层。因此它应作为同族 follow-on lifecycle 承接，而不是回写到已经 closeout 的 `I-20260318-1630`。

## Scope

1. 定义 `codex_oauth_sweep_all_slots` 作为新的 canonical inventory sweep 入口，供 watchdog、`freely ai status` 与 `freely ai switch codex auto` 共用。
2. 把 `.ai-auth/codex-*/auth.json` 从“仅供切换时复制的备份目录”提升为可并行扫描的 slot inventory truth source。
3. 恢复并重定义 `codex-slot-cooldowns.tsv`：
   - 由 OAuth full sweep 覆盖写回
   - 保存 rate-limit reset 与 slot 状态账本
   - 不再单独决定切号
4. 增加或强化 availability cache，使 watchdog / status / switch 共享同一份 machine-readable sweep 结果，而不是各自重扫。
5. 将真实 auth copy 与最小真实 probe 降级为 launch-time confirmation，只在最终决定切换/拉起目标 slot 时触发。

## Non-Goals

1. 不重开 `I-20260318-1630` 的历史 closeout judgement。
2. 不把 OAuth sweep 直接等同于所有 exec-path 健康检查；真实 launch-time confirmation 仍需保留。
3. 不在本 issue 同时扩写新的 scheduler、公平性或 quota 策略。
4. 不把 `.freely/run/codex-slot-cooldowns.tsv` 再升级回独立恢复真相源。

## Acceptance

1. 存在统一的 OAuth inventory sweep 入口，能够并行扫描 `.ai-auth/codex-*/auth.json`，且扫描期间不触碰 `~/.codex/auth.json`。
2. watchdog、`freely ai status`、`freely ai switch codex auto` 共用同一份 availability cache / sweep 输出，而不是各写一套 slot 判定逻辑。
3. `codex-slot-cooldowns.tsv` 由 full sweep overwrite 写回，rate-limited slot 的 reset 信息可被保留为账本与排序 hint，但不再单独驱动切换。
4. `deactivated_workspace`、`rate_limited`、`usable` 与 OAuth query 异常至少要在 inventory 层被明确分类，并进入统一 cache surface。
5. 只有在最终选定 candidate slot 进行 switch / launch 时，才允许复制授权文件到 `~/.codex/auth.json` 并做最小真实确认。
6. focused regression 至少覆盖：
   - OAuth sweep 不修改当前活跃 auth
   - cooldown ledger 被 sweep overwrite，而不是增量残留
   - `switch codex auto` 与 watchdog recovery 都先消费 sweep 结果，再进入 launch-time confirmation

## Completion

- `docs/epics/workspace-routing-foundation/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance/issues/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance.md`
- `docs/epics/workspace-routing-foundation/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance/tasks.md`
- `docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh`
- `docs/system/workspace/scripts/runtime/ai-cli`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-ai-account-switch`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager`
- `docs/system/workspace/scripts/tests/test-freely-rate-limit-defers-to-watchdog`

## Verification

- `./bin/governance-check`
- `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch`
- `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager`
- `bash docs/system/workspace/scripts/tests/test-freely-rate-limit-defers-to-watchdog`
- `bash docs/system/workspace/scripts/tests/test-ai-cli-switch-default-tool`
- `docs/epics/workspace-routing-foundation/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance/code-reviews/20260327-oauth-sweep-launch-confirmation-verification.md`
