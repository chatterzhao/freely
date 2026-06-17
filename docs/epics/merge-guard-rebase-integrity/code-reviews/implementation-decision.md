# Implementation Decision Note: Merge Guard + Rebase Integrity

## Decision
采用 **GitHub branch protection (required status check) + git post-rewrite/pre-rebase hooks + pr-merge-guarded gate** 三层防护。

## Why This
1. **Branch protection 是 GitHub 原生能力**：不需要额外基础设施，一个 `gh api` 调用即可配置
2. **git hooks 是行业标准**：Apache Mesos 等项目用 post-rewrite 做 rebase 后校验，自动触发、无法绕过
3. **pr-merge-guarded gate 是最后防线**：即使 hook 被跳过（如 `git -c core.hooksPath=/dev/null`），merge 前的显式检查仍然拦截
4. **复杂度极低**：总改动 ~250 行，零新依赖

## Alternatives Considered

### A. safe-rebase wrapper script
**否决原因**: 
- 需要开发者主动使用，`git rebase --continue` 会绕过
- 与现有 hook 架构不一致（项目已有成熟的 `.githooks/` 体系）
- 冲突解决场景下完全失效

### B. Affected-files gate (对比 issue 和 PR diff)
**否决原因**:
- Issue 中的 "Affected Files" 是规范而非实现记录，存在漂移
- 误报率高（实现可能改用不同文件）
- 当前只有 1 个 issue 有此字段，缺乏标准化基础

### C. Keep `--admin` flag, add documentation
**否决原因**: 不真正解决问题，GitHub UI merge 按钮仍然可用

## Boundary / Non-Goals
- **不覆盖** `git commit --amend`（post-rewrite 触发但不做比较，太 noisy）
- **不覆盖** 手动 `git merge`（已被 pre-merge-commit hook 的 state file 检查拦住）
- **不覆盖** force push 到 develop（已被 pre-push hook 拦住）
- **不强制** GitHub branch protection（作为可选的一次性配置；未配置时 pr-merge-guarded 仍然工作但 UI 按钮不灰掉）

## Residual Risk
1. **Hook 禁用**: `git -c core.hooksPath=/dev/null rebase` 可跳过 hooks。pr-merge-guarded 的 `check_rebase_integrity` gate 是二次防线。
2. **快照清理**: pre-rebase 快照 7 天自动过期。如果 rebase 挂起超过 7 天，快照可能丢失。
3. **GitHub API 调用失败**: `_set_governance_check_pass` 失败时静默 fallback（`|| true`）。未配置 branch protection 时不影响功能。
