# Pre-Tests: 认领判定下沉
- issue_id: I-20261102T133249Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: bash 中不得再出现“当前路径不等于项目才认领”的守卫
- acceptance_target: 认领调用不再被路径比较包住
- surface_kind: unit
- target_lane: dev-unit
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: fix/raw-20261102T133249Z-owner-lane-claim-guard
- required_evidence: wiring 测试的三条断言
- evidence_level: unit
- artifact_ref: docs/system/workspace/scripts/tests/test-owner-lane-claim-wiring.py
- test_command: python3 docs/system/workspace/scripts/tests/test-owner-lane-claim-wiring.py
- expected_output: OK
- expected_RED_output: AssertionError: path-inequality guard is back
- actual_RED_output: 2 failures —— 守卫匹配命中 span=(1249,1276)，且 claim 行含 2>/dev/null
- actual_output: OK —— 3 条断言通过（调用存在、无路径守卫、stderr 未吞）
- evidence_file: docs/B2-docs/worktree-lifecycle/owner-lane-claim/raw-20261102T133249Z/verification/test-evidence/test-owner-lane-claim-wiring-RED.log
- red-green-status: green
- status: passed
- blocker: ""

### acceptance-2
- id: AT-002
- requirement: project 与 path 相同时仍能判定并认领
- acceptance_target: 同路径且有 raw key 分支 → created；同路径且 develop 分支 → 不认领
- surface_kind: unit
- target_lane: dev-unit
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: fix/raw-20261102T133249Z-owner-lane-claim-guard
- required_evidence: 两条用例的返回值与写库次数
- evidence_level: unit
- artifact_ref: docs/system/workspace/scripts/tests/test-owner-lane-claim.py
- test_command: python3 docs/system/workspace/scripts/tests/test-owner-lane-claim.py
- expected_output: OK
- expected_RED_output: 不适用（claim 语义本就正确，缺陷在调用方）
- actual_RED_output: 不适用 —— 两条用例在修复前后都应为绿，它们是锁定用例
- actual_output: OK —— 9 条用例全过，其中两条为本次新增的同路径用例
- evidence_file: docs/B2-docs/worktree-lifecycle/owner-lane-claim/raw-20261102T133249Z/verification/test-evidence/test-owner-lane-claim.log
- red-green-status: green
- status: passed
- blocker: ""

### acceptance-3
- id: AT-003
- requirement: 全新工位（agent_working 零行）直接 daemon start 可成功，并留下认领日志
- acceptance_target: rc=0；daemon-launch.log 含 owner-lane claim；agent_working 出现 manager_01 行
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: integration
- target_environment: fix/raw-20261102T133249Z-owner-lane-claim-guard（零行工位）
- required_evidence: daemon start 输出、认领日志、DB 行
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/runtime/freely
- test_command: ./bin/freely daemon start --project <worktree> --task-mode listen
- expected_output: rc=0 且 supervisor_pid 有值
- expected_RED_output: ERROR unable to resolve agent identity … agent_working has no entry
- actual_RED_output: 该工位修复前报同一句；改后首跑又暴露 .freely/run 缺失导致 db daemon 失败
- actual_output: rc=0，supervisor_pid=22653，日志含 owner-lane claim → manager_01，DB 行 manager_id=manager_01
- evidence_file: docs/B2-docs/worktree-lifecycle/owner-lane-claim/raw-20261102T133249Z/verification/test-evidence/owner-lane-claim.log
- red-green-status: green
- status: passed
- blocker: ""
