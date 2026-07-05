---
local_id: raw-20260623T075200Z00Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260623T075200Z-A
platform_ids:
  github:
    issue_id: '3386'
    url: https://github.com/chatterzhao/freely/issues/3386
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-23T07:52:18Z'
updated_at: '2026-06-23T16:23:11Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 背景

#3381 分析发现：33 个 AI 周期的 `[CACHE]` 日志行全部显示 `input=0 cache_hit=0 cache_miss=0 output=0 total=0`。

原因：`run-acp-prompt.py`（第 545-552 行）从 ACP `session/prompt` 响应中读 `usage` 字段：
```python
usage = prompt_result.get("usage") or {}  # 始终为空 {}
```
ACP 服务器（claude-agent-acp）不把底层模型 API 返回的 `usage` 透传到 `session/prompt` 的 JSON-RPC 响应中。

影响：完全看不见 token 消耗和 cache 命中率，成本可观测性为零。#3384 的 L2（Token 空转检测）需要 token 数据。

## 注意：核心改动在外部依赖

**claude-agent-acp 是独立项目，不在 Freely 仓库内。** 阶段 1 需要向 ACP 项目提 issue/PR，或确认 ACP 协议是否已支持 `usage` 透传但 Freely 侧未启用。

## 要做的事

### 阶段 1：ACP 侧（外部依赖）
- 向 claude-agent-acp 提 issue：`session/prompt` JSON-RPC 响应的 `result` 中应包含底层模型 API 返回的 `usage` 对象
- Anthropic API：透传 `cache_read_input_tokens` / `cache_creation_input_tokens` / `input_tokens` / `output_tokens`
- DeepSeek API：透传 `prompt_cache_hit_tokens` / `prompt_cache_miss_tokens` / `prompt_tokens` / `completion_tokens`
- 如果 ACP 协议已支持但命名不同，确认实际字段名

### 阶段 2：Freely 侧——有 usage 数据时
- `run-acp-prompt.py` 第 547-548 行已处理两种命名（Anthropic/DeepSeek），无需改动
- `freely` 第 21589 行的 `append_runtime_event "cache_metrics"` 追加 `input_tokens`、`output_tokens`、`cache_hit_tokens`、`cache_miss_tokens`、`total_tokens`
- 确认 `freely_db_manager.py` 的 runtime event 写入支持动态新增字段（向后兼容）

### 阶段 3：Freely 侧——workaround（ACP 短期修不了时）
- `run-acp-prompt.py` 自行统计：记录 prompt_bytes + 响应 bytes 长度，作为 token 下限估计
- `[CACHE]` 行至少显示 `prompt_bytes`（已有）和 `response_bytes`（新增），减少全零盲区
- 估算公式：token ≈ bytes / 4（中英文混合）

### 阶段 4：可观测性告警
- 连续 N 轮 `input_tokens > 0` 但 `cache_hit_tokens = 0` → runtime event 告警
- 注意区分：DeepSeek 自动前缀缓存可能不报告 hit 数字 → 不等于缓存没工作 → 告警措辞应为 "cache hit 不可观测"而非 "缓存失效"

## 成功标准
- ACP 侧 issue 已提交（追踪链接）
- Freely 侧：`[CACHE]` 日志行显示非零 token 数据（至少 prompt_bytes 和 response_bytes）
- `cache_metrics` 事件包含 token 级指标
- #3384 L2 有数据源（或降级方案可用）

## 依赖
- 被 #3384（L0-L3 兜底）的 L2 依赖

## 参考
- 原始分析：https://github.com/chatterzhao/freely/issues/3381
- 会话 ID 污染 Bug（已修复于 `7974c4305`）
- #498：`raw-20260517T082247Z33Z`
- `run-acp-prompt.py` usage 读取：第 545-552 行
- `cache_metrics` 事件：`freely` 第 21589 行

