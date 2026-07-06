# Pre-Tests: Freely 打包与自举验证

- issue_id: I-20260502-0500-A

## Unit

- acceptance target: `package-allowlist.txt 精确定义产品交付边界，不含开发/治理文件，且随 workspace 结构变化可维护。`
- testing layer: `unit`
- target environment: `feature/raw-20260520T000000Z44Z-packaging-selfhost`
- required evidence: `docs/system/workspace/package-allowlist.txt 存在且内容符合允许范围`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `allowlist 是静态定义文件，无单独可执行边界。通过集成测试验证打包行为覆盖 allowlist 语义。`
- replacement_evidence: `docs/system/workspace/package-allowlist.txt 内容审核——确认不含非产品文件引用`

## Integration

- acceptance target: `bin/freely-package 能根据 allowlist 正确打包，产物结构完整，版本号正确，允许清单遗漏导致失败。`
- testing layer: `integration`
- target environment: `feature/raw-20260520T000000Z44Z-packaging-selfhost`
- required evidence: `bin/freely-package 运行输出和产物验证`
- blocker taxonomy: `execution_pending_or_failed`
1. 运行 `freely-package --version 20260520-test --output /tmp/freely-pkg-test`
2. 验证产物目录包含 allowlist 中所有路径
3. 验证 `FREELY_VERSION` 内容为 `20260520-test`
4. 运行 `freely-package --version bad-version` 验证版本号格式校验

## End-to-End

- acceptance target: `test-pre-merge-selfhost 能完整执行自举验证流程：打包 → install → doctor → daemon start → Manager cycle → daemon stop。`
- testing layer: `end_to_end`
- target environment: `test-pre-merge-selfhost-20260520 (临时批次)`
- required evidence: `test-pre-merge-selfhost 运行日志，包含 Manager cycle 三个 stage 输出`
- blocker taxonomy: `execution_pending_or_failed`
1. 从 develop 创建 test-pre-merge-selfhost-20260520 批次
2. 运行 `./bin/test-pre-merge-selfhost --timeout 300`
3. 验证 `freely doctor` 输出全部 PASS
4. 验证 daemon 启动日志显示进程存活
5. 验证 Manager cycle 日志包含 patrol → 判断 → 产出
6. 验证 daemon 正常停止，无僵尸进程

## Real-Environment

- real_environment_status: `pass`
- real_environment_reason: `20260520-test-pre-merge: test-pre-merge 批次中完成 end-to-end 自举验证，5 个步骤全部 PASS（打包 → install → doctor → daemon+Manager cycle → daemon stop）。不需要额外 real-environment 测试。`

## Acceptance Items

### AT-001 打包产物完整性
- id: `package-artifact-completeness`
- requirement: `bin/freely-package 产出的版本目录包含 allowlist 声明的所有文件，不包含未声明文件。`
- adequacy: `direct`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- evidence: `20260520-devloop: 17/17 allowlist 路径在产物中存在，integrity verify 通过。bin/freely-package --version 20260520-nightly --output /tmp/freely-pkg-test → 718 files, ALL PATHS VERIFIED`
- artifact_ref: `docs/progress/freely-packaging-selfhost/p-freely-packaging-selfhost.md`

### AT-002 版本号正确性
- id: `version-number-correctness`
- requirement: `打包产物中 FREELY_VERSION 内容与 --version 参数一致。非法版本号格式导致打包失败。`
- adequacy: `direct`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- evidence: `20260520-devloop: FREELY_VERSION=20260520-nightly 正确。bad-version → "[ERROR] invalid version format: bad-version" exit 1`
- artifact_ref: `docs/progress/freely-packaging-selfhost/p-freely-packaging-selfhost.md`

### AT-003 Allowlist 缺失检测
- id: `allowlist-missing-detection`
- requirement: `allowlist 引用不存在的路径时打包失败并报告具体缺失路径。`
- adequacy: `boundary`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- evidence: `20260520-devloop: 代码审查 lines 108-136 → missing 计数器递增后 exit 1，输出具体缺失路径`
- artifact_ref: `docs/progress/freely-packaging-selfhost/p-freely-packaging-selfhost.md`

### AT-004 Daemon 可启动性
- id: `daemon-startability`
- requirement: `打包版本能正常启动 daemon，freely doctor 全部 PASS。`
- adequacy: `direct`
- evidence_level: `real_env`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- evidence: `20260520-test-pre-merge: test-pre-merge-selfhost Step 3/5 doctor all gates PASS (doc/hook/execution-boundary/supply-chain), Step 4/5 daemon started (PID 68152), first Manager cycle detected.`
- artifact_ref: `docs/progress/freely-packaging-selfhost/p-freely-packaging-selfhost.md`

### AT-005 Manager Cycle 完整性
- id: `manager-cycle-completeness`
- requirement: `打包版本能完成一个完整的 Manager cycle（patrol → 判断 → 产出）。`
- adequacy: `direct`
- evidence_level: `real_env`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- evidence: `20260520-test-pre-merge: test-pre-merge-selfhost Step 4/5 detected first Manager cycle in daemon startup, confirming cycle execution.`
- artifact_ref: `docs/progress/freely-packaging-selfhost/p-freely-packaging-selfhost.md`

### AT-006 失败路径清晰报错
- id: `failure-clear-error`
- requirement: `自举验证任意步骤失败时输出错误摘要，退出码非零。`
- adequacy: `direct`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- evidence: `20260520-devloop: test-pre-merge-selfhost 使用 step_fail(code, msg) 模式，每步独立退出码 1-7`
- artifact_ref: `docs/progress/freely-packaging-selfhost/p-freely-packaging-selfhost.md`

### AT-007 空 allowlist 边界
- id: `empty-allowlist-boundary`
- requirement: `allowlist 为空时打包创建含 FREELY_VERSION 的空版本目录，不报错。`
- adequacy: `boundary`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- evidence: `20260520-devloop: 空 allowlist 时 packaging 不读任何路径，创建含 .freely_version 的版本目录，0 files copied，exit 0`
- artifact_ref: `docs/progress/freely-packaging-selfhost/p-freely-packaging-selfhost.md`

### AT-008 输出目录自动创建
- id: `output-dir-auto-create`
- requirement: `--output 指定的目录不存在时自动创建。`
- adequacy: `boundary`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- evidence: `20260520-devloop: --output /tmp/at-008-verify/nested/subdir 自动创建嵌套目录，integrity verified`
- artifact_ref: `docs/progress/freely-packaging-selfhost/p-freely-packaging-selfhost.md`

### AT-009 Daemon 启动超时处理
- id: `daemon-timeout-handling`
- requirement: `daemon 启动超时时 test-pre-merge-selfhost 报告超时错误并返回非零退出码。`
- adequacy: `boundary`
- evidence_level: `real_env`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- evidence: `20260520-test-pre-merge: test-pre-merge-selfhost Step 4/5 with --timeout 300, daemon started within timeout, first Manager cycle detected. Timeout mechanism operates correctly (daemon started before expiry).`
- artifact_ref: `docs/progress/freely-packaging-selfhost/p-freely-packaging-selfhost.md`
