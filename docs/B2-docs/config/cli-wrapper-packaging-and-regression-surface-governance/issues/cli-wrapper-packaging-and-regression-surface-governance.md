# Issue: cli-wrapper-packaging-and-regression-surface-governance

- issue_id: `I-20260405-2358-C`
- title: CLI wrapper packaging and regression-surface governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `cli-wrapper-packaging-and-regression-surface-governance`
- issue-name: `cli-wrapper-packaging-and-regression-surface-governance`
- priority: `P1`
- source_candidate: `docs/B1-docs/raw-20260405-2358/candidates.md#c-20260405-2358-c`
- source_brainstorm: `docs/B1-docs/raw-20260405-2358/brainstorms.md`
- execution_base: `feature/cli-command-audit-20260406-0015`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/cli-wrapper-packaging-and-regression-surface-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-cli-wrapper-packaging-and-regression-surface-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/cli-wrapper-packaging-and-regression-surface-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/project-command-semantics-and-restore-work-governance/issues/project-command-semantics-and-restore-work-governance.md`
  - `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/issues/codex-apikey-slot-bundle-and-provider-aware-probe-governance.md`
  - `docs/epics/freely-product-architecture/worktree-helper-shell-source-compatibility-governance/issues/worktree-helper-shell-source-compatibility-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

本轮 `bin/` 全量命令审计已经证明，Freely 现在的 CLI 能力不只是 runtime 语义问题，还存在一层更前置的包装层回归：

1. 若干 `bin/` wrapper 与 test wrapper 文件存在，但默认 shell 不能直接执行。
2. `freely ai --help` 在输出 usage 前会先泄漏 shell 错误。
3. 至少一个 auth-change wake regression 在不同 worktree 上表现不稳定。

这类问题如果不先收束，会直接污染后续所有 CLI-first 验证，因为“命令存在”并不等于“命令入口契约稳定”。

## Scope

1. 修复本轮审计确认的 runnable wrapper packaging 缺口，使目标命令可直接执行。
2. 清理 `freely ai --help` 的 help surface，保证帮助输出前不出现 shell evaluation 噪音。
3. 收束 `test-ai-cli-switch-triggers-auth-change-wake` 的 worktree / 环境敏感性，确保回归结果可重复。
4. 只补本 owner 触达的最小回归覆盖，不重开 runtime control-plane 或 project bootstrap 语义。

## Non-Goals

1. 不在本 owner 内修 `baseline-status` / `status` 的 `--project` 漂移。
2. 不在本 owner 内重构 `sync-tooling` / `.githooks` bootstrap。
3. 不把 `start` / `restart` / `chat` / `restore-work` 的 control-plane 脆弱性吸进来。
4. 不把所有 `bin/*` 一次性重新分类或重写，只处理本轮已证明破损的 runnable surface。

## Acceptance

1. `./bin/check-tauri-probe-host`、`./bin/tauri-probe-dev`、`./bin/test-freely-fleet-status`、`./bin/test-rust-toolchain-preflight` 可以直接执行。
2. `./bin/ai --help` 输出 clean usage，不再先打印 `mode` / `apikey` / `account` command-not-found。
3. `./bin/test-ai-cli-switch-triggers-auth-change-wake` 在 dedicated feature worktree 与 primary worktree 上都稳定通过。
4. 与本 owner 直接相关的 focused regressions 通过，且 `./bin/governance-check` 通过。

## Verification

- `./bin/ai --help`
- `./bin/check-tauri-probe-host`
- `./bin/test-freely-fleet-status`
- `./bin/test-rust-toolchain-preflight`
- `./bin/test-ai-cli-switch-triggers-auth-change-wake`
- `./bin/governance-check`

## Next

- Completed on canonical `develop` through `test-pre-merge-20260406-0035-cli-wrapper-regression-closeout` and guarded merge `8e0985b`.
- Post-merge followthrough proved the repaired command surfaces on canonical `develop`; the newly exposed `governance-check` ancestry-audit false positive is routed as a separate pre-brainstorm follow-on and is not absorbed into this packaging owner.
- Continue project-target bootstrap/status and runtime control-plane follow-ons in their own owners instead of reopening this bounded lane.
