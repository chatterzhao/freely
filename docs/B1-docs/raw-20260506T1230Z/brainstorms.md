# Brainstorms — wt-create Dual Worktree Creation

## Discovery

### Source
- Raw issue: `docs/B1-docs/raw-20260506T1230Z/issue.md`
- GitHub: https://github.com/chatterzhao/freely/issues/280
- Created: 2026-05-06, author: zhaoquan
- Channel: github
- 原始问题：wt-create 每次只创建一个工位，fix/feat 和 test-pre-merge 都基于 develop。

### 需求边界
wt-create 需要一次性创建两个工位：
1. **test-pre-merge** — 基于 develop
2. **fix/feature** — 基于 test-pre-merge，而非 develop

这样 fix→test-pre-merge 变为 fast-forward merge，消除 merge commit 和冲突风险。

### 当前状态调查

检查发现以下事实：

- **I-issue**: `docs/B1-docs/I-20260506T1230Z-A/issue.md` — 已存在，`phase_state: in_dev`
- **Milestone**: `M-20260506T1230Z-A` — 已存在且 active，已关联该 I-issue
- **Code review**: `docs/epics/wt-create-dual/code-reviews/review.md` — 已完成，决策正确
- **Pre-tests**: `docs/epics/wt-create-dual/verification/pre-tests.md` — 已完成，覆盖 unit/integration/e2e
- **Tasks**: `docs/epics/wt-create-dual/verification/tasks.md` — 全部已完成
- **实现脚本**: `docs/system/workspace/scripts/worktree/wt-create` — 已支持 `--raw-key --prefix --skill --slug`
- **Skill 更新**: `docs/system/workspace/skills/fix-execution/SKILL.md` 和 `feat-execution/SKILL.md` — 已更新

全部 B2/实现/验证工作已在并发开发中完成。

### 边界检查
- CONSTITUTION.md：分支/工作树策略与 dual worktree creation 无冲突
- LAWS.md：无涉及工位创建策略的约束
- PROJECT_INTENT.md：未限制 wt-create 一次性创建工位的数量

## Convergence

该 raw issue 描述的需求已被完整实现。从 I→B→M 全链路：
- **I**: Input 通过 GitHub issue #280 录入并物化到工位
- **B (本阶段)**: 证实全部实现已完成，无需额外 Brainstorm 发散
- **M**: Candidate 已 promoted 为 I-issue，Milestone 已关联

## Decision

- **结论**: absorbed
- **理由**: wt-create dual worktree creation 的全部 B2/实现/测试/合并工作已在并发开发中完成。当前代码库已支持一次性创建 test-pre-merge + fix/feature 双工位，fix→test-pre-merge 为 fast-forward。
- **证据**:
  - `docs/B1-docs/I-20260506T1230Z-A/issue.md` — I-issue 已存在
  - `docs/epics/wt-create-dual/code-reviews/review.md` — Code review 已完成
  - `docs/epics/wt-create-dual/verification/pre-tests.md` — 验收测试通过
  - `docs/epics/wt-create-dual/verification/tasks.md` — 全部任务完成
  - `docs/system/workspace/scripts/worktree/wt-create` — 实现已落地
