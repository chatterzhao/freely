# Implementation Decision Note: config.toml skip_ibm 配置
- issue_id: I-20260712T105347Z-A
- decision: 在 config.toml 中增加 [skip_ibm_gate] allowed_paths 列表，governance-merge-gate 读取并合并
- why_this: 硬编码路径无法适应项目特定治理目录，TOML 配置简单可靠
- alternatives_considered: 环境变量(不安全)，命令行参数(不易持久化)
- boundary_non_goals: 不改变 skip gate 的判断逻辑本身
- residual_risk: tomllib 不可用时会静默跳过配置路径(向后兼容)
