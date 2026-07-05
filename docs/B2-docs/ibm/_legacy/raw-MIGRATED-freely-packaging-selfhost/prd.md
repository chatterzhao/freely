# PRD: Freely 打包与自举验证

## Goal

建立 Freely 的可重复打包机制，用打包版本开发 Freely 自己（自举验证），作为 merge 到 develop 的前置门禁。

## Requirements

1. `bin/freely-package` 根据 allowlist 打包独立可运行的 Freely 版本
2. `bin/test-pre-merge-selfhost` 在 test-pre-merge 批次上执行自举验证
3. `docs/system/workspace/package-allowlist.txt` 定义产品交付边界
4. 版本号格式：YYYYMMDD-nightly（develop）/ YYYY.MM.DD-stable（main）
5. 自举验证通过 = frely doctor PASS + daemon 正常启动 + 完整 Manager cycle

## Scope

- `bin/freely-package` — 打包入口脚本
- `bin/test-pre-merge-selfhost` — 自举验证门禁脚本
- `docs/system/workspace/package-allowlist.txt` — 打包清单
- Versioning: YYYYMMDD-nightly, YYYY.MM.DD-stable

## Non-Goals

- nightly 自动发布 CI
- 用户项目打包
- 版本升级迁移
- 缓存优化验证

## Dev-Loop Handoff

### 前置条件
- B2_IBM 产物已批准（PRD, pre-tests, tasks, 实现决策说明）
- 当前 develop 无阻碍 test-pre-merge 的未合并改动

### 实现顺序
1. 创建 `package-allowlist.txt`
2. 实现 `bin/freely-package`
3. 实现 `bin/test-pre-merge-selfhost`
4. 在 develop 上打包自举验证
5. 修复自举失败问题（如有）
6. 输出验证报告

### 验收标准
- 打包产物可独立运行
- 自举验证门禁通过
- 所有 pre-tests 通过
