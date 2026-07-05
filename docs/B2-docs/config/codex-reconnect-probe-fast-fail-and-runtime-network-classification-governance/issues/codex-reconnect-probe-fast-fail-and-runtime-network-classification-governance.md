# Issue: codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance

- issue_id: `I-20260406-0901-A`
- title: Codex reconnect probe fast-fail and runtime network classification governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance`
- issue-name: `codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance`
- priority: `P1`
- source_candidate: `docs/B1-docs/raw-20260406T110500Z/candidates.md#c-20260406-0901-a`
- source_brainstorm: `docs/B1-docs/raw-20260406T110500Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/config/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance.md`
- verification_artifact_dir: `docs/B2-docs/config/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance/code-reviews`
- depends_on:
  - `docs/B2-docs/config/codex-apikey-slot-bundle-and-provider-aware-probe-governance/issues/codex-apikey-slot-bundle-and-provider-aware-probe-governance.md`
  - `docs/B2-docs/runtime/runtime-network-failure-taxonomy-and-bounded-recovery-governance/issues/runtime-network-failure-taxonomy-and-bounded-recovery-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 已经把 Codex API-key slot bundle、provider-aware probe routing、以及 runtime network-failure taxonomy 分别冻结为 canonical contract，但 dogfood 现场仍暴露一个新边界：

- `codex exec "hi"` 已经输出明确的 `ERROR: Reconnecting...` / connection-failure 证据
- probe 仍然继续占着 slot-switch lock 等待完整 timeout
- `ai status` / `ai switch codex` / manager bootstrap 因此把 incident 表现成 generic timeout，而不是 network-local failure

这不是重开旧的 slot bundle owner，也不是重写 runtime recovery state machine。需要一个新的 follow-on owner，专门冻结 “partial-output reconnect evidence -> immediate `network_failure` fast-fail -> runtime/network classification alignment” 这条边界。

## Scope

1. 冻结 Codex probe 在 partial output 中识别 reconnect / connection-failure evidence 的最小 matcher vocabulary。
2. 冻结该 fast-fail 路径的进程清理、artifact 写出、以及 canonical probe status `network_failure`。
3. 冻结 `ai status`、`ai switch codex`、manager bootstrap 对 `network_failure` 的消费语义。
4. 冻结 runtime execution-log network classification 对 Codex reconnect 文本的识别，避免继续落成 generic exit。
5. 明确与旧的 stale-slot / unsaved-live-auth 问题边界：本 owner 不重新吸收 0715 那条已 absorbed 的身份对齐主题。

## Non-Goals

1. 不移除 launch-time probe，也不发明全新的 bootstrap model。
2. 不把 reconnect 误当成 slot invalid、auth invalid、或自动 rotation 信号。
3. 不重开 Codex auth/config bundle、saved-slot naming、或 provider cleanup contract。
4. 不在本 owner 内做 upstream Codex root-cause diagnosis，只处理 Freely 的 bounded detection/classification behavior。
5. 不把旧的 `feature/fix-codex-apikey-availability-lock` 残差整包并入；只有直接服务本 owner acceptance 的最小片段可被摘取。

## Acceptance

1. `codex_probe_current_slot_now` 在观察到 `ERROR: Reconnecting...` 或等价 connection-failure evidence 时，返回 `network_failure`，不再等待完整 timeout。
2. fast-fail 路径会终止 probe 进程树并立即写出 artifact。
3. `ai status` 与 unsaved-live-auth `ai switch codex` 暴露 `probe_status=network_failure`，且仍把它视为 network-local temporary failure。
4. runtime/cycle log 中的 reconnect 文本进入 execution-network taxonomy，而不是 generic `ai_exit_rc_*`。
5. issue-bound tests 覆盖 reconnect fast-fail、child cleanup、artifact 写出、status/switch surface、以及 runtime classification。

## IBM Handoff

- implementation_scope_summary:
  - 在现有 `feature/codex-hi-fast-fail-and-runtime-availability` worktree 中继续 bounded implementation。
  - 只吸收与 `network_failure` fast-fail / classification 直接相关的 residual changes；旧的 live-auth identity reconciliation 残差不在本 owner scope。
- required_doc_refs:
  - `docs/B1-docs/raw-20260406T110500Z/brainstorms.md`
  - `docs/B2-docs/config/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance/prd.md`
  - `docs/B2-docs/config/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance/pre-tests.md`
  - `docs/B2-docs/config/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance/tasks.md`
  - `docs/B2-docs/runtime/runtime-network-failure-taxonomy-and-bounded-recovery-governance/issues/runtime-network-failure-taxonomy-and-bounded-recovery-governance.md`

## Completion

- `docs/B2-docs/config/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance/issues/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance.md`
- `docs/B2-docs/config/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance/brainstorms/b-codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance.md`
- `docs/B2-docs/config/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance/prd.md`
- `docs/B2-docs/config/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance/pre-tests.md`
- `docs/B2-docs/config/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance/tasks.md`
- `docs/progress/workspace-routing-foundation/p-codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance.md`
- milestone / candidate writeback showing `I-20260406-0901-A` is the canonical owner

## Next

- Continue dev-loop in `feature/codex-hi-fast-fail-and-runtime-availability`.
- The old `feature/fix-codex-apikey-availability-lock` residual has now been fully classified:
  - only `docs/system/workspace/scripts/runtime/freely`
  - and `docs/system/workspace/scripts/tests/test-freely-runtime-auth-failure-signal-filter`
  belonged to this owner and are already absorbed here
  - all current-live/bootstrap residuals route to `I-20260406-1829-A`
- Treat that old tree as `retire-only`; do not reopen residual triage from this lane before promotion.

## Verification

- `./bin/governance-check`
- review `docs/B1-docs/raw-20260406T110500Z/brainstorms.md`
- review `docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh`
- review `docs/system/workspace/scripts/runtime/ai-cli`
- review `docs/system/workspace/scripts/runtime/freely`
- pass the issue-bound reconnect/status/runtime regression set from `pre-tests.md`
- record verification evidence in `docs/B2-docs/config/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance/code-reviews/20260406-codex-reconnect-probe-fast-fail-and-runtime-network-classification-verification.md`
- record canonical closeout evidence in `docs/B2-docs/config/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance/code-reviews/20260406-codex-reconnect-probe-fast-fail-and-runtime-network-classification-canonical-closeout-verification.md`

## Next

- Completed on canonical `develop` through `test-pre-merge-codex-reconnect-fast-fail-20260406-2014` and guarded merge `7674bc3`.
- Post-merge followthrough passed on canonical `develop`; keep the unrelated `interruption-manager-handler` readiness patch outside this owner if it is materialized later.
