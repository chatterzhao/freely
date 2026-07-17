---
issue_id: I-20260716T114802Z-A
issue_path: docs/B2-docs/runtime/runtime-worker-launch-linkage-and-stall-recovery-governance/raw-20260716T114802Z/issues/I-20260716T114802Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260716T114802Z-A
- issue_path: docs/B2-docs/runtime/runtime-worker-launch-linkage-and-stall-recovery-governance/raw-20260716T114802Z/issues/I-20260716T114802Z-A.md

## Implementation Decision Note

- decision: _ai_shows_liveness_acp S2 进程态改前缀匹配 R*/S*，S3 函数内安全推导 base_tool
- why_this: 06:11 误杀根因是兜底链被两个实现缺陷击穿而非阈值不足；两处小修恰好堵住误杀路径且不改变 liveness 语义
- alternatives_considered: 提高 90s 阈值（治标，长推理可超任意阈值，否）；重构为 bridge session 状态查询（Option C，改动面大，留后续能力 issue）
- boundary_non_goals: 不动阈值与 stall 判定结构; direct 模式仅同修相同缺陷的进程态精确匹配副本(L14018),其余信号薄弱问题仍在边界外
- residual_risk: D（uninterruptible）态短暂存活进程仍会被判死——罕见且通常伴随真实 IO 卡死，可接受；direct 模式 liveness 信号薄弱为已知残留（本 lane 边界外，记录在案）
