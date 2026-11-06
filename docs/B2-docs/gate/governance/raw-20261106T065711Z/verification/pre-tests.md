# Pre-Tests: 批量化治理门禁读取
- issue_id: I-20261106T065711Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 治理门禁改用批量读取后，同一输入的 verdict、warning、退出码逐字节不变；staged / range / disk 三视图优先级与 FileNotFoundError 语义保持；Step 2e 评论决议的计数、判定与输出不变；git 子进程数降到个位数
- acceptance_target: 零语义变化的性能优化，禁止改搜索字段、重试、视图优先级与判定规则
- surface_kind: unit
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: feature/raw-20261106T065711Z-gate-batch-read
- required_evidence: 新增回归测试四组全 GREEN，含三视图优先级行为测试、6 种 gate 调用模式 parity、4,363 份真实治理文档逐函数退化审计、子进程计数
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-governance-gate-batch-read
- test_command: bash docs/system/workspace/scripts/tests/test-governance-gate-batch-read all
- expected_output: PASS: 11 checks, 0 failed
- expected_RED_output: FAIL: 9 of 10 checks failed
- actual_RED_output: RED 9 项失败（8 项 static + 1 项 unit），精确复现「无批量真源、Step 2e 仍逐文件循环、无单进程扫描」；等价性组已 PASS（AT-001-RED.log）
- actual_output: PASS: 11 checks, 0 failed；build_issue_index git 子进程 3423 → 8；Step 2e 纯计数 0.005s、完整扫描 3.487s（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/gate/governance/raw-20261106T065711Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5,T6,T7
- case_design: static 组校验两处单一真源存在、pr-create-guarded 不再逐文件循环且失败块文案保留；unit 组在临时隔离 git 仓库构造 disk / index / range 三份不同内容，逐项断言 read_repo_text 的 staged > range > disk 优先级、缺失文件 FileNotFoundError 文案、path_exists 布尔语义、staged_path_exists 与 range_path_exists 的缺失分支；equivalence 组在 804 份真实 issue.md 上比对 grep 正则与 startswith 计数、真实 grep 抽样、git show 与 git cat-file --batch 的字节一致性；perf 组分离测量纯计数算法与含 I/O 的完整扫描，并统计 build_issue_index 的 git 子进程数。
- red_how: fix RED — 在未修复的 develop 真源上运行同一断言组，确认批量真源缺失与逐文件循环。

## Unit
- acceptance_target: 三视图优先级、缺失路径语义、FileNotFoundError 文案与计数等价性
- testing_layer: unit
- target_environment: 临时隔离 git 仓库 + 真实语料
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-governance-gate-batch-read unit
2. bash docs/system/workspace/scripts/tests/test-governance-gate-batch-read equivalence

## Integration
- acceptance_target: 两处单一真源收敛且 Step 2e 失败块契约不退化
- testing_layer: integration
- target_environment: feature/raw-20261106T065711Z-gate-batch-read
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-governance-gate-batch-read static

## End-to-End
- acceptance_target: 优化前后 gate verdict 逐字节一致，子进程数下降
- testing_layer: end-to-end
- target_environment: 真实 develop 历史 range
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-governance-gate-batch-read perf
2. python3 docs/system/workspace/scripts/quality/governance-merge-gate --range 71bb71c0b..82cd1e8de

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 在真实 feature 工位以项目真源命令执行；6 种 gate 调用模式（3 种 range、range+source-branch、skip-ibm-gate、staged）新旧两版退出码与完整输出 byte-identical；--range 47.436s → 0.879s；4,363 份真实治理文档 × read_repo_text / path_exists × 双视图 0 差异；7 个直接相关回归测试以未修改 develop HEAD 复跑，0 新增失败；bin/check-epics-map 对齐通过。
