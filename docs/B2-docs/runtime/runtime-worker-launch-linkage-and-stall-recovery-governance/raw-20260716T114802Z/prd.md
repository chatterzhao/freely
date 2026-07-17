# PRD: liveness 兜底链修复
- issue_id: I-20260716T114802Z-A

## Goal
长推理静默期（S1 过期）时，存活的 bridge/AI 进程被 S2/S3 正确判活，不再触发 stall 误杀。

## 实现方案
b-I 两处修复。实现顺序：S2 → S3。

## Dev-Loop Handoff
RED 4 项 → 实现 → GREEN → test 工位全量。
