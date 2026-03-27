# 候选：oauth-api-usage-query-refactor

- id: `C-20260327-1115-A`
- title: Promote OAuth parallel sweep to canonical slot inventory truth
- source_brainstorm: `docs/pre-brainstorms/20260327-1115--oauth-api-usage-query-refactor/brainstorms.md`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- decision_reason:
  - 当前本机实测已经证明 `wham/usage` 可以在约 3.7 秒内并行扫描 25 个 `.ai-auth` slots，且不触碰 `~/.codex/auth.json`
  - sweep 返回不只包含 `usable` / `rate_limited`，还直接暴露了大量 `deactivated_workspace`，因此它已经具备承担 inventory truth 的能力潜力
  - 这已经超出已完成 `I-20260318-1630` 的 closeout contract，应以新的 follow-on lifecycle 物化，而不是继续把旧 completed issue 当作 reopen owner
- promoted_issue_path: `docs/epics/workspace-routing-foundation/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance/issues/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- why_now:
  - 旧的全量串行 probe 既慢又消耗 token，还会在扫描阶段反复复制授权文件到 `~/.codex/auth.json`
  - 新的 OAuth usage 路径已经证明可以直接扫 `.ai-auth` inventory，并把全量 slot 状态一次性覆盖写回
  - 这让恢复 cooldown ledger、维护 30 分钟周期 sweep、以及把真实 auth 切换推迟到 launch-time 成为可行重构方向
- expected_outcome:
  - freeze a canonical `codex_oauth_sweep_all_slots` entrypoint shared by watchdog, `freely ai status`, and `switch codex auto`
  - restore `codex-slot-cooldowns.tsv` as a sweep-driven ledger instead of passive residue
  - keep real auth copy / final confirmation only at launch-time, not during inventory scan
- likely_truth_sources:
  - `docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh`
  - `docs/system/workspace/scripts/runtime/ai-cli`
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
  - `.freely/run/codex-slot-cooldowns.tsv`
  - `.freely/run/codex-availability-state.env`
- next_action:
  - 当前 pre-brainstorm 已完成 materialization judgement；后续由 `I-20260327-1115` 承接 issue-bound IBM 与 dev-loop，实现 OAuth sweep、availability cache、cooldown overwrite 和 launch-time confirmation 分层
- revisit_trigger:
  - if implementation proves `wham/usage` unstable or insufficient for inventory truth, fall back to keeping it as supporting evidence instead of canonicalizing the refactor
