# Brainstorm: worktree-maintenance-governance

## Scope

- 只覆盖 worktree 创建之后的维护层
- 不替代 `branch-management` 的创建 / promotion / cleanup 基础命令
- 不替代 `premerge-reconcile` 的高风险冲突修复

## Modes

1. `audit`
2. `merge_prep`
3. `retirement_handoff`

## Key Decision

使用单一 skill 统一路由三种维护模式，比再新增多个零散入口更稳：
- 主管只需记住一个调用点
- skill 内部再根据当前问题选择具体模式
- 减少与 `branch-management` / `multi-worktree-supervision` 的重叠
