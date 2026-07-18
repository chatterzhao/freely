---
b1_id: B1-20260717T235950Z
phase_state: completed
source_raw: raw-20260717T235950Z
produced_candidate: C-20260717T235950Z-A
created_at: 2026-07-17
---

# B1_IBM: commands.md wt-close --force 描述与 autonomous gate 语义同步

## Input
raw-20260717T235950Z：PR #3980/#3984 后 usage() 已同步 autonomous gate 语义，commands.md §wt-close 选项表 --force 行仍旧文案。

## Problem
文档双真源漂移：--help（真源，随代码走门禁）已更新，commands.md（引用面）滞后。agent 按 commands.md 理解 --force 会缺"正常自治关闭不需要此标志、gate 自动判定放行"关键语义。

## Brainstorm
### Option A: commands.md --force 行同步 usage() 文案 ✅
一行文档修复，语义与 --help 一致。
### Option B: commands.md 删除选项表改为指向 --help
信息可达性下降，速查表价值丢失。❌

## Decision: Option A
最小修复，保持速查完整。范围仅 commands.md L193 一行（L35/L182 为场景示例行，语义不涉 gate 判定，不动）。

## Candidate
- candidate_id: C-20260717T235950Z-A
- status: promoted
- milestone: M-20260717T235950Z-A
