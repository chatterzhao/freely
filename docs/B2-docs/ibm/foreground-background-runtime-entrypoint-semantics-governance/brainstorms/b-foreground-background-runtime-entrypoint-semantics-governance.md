# IBM Brainstorm: foreground-background-runtime-entrypoint-semantics-governance

## Frozen Decisions

1. `freely start` / `freely restart` / `freely stop` / `freely status` 保持现有 foreground/control-plane contract，不做 silent semantic rewrite。
2. 后台自治 runtime 只通过显式 `freely daemon ...` 命令面 materialize。
3. UI/TUI 关闭默认只关闭前端 shell，不默认停止后台 runtime。
4. foreground 与 daemon 共享同一套 runtime truth surfaces：state files、`live-status`、`fleet-status`。
5. `operator_stop_requested` 在 foreground 模式仍可作为预期停止证据；daemon 模式下若父会话结束导致停机则视为实现失败。

## Guardrails

1. 不把 daemon 引入与 rate-limit / watchdog / recovery 其他 follow-on 缺口绑成同一 owner。
2. 不让 daemon tests 取代现有 foreground tests。
3. 不通过 UI 私有状态缓存解释 runtime 是否仍在运行。
4. 不在第一轮引入整套重命名后的命令面迁移。

## Open Implementation Questions

1. `daemon start` 的最小 detach 机制应复用当前 supervisor 进程，还是增加一层 launch wrapper。
2. `daemon logs` 是否只做 log follow，还是同时承担 attach 语义。
3. `daemon restart` 是否首轮需要，还是先只做 `start|stop|status|logs`。
4. daemon PID / state ownership 与现有 `supervisor.pid` 的关系如何保持 machine-readable 且不误伤 `stop/status/live-status`。
