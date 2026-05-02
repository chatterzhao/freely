# Code Review: Freely 打包与自举验证

- issue_id: I-20260502-0500-A
- review_date: 2026-05-02

## Implementation

- `bin/freely-package`：打包脚本，根据 package-allowlist.txt 复制 workspace 能力文件到版本目录
- `bin/test-pre-merge-selfhost`：自举验证门禁，打包 → 启动 daemon → 验证 Manager cycle
- `docs/system/workspace/package-allowlist.txt`：打包清单，定义 Freely 产品交付内容

## Implementation Decision Note

- decision: 通过 allowlist 机制打包 workspace 能力文件，用打包版本进行自举验证。版本号采用 YYYYMMDD-nightly 和 YYYY.MM.DD-stable。
- why_this: 编译器自举模型是最严格的正确性验证——打包版本能开发 Freely 自己即为通过。allowlist 比代码审计更简单可靠。
- alternatives_considered: 1) 全量复制整个 repo（太重，包含开发文档）2) 手动指定文件列表（易遗漏）3) 不打包直接开发树运行（T0 不稳定，无法验证缓存优化）
- boundary_non_goals: 不处理 nightly 自动发布 CI，不处理用户项目的打包，不处理版本升级迁移
- residual_risk: allowlist 需要随 workspace 结构变化维护，遗漏会导致打包不全

## Verification

- 打包版本 `freely doctor` 全部 PASS
- 打包版本成功启动 daemon，完成 Manager cycle，正常停止
