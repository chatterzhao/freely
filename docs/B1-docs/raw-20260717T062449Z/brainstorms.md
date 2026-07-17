---
b1_id: B1-20260717T062449Z
phase_state: completed
source_raw: raw-20260717T062449Z
produced_candidate: C-20260717T062449Z-A
created_at: 2026-07-17
---

# B1_IBM: trace 契约 known-gaps 落地（L041/L042/L090 链）

## Input
trace-contract §12 登记的三缺口（raw-20260717T004752Z lane 显式暴露）。

## Problem / 勘察
1. L041 发射点位于 post-cycle 变量准备段（wait 之后）→ launch_observed 实测晚 94s
2. L042 单点发射 expected_next=候选集：实际出口分散在主循环 6+ 分支（stop_ai exit0 / resume continue / MAX_RESTARTS exit1 / 网络自愈 continue / auto-recovery continue / 恢复失败 exit0 / 自然下一轮）
3. L090/L091/L092 无 expected_next；实际去向可在 cleanup 内判定（superseded→L091→TERM；正常→L092→ running?接力重拉:TERM）

## Brainstorm
### Option A：维持单点 L042 换成"运行后事后推断 to"
- 反对：推断层不拥有决策，违反契约 §8 打印权归属
### Option B：拆相打点（选定）
- API 已支持（append_lifecycle_trace_in/out 独立）
- L042：原位只打 IN；各真实出口分支打 OUT（supervisor 进程内可判定的去向：continue→L020，exit→TERM；接力型下一跳由下游 IN fr=L042 记录——语义修订同步写入 §12）
- L041：前移到 child 启动后首次 kill -0 确认处（≤5s 轮询，超时不发保持缺口显式）
- L090/L091/L092：出口条件声明（L090→L091|L092 按 superseded 分支各自打；L092 running→L240 else TERM；L091→TERM）
### Option C：monitor 全量重构
- 另案

## Decision: Option B

## 边界
只动 trace 打点（in/out 调用与位置），不改任何路由/清理逻辑本身；同步更新 trace-contract §12。

## Candidate
- candidate_id: C-20260717T062449Z-A
- status: promoted
- milestone: M-20260717T062449Z-A
