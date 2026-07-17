---
b1_id: B1-20260717T004752Z
phase_state: completed
source_raw: raw-20260717T004752Z
produced_candidate: C-20260717T004752Z-A
created_at: 2026-07-16
---

# B1_IBM: 监督面架构文档批量落后于实现 + trace 契约观测缺口

## Input
2026-07-16 三方审计（文档 vs 代码 vs raw issue 时间线）确认 6 类文档滞后（D1-D6）与 trace 契约执行缺口（C7）。同日四条修复 lane（raw-20260717T004620Z/004721Z/004654Z、raw-20260716T114802Z）已合并，实现真源进一步前移，文档缺口扩大。

## Problem
1. D1 heartbeat 机制（3b156c2e1, 2026-05-31）零文档；代码注释所称被替代的 L220-L240 grace chain 已不存在
2. D2 trace-contract §11 缺 16+ 已实现检查点（L090/091/092/201/202/210/211/212/225/230/231/232/300/310/320/330-336）
3. D4 bridge 生命周期（lazy-start/idle-sleep/auto-wake + 本日新增 warmup 宽限与 lazy 守卫）未入 capability-lifecycle
4. D5 task_mode auto/wait/listen 完整语义（wait=sleep+continue 跳过 prompt build；listen=scan-only 自动切 auto）未文档化；AI_MODE 与 task_mode 区分未记载
5. D6 storm 阈值（本日改为 WINDOW=120/COUNT=10/PEAK=3）与 supervisor 死亡记录未入 SKILL；Loop Guard L0-L3 零文档
6. C7 trace 执行缺口：A-L240 恒 to=UNSET ok=0（L19292 未传 expected_next，实际下一跳=supervisor_started）；A-L041 实际在 cycle 尾部发出、A-L042 OUT to= 打印候选集而非实际下一跳（契约 §4/§8 偏差）
7. AGENTS.md 引用不存在的 `freely pre-init-runtime` 命令（test 工位 runtime 初始化实际=wt-create 放置 config/db + 手工补 agent-table.toml）

## Brainstorm
### Option A：只补文档
- 反对：C7 的 L240 是一行可修的真观测缺口（契约 §5 说 UNSET"必须尽快补齐"），放着不修让契约继续自我违反
### Option B：文档批量对齐 + L240 一行修复 + L041/L042 现实语义入契约 known-gaps（选定）
- L240 补 expected_next=L010（watchdog 重拉的真实下一跳）；L041 晚发/L042 候选集打印牵涉 monitor 结构，本 lane 不动代码，在 trace-contract 增设 known-gaps 表显式记录（契约允许 UNSET 显式暴露缺口的精神）
### Option C：连 L041/L042 一并重构
- monitor 结构改动风险大，独立 lane 承接

## Decision: Option B

## 边界
- 文档：three-loop-capability-lifecycle.md、three-loop-trace-contract.md、watchdog-control-plane SKILL.md、AGENTS.md（仅纠错 pre-init-runtime 引用）
- 代码：仅 L240 打点参数一行；不动 monitor/L041/L042 逻辑
- skill 文件修改后须 freely deploy-skills（AGENTS.md 规定）

## Candidate
- candidate_id: C-20260717T004752Z-A
- status: promoted
- milestone: M-20260717T004752Z-A
