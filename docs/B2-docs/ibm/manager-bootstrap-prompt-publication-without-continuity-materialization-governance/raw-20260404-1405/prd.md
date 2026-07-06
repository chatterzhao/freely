# PRD: manager-bootstrap-prompt-publication-without-continuity-materialization-governance

## Goal

修复 `freely start` 从 manager prompt publication 到 continuity materialization 的控制面真相，让 bootstrap 不再在首个 AI launch 前被 watchdog 误杀，并让 `## Worker Dispatch` 下的 prompt 能被 runtime 识别为可消费的 worker handoff 证据。

## Why Now

这条缺口真实阻断了 Freely 自举中的 manager bootstrap truth。若 prompt 已生成但 continuity / worker handoff 仍显示为 `none`，runtime 会把启动失败、恢复停止与真实 operator stop 混在一起，导致后续 owner 无法在 canonical `develop` 上继续。

## Product Surface

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-manager-continuity-current-worker-prompt-parsing`
- `docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption-current-format`
- `freely live-status`

## Non-Goals

- 不重写整个 watchdog restart policy
- 不泛化 continuity schema 到所有未来 heading 变体
- 不在本 owner 内解决 `auth_failure / primary_rate_limit_exhausted` restart churn

## Non-Negotiables

- bootstrap grace 只能覆盖 `LAST_EXIT_REASON=starting` 的狭窄窗口
- `latest_manager_worker_prompts_generated` 不得在已有可消费 prompt 时继续显示 `none`
- runtime truth 必须能解释 manager 是否启动、是否写出 continuity、以及 worker prompt 是否已 materialize

## Decomposition

1. freeze bootstrap race from prompt publication to first AI launch
2. keep bounded startup grace instead of widening generic restart semantics
3. teach runtime continuity parsing to consume `## Worker Dispatch` prompt evidence
4. verify the repaired path on canonical `develop`, then close the owner as completed traceability
