# Pre-tests — scan lifecycle migration

- issue_id: `I-20260503-0200-A`
- issue_path: `docs/epics/workspace-routing-foundation/scan-lifecycle-migration/issues/I-20260503-0200-A.md`

## Unit
- acceptance target: `task-lifecycle-scan.py 输出准确，chain trace 逐 key 验证通过`
- testing layer: `unit`
- target environment: `feature/scan-lifecycle-migration`
- required evidence: `scan 输出与实际状态对比`
- blocker taxonomy: `execution_pending_or_failed`
1. 运行 `SKIP_PLATFORM_CHECK=1 python3 task-lifecycle-scan.py --project .`
2. 验证 chat_inbox (7条), chain_trace (17条), governance (11条) 与实际一致

## Integration
- acceptance target: `daemon 正常启动，prompt 包含 lifecycle scan 输出`
- testing layer: `integration`
- target environment: `test-pre-merge-scan-lifecycle-20260503`
- required evidence: `daemon launch log 无错误，prompt 文件包含 chain trace`
- blocker taxonomy: `execution_pending_or_failed`
1. 在 test-pre-merge 工位启动 daemon
2. 检查 prompt 文件包含 "Lifecycle task scan" 和 chain trace 结果

## Acceptance
- acceptance target: `scan 输出从 147 条降到 35 条，无重复，逐条验证准确`
- testing layer: `acceptance`
- target environment: `develop`
- required evidence: `scan 输出完整对比`
- blocker taxonomy: `execution_pending_or_failed`
1. 对比旧 scan (147条) vs 新 scan (35条)
2. 逐条核实 chain trace 每个 key 的 current/next/blokers
