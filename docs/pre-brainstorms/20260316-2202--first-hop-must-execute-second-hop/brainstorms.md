# Brainstorms: first-hop-must-execute-second-hop

## Problem

Freely 当前 auto-loop 的首跳协议存在歧义：

- `lead-agent.md` 写的是“使用组装后的 prompt 进入对应第二跳 skill”
- 但 `start-lead-agent.sh` 的执行要求又强调“你负责产出工具选择与下一跳提示词”

这会把模型推向“产出 `next_prompt` 作为 handoff”而不是“继续执行第二跳”。后台 Codex 因此会稳定反复完成首跳路由，却不真正进入 `doc-ibm-execution` 或 `dev-loop-execution`。

## Decision

1. 首跳默认不是终点，而是第二跳的入口。
2. 若 `selected_tool` 与当前运行工具相同，必须在同一会话内继续执行第二跳，而不是只输出 `next_prompt`。
3. 只有在以下情况才允许把 `next_prompt` 作为纯交接产物返回：
   - 下一跳工具与当前工具不同
   - 当前 loop 明确要求把执行权交回外层 runtime
   - 当前轮次被系统约束提前中止（例如 rate limit / forced rotation）
4. 测试要锁住：首跳 prompt 中必须出现“不允许只输出 `next_prompt` 结束”的明确要求。
