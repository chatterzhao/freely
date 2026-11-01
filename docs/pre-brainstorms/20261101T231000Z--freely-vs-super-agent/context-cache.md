---
analysis_id: CC-20261101T231000Z
phase_state: in_progress
topic: Freely 的 prompt 顺序与 cache 语义
created_at: 2026-11-01
---

# 上下文与缓存：Freely 已经有排序，但没有契约

## 0. 先纠正一个过度表述

之前写“Freely 没有稳定前缀”，不准确。读 `freely` 的 prompt 组装和 `start-lead-agent.sh` 后，实际顺序是：

1. **STABLE**：`=== Agent 角色定义 ===`（manager-agent.md / worker-agent.md）
2. `start-lead-agent.sh` 输出：Intent、Constitution、任务/工位等
3. **SEMI-STABLE**：fleet worktree 状态（只在工位变化时变）
4. **STABLE**：exit contract 格式（`a2a-exit` 指令；resume 时跳过）
5. **DYNAMIC**：scan、chat intake、continuation、context warning、checkpoint、supervision alert
6. **DYNAMIC**：auto-retry hint
7. **MANAGER-ONLY / DYNAMIC**：thread history、unconsumed workers
8. **DYNAMIC**：session handoff/continuity（最后追加）

还有 `fresh_with_handoff` 的特殊路径：当 context 超过阈值时，只发 handoff 内容（几 KB），不重发 68KB 全量 prompt。

所以 Freely 不是“没有前缀纪律”，而是：**有粗粒度排序 + 注释，但没有显式 manifest/校验；cache 语义也没被验证。**

## 1. ACP 传输层的事实

`run-acp-prompt.py`：

- `session/new` / `session/resume` / `session/fork` 的 params 只有 `cwd`、`mcpServers: []`、可选 `sessionId`；**没有 systemPrompt 字段**。
- 完整 prompt 通过 `session/prompt` 的 `prompt: [{type:text, text: prompt_text}]` 发送。
- 每次 prompt 都发完整文本，不是“只发 delta”；resume 时依赖服务端会话记忆，但仍发送本轮 prompt。
- 因此 cache 是否命中，取决于 ACP agent/provider 对会话前缀的缓存策略，不是 Freely 自己能保证的。

## 2. Cache 日志的事实

`run-acp-prompt.py` 从 `usage` 取：

- `cache_read_input_tokens` / `prompt_cache_hit_tokens` → `cache_hit`
- `cache_creation_input_tokens` / `prompt_cache_miss_tokens` → `cache_miss`
- `input_tokens` / `prompt_tokens` → `input`
- 若 `total_tokens==0 && input_tokens==0`，用 `prompt_bytes // 4` 估算 `input`，`total=input`。

问题：

- 没有 `usage_reported` 标志；只能靠 `input == prompt_bytes//4` 反推（`harness-status` 现在这么做）。
- `cache_hit/miss=0` 既可能是“没缓存”，也可能是“provider 没上报”，日志无法区分。
- 没有记录 provider/model/prompt hash/prefix hash，无法回归“同一前缀是否命中”。
- `[CACHE]` 行重复打印两次，聚合时靠去重；不是结构化事件。

## 3. 与 Super-agent 的对比

| 维度 | Super-agent | Freely |
| --- | --- | --- |
| 排序 | 明确段序，Policy 置尾，revision 绑定 | STABLE/SEMI/DYNAMIC 注释 + 顺序 |
| 强制 | 代码构造 prompt，顺序内建 | shell 拼接，顺序靠注释/约定 |
| 小上下文 | Inline/Spill、Chain of Recall | 文档长期记忆；handoff-only prompt |
| cache 指标 | 无 cache 指标 | `[CACHE]` 日志，但多为估算 |
| 可回归 | 无 | 无 prompt hash/prefix hash |

结论：**Super-agent 的排序更“内建”，Freely 的排序更“约定”；两者都没有可验证的 cache 命中率。** Freely 不是缺排序，是缺“契约 + 度量”。

## 4. 建议（研究结论，不是实现）

1. **显式 prompt manifest**：每轮记录段名、顺序、hash、字节数；CI/测试校验“STABLE 段必须在 DYNAMIC 段之前”。
2. **usage_reported / cache_reported**：区分 provider 上报、估算、缺失；不要用 `input==bytes//4` 猜。
3. **prefix hash**：对稳定前缀做 hash；同一 hash 的连续 cycle 才能比较 cache。
4. **保留 handoff-only 路径**：context 超阈值时只发 handoff，是正确方向；应记录触发原因。
5. **不要让 skill 插入动态内容到前缀**：skill 文本属于稳定段，运行时状态属于尾部。

## 5. 未解

- ACP provider 到底缓存“会话历史”还是“system prompt”？不同 harness 可能不同。
- `session/resume` 是否真的复用 provider cache，还是只复用会话状态？
- 是否要把 `[CACHE]` 升级为结构化事件（DB 表），而不是日志行？
- prompt manifest 的 hash 要不要包含 model/provider 版本？
- Fresh vs fork vs resume 的 cache 对照实验怎么做（同一任务、同一 prompt）？
