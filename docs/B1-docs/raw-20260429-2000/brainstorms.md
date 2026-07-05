# Brainstorm — Gate 开发体验优化

## 背景

开发者在 feature worktree 中完成代码后，需要先创建 test-pre-merge worktree、
执行 merge、再跑 governance-merge-gate --staged 才能知道门禁是否通过。
如果门禁失败，需要删除 test-pre-merge、修复、重建、重合并。每轮约 2 分钟。

同时，pre-commit 密钥检测对 milestones.md 中的文件路径
（如 `task-source-scan-idle-replan-boundary-governance`）产生误报，
强制使用 `--no-verify` 提交。

## 问题分析

1. governance-merge-gate 已有 `--range` 参数但不可用：从 develop 分支运行时，
   无法读取 feature 分支的新文件（`read_repo_text` 只从文件系统读取）。

2. pr-merge-guarded 在 feature→test-pre-merge 时不做事先检查，
   等 merge 完成才知道门禁失败。

3. 密钥检测对 `.md` 文件中反引号内的路径名误报。

## 决策

1. governance-merge-gate --range：增加从 git source ref 读取文件的后备路径。
2. pr-merge-guarded：feature→test-pre-merge 时先跑 --range 预检。
3. pre-commit：.md 文件中反引号内的匹配跳过。

## 替代方案

- 完全移除密钥检测的 sk- 模式：风险太大，可能放过真正的密钥。
- 在 pr-merge-guarded 中做完整的 test-pre-merge 预演：太重量级。

## 结论

三个改动均为最小化质量改进，不改变核心门禁逻辑。
