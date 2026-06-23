# Brainstorm: ACP usage 透传 workaround
## Discovery: #3386, ACP 不返回 usage 导致 [CACHE] 全零
## Research: 外部依赖 claude-agent-acp。Freely 侧可做 bytes→tokens 估算作为 workaround
## Decision: prompt_bytes/4 估算 + cache_metrics 加 estimated_input_tokens。等 ACP 修了再换真实数据。
