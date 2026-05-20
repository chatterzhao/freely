# Implementation Decision Note: Freely 打包与自举验证

## Decision

采用 allowlist 机制从 develop 打包 workspace 能力文件为独立 Freely 版本，用打包版本进行自举验证（打包版本能开发 Freely 自己即为验证通过）。版本号采用 YYYYMMDD-nightly（develop）/ YYYY.MM.DD-stable（main）双轨制。

## Why This

编译器自举模型是最严格的正确性验证范式——如果打包版本能正常完成 Manager cycle，就证明产物的功能完整性。Allowlist 机制比代码审计更简单可靠：显式声明每个产品文件，防止开发/治理文件混入发布产物。

## Alternatives Considered

| # | 方案 | 评价 |
|---|------|------|
| 1 | 全量 git archive 打包整个 repo | 太重，包含开发文档、治理文件、pre-brainstorms 等非产品内容。需额外过滤，增加复杂度 |
| 2 | 手动指定打包文件列表（硬编码在脚本中） | 易遗漏，维护成本高，修改 workspace 结构时需要同步修改脚本 |
| 3 | 不打包，直接在开发树运行 | T0 状态不稳定，无法验证缓存独立性，打包版本和开发环境可能行为不一致 |
| 4 | Docker 镜像 | 依赖 Docker 运行时，增加用户 setup 成本。对 AI 自主开发场景过重 |

## Boundary / Non-Goals

- 不处理 nightly 自动发布 CI——由外部 runner 驱动，不在仓库代码中
- 不处理用户项目的打包——仅打包 Freely 自身
- 不处理版本升级迁移—— nightly 到 stable 的升级策略后续定义
- 不验证缓存优化效果——仅验证功能正确性

## Residual Risk

| 风险 | 影响 | 缓解 |
|------|------|------|
| allowlist 随 workspace 结构变化需维护 | 遗漏新文件导致打包不全 | allowlist 注释标明维护责任；完整性验证检查引用文件是否存在 |
| 自举验证可能漏掉仅在生产环境暴露的问题 | 生产环境与开发环境行为差异 | test-pre-merge 从 develop HEAD 打包，模拟正式发布流程 |
| Manager cycle 验证深度有限 | 仅验证流程完整性，不验证输出质量 | 自举验证作为门禁下限；质量验证在后续阶段补充 |
