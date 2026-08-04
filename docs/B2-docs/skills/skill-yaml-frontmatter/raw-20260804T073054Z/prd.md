# PRD: SKILL.md frontmatter YAML 修复 + 部署链校验

## Goal

让全部 workspace skill 的 SKILL.md frontmatter 合法可解析，并在部署与提交链路拦截坏 frontmatter，杜绝复发。

## 实现方案

1. 批量修复 `docs/system/workspace/skills/*/SKILL.md`：`description: >-` 后换行 + 缩进内容。
2. `bin/deploy-skills`：对每个 SKILL.md 解析 frontmatter，失败即拒绝部署并列出文件。
3. `.githooks/pre-commit`：扫描 `docs/system/workspace/skills/**/SKILL.md` 变更，frontmatter 解析失败即拦截。
4. `.bak` 处理：`feature-execution`、`fix-execution` 的 `SKILL.md.bak` 恢复为 `SKILL.md`。
5. 重新部署并验证 codex 启动加载全部 skill。

## Dev-Loop Handoff

- pre-tests：frontmatter 解析单测（30 个文件全过）、deploy-skills 拦截测试（坏文件拒绝）、pre-commit 拦截测试、部署后加载验证。
- tasks：修复文件 → 校验脚本 → hook → .bak → 部署验证。
