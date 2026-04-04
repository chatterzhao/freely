# Pre-tests

## Pre-merge acceptance

1. 当默认 `$FREELY_HOME` 所在位置不可写时：
   - `freely start --project <project>` 不得因为写 `~/.freely` 失败而直接崩溃
   - Freely 必须切到一个合法的 project-scoped fallback operator-state root，或明确报出当前采用的 fallback contract
2. fallback bootstrap 后：
   - project registry / control-plane state 必须写入 fallback root
   - 不得把 shared/global-only truth 偷偷写回 project-local state
3. 当 `ps`/process inspection 被 sandbox 拦截时：
   - `status`/`live-status`/AI process snapshot surfaces 必须返回 degraded 或 unavailable 证据
   - 不得因为 `ps` 不可用就把整个命令判成失败
4. 当前 project 没有 live pid 时，snapshot surface 仍必须如实显示 `none`，而不是 degraded 误报为 active。
5. 当 `ps` 不可用且 pid file 指向 foreign live process 时，`start`/`stop` 不得把该 PID 误认成当前 project runtime。
6. 本轮 regression 必须直接断言 fallback root、degraded evidence 和 foreign-pid refusal，而不是只看退出码。

## Post-merge acceptance

1. 在 canonical `develop` 上，sandbox-constrained operator session 仍能通过 Freely 把 owner work 路由进正确 project/worktree。
2. runtime/status surfaces 在 `ps` 不可用环境下仍保持 truthful：
   - 有进程证据但无 `ps` 细节时显示 unavailable / degraded snapshot
   - 无进程证据时继续显示 `none`
3. `ps` 不可用时，PID-file fallback 不得因为 bare live PID 就复用/终止别的 project process。
4. 这条修复不能被解释成允许在 protected root 上直接做 owner development。
