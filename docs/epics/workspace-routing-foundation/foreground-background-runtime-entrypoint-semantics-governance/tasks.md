# Tasks - foreground-background-runtime-entrypoint-semantics-governance

1. Freeze the CLI/runtime contract that keeps `start/restart/stop/status` as foreground/control-plane semantics.
2. Add an explicit `daemon start|stop|status|logs` control surface for background runtime ownership.
3. Preserve one shared runtime truth across foreground and daemon status/log surfaces.
4. Add focused daemon regressions for parent-shell detachment, explicit stop, and shared status truth.
5. Record verification evidence that separates foreground contract preservation from daemon persistence proof.
