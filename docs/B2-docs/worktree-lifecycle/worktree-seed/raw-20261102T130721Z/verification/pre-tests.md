# Pre-Tests: 声明式工作树种子清单
- issue_id: I-20261102T130721Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 清单缺失时回落内置默认，保证现有行为不倒退
- acceptance_target: source=builtin 且复制 .freely/agent-table.toml
- surface_kind: unit
- target_lane: dev-unit
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: feature/raw-20261102T130721Z-worktree-seed-manifest
- required_evidence: load 返回的 source 与 apply 的 copied 列表
- evidence_level: unit
- artifact_ref: docs/system/workspace/scripts/worktree/worktree_seed.py
- test_command: python3 docs/system/workspace/scripts/tests/test-worktree-seed.py
- expected_output: OK
- expected_RED_output: FileNotFoundError: worktree_seed.py
- actual_RED_output: FileNotFoundError: worktree_seed.py（9 个用例全部 error）
- actual_output: OK —— source=builtin，copied=[.freely/agent-table.toml]
- evidence_file: docs/B2-docs/worktree-lifecycle/worktree-seed/raw-20261102T130721Z/verification/test-evidence/test-worktree-seed-RED.log
- red-green-status: green
- status: passed
- blocker: ""

### acceptance-2
- id: AT-002
- requirement: 清单存在时完全替换内置列表
- acceptance_target: 只应用清单条目，不再隐含 agent-table
- surface_kind: unit
- target_lane: dev-unit
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: feature/raw-20261102T130721Z-worktree-seed-manifest
- required_evidence: entries 的 path 集合
- evidence_level: unit
- artifact_ref: docs/system/workspace/scripts/worktree/worktree_seed.py
- test_command: python3 docs/system/workspace/scripts/tests/test-worktree-seed.py
- expected_output: OK
- expected_RED_output: FileNotFoundError: worktree_seed.py
- actual_RED_output: FileNotFoundError: worktree_seed.py
- actual_output: OK —— source=manifest，entries=[.env]
- evidence_file: docs/B2-docs/worktree-lifecycle/worktree-seed/raw-20261102T130721Z/verification/test-evidence/test-worktree-seed.log
- red-green-status: green
- status: passed
- blocker: ""

### acceptance-3
- id: AT-003
- requirement: 幂等且不覆盖工位内已有文件
- acceptance_target: 目标存在时 skipped，内容保持原样
- surface_kind: unit
- target_lane: dev-unit
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: feature/raw-20261102T130721Z-worktree-seed-manifest
- required_evidence: skipped 列表与目标文件内容
- evidence_level: unit
- artifact_ref: docs/system/workspace/scripts/worktree/worktree_seed.py
- test_command: python3 docs/system/workspace/scripts/tests/test-worktree-seed.py
- expected_output: OK
- expected_RED_output: FileNotFoundError: worktree_seed.py
- actual_RED_output: FileNotFoundError: worktree_seed.py
- actual_output: OK —— skipped=[.freely/agent-table.toml]，内容仍为 local edit
- evidence_file: docs/B2-docs/worktree-lifecycle/worktree-seed/raw-20261102T130721Z/verification/test-evidence/test-worktree-seed.log
- red-green-status: green
- status: passed
- blocker: ""

### acceptance-4
- id: AT-004
- requirement: required 缺失即失败并指出路径；optional 缺失只记录
- acceptance_target: SeedError 含路径；optional 进 missing 列表
- surface_kind: unit
- target_lane: dev-unit
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: feature/raw-20261102T130721Z-worktree-seed-manifest
- required_evidence: 异常消息与 missing 列表
- evidence_level: unit
- artifact_ref: docs/system/workspace/scripts/worktree/worktree_seed.py
- test_command: python3 docs/system/workspace/scripts/tests/test-worktree-seed.py
- expected_output: OK
- expected_RED_output: FileNotFoundError: worktree_seed.py
- actual_RED_output: FileNotFoundError: worktree_seed.py
- actual_output: OK —— required 抛 SeedError(.env)；optional 返回 missing=[.env]
- evidence_file: docs/B2-docs/worktree-lifecycle/worktree-seed/raw-20261102T130721Z/verification/test-evidence/test-worktree-seed.log
- red-green-status: green
- status: passed
- blocker: ""

### acceptance-5
- id: AT-005
- requirement: 绝对路径与 .. 越界被拒绝
- acceptance_target: 两类非法路径都抛 SeedError，且不产生任何写入
- surface_kind: unit
- target_lane: dev-unit
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: feature/raw-20261102T130721Z-worktree-seed-manifest
- required_evidence: 两次 SeedError
- evidence_level: unit
- artifact_ref: docs/system/workspace/scripts/worktree/worktree_seed.py
- test_command: python3 docs/system/workspace/scripts/tests/test-worktree-seed.py
- expected_output: OK
- expected_RED_output: FileNotFoundError: worktree_seed.py
- actual_RED_output: FileNotFoundError: worktree_seed.py
- actual_output: OK —— ../secrets.env 与 /etc/passwd 均被拒
- evidence_file: docs/B2-docs/worktree-lifecycle/worktree-seed/raw-20261102T130721Z/verification/test-evidence/test-worktree-seed.log
- red-green-status: green
- status: passed
- blocker: ""

### acceptance-6
- id: AT-006
- requirement: link 模式生成软链接并跟随源变化；目录递归复制
- acceptance_target: is_symlink 为真且源改动可见；目录内容完整
- surface_kind: unit
- target_lane: dev-unit
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: feature/raw-20261102T130721Z-worktree-seed-manifest
- required_evidence: 软链接读回内容与目录文件
- evidence_level: unit
- artifact_ref: docs/system/workspace/scripts/worktree/worktree_seed.py
- test_command: python3 docs/system/workspace/scripts/tests/test-worktree-seed.py
- expected_output: OK
- expected_RED_output: FileNotFoundError: worktree_seed.py
- actual_RED_output: FileNotFoundError: worktree_seed.py
- actual_output: OK —— linked 列表与 version = 2 读回；certs/a.pem 存在
- evidence_file: docs/B2-docs/worktree-lifecycle/worktree-seed/raw-20261102T130721Z/verification/test-evidence/test-worktree-seed.log
- red-green-status: green
- status: passed
- blocker: ""

### acceptance-7
- id: AT-007
- requirement: wt-create 只保留一个 seed 调用点，且源指向主树
- acceptance_target: 语法通过；在工位内以 FREELY_HOME 为源执行 seed 成功
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: integration
- target_environment: feature/raw-20261102T130721Z-worktree-seed-manifest
- required_evidence: bash -n 结果与一次真实 apply 的 JSON
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/worktree/wt-create
- test_command: bash -n docs/system/workspace/scripts/worktree/wt-create
- expected_output: 语法通过；apply 返回 copied 或 skipped 且 rc=0
- expected_RED_output: 工位内以自身为源 apply 报 required seed missing
- actual_RED_output: "[wt-seed] required seed missing: .freely/agent-table.toml"（源误指向工位）
- actual_output: OK —— 以主树为源 apply 返回 copied=[.freely/agent-table.toml]，rc=0
- evidence_file: docs/B2-docs/worktree-lifecycle/worktree-seed/raw-20261102T130721Z/verification/test-evidence/test-worktree-seed.log
- red-green-status: green
- status: passed
- blocker: ""
