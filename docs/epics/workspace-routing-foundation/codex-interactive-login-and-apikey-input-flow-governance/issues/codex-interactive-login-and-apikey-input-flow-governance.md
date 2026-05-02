# Issue: codex-interactive-login-and-apikey-input-flow-governance

- issue_id: `I-20260406-1851-A`
- title: Codex interactive login and API-key input flow governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `codex-interactive-login-and-apikey-input-flow-governance`
- issue-name: `codex-interactive-login-and-apikey-input-flow-governance`
- priority: `P1`
- source_candidate: `docs/pre-brainstorms/20260406-1851--codex-interactive-login-and-apikey-input-flow/candidates.md#c-20260406-1851-a`
- source_brainstorm: `docs/pre-brainstorms/20260406-1851--codex-interactive-login-and-apikey-input-flow/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/codex-interactive-login-and-apikey-input-flow-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-codex-interactive-login-and-apikey-input-flow-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/codex-interactive-login-and-apikey-input-flow-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/issues/codex-apikey-slot-bundle-and-provider-aware-probe-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 还缺一个受治理约束的 Codex-first interactive login contract。当前 dirty implementation 已经证明这条 UX follow-on 足够具体，但它仍悬空在未归档实现树里：

- `freely ai login codex` 还没有 canonical 的 auth-mode 交互选择
- `freely ai login codex apikey` 还没有 canonical 的 provider/base-url/api-key 输入收集与 direct-arg parity
- empty-input failure、live bundle materialization、saved-slot continuity 还没有 owner-bound acceptance

这不是重开 bundle/probe owner，也不是 current-live bootstrap 或 reconnect fast-fail。它是一个独立的 first-hop UX owner。

## Scope

1. 冻结 `freely ai login codex` 的 bounded interactive auth-mode selection。
2. 冻结 `freely ai login codex apikey` 的 provider/base-url/api-key prompt flow 与 `--name/--url/--key` direct-arg parity。
3. 冻结 empty required input failure semantics，确保不会错误写入 live auth/config 或 saved-slot state。
4. 冻结成功路径的 live bundle materialization、slot save、以及 JSON output continuity。
5. 用现有 4 个 issue-bound regressions 锁住该 Codex-first UX path。

## Non-Goals

1. 不重开 provider-aware probe routing 或 bundle residue cleanup。
2. 不扩大为 current-live bootstrap without saved-slot owner。
3. 不扩大为 watchdog/bootstrap identity 语义。
4. 不在本 owner 内做 standalone `ai-switch-cli` extraction。
5. 不把本 owner 提升成 generic multi-tool interactive login framework。

## Acceptance

1. `freely ai login codex` 可通过交互选择在 `account` 与 `apikey` 间路由。
2. `freely ai login codex apikey` 支持交互 prompt 与 `--name/--url/--key` direct-arg parity。
3. empty input 会以 bounded failure 退出，且不写入 live auth/config 或 slot state。
4. 成功路径会 materialize live Codex API-key bundle 并保存 slot，同时保持 machine-readable output continuity。
5. 四个 issue-bound regression tests 与治理门通过。

## Verification

- `docs/epics/workspace-routing-foundation/codex-interactive-login-and-apikey-input-flow-governance/code-reviews/20260406-codex-interactive-login-and-apikey-input-flow-verification.md`
- `docs/epics/workspace-routing-foundation/codex-interactive-login-and-apikey-input-flow-governance/code-reviews/20260406-codex-interactive-login-and-apikey-input-flow-implementation-decision.md`
- `docs/epics/workspace-routing-foundation/codex-interactive-login-and-apikey-input-flow-governance/code-reviews/20260406-codex-interactive-login-and-apikey-input-flow-canonical-closeout-verification.md`

## Boundary Reminder

- This owner is not the absorption surface for `feature/fix-codex-apikey-availability-lock`.
- Old residual current-live/bootstrap semantics route to `I-20260406-1829-A`.
- Old residual runtime auth-signal filtering routes to `I-20260406-0901-A`.

## Next

- Completed on canonical `develop` through `test-pre-merge-codex-interactive-login-20260406-2004` and guarded merge `7dc4074`.
- Post-merge followthrough passed on canonical `develop`; keep future regressions in narrower follow-ons instead of reopening this bounded UX owner.
