# Brainstorms - 20260403-1100--governance-chain-legacy-repair

## Context

- 日期：2026-04-03
- 触发：
  - `governance-merge-gate` 收紧后，暴露出一批历史治理链断裂与 repair-slice owner truth 漏写
  - `1100` 曾经 materialize 为 umbrella owner，但后续清理时误删了 canonical issue/progress/epic 文档，只剩 pre-brainstorm truth
  - `1200/1201/1202/1203` 与 `20260402-1719` 的目录已删除，但 `INDEX`、`milestones` 仍残留悬挂引用

## Current Repo Facts

1. `1100` 曾在 `milestones` 与 candidate 中被当作 canonical umbrella owner 使用
2. 当前树中缺失的 `docs/B2-docs/gate/governance-chain-legacy-repair/**` 与 `docs/progress/workspace-routing-foundation/p-governance-chain-legacy-repair.md` 已在 2026-04-04 truth-repair 中恢复
3. `20260402-1912` 已明确写明不要再复用已删除且 stale 的 `1719`
4. 当前需要修的不是 gate 放宽，而是 canonical truth 对齐、残留引用清理，以及把 `1100` 从活跃 owner 语义收口为历史完成态

## Problem

### 核心问题

1. **umbrella owner 真相断裂**
   - `1100` 曾被写成 promoted / committed owner
   - 但它对应的 issue / progress / epic 文档被误删，导致 owner 链只剩半套真相，并留下错误的 active-owner 叙述

2. **已删除 repair slices 仍被 canonical 文档消费**
   - `1200/1201/1202/1203` 与 `1719` 已删除
   - `INDEX`、`milestones` 仍把它们当作当前条目继续引用

3. **历史悬挂引用继续误导后续治理判断**
   - `20260325-0921` 等已删除路径仍残留在 milestone / inventory / issue depends_on 中
   - 这些引用会让后续 review 错判哪些 owner 仍然 active

## Solution Space

### 方案 A：恢复 `1100` 的 canonical owner 链，再把它收口为 historical/completed truth 并清理残留引用

- 优点：先补齐最少 canonical truth 缺口，再合法关闭 active-owner 语义
- 缺点：需要补回误删的 owner artifact，并同步刷新多处历史叙述

### 方案 B：把 `1100` 直接降级或退休，只保留 pre-brainstorm

- 优点：减少 active owner 数量
- 缺点：需要重写 milestone / candidate 生命周期，并解释为何已 promoted owner 可以无 issue/progress 收场

### 方案 C：只修索引，不修 owner

- 优点：改动最小
- 缺点：仍会留下 `1100` 自身的 canonical 断链，不符合当前法律质量线

## Proposed Approach

采用方案 A，并在 truth repair 完成后立即关闭活跃 owner 语义：

### Phase 1：恢复 umbrella owner 真相并冻结 closeout 依据

1. 恢复 `1100` 的 issue / progress / issue-bound artifacts
2. 保持 candidate / milestone 对 `1100` 的 owner 叙述不再指向不存在目标

### Phase 2：清理已删除 slice 与历史悬挂引用

1. 从 `INDEX` 移除 `1200/1201/1202/1203` 与 `1719` 幽灵条目
2. 从 `milestones`、inventory、issue `depends_on` 中移除已删除路径
3. 只保留仍存在于当前树中的 pre-brainstorm canonical 条目

### Phase 3：验证 owner 链重新闭合

1. `./bin/governance-check`
2. targeted missing-path sweep
3. merge back through guarded develop path
4. 把 `1100` 写回 completed/historical truth，禁止后续把它当作 current umbrella owner 继续推进

## Open Questions

1. 结论：`1100` 不再保留为 active owner，而是作为 2026-04-04 truth-repair 的 completed historical owner 留痕。
2. 未来若再出现 governance repair slices，应直接新开 lifecycle，并评估是否需要额外 cleanup gate 防止 owner artifact 被误删而 milestone truth 未同步。
