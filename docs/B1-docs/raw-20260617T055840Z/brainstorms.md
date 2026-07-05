# Brainstorm: Merge Guard + Rebase Integrity

## Discovery

### 触发事件
ACP/A2A 重构期间（2026-06-16/17），3 个 GitHub PR (#2879, #2881, #2882) 通过 GitHub UI "Merge pull request" 直接合入 develop，绕过了 `pr-merge-guarded` 的 governance gate。其中：
- PR #2881 (35a4cca3, 9 fixes) merge 后 rebase 丢失了 2 项变更
- PR #2882 (75e1499c, "re-apply") 也丢失了变更
- 另外 1 个变量名错误在 rebase 中引入

丢失的变更事后通过人工审查发现，产生了 3 个补救 PR (040640Z, 042034Z, skill-doc-fix)。

### 根因分析
1. **双 merge 路径**：GitHub UI "Merge pull request" 和 `pr-merge-guarded` 并行存在，前者无门禁
2. **rebase 无完整性校验**：`git rebase` 后没有任何自动机制检测冲突解决是否静默丢弃了变更
3. **事后审查不可靠**：丢失的变更依赖人工/subagent 审查才发现，延迟大、遗漏风险高

### 价值判断
- **时效性**：刚刚发生，问题仍在
- **未被覆盖**：此前无相关 issue 或 candidate 覆盖此问题
- **P0 优先级**：直接导致代码丢失，影响所有未来开发

## Research

### 行业实践
1. **GitHub 拦截直接 merge**：branch protection ruleset + required status check 是 GitHub 原生能力。Merge Gatekeeper (starkware-libs) 是成熟的开源参考实现。
2. **rebase 完整性**：Apache Mesos 等项目使用 `post-rewrite` hook 在 rebase 后自动运行 `git diff-index --check`。`git rerere` 可自动复用冲突解决。`git range-diff` 可比较 rebase 前后。

### 方案评估
| 方案 | 复杂度 | 防护效果 | 侵入性 |
|------|--------|---------|--------|
| GitHub branch protection + check API | 低 | 堵死 UI merge 路径 | 低（仅 pr-merge-guarded 内部改动 + CI workflow） |
| post-rewrite hook | 低 | rebase 丢代码立即发现 | 低（纯 hook，自动触发） |
| pre-rebase hook | 低 | 保存快照供 post-rewrite 对比 | 低 |
| 安全 rebase 封装脚本 | 中 | 需主动使用，易被绕过 | 中 |
| 代码审查变更文件 fidelity gate | 中 | merge 前验证 | 中 |

### 选定方案
采用 **GitHub branch protection + post-rewrite/pre-rebase hooks + pr-merge-guarded 门禁** 组合。理由：
- 全部使用行业标准机制（branch protection、git hooks、check runs API）
- hook 自动触发，不需要开发者记忆使用封装脚本
- pr-merge-guarded 门禁在 merge 前做最后拦截
- 复杂度低，总改动 ~250 行

## Decision

**Promote**。问题明确、方案成熟、实现已完成。进入 B2_IBM 阶段物化到 I-issue。
