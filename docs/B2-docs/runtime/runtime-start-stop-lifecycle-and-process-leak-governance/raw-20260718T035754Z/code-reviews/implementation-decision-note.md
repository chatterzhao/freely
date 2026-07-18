# IDN: ACP binary 自愈回写
- issue_id: I-20260718T035754Z-A
- decision: bridge PATH成功分支 upsert_config_key 回写；|| true 保护；幂等
- why_this: 单行修复，自我修复；对已正常工作系统零影响（config 已填则走缓存分支）
- alternatives_considered: ①修 init resolution 链——改动面大且需手工重跑 init；②daemon status 路径写回——status 是只读操作不应写 config
- boundary_non_goals: 不改 init/agent-table/slot 解析；不回填非 claude 的 binary（其他 tool 的 bridge 首次启时同理触发）
- residual_risk: freely_config.py upsert 可能失败（python/module 不可用）→ `|| true` 降级，bridge 仍用 PATH fallback 正常启动
