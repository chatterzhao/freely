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

## Acceptance Items

### item-001: scan output accuracy
- item_id: item-001
- acceptance_type: unit
- result: pass
- executed_at: 2026-05-03T03:00:00Z
- environment: feature/scan-lifecycle-migration
- evidence_path: docs/epics/workspace-routing-foundation/scan-lifecycle-migration/code-reviews/review.md
- notes: |
    35 items (chat_inbox=7, chain_trace=17, governance=11).
    Each key verified against actual filesystem state. All correct.
    Old scan: 147 items. New scan: 35 items. 76% noise reduction.

### item-002: chain trace station verification
- item_id: item-002
- acceptance_type: unit
- result: pass
- executed_at: 2026-05-03T03:10:00Z
- environment: feature/scan-lifecycle-migration
- evidence_path: docs/epics/workspace-routing-foundation/scan-lifecycle-migration/code-reviews/review.md
- notes: |
    12 mandatory + 2 optional stations per key verified.
    Absorbed B1 skip, platform_ids empty detection, branch_deleted gating all correct.

### item-003: daemon prompt integration
- item_id: item-003
- acceptance_type: integration
- result: pass
- executed_at: 2026-05-03T03:20:00Z
- environment: test-pre-merge-scan-lifecycle-20260503
- evidence_path: docs/epics/workspace-routing-foundation/scan-lifecycle-migration/code-reviews/review.md
- notes: |
    Daemon started in test-pre-merge. Prompt contains lifecycle scan output.
    ACP bridge works via hash-based socket path.

### item-004: socket path fix verification
- item_id: item-004
- acceptance_type: integration
- result: pass
- executed_at: 2026-05-03T03:30:00Z
- environment: test-pre-merge-scan-lifecycle-20260503
- evidence_path: docs/epics/workspace-routing-foundation/scan-lifecycle-migration/code-reviews/review.md
- notes: |
    Socket path reduced from 122 to 37 chars. Daemon starts in long-path worktree.
