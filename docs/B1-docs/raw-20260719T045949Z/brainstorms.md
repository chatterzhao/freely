---
b1_id: B1-20260719T045949Z
phase_state: completed
source_raw: raw-20260719T045949Z
source_url: https://github.com/chatterzhao/freely/issues/3997
produced_candidate: C-20260719T045949Z-A
created_at: '2026-07-19'
---

# B1_IBM: B1/B2 skill 补充三环能力生命周期交叉引用

## Input
- raw issue: raw-20260719T045949Z
- 两个核心 skill（freely-doc-B1_IBM-execution、freely-doc-B2_IBM-execution）缺少对三环能力生命周期总图的交叉引用

## Problem
这两个 skill 定义了 B1→B2→dev 的 IBM 工作流，但从未显式引用三环能力生命周期总图。读者看完 skill 不知道自己在三环中的位置，也不知道三环生命周期是这些引用目标。

## Brainstorm

### Option A：每个 skill 只加一个链接
最简：在文件末尾各加一行三环生命周期链接。
- 优点：改动极小
- 缺点：无上下文，读者不知道为什么要看

### Option B：加链接 + 说明位置和流转关系（采纳）
B1 skill：说明 B1 是 doc-loop 第一阶段，promote 后进入 B2→dev-loop
B2 skill：聚合关键参考（PRD 质量门槛、设计派生约束、三环生命周期），说明 B2→dev 交付关系
- 优点：有上下文，可独立理解
- 缺点：改动略多（2 个文件，各多一段）

→ **采纳 Option B**。评审确认方向正确、内容精准。
