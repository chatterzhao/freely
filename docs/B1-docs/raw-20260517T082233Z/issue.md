---
local_id: raw-20260517T082247Z33Z
kind: raw
priority: P2
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
source: chat-inbox
created_at: '2026-05-17T08:22:33Z'
title: 实现跨模型 cache 命中率检测模块，支持 Anthropic/DeepSeek/OpenAI 等多提供商
platform_ids:
  github:
    issue_id: '498'
    url: https://github.com/chatterzhao/freely/issues/498
    synced_at: '2026-05-17T08:22:41Z'
updated_at: '2026-05-17T08:22:41Z'
primary_platform: github
platform_state: closed
---

## 背景

当前 `run-acp-prompt.py` 已有 cache 字段提取（行 448-449）：
```python
cache_hit = usage.get("cache_read_input_tokens") or usage.get("prompt_cache_hit_tokens") or 0
cache_miss = usage.get("cache_creation_input_tokens") or usage.get("prompt_cache_miss_tokens") or 0
```

已覆盖 Anthropic (`cache_read_input_tokens`/`cache_creation_input_tokens`) 和 DeepSeek (`prompt_cache_hit_tokens`/`prompt_cache_miss_tokens`)。

## 问题

1. Cache 数据仅打印到 cycle log (`[CACHE]` 行)，未结构化存储
2. `cache_metrics` runtime event 不含 token 级数据（只有 `prompt_bytes`、`resume_streak`）
3. 无法跨会话聚合分析 cache 命中率趋势
4. 无法基于 cache 命中率做优化决策（如调整 prompt 结构）

## 设计

创建 `docs/system/workspace/scripts/runtime/cache-metrics.py` 模块：

### 功能
- 解析 ACP `session/prompt` 返回的 `usage` 字段，提取各提供商的 cache 数据
- 存入 SQLite（`cache_metrics` 表），支持按 session/tool/时间 查询
- 在 `freely live-status` 中展示 cache 命中率
- 在 `manager-agent.md` 中增加根据 cache 命中率调整 patrol 策略的指导

### 支持的提供商 cache 字段

| 提供商 | cache_hit | cache_miss |
|--------|-----------|------------|
| Anthropic | `cache_read_input_tokens` | `cache_creation_input_tokens` |
| DeepSeek | `prompt_cache_hit_tokens` | `prompt_cache_miss_tokens` |
| OpenAI | (待确认) | (待确认) |

### 参考
- DeepSeek API 文档已在 `usage` 字段中返回 `prompt_cache_hit_tokens`/`prompt_cache_miss_tokens`
- Anthropic 文档：https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching

## 范围
- 新增 `docs/system/workspace/scripts/runtime/cache-metrics.py`
- 增强 `cache_metrics` runtime event 包含 token 级数据
- `freely live-status` 增加 cache 命中率展示
