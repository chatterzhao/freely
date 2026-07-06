---
b1_id: B1-20260706T084817Z
phase_state: completed
source_raw: raw-20260706T084817Z
produced_candidate: C-20260706T084817Z-A
---
# B1: 移除 AI_TOOL 降级链

## Problem
agent-table.toml 已是多 agent 唯一真源，但 211 处 AI_TOOL 引用形成降级链。

## Fix
- AI_TOOL → AGENT_AI_TOOL
- AI_TOOL_ADAPTER → AGENT_AI_TOOL_ADAPTER  
- AI_TOOL_ADAPTER_POLICY → AGENT_AI_TOOL_ADAPTER_POLICY
- 去掉硬编码 fallback
- 保留 AI_TOOL_CAPABILITIES/POLICY 配置键
- 保留 export AI_TOOL 向后兼容 bridge

## Candidate
- candidate_id: C-20260706T084817Z-A
- status: promoted
- milestone: M-20260706T084817Z-A
