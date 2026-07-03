# Pre-Tests
- issue_id: I-20260703T121233Z-A

## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: freely stop 后无遗留进程
- acceptance_target: ps aux 无 watchdog_sse/sse-watchdog/a2a_server/opencode
- testing_layer: end-to-end
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: A1
- case_design: daemon start → stop → verify 0 process count
- target_environment: test-pre-merge
- required_evidence: after stop: 0 processes
- evidence_level: real_env
- artifact_ref: docs/epics/closeout-chain/stop-process-cleanup/raw-20260703T121233Z/verification/test-evidence/acceptance-1.log
- test_command: freely stop && ps aux | grep "watchdog_sse\|sse-watchdog\|a2a_server" | grep -v grep | wc -l
- expected_output: 0
- expected_RED_output: >0 (7 watchdog_sse at 080443Z)
- actual_RED_output: 7 watchdog_sse.py at 080443Z + 3 at other worktrees
- actual_output: 0
- evidence_file: docs/epics/closeout-chain/stop-process-cleanup/raw-20260703T121233Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: fix: 修复前 stop 后遗留 7 watchdog_sse.py 等进程

### acceptance-2
- id: AT-002
- requirement: 每个 watchdog 只有 1 个实例
- acceptance_target: ps shows exactly 1 watchdog_sse.py + 1 sse-watchdog.sh
- testing_layer: integration
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: A2
- case_design: daemon start → count watchdog instances
- target_environment: test-pre-merge
- required_evidence: 2 instances (1+1)
- evidence_level: real_env
- artifact_ref: docs/epics/closeout-chain/stop-process-cleanup/raw-20260703T121233Z/verification/test-evidence/acceptance-2.log
- test_command: ps aux | grep "watchdog_sse\|sse-watchdog" | grep -v grep | wc -l
- expected_output: 2
- expected_RED_output: 8+ (stacked from multiple restarts)
- actual_RED_output: 7 at 080443Z
- actual_output: 2 (1 watchdog_sse.py + 1 sse-watchdog.sh)
- evidence_file: docs/epics/closeout-chain/stop-process-cleanup/raw-20260703T121233Z/verification/test-evidence/acceptance-2.log
- red-green-status: green
- status: passed
- red_how: fix: 修复前每次 daemon 重启 +1 watchdog_sse.py

### acceptance-3
- id: AT-003
- requirement: ACP bridge 不再每个 cycle 重启
- acceptance_target: loop.log 无 "tool changed" 或 "binary changed"
- testing_layer: integration
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: A3
- case_design: daemon start → check loop.log for bridge restart messages
- target_environment: test-pre-merge
- required_evidence: no bridge restart log entries
- evidence_level: real_env
- artifact_ref: docs/epics/closeout-chain/stop-process-cleanup/raw-20260703T121233Z/verification/test-evidence/acceptance-3.log
- test_command: grep "bridge.*changed\|tool changed\|binary changed" .freely/logs/loop.log | wc -l
- expected_output: 0
- expected_RED_output: 1 per cycle
- actual_RED_output: 3 per 3 cycles
- actual_output: 0
- evidence_file: docs/epics/closeout-chain/stop-process-cleanup/raw-20260703T121233Z/verification/test-evidence/acceptance-3.log
- red-green-status: green
- status: passed
- red_how: fix: 修复前每个 cycle "tool changed (opencode-apikey-ds-flash-auto → opencode)"

## Unit/Integration/End-to-End/Real-Environment
- acceptance_target: all three fixes verified
- testing_layer: end-to-end
- target_environment: test-pre-merge
- required_evidence: 0 orphan procs + 1 instance each + 0 bridge restarts
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001/002/003 覆盖端到端验证

## Real-Environment
- real_environment_status: pass
- real_environment_reason: test-pre-merge daemon 验证通过
