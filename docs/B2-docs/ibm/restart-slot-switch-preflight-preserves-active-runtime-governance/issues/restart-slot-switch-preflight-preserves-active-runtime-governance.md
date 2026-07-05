# Issue: restart-slot-switch-preflight-preserves-active-runtime-governance

- issue_id: `I-20260405-2055-A`
- title: Restart slot-switch preflight preserves active runtime governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `restart-slot-switch-preflight-preserves-active-runtime-governance`
- issue-name: `restart-slot-switch-preflight-preserves-active-runtime-governance`
- priority: `P1`
- source_candidate: `docs/pre-brainstorms/20260405-2055--restart-slot-switch-preflight-preserves-active-runtime/candidates.md#c-20260405-2055-a`
- source_brainstorm: `docs/pre-brainstorms/20260405-2055--restart-slot-switch-preflight-preserves-active-runtime/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/restart-slot-switch-preflight-preserves-active-runtime-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-restart-slot-switch-preflight-preserves-active-runtime-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/restart-slot-switch-preflight-preserves-active-runtime-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/slot-switch-startup-preflight-and-lock-observability-governance/issues/slot-switch-startup-preflight-and-lock-observability-governance.md`
  - `docs/epics/workspace-routing-foundation/project-command-semantics-and-restore-work-governance/issues/project-command-semantics-and-restore-work-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 已经为 `freely start` 冻结了 shared codex slot-switch lock 的 startup preflight，也已经为 project command family 冻结了 `restart` 的语义层级；但两者之间仍留了一个真实缺口：当 restart 将要被 active shared lock 阻塞时，当前 project runtime 仍可能先被停掉，再发现下一次启动无法前进。对于 dogfood 中的真实运行项目，这个顺序错误会把“有界失败”升级成“可避免的 runtime 中断”。

## Scope

1. 冻结 `freely restart` 的 slot-switch preflight 顺序：必须先判共享 lock，再决定是否停止当前 runtime。
2. 冻结 active shared lock 下的 restart-preserve contract：preflight 失败时不得先停止当前 supervisor / AI child。
3. 收束 restart 路径依赖的最小 runtime durability hardening：
   - relaunch helper 进程锚定目标 project cwd
   - stop 请求在下一次 AI launch 前再次判定
   - restart 邻近的 session-state 写入采用原子替换
   - dispatcher/watchdog readiness polling 避免粗粒度长等待带来的脆弱性
4. 为上述 contract 补齐 focused regression tests。

## Non-Goals

1. 不重新打开 `I-20260404-2148-A` 的 start/status/doctor lock observability owner。
2. 不重开 `I-20260327-2006-A` 的整个 project command taxonomy。
3. 不把本 owner 扩写成全局 watchdog 重构、generic restart manifest、或 broader account-switch redesign。
4. 不在本 owner 内吸收与 restart contract 无关的 status 文案或 runtime 架构整理。

## Acceptance

1. `freely restart` 在 `stop_project_runtime` 之前执行 shared codex slot-switch startup preflight。
2. 当 active shared slot-switch lock 触发 bounded failure/defer 时，当前 project runtime 保持存活且 pid 不变。
3. restart followthrough 使用的 relaunch helper 进程锚定到目标 project root，避免 cwd 退化时的 ownership 漂移。
4. operator stop 若在 supervisor 下一次 AI launch 前到达，不会再多启动一轮 AI child。
5. restart 相关的 session-state durability 与 readiness polling regression tests 全部通过。

## Verification

- `bash -n docs/system/workspace/scripts/runtime/freely`
- `bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
- `bash docs/system/workspace/scripts/tests/test-freely-restart-preserves-runtime-on-active-slot-switch-lock`
- `bash docs/system/workspace/scripts/tests/test-freely-session-rotation`
- `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch-serialization`
- `bash docs/system/workspace/scripts/tests/test-ai-cli-login-triggers-auth-change-wake`
- `bash docs/system/workspace/scripts/tests/test-ai-cli-login-does-not-block-on-auth-change-wake`
- `bash docs/system/workspace/scripts/tests/test-freely-checkpoint-governance`
- `bash docs/system/workspace/scripts/tests/test-freely-checkpoint-drift-escalation`
- `bash docs/system/workspace/scripts/tests/test-freely-codex-current-slot-does-not-capture-switch-warning`
- `git diff --check`
- `./bin/governance-check`

## Completion

- `docs/pre-brainstorms/20260405-2055--restart-slot-switch-preflight-preserves-active-runtime/brainstorms.md`
- `docs/pre-brainstorms/20260405-2055--restart-slot-switch-preflight-preserves-active-runtime/candidates.md`
- `docs/epics/workspace-routing-foundation/restart-slot-switch-preflight-preserves-active-runtime-governance/issues/restart-slot-switch-preflight-preserves-active-runtime-governance.md`
- `docs/epics/workspace-routing-foundation/restart-slot-switch-preflight-preserves-active-runtime-governance/brainstorms/b-restart-slot-switch-preflight-preserves-active-runtime-governance.md`
- `docs/epics/workspace-routing-foundation/restart-slot-switch-preflight-preserves-active-runtime-governance/prd.md`
- `docs/epics/workspace-routing-foundation/restart-slot-switch-preflight-preserves-active-runtime-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/restart-slot-switch-preflight-preserves-active-runtime-governance/tasks.md`
- `docs/epics/workspace-routing-foundation/restart-slot-switch-preflight-preserves-active-runtime-governance/code-reviews/20260405-restart-slot-switch-preflight-implementation-decision.md`
- `docs/epics/workspace-routing-foundation/restart-slot-switch-preflight-preserves-active-runtime-governance/code-reviews/20260405-restart-slot-switch-preflight-verification.md`
- `docs/progress/workspace-routing-foundation/p-restart-slot-switch-preflight-preserves-active-runtime-governance.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-restart-preserves-runtime-on-active-slot-switch-lock`
- updated restart-adjacent focused tests under `docs/system/workspace/scripts/tests/`

## Next

- Completed on canonical `develop` via guarded merge `255d6dd`.
- Post-merge closeout verification is recorded in `docs/epics/workspace-routing-foundation/restart-slot-switch-preflight-preserves-active-runtime-governance/code-reviews/20260405-restart-slot-switch-preflight-canonical-closeout-verification.md`.
- Reopen only if canonical `develop` again allows restart to stop a live runtime before shared slot-switch preflight resolves, or if adjacent durability hardenings regress the preserved-runtime contract.
