# Candidates

## C-20260507T0100Z-A: fix-execution SKILL.md 分支命名前缀修复

- candidate_format_version: v2
- title: fix-execution SKILL.md 分支命名规范中 feature/ 前缀统一替换为 fix/
- status: promoted
- promoted_issue_path: docs/issues/I-20260507T0100Z-A/issue.md
- decision_reason: 分支命名规范直接影响工位创建正确性和 pr-merge-guarded 门禁判断；fix-execution 已投入使用，此命名问题需优先修复；修复范围清晰（7 处 feature/ 替换），风险可控
- milestone: M-20260507T0100Z-A
- acceptance_criteria:
  - fix-execution SKILL.md 中 7 处 feature/ 前缀统一替换为 fix/
  - 分支名格式使用 raw-{raw-key}-{slug} 规范
  - 不破坏其他 skill 的分支命名逻辑
