# Pre-Tests: bin 投影注册表分类落地（C-A）
- issue_id: I-20261111T125724Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 35 条按设计意图逐条分类（22 standalone / 13 待迁移）、每条具体 reason；lint 加 class 白名单与占位 reason 拒绝；coverage/staleness/shrink 三条原规则对 standalone-tool 同样生效；基线因占位 reason 判红
- acceptance_target: 分类落地且不产生永久豁免、门禁强度不降
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 真实 `bin/check-bin-projection` 对构造的临时项目目录运行（不触网、不动真平台）
- required_evidence: AT-001 静态 8 + 行为 6 + 基线控制 2 全 GREEN；unit 7 项 PASS
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-bin-projection-classification.py
- test_command: python3 docs/system/workspace/scripts/tests/test-bin-projection-classification.py
- expected_output: SUMMARY: 14 ok, 0 failed
- expected_RED_output: SUMMARY: 7 ok, 9 failed
- actual_RED_output: develop 63de67645 快照上 S1/S2/S3/S4/S5/S6/S8 全红（无 standalone-tool 类别、35 条仍是占位 reason、lint 无 class/placeholder 校验）；B5/B6 红；基线 R1/R2 通过，证明 35 条占位 reason 真实存在（AT-001-RED.log）
- actual_output: SUMMARY: 14 ok, 0 failed；B2 coverage、B3 staleness、B4 shrink（对 standalone-tool 同样生效）、B5 非法 class、B6 占位 reason 全部按预期拒绝（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/command-wrapper/pr-review-projection/raw-20261111T125724Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log,unit-t-bin-projection-01.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4
- case_design: 静态组读真实注册表校验类别数量与非占位 reason、读 lint 源码确认三条原规则与新校验都在；行为组在临时项目里构造 bin/ 文件 + 注册表，调用**真实** `check-bin-projection --json`，逐条负向验证六条规则；基线组对 develop 源码断言 35 条占位 reason 与缺失 class。
- red_how: fix RED — git archive develop 导出基线树，用 --source-dir 与 --baseline 运行同一 AT。

## Unit
- acceptance_target: 分类计数、三条门禁规则、新校验、真实仓库 lint 通过
- testing_layer: unit
- target_environment: feature/raw-20261111T125724Z-bin-projection-batch
- required_evidence: t-bin-projection-01.sh 7 项 PASS
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/unit/t-bin-projection-01.sh

## Integration
- acceptance_target: 既有 lint / CI 子集不退化
- testing_layer: integration
- target_environment: test-pre-merge 工位
- required_evidence: bin/test-all --ci 全绿；bin/check-bin-projection ok；三门禁 ok
- blocker_taxonomy: execution_pending_or_failed
1. bin/test-all --ci

## End-to-End
- acceptance_target: 本轮 PR 与收口链路不受分类改动影响
- testing_layer: end-to-end
- target_environment: 本 issue 的 pr-create-guarded / wt-close
- required_evidence: PR 创建与合并成功
- blocker_taxonomy: execution_pending_or_failed
1. ./bin/freely pr-create-guarded

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 35 条占位登记是 R32 真实遗留；本轮用真实注册表与真实 lint 验证分类，行为零变化。
