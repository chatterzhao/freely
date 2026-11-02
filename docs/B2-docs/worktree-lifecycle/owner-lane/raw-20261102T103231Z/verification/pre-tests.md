# Pre-Tests: owner lane 显式认领 manager 身份
- issue_id: I-20261102T103231Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 已有绑定的工位不被覆盖
- acceptance_target: 任一角色已有值时原样返回，且不触发写库
- surface_kind: unit
- target_lane: dev-unit
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: feature/raw-20261102T103231Z-owner-lane-daemon-identity
- required_evidence: 返回值 agent_id 与写库次数
- evidence_level: unit
- artifact_ref: docs/system/workspace/scripts/runtime/owner_lane.py
- test_command: python3 docs/system/workspace/scripts/tests/test-owner-lane-claim.py
- expected_output: OK
- expected_RED_output: FileNotFoundError: owner_lane.py
- actual_RED_output: FileNotFoundError: owner_lane.py（5 个用例全部 error）
- actual_output: OK —— agent_id=worker_03，created=false，writes=[]
- evidence_file: docs/B2-docs/worktree-lifecycle/owner-lane/raw-20261102T103231Z/verification/test-evidence/test-owner-lane-claim-RED.log
- red-green-status: green
- status: passed
- blocker: ""

### acceptance-2
- id: AT-002
- requirement: 零行工位认领唯一 manager 并落库
- acceptance_target: 返回 manager_01 与解析出的 raw key，写库一次
- surface_kind: unit
- target_lane: dev-unit
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: feature/raw-20261102T103231Z-owner-lane-daemon-identity
- required_evidence: 写库参数 role 与 agent_id
- evidence_level: unit
- artifact_ref: docs/system/workspace/scripts/runtime/owner_lane.py
- test_command: python3 docs/system/workspace/scripts/tests/test-owner-lane-claim.py
- expected_output: OK
- expected_RED_output: FileNotFoundError: owner_lane.py
- actual_RED_output: FileNotFoundError: owner_lane.py
- actual_output: OK —— created=true，agent_id=manager_01，raw_key=20261102T103231Z，writes=1
- evidence_file: docs/B2-docs/worktree-lifecycle/owner-lane/raw-20261102T103231Z/verification/test-evidence/test-owner-lane-claim.log
- red-green-status: green
- status: passed
- blocker: ""

### acceptance-3
- id: AT-003
- requirement: 三条守卫在条件不满足时保持 fail-closed
- acceptance_target: 多个 manager / 非本仓 worktree / 分支无 raw key 均返回 None 且不写库
- surface_kind: unit
- target_lane: dev-unit
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: feature/raw-20261102T103231Z-owner-lane-daemon-identity
- required_evidence: reason 字段与 writes 为空
- evidence_level: unit
- artifact_ref: docs/system/workspace/scripts/runtime/owner_lane.py
- test_command: python3 docs/system/workspace/scripts/tests/test-owner-lane-claim.py
- expected_output: OK
- expected_RED_output: FileNotFoundError: owner_lane.py
- actual_RED_output: FileNotFoundError: owner_lane.py
- actual_output: OK —— manager_not_unique / not_a_worktree / raw_key_unresolved 三例均 None 且零写库
- evidence_file: docs/B2-docs/worktree-lifecycle/owner-lane/raw-20261102T103231Z/verification/test-evidence/test-owner-lane-claim.log
- red-green-status: green
- status: passed
- blocker: ""

### acceptance-4
- id: AT-004
- requirement: 工位没有 agent-table.toml 时从 FREELY_HOME 读取，且 test-pre-merge 分支也能解析 raw key
- acceptance_target: _home 回落生效；test 车道分支不因缺 raw- 前缀而失败
- surface_kind: unit
- target_lane: dev-unit
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: feature/raw-20261102T103231Z-owner-lane-daemon-identity
- required_evidence: _home 返回值与 test 车道分支的 claim 结果
- evidence_level: unit
- artifact_ref: docs/system/workspace/scripts/runtime/owner_lane.py
- test_command: python3 docs/system/workspace/scripts/tests/test-owner-lane-claim.py
- expected_output: OK
- expected_RED_output: manager_not_unique（实际遇到的第一个失败）
- actual_RED_output: manager_not_unique —— 工位无 agent-table.toml，manager 列表为空
- actual_output: OK —— _home 读 config.toml 的 FREELY_HOME；test-pre-merge 分支解析出 20261102T103231Z
- evidence_file: docs/B2-docs/worktree-lifecycle/owner-lane/raw-20261102T103231Z/verification/test-evidence/test-owner-lane-claim.log
- red-green-status: green
- status: passed
- blocker: ""

### acceptance-5
- id: AT-005
- requirement: 真实工位可启动 daemon，并在 stop 时自动写 test-gate.env
- acceptance_target: 修复前失败于身份解析；修复后 rc=0 且 test-gate.env 由 daemon 写入
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: integration
- target_environment: test-pre-merge-20261102T103231Z-owner-lane-daemon-identity
- required_evidence: daemon start 输出、stop 后的 test-gate.env
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/runtime/freely
- test_command: ./bin/freely daemon start --project <test worktree> --task-mode listen
- expected_output: rc=0 且 supervisor_pid 存在；stop 后 TEST_STATUS=completed
- expected_RED_output: ERROR unable to resolve agent identity … agent_working has no entry
- actual_RED_output: ERROR unable to resolve agent identity for <test worktree>: agent_working has no entry；随后 AGENT_AI_TOOL not set
- actual_output: rc=0，supervisor_pid=91429；stop 后 TEST_STATUS=completed，LAST_TESTED_COMMIT=9d1dbe8e74e450760c089cdb2abab67abb5fbab6
- evidence_file: docs/B2-docs/worktree-lifecycle/owner-lane/raw-20261102T103231Z/verification/test-evidence/daemon-start-owner-lane.log
- red-green-status: green
- status: passed
- blocker: ""
