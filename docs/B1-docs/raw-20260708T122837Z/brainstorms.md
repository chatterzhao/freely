---
b1_id: B1-20260708T122837Z
phase_state: completed
source_raw: raw-20260708T122837Z
produced_candidate: C-20260708T122837Z-A
---

# B1: scan 恢复 stage 分级 + batch 聚合 + derive_action

## Discovery: lifecycle-v3 丢弃的核心能力

### value_check: P1
Manager 面对 271 条无差异的 2a_non_terminal，无法判断先做什么。
旧 scan (bak.py) 通过 stage 分级让每条 item 都有具体操作指引。

### 旧 scan 的三层输出结构

```
scan → items:
  ① platform_sync_batch (最高优先级, 1 条聚合)
  ② 生命周期 items (每条含 stage + next_action)
  ③ chat inbox items
```

### 新 scan 保留的改进
- argparse --project ✅
- platform-adapter 集成 ✅
- extract_platform_ids 多平台 ✅
- py_compile ✅

## Brainstorm

### 恢复方案

**Option A: 重写 scan，合并新旧优势**
- 优点: 彻底
- 缺点: 工作量大

**Option B: 在 lifecycle-v3 上增量加 stage 分级 ✅**
- 在现有的 3 类基础上增加 stage 字段
- 增加 platform_sync_batch 聚合函数
- 增加 _derive_action 函数
- 优点: 改动可控

**Decision: Option B** — 增量改造。

### stage 分级设计

```
1a_fresh + platform_closed → stage: close_local
1a_fresh + platform_open   → stage: B1_proposed
2a_non_terminal + platform_closed → stage: close_local
2a_non_terminal + platform_open   → stage: 收口
2a_state_mismatch → stage: close_platform
2b_worktree_not_cleaned → stage: 收口
3a_never_bound → stage: 恢复
3b_session_dead → stage: 恢复
```

### batch 聚合

platform_sync_batch 聚合所有 close_platform + close_local + state_mismatch → 1 条 batch item

## Candidate: C-20260708T122837Z-A, promoted
