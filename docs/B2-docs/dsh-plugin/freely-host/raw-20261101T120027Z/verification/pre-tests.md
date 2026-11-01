# pre-tests：@freely/dsh-freely P1

> P1 只验收打包插件；issue→PR 由 successor raw `20261101T124657Z` 承接。

## Unit
- acceptance_target: plugin apply/session/tools/bridge
- testing_layer: unit
- target_environment: node --test + fake ctx
- required_evidence: test log
- blocker_taxonomy: execution_pending_or_failed
1. 运行 `node --test packaging/dsh-freely/test/plugin.test.mjs`。

### acceptance-1：插件加载与 inject
- id: DE-1
- requirement: apply 创建 manager session，注册四个工具
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: packaging/dsh-freely/index.js
- test_command: node --test packaging/dsh-freely/test/plugin.test.mjs
- expected_output: 4 tests pass
- actual_output: 4 tests pass
- evidence_file: docs/B2-docs/dsh-plugin/freely-host/raw-20261101T120027Z/verification/test-evidence/plugin.log

### acceptance-2：三角色工具白名单
- id: DE-2
- requirement: manager 含四个 freely_* 工具；worker=read/write/edit/grep/glob；reviewer=read/grep/glob
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: packaging/dsh-freely/index.js
- test_command: node --test packaging/dsh-freely/test/plugin.test.mjs
- expected_output: role allow lists match
- actual_output: role allow lists match
- evidence_file: docs/B2-docs/dsh-plugin/freely-host/raw-20261101T120027Z/verification/test-evidence/plugin.log

### acceptance-3：freely_status/freely_gate + fail-closed
- id: DE-3
- requirement: subprocess 返回 stdout/exitCode；缺 bin/freely 时 apply fail-closed
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: packaging/dsh-freely/index.js
- test_command: node --test packaging/dsh-freely/test/plugin.test.mjs
- expected_output: bridge exit code + apply rejects
- actual_output: bridge exit code + apply rejects
- evidence_file: docs/B2-docs/dsh-plugin/freely-host/raw-20261101T120027Z/verification/test-evidence/plugin.log

## Integration
- acceptance_target: DSH web profile 加载本地插件
- testing_layer: integration
- target_environment: web profile + dsh 0.2.1-rc.5
- required_evidence: load log
- blocker_taxonomy: execution_pending_or_failed
1. `dsh plugin --profile freely-product-spike add packaging/dsh-freely`
2. `dsh --profile freely-product-spike`，断言 `[dsh-freely] applied`。

### acceptance-4：host 加载
- id: DE-4
- requirement: web profile 加载插件并输出 applied
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
- status: passed
- red-green-status: green
- artifact_ref: packaging/dsh-freely/cordis.patch.yml
- test_command: dsh --profile freely-product-spike
- expected_output: dsh-freely applied
- actual_output: dsh-freely applied manager=freely-manager-*
- evidence_file: docs/B2-docs/dsh-plugin/freely-host/raw-20261101T120027Z/verification/test-evidence/runtime-load.md

## End-to-End
- acceptance_target: P1 不做完整 issue→PR
- testing_layer: end_to_end
- target_environment: successor raw 20261101T124657Z
- required_evidence: successor raw E2E
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: P1 只交打包插件；issue→PR 依赖 C-B/C-D 上游，已开 successor raw 20261101T124657Z。
- replacement_evidence: test-evidence/runtime-load.md

## Real-Environment
- real_environment_status: pass
- real_environment_reason: DSH 0.2.1-rc.5 web profile 真加载产品插件，输出 dsh-freely applied manager=freely-manager-*；见 test-evidence/runtime-load.md。

## Acceptance Items
### acceptance-1
- id: DE-1
- requirement: 插件加载与 inject
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: packaging/dsh-freely/index.js
- test_command: node --test packaging/dsh-freely/test/plugin.test.mjs
- expected_output: 4 tests pass
- actual_output: 4 tests pass
- evidence_file: docs/B2-docs/dsh-plugin/freely-host/raw-20261101T120027Z/verification/test-evidence/plugin.log

### acceptance-2
- id: DE-2
- requirement: 三角色工具白名单
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: packaging/dsh-freely/index.js
- test_command: node --test packaging/dsh-freely/test/plugin.test.mjs
- expected_output: role allow lists match
- actual_output: role allow lists match
- evidence_file: docs/B2-docs/dsh-plugin/freely-host/raw-20261101T120027Z/verification/test-evidence/plugin.log

### acceptance-3
- id: DE-3
- requirement: freely_status/freely_gate + fail-closed
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: packaging/dsh-freely/index.js
- test_command: node --test packaging/dsh-freely/test/plugin.test.mjs
- expected_output: bridge exit code + apply rejects
- actual_output: bridge exit code + apply rejects
- evidence_file: docs/B2-docs/dsh-plugin/freely-host/raw-20261101T120027Z/verification/test-evidence/plugin.log

### acceptance-4
- id: DE-4
- requirement: host 加载
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
- status: passed
- red-green-status: green
- artifact_ref: packaging/dsh-freely/cordis.patch.yml
- test_command: dsh --profile freely-product-spike
- expected_output: dsh-freely applied
- actual_output: dsh-freely applied manager=freely-manager-*
- evidence_file: docs/B2-docs/dsh-plugin/freely-host/raw-20261101T120027Z/verification/test-evidence/runtime-load.md
