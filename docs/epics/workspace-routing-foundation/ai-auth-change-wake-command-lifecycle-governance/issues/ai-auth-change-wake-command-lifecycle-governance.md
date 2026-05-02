# Issue: ai-auth-change-wake-command-lifecycle-governance

- issue_id: `I-20260329-2045-A`
- title: AI auth-change wake command lifecycle governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `ai-auth-change-wake-command-lifecycle-governance`
- issue-name: `ai-auth-change-wake-command-lifecycle-governance`
- priority: P1
- source_candidate: `docs/pre-brainstorms/20260329-2045--ai-auth-change-wake-recursion-and-command-lifecycle/candidates.md#c-20260329-2045-a`
- source_brainstorm: `docs/pre-brainstorms/20260329-2045--ai-auth-change-wake-recursion-and-command-lifecycle/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
  - `docs/epics/workspace-routing-foundation/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance/issues/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance.md`
- pre_tests_path: `docs/epics/workspace-routing-foundation/ai-auth-change-wake-command-lifecycle-governance/pre-tests.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/ai-auth-change-wake-command-lifecycle-governance/code-reviews`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

`bin/ai` 的账号成功路径当前暴露了一个独立于账号池可用性和 OAuth 成功率的命令生命周期问题：

- `ai list` / `whoami` / `status` 可以自行退出
- `ai switch codex <slot>` 在打印成功结果后仍可能不退出
- 这个问题即使在 no-op `switch codex <current-slot>` 上也成立
- 前台 `ai-cli` 存活时，其同步子进程是 `freely auth-change-wake --reason switch_success`

这说明当前缺口不是“账号不能切”，而是“成功后的 wake 语义与命令退出语义没有收口”。在 watchdog 路径也会触发 `ai switch` 的前提下，这条链还存在自激递归风险。

`ai login codex` 当前只作为同族 follow-on 风险记录。第一阶段 IBM 和修复以 `switch` 的硬复现为准，不要求执行真实登录。

## Scope

1. 冻结 `ai switch` 成功路径的退出 contract。
2. 明确 `notify_freely_auth_change()` 与 `auth-change-wake` 的允许阻塞面。
3. 冻结 wake re-entrancy contract，避免 watchdog/manager 路径回流到同一 success-path 通知环。
4. 补足 focused regressions，覆盖：
   - no-op `switch codex <current-slot>` 成功后应退出
   - success-path wake 不得把命令无限阻塞在前台
   - watchdog-auth recovery 语义不被误伤
5. 只修已证实的 codex `switch` auth-change lifecycle 缺口，不扩大到 slot 删除、真实登录流程 redesign 或一般化账号治理。

## Non-Goals

1. 不在本 issue 内重新设计 OAuth 登录 UX，也不把真实 `login` 执行纳入第一阶段验证。
2. 不把本 issue 扩成“所有后台 helper 都算泄漏”的总论。
3. 不修改 slot 删除/清理行为。
4. 不把 invalid resume evidence、live-status 空白或 manager runtime 不一致并入同一 owner issue。
5. 不为了让 `login/switch` 早退出而破坏现有 manager/watchdog auth recovery。

## Acceptance

1. `ai switch codex <current-slot>` 在成功输出后会及时退出。
2. `ai switch codex <other-slot>` 在成功输出后会及时退出。
3. `auth-change-wake` 不会通过 watchdog/manager 路径自激回流到同一 `switch` success-path notify loop。
4. operator interruption 后不会留下同族递归 wake helper 超过 issue 定义的 bounded cleanup window。
5. manager/watchdog 的 auth-change recovery 仍保持可用。
6. 如果后续 issue 内获得不依赖真实登录的 clean evidence，再把同一退出 contract 扩展到 `login`。

## Verification

- `./bin/governance-check`
- real-command replay for `ai list codex`, `ai whoami codex`, `ai status codex`
- real-command replay for no-op `ai switch codex <current-slot>` with process-tree observation
- focused regression for success-path wake re-entrancy
- focused regression proving manager/watchdog auth recovery still works after the repair

## Implementation References

- `docs/epics/workspace-routing-foundation/ai-auth-change-wake-command-lifecycle-governance/prd.md`
- `docs/epics/workspace-routing-foundation/ai-auth-change-wake-command-lifecycle-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/ai-auth-change-wake-command-lifecycle-governance/tasks.md`
- `docs/system/workspace/scripts/runtime/ai-cli`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh`

## Next

- `2026-03-30 17:34 PDT` owner implementation and verification are already absorbed by `develop` commit `44bb13c`. The canonical closeout evidence is the focused regression set plus `docs/epics/workspace-routing-foundation/ai-auth-change-wake-command-lifecycle-governance/code-reviews/20260330-ai-auth-change-wake-command-lifecycle-verification.md`.
- Future auth UX or helper-process expansion must open a new lifecycle rather than reopening this completed owner.
