---
b1_id: B1-20260706T084817Z
phase_state: completed
source_raw: raw-20260706T084817Z
source_url: https://github.com/chatterzhao/freely/issues/3774
produced_candidate: C-20260706T084817Z-A
created_at: 2026-07-06
---

# B1: 多 Agent 独立 Base Tool — agent-table 唯一真源

## Input
- raw-20260706T084817Z (#3774)
- agent-table.toml 已存在，定义 manager→claude, worker→opencode, reviewer→cline
- _init_agent_table_slot_pin 已实现 agent-table → AGENT_AI_TOOL 的链路

## Discovery

### value_check: 当前代码问题
1. AI_TOOL env var (211处) 形成降级链: `${AI_TOOL:-codex}` 硬编码 fallback
2. agent-table 已配置 per-role slot 但代码绕过它直接读 AI_TOOL
3. 多 agent 场景下 AI_TOOL 全局变量无法区分 manager vs worker 的不同 tool
4. bin/pr-review-guarded 硬编码 `REVIEWER_SLOT="${AI_TOOL:-claude-apikey-ds-pro-auto}"`

### scope_check: 改动范围
- 主脚本 freely: ~200 处替换
- bin/pr-review-guarded: 1 处
- bin/freely-review: 1 处注释
- skills 文档: 2 处提及

### 架构分析

当前多 agent tool 分配链路:
```
agent-table.toml → _init_agent_table_slot_pin() → AGENT_AI_TOOL export
                                                      ↓
                                            _ensure_acp_bridge_running
                                            _bridge_env_for_registered_tool
```

旧 AI_TOOL 降级链（应删除）:
```
AI_TOOL env var → ${AI_TOOL:-codex} → 绕过 agent-table
AI_TOOL_ADAPTER → 直接使用
AI_TOOL_ADAPTER_POLICY → 直接使用
```

## Brainstorm

### Option A: 全局替换 AI_TOOL → AGENT_AI_TOOL
- 把 211 处 AI_TOOL 全部改为 AGENT_AI_TOOL
- 保留 export AI_TOOL=$AGENT_AI_TOOL 向后兼容桥
- 风险: 向后兼容桥仍是降级链，agent-table 不是唯一真源

### Option B: 彻底移除 AI_TOOL，agent-table 唯一真源 ✅
- 211 处 → AGENT_AI_TOOL
- 删除 export AI_TOOL 桥
- 删除 unset AI_TOOL 清理
- 所有需要 tool 信息的地方从 AGENT_AI_TOOL 或其派生变量读取
- agent-table 查询失败 → 明确报错，不降级

### Option C: 保留 AI_TOOL 作为用户配置入口
- agent-table 读取 AI_TOOL 作为 fallback
- 不推荐: 多 agent 场景下全局 AI_TOOL 没有意义

## Decision: Option B

理由:
1. agent-table.toml 已明确声明 "AI_TOOL is deprecated"
2. 多 agent 架构必须 per-role slot，全局 AI_TOOL 无意义
3. 降级链隐藏配置错误——应该报错让用户修，不是静默 fallback
4. agent-table-query CLI 工具已可用

## Candidate
- candidate_id: C-20260706T084817Z-A
- status: promoted
- milestone: M-20260706T084817Z-A
