# Tasks: fix flow 统一为 B1→B2→dev→test

## T1: 重写 freely-fix-execution SKILL.md
- 流程顺序: dev→test→B1→B2 → B1→B2→dev→test
- 去掉 test-pre-merge cherry-pick 机制
- 更新"核心原则"章节
- 更新"与 feature 的分工"对比表
- 输出: ~/.claude/skills/freely-fix-execution/SKILL.md

## T2: 更新 freely-test-execution SKILL.md
- fix 流程序列: dev→test→B1→B2 → B1→B2→dev→test
- 输出: ~/.claude/skills/freely-test-execution/SKILL.md

## T3: 更新 freely-feature-execution SKILL.md
- 分工表: fix 的 IBM 顺序从"实现后治理"改为"治理后实现"
- 输出: ~/.claude/skills/freely-feature-execution/SKILL.md

## T4: 更新 three-loop-capability-lifecycle.md
- Fix 变体路径: dev→test→B1→B2 → B1→B2→dev→test
- 输出: docs/system/workspace/three-loop-capability-lifecycle.md

## T5: 更新 AGENTS.md
- fix 流程序列 + Bug修复章节
- 输出: AGENTS.md

## T6: 同步项目级 skill 副本
- deploy-skills 部署到 ~/.claude/skills/
- 输出: 3 个 skill 文件更新

## T7: wt-close 改进（附带修复）
- 增强 Check 4 错误提示: 解释为什么 dev↔test 不同步有问题
- 修正 force 说明
- 修复 stray _dev_wt 行
- 更新 help 文本
