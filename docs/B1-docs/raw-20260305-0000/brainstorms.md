# 头脑风暴：Worktree 策略中 pre-develop 的排除

## 背景

用户发现一个严重问题：`pre-develop` 不应该使用 worktree。

### 问题分析

1. **pre-develop 的性质**
   - 它是集成/合并分支
   - 不允许直接 add/commit
   - 只接收来自 feature 分支的合并

2. **当前策略的问题**
   - CONSTITUTION.md 规定"所有非 main/develop 的开发分支都使用 worktree"
   - 这意味着 pre-develop 需要单独的 worktree 目录
   - 但 pre-develop 不允许提交，不需要隔离

3. **AI 上下文问题**
   - worktree 是独立目录
   - 新提交到达时，AI 如果在旧 worktree 目录里看不到
   - AI 默认只在注册目录（主工作目录）
   - 导致"分析项目"时分析的是旧版本

## 讨论

### 核心洞察

worktree 的目的是隔离**开发工作**（add/commit）。

不允许提交的分支没有开发工作，只是合并目标，不需要 worktree。

### 分支分类

| 类型 | 分支 | add/commit | 需要 worktree |
|------|------|------------|---------------|
| 开发分支 | feature/* | ✅ | ✅ |
| 发布分支 | release/* | ✅ | ✅ |
| 热修分支 | hotfix/* | ✅ | ✅ |
| 集成分支 | main/develop/pre-develop | ❌ | ❌ |

## 结论

**推荐方案**：按"是否允许提交"决定 worktree

修改 CONSTITUTION.md 第 2 章第 3 条：

**原文**：
> 所有非 `main`/`develop` 的开发分支都使用 `git worktree`

**改为**：
> 所有**允许 add/commit** 的分支使用 `git worktree`

## 下一步

- [ ] 在 candidates.md 中详细记录候选方案
- [ ] 等待决策确认
- [ ] 修改 CONSTITUTION.md
