# Issue: foreground-background-runtime-entrypoint-semantics-governance

- issue_id: `I-20260413-0208-A`
- title: Foreground/background runtime entrypoint semantics governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `foreground-background-runtime-entrypoint-semantics-governance`
- issue-name: `foreground-background-runtime-entrypoint-semantics-governance`
- priority: `P0`
- source_candidate: `docs/pre-brainstorms/20260413-0208--foreground-background-runtime-entrypoint-semantics/candidates.md#c-20260413-0208-a`
- source_brainstorm: `docs/pre-brainstorms/20260413-0208--foreground-background-runtime-entrypoint-semantics/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/foreground-background-runtime-entrypoint-semantics-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-foreground-background-runtime-entrypoint-semantics-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/foreground-background-runtime-entrypoint-semantics-governance/code-reviews`
- created_at: `2026-04-13`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 当前的产品心智与运行时入口 contract 仍存在一条会误导用户和未来 UI 接口的错位：

1. `freely start` 实际是前台附着 supervisor，会跟随调用会话结束而停机
2. 产品 intent 又要求 runtime 持续运行，除非明确停止
3. 现有测试已经把 `start/restart/stop/status` 锁成前台/控制面 contract，不能静默改成后台
4. 若不先冻结 foreground/background/UI close/state truth 的边界，后续实现极易把入口语义变更、daemon 引入、恢复链回归混成一次高风险改动

## Scope

1. 冻结 foreground attached runtime 与 background daemon runtime 的语义分层
2. 冻结 `start/restart/stop/status` 的既有 foreground/control-plane contract，不做静默重定义
3. 冻结只有显式 `daemon ...` 命令面才代表后台 runtime control plane
4. 冻结 UI/TUI 默认连接后台 runtime，关闭前端默认不停止后台
5. 冻结 shared runtime truth 继续来自现有 state files、`live-status`、`fleet-status`
6. 冻结 foreground test family 与 daemon test family 的分离回归面

## Non-Goals

1. 不在本 owner 中顺手修复 `primary_rate_limit_exhausted` 之后的 recovery gap
2. 不把 `freely start` 直接改成后台默认入口
3. 不引入第二套 UI 专属 runtime 状态真源
4. 不在第一轮同时做整套命令面迁移，例如直接改成 `up/down/run/ps/logs`

## Acceptance

1. Freely 真源明确：`freely start` 是 foreground attached mode，`Ctrl+C` 或终端关闭导致停机属于预期 contract。
2. Freely 真源明确：后台自治 runtime 只由显式 `freely daemon start|stop|status|logs` 承担。
3. Freely 真源明确：UI/TUI 的默认启停心智对接 daemon 模式；关闭前端默认不执行 `daemon stop`。
4. Freely 真源明确：foreground tests 继续保护 `start/restart/stop/status` 现有语义；daemon 行为新增独立测试族，不复写现有 foreground 基本假设。
5. Freely 真源明确：daemon 与 foreground 共享同一套 runtime truth，不产生并行状态面。
6. 首轮 daemon 成功标准必须包含“父会话结束后后台 runtime 继续存活”，且不再把这类停机记为 foreground `operator_stop` 误归因。

## IBM Handoff

- implementation_scope_summary:
  - 先保留 foreground contract，再新增显式 daemon control plane；不要把入口语义重构和 recovery hardening 混成一轮大改。
  - 第一轮优先落命令 contract、runtime detach/attach 边界、shared status truth 与 focused regressions；UI 只冻结默认语义，不在本轮做完整前端实现。
- required_doc_refs:
  - `docs/epics/workspace-routing-foundation/foreground-background-runtime-entrypoint-semantics-governance/issues/foreground-background-runtime-entrypoint-semantics-governance.md`
  - `docs/epics/workspace-routing-foundation/foreground-background-runtime-entrypoint-semantics-governance/brainstorms/b-foreground-background-runtime-entrypoint-semantics-governance.md`
  - `docs/epics/workspace-routing-foundation/foreground-background-runtime-entrypoint-semantics-governance/prd.md`
  - `docs/epics/workspace-routing-foundation/foreground-background-runtime-entrypoint-semantics-governance/pre-tests.md`
  - `docs/epics/workspace-routing-foundation/foreground-background-runtime-entrypoint-semantics-governance/tasks.md`
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
  - `docs/system/workspace/scripts/tests/test-freely-runtime-supervisor-event-log`
  - `docs/system/workspace/scripts/tests/test-freely-stop-terminates-all-same-project-supervisors`
  - `docs/PROJECT_INTENT.md`

## Verification

- `docs/epics/workspace-routing-foundation/foreground-background-runtime-entrypoint-semantics-governance/code-reviews/20260413-foreground-background-runtime-entrypoint-semantics-verification.md`
- `docs/epics/workspace-routing-foundation/foreground-background-runtime-entrypoint-semantics-governance/code-reviews/20260413-foreground-background-runtime-entrypoint-semantics-closeout-verification.md`
- `bash docs/system/workspace/scripts/tests/test-freely-daemon-command-semantics`
- `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
- `bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
- `bash docs/system/workspace/scripts/tests/test-freely-runtime-supervisor-event-log`
- `bash docs/system/workspace/scripts/tests/test-freely-stop-terminates-all-same-project-supervisors`
- `./bin/governance-check`

## Completion

- `docs/pre-brainstorms/20260413-0208--foreground-background-runtime-entrypoint-semantics/candidates.md`
- `docs/epics/workspace-routing-foundation/foreground-background-runtime-entrypoint-semantics-governance/issues/foreground-background-runtime-entrypoint-semantics-governance.md`
- `docs/epics/workspace-routing-foundation/foreground-background-runtime-entrypoint-semantics-governance/brainstorms/b-foreground-background-runtime-entrypoint-semantics-governance.md`
- `docs/epics/workspace-routing-foundation/foreground-background-runtime-entrypoint-semantics-governance/prd.md`
- `docs/epics/workspace-routing-foundation/foreground-background-runtime-entrypoint-semantics-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/foreground-background-runtime-entrypoint-semantics-governance/tasks.md`
- `docs/epics/workspace-routing-foundation/foreground-background-runtime-entrypoint-semantics-governance/code-reviews/20260413-foreground-background-runtime-entrypoint-semantics-verification.md`
- `docs/epics/workspace-routing-foundation/foreground-background-runtime-entrypoint-semantics-governance/code-reviews/20260413-foreground-background-runtime-entrypoint-semantics-closeout-verification.md`
- `docs/progress/workspace-routing-foundation/p-foreground-background-runtime-entrypoint-semantics-governance.md`
- `docs/PROJECT_INTENT.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-daemon-command-semantics`
- `docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
- `docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
- `docs/system/workspace/scripts/tests/test-freely-runtime-supervisor-event-log`
- `docs/system/workspace/scripts/tests/test-freely-stop-terminates-all-same-project-supervisors`

## Next

- `2026-04-13` closeout: canonical `develop` absorbed the explicit daemon control plane through merge `1b55aae6`, and this closeout lane only rewrites lifecycle truth after guarded promote, push followthrough, and worktree retirement completed.
- Keep this owner closed as the canonical foreground-versus-daemon entrypoint record; any future daemon restart semantics, UI shell implementation, or broader command-surface renaming must reopen as a new bounded owner on current `develop`.
