# Pre-tests: chat-triggered-worker-runtime-reactivation-governance

1. worker 工位在 `operator_stop` 后，`freely chat` 触发 delegated continuation 时，会重新拉起本工位主循环。
2. `handoff://verification` 也按 gate 判定是否应重激活。
3. 当前已有 active AI 时，不会重复拉起第二个主循环。
4. `auth_failure` 与 operator stop 不被混成同一条自动重启语义。
5. `freely intake chat` 继续只是低层 durable primitive，不自动承担高层 reactivation 语义。
