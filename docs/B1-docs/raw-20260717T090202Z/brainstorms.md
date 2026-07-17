---
b1_id: B1-20260717T090202Z
phase_state: completed
source_raw: raw-20260717T090202Z
produced_candidate: C-20260717T090202Z-A
created_at: 2026-07-17
---

# B1_IBM: PEAK=3 误报回归（自查）

## Input
生产实抓：2026-07-17T08:59:43Z 起每 cycle `restart_storm_pause reason=process_churn_peak_threshold peak=3 observe_delay=30`。

## Problem
raw-20260717T004620Z C4-fix-2 将 PROCESS_CHURN_PEAK 10→3；update_restart_storm_window 每次 AI cycle 完成记录活进程数（健康态恒 3）→ 健康即满值恒触发。原 AC"阈值落在可达域"语义判断错误：可达≠应达。

## Brainstorm
- Option A：PEAK 回 10（条件重新虚设）——备选
- Option B（选定）：tsv 行加 kind 列（cycle|death），peak 仅对 death 行计——churn 语义恢复；旧 2 列行不计峰（兼容且保守）
- Option C：删 peak 条件——减观测面，否

## Decision: Option B

## 边界
update_restart_storm_window 第 4 参 kind（默认 cycle）；death 记录传 death；stats peak 仅 death 行；count 口径不变；capability-lifecycle 口径同步。不改原 lane 文件（GATE 1）。

## Candidate
- candidate_id: C-20260717T090202Z-A
- status: promoted
- milestone: M-20260717T090202Z-A
