# Pre-Tests: raw 身份不漂移与平台标题达标
- issue_id: I-20261105T051136Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 平台标题不含 canonical 前缀时，物化目录名、返回值与 frontmatter 身份仍等于调用方 raw key，平台标题被修正为达标格式并同步双平台，且四处既有兼容能力不退化
- acceptance_target: 兼容判定与兼容动作解耦，本地身份唯一真源，达标规则单一真源
- surface_kind: unit
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: fix/raw-20261105T051136Z-raw-key-drift
- required_evidence: 新增回归测试三组全 GREEN，含 17 条单元断言与隔离仓库行为验证；退化审计覆盖 803 份真实 B1 issue
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-raw-key-drift
- test_command: bash docs/system/workspace/scripts/tests/test-raw-key-drift all
- expected_output: PASS: raw identity contract holds
- expected_RED_output: RED: 7 assertion(s) failed
- actual_RED_output: RED: 7 项单元断言失败，复现漂移目录 raw-20261105T051142Z、返回值与 frontmatter 身份被改写、仅一个平台被 no-op 修正且标题仍不达标；另有 8 项 static/wtcreate 检查失败（AT-001-RED.log）
- actual_output: PASS: raw identity contract holds，unit 17/17 断言通过，static 6 项与 wtcreate 3 项共 9 项检查通过（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/platform/issue-parity/raw-20261105T051136Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5
- case_design: importlib 隔离加载 platform-adapter 模块并替换平台 I/O，构造 github 与 gitee 两份无 canonical 前缀且 created_at 与调用方 key 不同的副本；断言无漂移目录、本地身份一致、双平台标题均被修正为达标格式；再单测 canonical_raw_title 的去重前缀、幂等、100 字符上限、空值兜底，并确认 _resolve_raw_identity 单条兜底与 _created_at_to_key 兼容分支仍工作；static 组校验五处真源收敛与告警契约；wtcreate 组在隔离临时仓库注入伪造的 raw-issue-pull 输出，验证错误 local_id 与缺失 issue.md 均被拒绝。
- red_how: fix RED — 在当前未修复的真源上运行同一断言组，确认 7 项失败并复现身份漂移。

### acceptance-2
- id: AT-002
- requirement: raw-issue-pull 的标准输出必须始终是单个可解析 JSON 文档，issue-sync 的诊断信息不得污染该流，且诊断仍需可见
- acceptance_target: PR review 阶段发现的真实回归守卫，保证 wt-create 的严格身份校验有可解析输入
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 临时隔离 git 仓库（不触网）
- required_evidence: stdout 可被 json.load 解析且 local_id 正确，issue-sync 诊断出现在 stderr
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-raw-key-drift
- test_command: bash docs/system/workspace/scripts/tests/test-raw-key-drift pull
- expected_output: RESULT: 2 passed, 0 failed
- expected_RED_output: json.decoder.JSONDecodeError: Extra data
- actual_RED_output: RED: 2 项检查失败，stdout 混入了 issue-sync 的两行输出，json.load 报 Extra data: line 2 column 1（AT-002-RED.log）
- actual_output: RESULT: 2 passed, 0 failed；全量套件 11 passed, 0 failed（AT-002-GREEN.log）
- evidence_file: docs/B2-docs/platform/issue-parity/raw-20261105T051136Z/verification/test-evidence/AT-002-RED.log,AT-002-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T9
- case_design: 在 mktemp 隔离 git 仓库中放置真实的 bin/raw-issue-pull，并用假的 platform-adapter（打印 JSON 并落盘 issue.md）与假的 issue-sync（打印两行诊断）替换平台依赖；执行后断言 stdout 能被 json.load 解析且 local_id 等于调用方 key，并断言 issue-sync 诊断出现在 stderr。
- red_how: fix RED — 在修复前的 raw-issue-pull 上运行同一隔离仓库测试，确认 stdout 被污染导致 json.load 失败。

## Unit
- acceptance_target: 达标纯函数契约与兼容能力的单元正确性
- testing_layer: unit
- target_environment: fix/raw-20261105T051136Z-raw-key-drift
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-raw-key-drift unit

## Integration
- acceptance_target: adapter、issue-sync、feedback edit、raw-issue-pull、wt-create 五处真源收敛且无静默失败
- testing_layer: integration
- target_environment: fix/raw-20261105T051136Z-raw-key-drift
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-raw-key-drift static

## End-to-End
- acceptance_target: wt-create 物化入口在身份不匹配或缺文件时真实拒绝，且 raw-issue-pull 输出契约不污染身份校验
- testing_layer: end-to-end
- target_environment: 临时隔离仓库（不触网）
- required_evidence: AT-001, AT-002
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-raw-key-drift wtcreate
2. bash docs/system/workspace/scripts/tests/test-raw-key-drift pull

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 在真实项目工位以项目真源命令执行 wt-create 创建 dev 与 test 双工位并物化成功；隔离仓库中四组测试全 GREEN；对 803 份真实 B1 issue.md 做新旧达标契约退化审计，14 个相关回归测试以未修改 develop HEAD 做基线对比，确认零新增失败；PR review 阶段用隔离仓库实测发现并修复了 stdout 污染回归（AT-002）。
