# Brainstorms - 20260403-1100--governance-chain-legacy-repair

## Context

- 日期：2026-04-03
- 触发：
  - `governance-merge-gate` 对 legacy governance artifacts 的约束已收紧到当前 canonical 质量线
  - `develop` 上暴露出一批历史遗留治理断裂，同时当前修复又裂成 `1100/1200/1201/1202/1203` 多个 lane
  - 如果母链只停留在 promoted candidate，子切片就会继续用伪 owner 状态运行，形成新的治理失真

## Current Repo Facts

1. 当前 legacy drift 不是单一字段缺失，而是 candidate / issue / progress / review 多层真相长期未同步
2. `feature/governance-chain-legacy-repair-20260403-1100` 与 `1200/1201/1202/1203` 共享旧基线，但这些子切片并不是 git ancestry 上的真实下游
3. `1200/1201/1202/1203` 更像同一批次的 repair slices，需要 canonical parent owner 承接，而不是各自伪造独立 materialized issue
4. 当前真正需要恢复的是 lawful governance chain，而不是为了 unblock push 临时降低 gate 强度

## Problem

- 历史遗留 drift 现在已经阻断 canonical chain，但当前 repair 自身也处于半失真的生命周期状态
- 如果没有一个 materialized umbrella owner，child slices 会继续：
  - 声称 promoted 到不存在的 issue
  - 在 commit message 里暗示彼此关系，却不把关系写回 canonical docs
  - 让后续 reviewer 无法判断哪些是同一批次的 repair、哪些是独立 owner

## Boundary

- In scope:
  - 把 `1100` materialize 成当前 legacy governance-chain repair 的 canonical owner
  - 在 canonical docs 中记录 `1200/1201/1202/1203` 的父子关系和当前状态
  - 为后续 artifact backfill 先建立 lawful owner truth
- Out of scope:
  - 放宽 `governance-merge-gate`
  - 仅凭“当前 push 被阻塞”就把所有 legacy drift 一次性揉成永久 mega-owner
  - 用跨分支引用代替当前 worktree 内可审计的 canonical docs

## Option Space

### Option A：weaken the gate

- 优点：表面上最快解除阻塞
- 缺点：直接回避当前 repair 的治理目标，也会继续制造 future drift

### Option B：先给每个子切片单独 materialize owner

- 优点：每条 repair slice 看起来都有完整 issue 链
- 缺点：在 parent 还未合法化前，先把 authority 继续拆散

### Option C：先 materialize umbrella owner，再吸收或合法化子切片

- 优点：先恢复 canonical authority，再决定 leaf-level 归属
- 缺点：要求 parent lane 显式记录 child-slice truth，而不是把关系藏在口头说明里

## Route Decision

- 采用 Option C
- 当前 `1100` 先负责：
  - materialize umbrella owner
  - 把 `1200/1201/1202/1203` 从伪 promoted 状态纠正为 lawful pre-brainstorm child slices
  - 维持 gate 严格度不变，后续再做具体 legacy artifact backfill

## Acceptance Targets (Pre-Brainstorm)

- `1100` 的 candidate / issue / progress / milestone entry 必须形成单义 owner truth
- `1200/1201/1202/1203` 在 canonical docs 中必须有可追溯 parent relation，且不再指向不存在 issue
- 下一跳必须从“先把当前 repair 的治理链修好”开始，而不是先讨论如何豁免当前 gate

## Open Questions

1. 这四个子切片最终应全部 absorbed 到 `I-20260403-1100-A`，还是其中部分后续独立 materialize？
2. legacy drift 的实际 backfill 应按 field class 批量推进，还是按 owner lineage 分批推进？
3. 完成这轮 canonical repair 后，哪些已完成或陈旧 worktree 应立即退休，避免继续污染 fleet 判断？
