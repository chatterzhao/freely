# Brainstorms - 20260403-1100--governance-chain-legacy-repair

## Context

- 日期：2026-04-03
- 触发：
  - `develop` 分支有 787 commits ahead of origin，无法 push
  - `governance-merge-gate` 检测到 358 个治理链断裂问题
  - 这些问题分为两类：
    - 9 个 source_candidate 缺失或无法解析
    - 46 个 issue 无法解析（missing）
    - 其余为其他类型的引用断裂

## Current Repo Facts

1. `governance-merge-gate` 最近多次收紧检查（从 `936e56a` 到 `c2ca02b`）
2. 历史遗留的 progress/review 文件引用了不存在的 issue 或 source_candidate
3. 部分预研目录被删除但 issue/progress 仍引用它们
4. 部分 issue 文件格式不符合当前解析器要求

## Problem

### 核心问题

1. **历史遗留问题暴露**
   - 之前 gate 检查不够严格，很多不完整治理链被合并到 develop
   - 现在收紧后，这些历史问题阻塞了 push

2. **source_candidate 缺失**
   - 部分 issue 引用的 pre-brainstorm 目录不存在
   - 部分 candidate 文件格式不符合解析器要求

3. **issue 缺失**
   - 部分 progress/review 引用的 issue 不存在
   - 部分引用格式不正确

## Solution Space

### 方案 A：逐一修复所有治理链

- 优点：彻底解决，符合规范
- 缺点：工作量大，358 个问题

### 方案 B：放宽 gate 检查范围

- 优点：快速恢复 push
- 缺点：治标不治本，积累更多技术债

### 方案 C：分阶段修复

- 先修复阻塞 push 的问题（已 staged 的改动相关）
- 后续逐步修复历史遗留问题
- 优点：平衡短期和长期目标
- 缺点：需要明确定义优先级

## Proposed Approach

采用方案 C，分阶段修复：

### Phase 1：修复阻塞 push 的问题

1. 修复已 staged 改动相关的治理链
2. 恢复缺失的 pre-brainstorm 目录
3. 确保当前改动可以 push

### Phase 2：批量修复历史遗留问题

1. 分析所有 358 个问题
2. 分类修复：
   - 缺失文件：从历史 commit 恢复或创建占位符
   - 格式问题：修正格式
   - 引用断裂：修正引用

### Phase 3：加固治理检查

1. 添加 pre-commit 检查防止新增断裂
2. 添加批量修复工具

## Open Questions

1. 是否需要为每个断裂创建单独的 issue，还是批量处理？
2. 历史遗留问题的修复优先级如何定义？
3. 是否需要引入"legacy_backfill"标记来区分历史补录？
