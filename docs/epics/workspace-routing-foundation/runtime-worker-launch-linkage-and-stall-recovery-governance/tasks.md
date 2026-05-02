# Tasks - runtime-worker-launch-linkage-and-stall-recovery-governance

1. 定义 manager handoff runtime ingestion contract
2. 在 runtime 中把 worker prompt artifact 转成 target worker continuation intake
3. 让 target worker 进入 expected-running / supervisor launch
4. 实现 stalled AI detection 与 graceful recovery
5. 补 runtime / integration tests
6. 写 verification evidence，并决定是否可合并到 `develop`
