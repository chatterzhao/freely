# Tasks: I-20260804T073054Z-A

- [x] 修复 30 个 `SKILL.md` 的 `description: >-` 换行缩进（+ workflow skill frontmatter 置顶）
- [x] `bin/deploy-skills` 增加 frontmatter YAML 校验
- [x] pre-commit hook 增加 skills frontmatter 校验
- [x] `feature-execution`/`fix-execution` 的 `SKILL.md.bak` 退役（同名废弃变体，恢复会造成部署冲突）
- [x] 新增 4 个测试（parse/deploy-gate/precommit-gate/deploy-load）
- [x] 重新部署并验证 codex 加载无告警
