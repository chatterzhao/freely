# 研究：Freely 自举开发下的 Worktree/Hook/Governance 一体化策略

## Context

- 日期：2026-03-05
- 触发：Freely 在开发 Freely 时，worktree 根目录位于项目外同级目录会触发权限与可维护性问题讨论。
- 目标：明确哪些属于宪法硬约束，哪些属于产品化能力（模板、可视化治理、预检修复）。

## 核心结论

1. worktree 根目录应强制为项目外同级 `{project-name}-worktrees`，不默认放入项目内。
2. “每次执行提权”不可接受，应通过一次性环境预检与可执行修复建议替代。
3. hook/约束策略不应散落在临时脚本里，必须模板化并由单一策略源驱动。
4. Freely 开发 Freely 必须显式执行 dogfooding：治理规则先作用于自身仓库，再对外输出。

## 边界划分

### 属于宪法（硬约束）
- worktree 根目录与命名规则
- 不允许默认项目内 worktree
- 自举开发必须遵循同一治理路径（无例外）

### 属于产品实现（可演进）
- `policy.json`/模板系统驱动 hooks
- `init doctor` 的权限预检与修复向导
- Governance 可视化配置（hook/worktree/约束开关）

## 落地顺序建议

1. P0：worktree 规则执行器 + 权限预检
2. P0：hook 模板编译器（策略到脚本）
3. P1：Governance UI（读取/编辑策略）
4. P1：修复向导（自动生成建议命令）

## 风险

- 若仅靠 CLI 授权错误回传而无 Freely 预检，用户将持续遇到高频权限阻塞。
- 若允许项目内 worktree 作为默认路径，会稀释隔离约束并放大目录污染风险。
