# 候选方案

## 问题陈述

- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []

当前 CONSTITUTION.md 第 2 章规定：

> "所有非 `main`/`develop` 的开发分支都使用 `git worktree`"

这导致 `pre-develop` 被要求使用 worktree，但存在以下问题：

### 问题 1：冗余
- `pre-develop` **不允许 add/commit**（见分支规则表）
- 不需要提交的分支不需要 worktree 隔离

### 问题 2：状态不同步
- worktree 是独立目录
- 新提交到达时，如果在旧 worktree 目录里看不到最新状态
- AI 默认在主工作目录，分析项目时可能基于过时代码

### 问题 3：AI 上下文混乱
- AI 默认在注册目录（主工作目录）
- 如果 `pre-develop` 有独立 worktree，AI 在主目录时看不到 `pre-develop` 的最新变更
- 导致"分析项目"时分析的是旧版本

---

## 候选方案

### 方案 A：按"是否允许提交"决定 worktree（推荐）

**规则改为**：
> "所有**允许 add/commit** 的分支使用 `git worktree`"

**逻辑**：
- 需要 worktree 的分支：`feature/*`、`release/*`、`hotfix/*`
- 不需要 worktree 的分支：`main`、`develop`、`pre-develop`

**理由**：
1. worktree 的目的是隔离**开发工作**
2. 不允许提交的分支没有开发工作，只是合并目标
3. AI 默认在主目录，能看到最新的集成状态

**修改点**：
- CONSTITUTION.md 第 2 章第 3 条

### 方案 B：保持现状

**理由**：
- 统一规则简单
- 不需要区分分支类型

**问题**：
- 无法解决上述三个问题

---

## 决策标准

1. **AI 上下文一致性**：AI 应始终看到最新的项目状态
2. **最小必要 worktree**：只为真正需要隔离的分支创建 worktree
3. **治理简洁性**：规则应清晰易懂

---

## 当前推荐

**方案 A'**：直接在排除列表中添加 `pre-develop`

---

## 最终决策

**采用方案 A'**：在 CONSTITUTION.md 中将 `pre-develop` 添加到不需要 worktree 的分支列表。

**修改内容**：

1. **CONSTITUTION.md 第 2 章第 3 条**：
   - 原文：`所有非 main/develop 的开发分支都使用 git worktree`
   - 改为：`所有非 main/develop/pre-develop 的开发分支都使用 git worktree`

2. **`.githooks/post-checkout` 第 20-23 行**：
   - 原文：`main|develop`
   - 改为：`main|develop|pre-develop`

**理由**：
- `pre-develop` 不允许 add/commit，不需要 worktree 隔离
- AI 默认在主工作目录，能看到最新的集成状态
- 避免状态不同步问题
