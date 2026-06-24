# Implementation Decision Note: tool-registry TOML 配置驱动（Phase 1+2）
- issue_id: I-20260624T013737Z-A
- issue_path: docs/issues/I-20260624T013737Z-A/issue.md
- milestone: M-20260624T013737Z-A

## Implementation Decision Note
- decision: JSON5 → TOML + 双文件合并 + config_schema.fields 抽象层消除权限字段硬编码
- why_this: TOML 用户更友好（已有 config.toml 先例）；双文件合并让用户可扩展而不改源码；config_schema 翻译层是消除全部 28 处硬编码的基础模式
- alternatives_considered: (1) 保留 JSON5 只加字段 — JSON5 不是 TOML，用户需学两种格式 (2) 一次性全部 10 phase — 风险太高，渐进迁移更安全 (3) 用 YAML — TOML 在 Python 生态中更标准
- boundary_non_goals: 不删除旧 JSON5（并行运行）；不迁移 Phase 3-10 case 分支；不改变 tool 行为逻辑
- residual_risk: 旧 JSON5 reader（deploy-skills）需在 TOML 切换时同步更新，否则双格式不一致
