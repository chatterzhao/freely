# Brainstorms: 门禁收口链路 — platform_ids 追溯与继承

- source: `docs/issues/raw-20260508T050922Z/issue.md` (GitHub #255)
- timestamp: 2026-05-08T05:09:22Z
- author: zhaoquan

## Discovery

### 问题陈述

I-* issue 在 `cmd_promote` 创建后 `platform_ids` 字段为空。当 `issue-sync close` 尝试自动关闭对应的平台 issue 时，因缺少 `platform_ids` 无法映射到目标平台 issue，导致关闭链路中断。

### 根因分析

1. **`cmd_promote` 阶段**：将 raw-* 提升为 I-* issue 时，raw-* 的 `platform_ids`（包含 GitHub issue #255 的 URL 和 ID）未被传播到新创建的 I-* issue。I-* 的 frontmatter 中 `platform_ids` 保持初始空值。
2. **`cmd_close` 阶段**：关闭 I-* issue 时，`issue-sync close` 依赖 `platform_ids` 找到对应平台 issue 并关闭。由于 I-* 无此字段，程序无法追溯，关闭操作仅发生在本地。

### 影响范围

- issue-sync 双向同步的关闭方向断裂
- 平台 issue 在本地 issue 关闭后保持 OPEN 状态，造成状态不一致
- 影响 GitHub #255 及后续所有经 `cmd_promote` 创建的 I-* issue

### 边界条件

- raw-* issue 始终持有初始的 `platform_ids`（从平台拉取时写入）
- I-* issue 仅在 `cmd_promote` 之后创建，此时 raw-* parent 仍然可寻址
- `cmd_close` 需要主动追溯 raw-* parent 来获取 platform_ids

## Research

### 现有机制

- `issue-sync` 依赖 `platform_ids` 做双向状态映射
- `raw-*` → `I-*` 的单向提升链路已存在，但 frontmatter 字段复制不完整
- close 操作在本地执行后，通过 `issue-sync close` 推送关闭信号到平台

### 修复方向收敛

两条修复路径，互补而非互斥：

| 路径 | 改动点 | 效果 |
|------|--------|------|
| **cmd_promote** | 在创建 I-* 时从 raw-* parent 复制 `platform_ids` | 从源头预防，新 I-* 天生带 platform_ids |
| **cmd_close** | 关闭 I-* 时若 `platform_ids` 为空，向上追溯 raw-* parent 获取 | 兜底修复，处理已存在的无 platform_ids 的 I-* |

### 依赖

- 无外部依赖
- 仅涉及 `bin/issue-sync` 或关联的 `cmd_promote` / `cmd_close` 代码路径
- 属于 issue lifecycle 的基础设施修复

## Decision

该问题构成 issue lifecycle 的基础链路断裂，影响所有 I-* close 操作。修复后能消除 issue 状态不一致的根本原因。

- **价值确认**：高。影响所有通过 `cmd_promote` 创建的 I-* issue 的关闭链路。
- **时效性**：已由 `C-20260508T050922Z-A` 承载并在 `I-20260508T050922Z-A` 中完成实现。
- **当前状态**：该修复已通过 dev-loop → merge → closeout 的完整生命周期，已被吸收到 `develop`。

### 后验复盘

该问题的 B1_IBM → B2_IBM → dev-loop 流程已在 2026-05 月 batch round7 中完成。候选方案（cmd_promote 复制 + cmd_close 追溯）在当时被采纳并实现，修复正确且已 closeout。

当前 worktree 存在是因为该 raw issue 需要专用工位处理。由于整个生命周期已走完，此处不再需要新的 candidate 或二次执行。

### 下一跳

- 不需要新的 B1_IBM 或 B2_IBM 执行
- 该 candidate `C-20260508T050922Z-A` 保持现有 `promoted` 状态
- 里程碑 `M-20260508T050922Z-A` 记录完整且正确
- 建议：关闭 worktree，本次 B1_IBM 执行仅为审计归档
