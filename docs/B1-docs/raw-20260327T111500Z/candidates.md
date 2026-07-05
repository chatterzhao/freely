# 候选：oauth-api-usage-query-refactor

- id: `C-20260327T111500Z-A`
- title: Rebuild limit recovery around OAuth-backed inventory truth and earliest-reset sleep
- source_brainstorm: `docs/B1-docs/raw-20260327-1115/brainstorms.md`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- decision_reason:
  - 当前本机实测已经证明 `wham/usage` 可以在约 3.7 秒内并行扫描 25 个 `.ai-auth` slots，且不触碰 `~/.codex/auth.json`
  - 但这条 lane 的真正 owner 问题不是“接 OAuth API”，而是把 `limit -> switch usable -> otherwise earliest-reset sleep -> wake -> continue` 的恢复闭环写成 canonical contract
  - `cooldown` 需要被升级成半小时维护的 recovery ledger reset 面，而不是临时残留；命中 limit 时必须先吃这份账本快速切换
  - 无参 `switch codex` 也应刷新所有 auth 目录并直接切一个可用 slot；这已经超出已完成 `I-20260318T163000Z` 的 closeout contract，应以新的 follow-on lifecycle 物化
- promoted_issue_path: `docs/B2-docs/ibm/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance/issues/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance.md`
- legacy_id_mapping: I-20260327T111500Z  # 历史遗留的 issue id
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- why_now:
  - 旧路径没有把 `usable` 优先级、`sleep` 的前提、以及 `.codex` parking/wake 语义钉死，limit 恢复仍然容易混乱
  - OAuth usage 路径已经证明可以低成本提前知道哪些 auth 现在可用、哪些最早恢复，因此适合承担 inventory truth
  - 只有先把恢复状态机写清楚，OAuth sweep、cooldown ledger、active auth switch 才不会各自变成半套逻辑
- expected_outcome:
  - freeze a canonical recovery contract: `limit -> usable switch -> otherwise earliest-reset sleep -> wake -> continue`
  - freeze a canonical `codex_oauth_sweep_all_slots` entrypoint shared by watchdog, `freely ai status`, and `switch codex auto`
  - restore `codex-slot-cooldowns.tsv` as the reset face of a continuously maintained recovery ledger
  - make no-arg `switch codex` refresh all saved auth directories and directly replace `~/.codex/auth.json` with a chosen usable slot
  - define `.codex` changes as either `usable switch` or `earliest-reset parking`, so watcher behavior cannot self-loop
- likely_truth_sources:
  - `docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh`
  - `docs/system/workspace/scripts/runtime/ai-cli`
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/B2-docs/ibm/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
  - `.freely/run/codex-slot-cooldowns.tsv`
  - `.freely/run/codex-availability-state.env`
- next_action:
  - 当前 pre-brainstorm 已完成 materialization judgement；后续由 `I-20260327T111500Z` 承接 issue-bound IBM 与 dev-loop，先重写 recovery state machine，再收紧 30 分钟 ledger maintenance、switch-on-demand refresh、parking sleep 和 launch-time continuation
- revisit_trigger:
  - if implementation proves `wham/usage` unstable or insufficient for inventory truth, keep it as supporting inventory evidence and preserve the same recovery contract with a different signal source
