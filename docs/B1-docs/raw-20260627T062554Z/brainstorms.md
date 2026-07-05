---
b1_id: B1-20260627T062554Z
phase_state: completed
source_raw: raw-20260627T062554Z
source_url: https://github.com/chatterzhao/freely/issues/3583
produced_candidate: C-20260627T062554Z-A
created_at: 2026-06-27
---

# B1_IBM: task-lifecycle-scan v3 — 三分类重构

## Input
- 来源: raw-20260627T062554Z (GitHub #3583)
- 调研文档: .scan-review-findings.md（9 个 Bug + 6 条设计原则）
- 新实现: task-lifecycle-scan.py (~800 行, 旧版 2007 行)

## 架构对比

| | 旧 scan (2007行) | 新 scan (~800行) |
|--|-----------------|-----------------|
| 分类 | 8 source_family 混在一起 | 3 类分叉，精准 |
| 平台 | 硬编码 gh + gitee-issue.py | _detect_platforms() 自动发现 |
| 性能 | 无缓存 | HEAD skip + API cache (5min TTL) |
| 冷启动 | ~60s (逐个 API 调) | ~11s (批量 + 缓存) |
| 热缓存 | N/A | 0.04s |
| 中间态 | 全扫，干扰 manager | A2A 活着跳过（TODO） |
| push=176 | ✅ 误报 | ❌ 修复（检查本地 platform_state） |

## 分类架构

基于 Freely 生命周期三个物理位置分叉：

```
对每个 raw-{key}:
  ├─ 工位存在 → Cat 3（进行中，判死活）
  ├─ docs/B1-docs/raw-{key}/ 存在 → Cat 2（已完成，判对齐）
  └─ 都没有 → Cat 1（未开始）
```

### Cat 1: 未开始
- 1a: 平台 OPEN + 无工位 + 无本地目录 → wt-create
- 1b: 平台 OPEN + 本地 phase=completed → reopen → wt-create
- 1c: Chat inbox 未消费 + 无工位 + 无本地目录 → AI 判断

### Cat 2: 已完成但不对齐
- 2a: phase_state 非 terminal（proposed/done_b2_ibm/空）
- 2a-2: terminal 但 platform_state 缺失
- 2a-3: terminal 但 platform_state != 平台实际状态
- 2b: terminal + 工位仍存在 → wt-close
- 2d: Chat 未消费但 raw 已存在

### Cat 3: 进行中但 agent 死
- 3a: 工位存在 + agent-id.env 缺失 → 委派未绑定
- 3b: 工位存在 + agent-id.env 有值 + A2A session 失效 → 重委派/resume

## 性能设计

1. HEAD-based skip: HEAD 未变 → 不重扫文件（docs/B1-docs/ 只通过 git commit 变更）
2. Platform cache: 5min TTL，避免重复 API 调用
3. Timer 嵌入: 每步耗时可见，方便排查瓶颈

```
冷启动 ~11s:  platform_open(4.5s) + platform_states(6.0s) + file_scan(0.21s)
热缓存 0.04s: 全部命中
```

## 待完善（依赖其他 raw issue）

- Cat 3 agent 存活判断：当前读 agent-id.env（文件），应改为读 a2a_tasks（SQLite）— 依赖 a2a_tasks agent_id 改编号
- Cat 3 session 存活：依赖 agent-lifecycle 的 reconcile + session/close 修复
- Cat 1c Chat inbox：column index bug 已修（PRAGMA d[0]→d[1]）

## Candidate
- candidate_id: C-20260627T062554Z-A
- status: promoted
- milestone: M-20260627T062554Z-A
