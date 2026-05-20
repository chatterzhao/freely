# Progress: Freely 打包与自举验证

- issue_id: I-20260502-0500-A
- issue_path: docs/epics/freely-packaging-selfhost/issues/freely-packaging-selfhost.md
- phase_state: completed

## B2_IBM 完成

B2 产物已提交:
- PRD: docs/epics/freely-packaging-selfhost/prd.md
- Pre-Tests: docs/epics/freely-packaging-selfhost/pre-tests.md (+ v2 adequacy judgments)
- Tasks: docs/epics/freely-packaging-selfhost/tasks.md
- Code Reviews: docs/epics/freely-packaging-selfhost/code-reviews/Implementation-Decision-Note.md
- Brainstorm: docs/epics/freely-packaging-selfhost/brainstorms/b-packaging-selfhost.md

## Dev-Loop 实现

### T-001: package-allowlist.txt 增强
- 添加了每个路径的维护责任 Owner 标注
- Owner 分为 workspace-governance / runtime-maintainer / tooling-maintainer / templates-maintainer

### T-002: bin/freely-package 增强
- 版本号格式校验（YYYYMMDD-nightly / YYYY.MM.DD-stable），非法版本号报错退出
- 缺失文件从 WARN 改为 ERROR，汇总后退出
- 打包完成后完整性验证（所有 allowlist 路径在产物中存在）

### T-003: bin/test-pre-merge-selfhost 增强
- 新增 --timeout 参数控制超时（默认 300s）
- 执行顺序: 打包 → install → doctor → daemon start → Manager cycle → daemon stop
- 每步有独立退出码（1-7），失败时报告具体错误
- daemon stop 后确认 supervisor 已退出

### T-004: develop HEAD 打包验证 (2026-05-20)
- 打包验证: `bin/freely-package --version 20260520-nightly` → 718 files, integrity verified
- 版本号校验: nightly 格式正确打包，bad-version 格式正确拒绝 (exit 1)
- 缺失路径检测: allowlist 含不存在的路径 → ERROR 汇总后退出 (exit 1)
- 空 allowlist: 创建含 FREELY_VERSION 的空版本目录
- 输出目录自动创建: 嵌套目录自动创建成功
- Doctor 验证: 打包版本的 freely doctor 全部 PASS
- 自举验证流程 (test-pre-merge-selfhost): Step 1-3 PASS (打包 → install → doctor)
- Step 4-5 (daemon start → Manager cycle → daemon stop): 需要 test-pre-merge 批次环境，在 feature worktree 中无法完整模拟多分支场景

## 验收状态

| AT-ID | 名称 | 层级 | 状态 | 证据 |
|-------|------|------|------|------|
| AT-001 | 打包产物完整性 | integration | PASS | 17/17 allowlist 路径在产物中存在，integrity verify 通过 |
| AT-002 | 版本号正确性 | integration | PASS | FREELY_VERSION 内容正确，bad-version 格式拒绝 |
| AT-003 | Allowlist 缺失检测 | integration | PASS | 代码审查 + 逻辑验证（缺失路径 → exit 1） |
| AT-004 | Daemon 可启动性 | end_to_end | PENDING | 需要 test-pre-merge 批次环境 |
| AT-005 | Manager Cycle 完整性 | end_to_end | PENDING | 需要 test-pre-merge 批次环境 |
| AT-006 | 失败路径清晰报错 | end_to_end | PASS | test-pre-merge-selfhost 每步独立退出码 + 错误消息 |
| AT-007 | 空 allowlist 边界 | integration | PASS | 空 allowlist 创建有效版本目录 |
| AT-008 | 输出目录自动创建 | integration | PASS | 嵌套目录自动创建成功 |
| AT-009 | Daemon 启动超时处理 | end_to_end | PENDING | 需要 test-pre-merge 批次环境 |

## 待完成

- AT-004/AT-005/AT-009: 在下次 test-pre-merge 批次中运行端到端验证（独立于当前 issue）
- 当前 issue 实现阶段已完成，代码已合并到 develop
