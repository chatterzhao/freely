# Pre-Tests: 物化时写入达标 H1
- issue_id: I-20261104T082542Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: raw-issue-pull 物化平台 raw issue 时必须在 frontmatter 之后写入且仅写入一个不含 [RAW-] 前缀的一级标题，本地与平台 canonical projection 的 title/body/fingerprint 完全一致；Q2 既有标题契约与兼容能力不退化；提供默认 dry-run 的安全回填命令
- acceptance_target: 消除每个新 raw issue 首次 PR 的 content_diverged，且不改写历史语料
- surface_kind: unit
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: fix/raw-20261104T082542Z-materialize-h1
- required_evidence: 新增回归测试三组全 GREEN，18 项检查；真实双平台副本 fingerprint parity；805 份真实 issue.md 的 Q2 契约退化审计；7 个相关回归
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-materialize-h1
- test_command: bash docs/system/workspace/scripts/tests/test-materialize-h1 all
- expected_output: PASS: 18 checks, 0 failed
- expected_RED_output: FAIL: 6 of 11 checks failed
- actual_RED_output: RED 6 项失败（4 项单元断言复现物化无 H1 / 重复 pull 无 H1 / 非 canonical 标题无 H1，3 项 static 缺单一真源与回填命令，1 项 backfill 命令缺失）；Q2 兼容能力 5 项已 PASS（AT-001-RED.log）
- actual_output: PASS: 18 checks, 0 failed；真实双平台副本物化后 fingerprint 9140d678763e4dd9 一致，TITLE/BODY MATCH（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/platform/issue-parity/raw-20261104T082542Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5,T6
- case_design: unit 组隔离加载 platform-adapter 并替换平台 I/O，构造 github/gitee 双副本与不带 canonical 前缀的标题，断言物化后有且仅有一个 H1、H1 无身份前缀、重复 pull 幂等、非标准历史 key（20260501 / 20260503 / 20260503-0000 / MIGRATED）H1 前缀无关、Q2 created_at 兼容分支保留且本地身份不漂移；static 组校验单一真源与 Q2 五个既有能力仍在；backfill 组在隔离项目构造缺 H1 / 已有 H1 / 有 issue_title 三种文件，断言 dry-run 不写文件、apply 只补可靠来源、已有 H1 逐字节不动、二次 apply 幂等。
- red_how: fix RED — 在未修复的 develop 真源上运行同一断言组，确认物化无 H1。

## Unit
- acceptance_target: 物化 H1 契约、幂等、非标准 key、Q2 兼容不退化
- testing_layer: unit
- target_environment: 临时隔离目录 + 真实平台副本
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-materialize-h1 unit
2. bash docs/system/workspace/scripts/tests/test-materialize-h1 static

## Integration
- acceptance_target: raw_title_contract 单一真源与 Q2 既有函数零差异
- testing_layer: integration
- target_environment: 805 份真实 B1 issue.md
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-materialize-h1 all

## End-to-End
- acceptance_target: 真实双平台副本物化后本地与平台 fingerprint 一致
- testing_layer: end-to-end
- target_environment: GitHub #4181 / Gitee IKSWR8 真实副本
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-materialize-h1 backfill
2. python3 真实 pull_raw_issue + canonical_projection parity 验证（evidence 记录）

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 在真实 fix 工位以项目真源命令执行 wt-create 创建 dev 与 test 双工位并物化成功（物化时确认 H1 缺失，复现缺陷）；用真实双平台副本执行修复后的 pull_raw_issue，本地与平台 canonical_projection 的 fingerprint 均为 9140d678763e4dd9、title 与 body 双 MATCH；805 份真实 issue.md 上 Q2 四个既有函数新旧对比 0 差异；7 个相关回归测试（含 Q1/Q2/R1）全 PASS；bin/check-epics-map 对齐通过。
