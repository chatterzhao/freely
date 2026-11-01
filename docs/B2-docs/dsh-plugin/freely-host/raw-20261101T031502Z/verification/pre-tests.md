# pre-tests：@freely/dsh-freely P1

> B2 写入 pending；RED 后 red；GREEN 后 green。

## Unit
- acceptance_target: plugin apply/session/tools/bridge
- testing_layer: unit
- target_environment: node --test + fake ctx
- required_evidence: test log
- blocker_taxonomy: execution_pending_or_failed
1. 运行 `node --test packaging/dsh-freely/test/plugin.test.mjs`。

### acceptance-1：插件加载与 inject
- id: DE-1
- requirement: apply 创建 manager session，inject 服务齐
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: packaging/dsh-freely/index.js
- test_command: node --test packaging/dsh-freely/test/plugin.test.mjs
- actual_output: pass
- evidence_file: docs/B2-docs/dsh-plugin/freely-host/raw-20261101T031502Z/verification/test-evidence/plugin.log
- expected_output: pass
- actual_output: pending

### acceptance-2：工具白名单
- id: DE-2
- requirement: manager/reviewer 只有 read/grep/glob；worker 多 write/edit/bash
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: packaging/dsh-freely/index.js
- test_command: node --test packaging/dsh-freely/test/plugin.test.mjs
- actual_output: pass
- evidence_file: docs/B2-docs/dsh-plugin/freely-host/raw-20261101T031502Z/verification/test-evidence/plugin.log
- expected_output: pass
- actual_output: pending

### acceptance-3：freely_status bridge
- id: DE-3
- requirement: 工具调用 subprocess 并返回 stdout，失败结构化
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: packaging/dsh-freely/index.js
- test_command: node --test packaging/dsh-freely/test/plugin.test.mjs
- actual_output: pass
- evidence_file: docs/B2-docs/dsh-plugin/freely-host/raw-20261101T031502Z/verification/test-evidence/plugin.log
- expected_output: pass
- actual_output: pending

## Integration
- acceptance_target: DSH web profile 加载本地插件
- testing_layer: integration
- target_environment: web profile + dsh 0.2.1-rc.5
- required_evidence: load log
- blocker_taxonomy: execution_pending_or_failed
1. `dsh plugin --profile freely-web-spike add packaging/dsh-freely`
2. `dsh --profile freely-web-spike`，断言 `[dsh-freely] loaded`。

### acceptance-4：host 加载
- id: DE-4
- requirement: web profile 加载插件且不 pending
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
- status: passed
- red-green-status: green
- artifact_ref: packaging/dsh-freely/cordis.patch.yml
- test_command: dsh --profile freely-web-spike
- expected_output: loaded
- actual_output: pending

## End-to-End
- acceptance_target: 一个 issue 从 Manager 到 PR 全程无 ACP
- testing_layer: end_to_end
- target_environment: web profile + real issue
- required_evidence: issue/PR links
- blocker_taxonomy: execution_pending_or_failed
1. 真实 issue E2E（未实现）。

### acceptance-5：issue→PR
- id: DE-5
- requirement: 全程无 ACP，消息不丢，gate 阻断
- surface_kind: e2e
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
- status: pending
- red-green-status: pending
- artifact_ref: docs/B2-docs/dsh-plugin/freely-host
- test_command: manual e2e
- expected_output: issue→PR
- actual_output: pending

## Real-Environment
- real_environment_status: fail
- real_environment_reason: P1 插件已在 web profile 加载（manager=freely-manager-*）；issue→PR E2E 未跑，不能 pass。

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
- expected_output: pass
- actual_output: pending

### acceptance-2
- id: DE-2
- requirement: 工具白名单
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: packaging/dsh-freely/index.js
- test_command: node --test packaging/dsh-freely/test/plugin.test.mjs
- expected_output: pass
- actual_output: pending

### acceptance-3
- id: DE-3
- requirement: freely_status bridge
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: packaging/dsh-freely/index.js
- test_command: node --test packaging/dsh-freely/test/plugin.test.mjs
- expected_output: pass
- actual_output: pending

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
- test_command: dsh --profile freely-web-spike
- expected_output: loaded
- actual_output: pending

### acceptance-5
- id: DE-5
- requirement: issue→PR
- surface_kind: e2e
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
- status: pending
- red-green-status: pending
- artifact_ref: docs/B2-docs/dsh-plugin/freely-host
- test_command: manual e2e
- expected_output: issue→PR
- actual_output: pending
