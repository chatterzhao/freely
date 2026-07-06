# Pre-tests — scan lifecycle migration

- issue_id: `I-20260503-0200-A`
- issue_path: `docs/B2-docs/runtime/scan-lifecycle-migration/issues/I-20260503-0200-A.md`

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
- required evidence: `daemon launch log, prompt file`
- blocker taxonomy: `execution_pending_or_failed`
1. 在 test-pre-merge 工位启动 daemon
2. 检查 prompt 文件包含 "Lifecycle task scan" 和完整 chain trace

## End-to-End
- acceptance target: `扫描从 147 条降到 35 条，扫描结果与实际状态完全一致`
- testing layer: `end_to_end`
- target environment: `test-pre-merge-scan-lifecycle-20260503`
- required evidence: `scan output comparison`
- blocker taxonomy: `execution_pending_or_failed`
1. 对比旧 scan (147条) vs 新 scan (35条)，逐条核实

## Real-Environment
- acceptance target: `guarded promote 通过 develop merge gate，无回归`
- testing layer: `real_environment`
- target environment: `develop`
- required evidence: `pr-merge-guarded 成功，governance-check 通过`
- blocker taxonomy: `protected_environment_only`
- real_environment_status: `pass`
- real_environment_reason: `Validated in test-pre-merge-scan-lifecycle-20260503; guarded promote ready.`

## Acceptance Items

### scan output accuracy verified
- id: `scan-output-accuracy`
- requirement: `scan 输出 35 条，chat_inbox=7, chain_trace=17, governance=11，逐条与实际状态一致`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/scan-lifecycle-migration/raw-20260503-0200/code-reviews/review.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-1`
- case_design: `运行 SKIP_PLATFORM_CHECK=1 python3 task-lifecycle-scan.py --project . 并逐 key 对比实际文件系统状态`

### chain trace stations accurate
- id: `chain-trace-stations`
- requirement: `12 mandatory + 2 optional stations per key，每站 current/next/blokers 与实际一致`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/scan-lifecycle-migration/raw-20260503-0200/code-reviews/review.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-3`
- case_design: `逐 key 验证 chain trace 的 reached stations，包括 absorbed B1 skip, platform_ids empty detection, branch_deleted 证据门控`

### socket path under 104 chars
- id: `socket-path-short`
- requirement: `AF_UNIX socket path < 50 chars，daemon 在长路径工位下正常启动`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/scan-lifecycle-migration/raw-20260503-0200/code-reviews/review.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-5`
- case_design: `在 test-pre-merge 工位启动 daemon，验证 socket 路径为 /tmp/freely-acp-{hash}.sock (< 50 chars)`

### premerge-integration verified
- id: `premerge-verified`
- requirement: `test-pre-merge 集成验证通过，daemon 启动正常，scan 输出准确`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/scan-lifecycle-migration/raw-20260503-0200/code-reviews/review.md`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#task-1`
- case_design: `在 test-pre-merge 工位启动 daemon，验证 prompt 包含 lifecycle scan，scan 输出 35 条全部准确`

### governance gate passes
- id: `governance-gate-pass`
- requirement: `governance-merge-gate --range develop..HEAD 通过`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/runtime/scan-lifecycle-migration/raw-20260503-0200/code-reviews/review.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#task-6`
- case_design: `运行 ./bin/governance-merge-gate --range develop..HEAD，验证 C/M/I chain 完整`
